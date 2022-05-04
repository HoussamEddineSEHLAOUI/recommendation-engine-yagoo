
import pandas as pd
import matplotlib.pyplot as plt
from repository import Repository
import environement
from datetime import datetime
from datetime import date
from bson.objectid import ObjectId
from tabulate import tabulate
import random
from datetime import datetime
from recommendation import Recommendation
from profiling import Profiling


class CleaningData:
    def __init__(self):
        self.repository = Repository()

    def get_guestReviews_clean(self):
        DataFrame_GuestReviewsScore = self.repository.get_guestReviews({})
        # Drop colone _id
        DataFrame_GuestReviewsScore = DataFrame_GuestReviewsScore.drop(
            "_id", axis=1)

        DataFrame_GuestReviewsScore = DataFrame_GuestReviewsScore.reset_index()
        # Score Data
        NB_score = environement.SCORE_nbClickRecoCard + environement.SCORE_nbClickRecoMarker+environement.SCORE_nbClickRecoWebSite + \
            environement.SCORE_nbClickRecoDirection + \
            environement.SCORE_clickOnSliderPictures
        List_DATA = []
        for index, row in DataFrame_GuestReviewsScore.iterrows():
            # initialise sum to zero:
            SUM_MOY = 0
            DATA = {}

            SCORE_nbClickRecoCard = row['nbClickRecoCard'] * \
                environement.SCORE_nbClickRecoCard
            SCORE_nbClickRecoMarker = row['nbClickRecoMarker'] * \
                environement.SCORE_nbClickRecoMarker
            SCORE_nbClickRecoWebSite = row['nbClickRecoWebSite'] * \
                environement.SCORE_nbClickRecoWebSite
            SCORE_nbClickRecoDirection = row['nbClickRecoDirection'] * \
                environement.SCORE_nbClickRecoDirection
            SCORE_clickOnSliderPictures = row['clickOnSliderPicturesScore'] * \
                environement.SCORE_clickOnSliderPictures

            # Summ all scores :
            SUM_MOY = SCORE_nbClickRecoCard + SCORE_nbClickRecoMarker+SCORE_nbClickRecoWebSite + \
                SCORE_nbClickRecoDirection+SCORE_clickOnSliderPictures

            # create Score Beheiver :
            SCORE_BEHAVIOR = (SUM_MOY/NB_score)*10
            if int(SCORE_BEHAVIOR) == 0:
                DATA['SCORE_BEHAVIOR'] = None
            else:
                DATA['SCORE_BEHAVIOR'] = int(SCORE_BEHAVIOR)
            DATA['guestId'] = row['guestId']
            DATA['recommendationId'] = row['recommendationId']
            List_DATA.append(DATA)

        return pd.DataFrame(list(List_DATA), columns=['guestId', 'recommendationId', 'SCORE_BEHAVIOR'])

    def get_Matrix_Guest_x_Recommendation_likes(self):
        # NO BIGS
        DataFrame_Recommendation = self.repository.get_Recommendation_DataFrame({
        })
        List_DATA = []
        for index, row in DataFrame_Recommendation.iterrows():
            recommendationId = row['_id']
            bookingWhichLikes = row['bookingWhichLikes']
            if(isinstance(bookingWhichLikes, list) and bookingWhichLikes != None):
                for _id in bookingWhichLikes:
                    DATA = {}
                    DATA['guestId'] = _id
                    DATA['recommendationId'] = recommendationId
                    DATA['SCORE_Like'] = 1
                    List_DATA.append(DATA)

        return pd.DataFrame(list(List_DATA), columns=['guestId', 'recommendationId', 'SCORE_Like'])

    def get_guest_Tags_Matric(self):
        # bug stil here
        DataFrame_Tags = self.repository.get_Tags_DataFrame({}).head(5)
        DataFrame_guest = self.repository.get_Guest_DataFrame({})

        print('Get data is DONE !')
        List_DATA = []
        for index, row_guest in DataFrame_guest.iterrows():
            for index, row_tags in DataFrame_Tags.iterrows():
                # initialise sum to zero:
                DATA = {}
                guestId = row_guest['_id']
                # guestId = ObjectId('61f1347c14a5f64c2859eddf')
                tagId = row_tags['_id']
                # nbClickTag = repository.get_guestTag_byId({'_id': _id})
                nbClickTag = self.repository.get_guestTag_byId_new(
                    {},  {'guestId': guestId, 'tagId': tagId})

                DATA['guestId'] = guestId
                DATA['tagId'] = tagId
                DATA['nbClickTag'] = nbClickTag
                print(DATA)
                List_DATA.append(DATA)
        return pd.DataFrame(list(List_DATA), columns=['guestId', 'tagId', 'nbClickTag'])

    # All the matrix :

    def get_Matrix_Guest_x_Recommendation_Behavior(self):
        # Create a guest :
        Guest = {
            '_id': '6255272e196ab66cbe41363b',
            'guestGender': 'femme',
            'guestBirthDate': '1968-08-16',
            'guestCountry': 'FR',
            'startDate': '2000-05-10'}

        # NO BUGS
        DataFrame_Guest_Reviews_Behaivor = self.get_guestReviews_clean()
        DataFrame_Recommendation = self.repository.get_Recommendation_DataFrame({
        })
        DataFrame_APPROXIMATE_Recommendation = Recommendation(
            DataFrame_Recommendation).get_Recommendation()
        print("GET RECOMMENDATION EN PARIS")
        DataFrame_guest = self.repository.get_Guest_DataFrame({})
        DataFrameOfProfiles = Profiling(Guest, DataFrame_guest).get_Profiles()
        print(DataFrameOfProfiles)
        print("GET DATA OF PROFILES ")
        # Start traitement
        List_DATA = []
        for index, row_guest in DataFrameOfProfiles.iterrows():
            for index, row_recommendation in DataFrame_APPROXIMATE_Recommendation.iterrows():
                # initialise sum to zero:
                DATA = {}
                guestId = row_guest['_id']
                recommendationId = row_recommendation['_id']
                # Get score behaivor :
                # None was here before
                # random.choice([0, 10, 15, 20, 12, 15, 19, 151, 1])
                SCORE_BEHAVIOR = random.choice(
                    [1, 2, 3, 4, 5, None, None])
                for index, row_guest_recommendation_behaivor in DataFrame_Guest_Reviews_Behaivor.iterrows():
                    if(str(guestId) == str(row_guest_recommendation_behaivor['guestId']) and str(recommendationId) == str(row_guest_recommendation_behaivor['recommendationId'])):
                        SCORE_BEHAVIOR = row_guest_recommendation_behaivor['SCORE_BEHAVIOR']
                        break
                # Add DATA
                DATA['guestId'] = str(guestId)
                DATA['recommendationId'] = str(recommendationId)
                DATA['SCORE_BEHAVIOR'] = SCORE_BEHAVIOR
                DATA['rating'] = SCORE_BEHAVIOR
                List_DATA.append(DATA)
                # print(DATA)
        print('DONE GET DATA')
        return (pd.DataFrame(list(List_DATA), columns=['guestId', 'recommendationId', 'SCORE_BEHAVIOR', 'rating']), DataFrame_Recommendation)
