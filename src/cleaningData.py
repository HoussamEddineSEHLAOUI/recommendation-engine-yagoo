
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

    # All the matrix :

    def get_Matrix_Guest_x_Recommendation_Behavior(self, guestId):
        # Create a guest :
        Guest = self.repository.get_guest_byId(guestId)

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
