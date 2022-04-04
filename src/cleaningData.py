from cmath import nan
import pandas as pd
import matplotlib.pyplot as plt
from repository import Repository
import environement
from datetime import datetime
from datetime import date
from bson.objectid import ObjectId
from tabulate import tabulate


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

    def get_OnLineChek_clean(self):
        DataFrame_OnlineChek = self.repository.get_OnLineChek_DataFrame({})
        List_DATA = []
        for index, row in DataFrame_OnlineChek.iterrows():
            DATA = {}

            # Get Guest ID
            DATA['guestId'] = row['propertyBookingId']
            # Get age
            guestBirthDate = row['guestBirthDate']
            if(isinstance(guestBirthDate, str)):
                Age = abs(date.today().year -
                          datetime.strptime(guestBirthDate, '%Y-%m-%d').year)
                if(Age < 20):
                    DATA['SCORE_guestAge'] = 1
                elif(Age < 30 and Age >= 20):
                    DATA['SCORE_guestAge'] = 2
                elif(Age < 40 and Age >= 30):
                    DATA['SCORE_guestAge'] = 3
                else:
                    DATA['SCORE_guestAge'] = 4
            else:
                DATA['SCORE_guestAge'] = 2
            # Get gender
            guestGender = row['guestGender']
            if(guestGender == environement.GEUST_GENDER_FEMALE):
                DATA['SCORE_guestGender'] = 1
            elif(guestGender == environement.GEUST_GENDER_MALE):
                DATA['SCORE_guestGender'] = 2
            else:
                DATA['SCORE_guestGender'] = 0
            List_DATA.append(DATA)
        return pd.DataFrame(list(List_DATA), columns=['guestId', 'SCORE_guestAge', 'SCORE_guestGender'])

    def get_Recommendation_Clean(self):
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

    def get_FactoryMatric_Behavior(self):
        # NO BUGS
        DataFrame_Guest_Reviews_Behaivor = self.get_guestReviews_clean({
        })
        DataFrame_Recommendation = self.repository.get_Recommendation_DataFrame({
        })
        DataFrame_guest = self.repository.get_Guest_DataFrame({}).head(1)

        List_DATA = []
        for index, row_guest in DataFrame_guest.iterrows():
            for index, row_recommendation in DataFrame_Recommendation.iterrows():
                # initialise sum to zero:
                DATA = {}
                guestId = row_guest['_id']
                recommendationId = row_recommendation['_id']

                # Get score behaivor :
                SCORE_BEHAVIOR = None
                for index, row_guest_recommendation_behaivor in DataFrame_Guest_Reviews_Behaivor.iterrows():
                    if(guestId == row_guest_recommendation_behaivor['guestId'] and recommendationId == row_guest_recommendation_behaivor['recommendationId']):
                        SCORE_BEHAVIOR = row_guest_recommendation_behaivor['SCORE_BEHAVIOR']
                        break

                    # Add DATA
                DATA['guestId'] = guestId
                DATA['recommendationId'] = recommendationId
                DATA['SCORE_BEHAVIOR'] = SCORE_BEHAVIOR
                List_DATA.append(DATA)
        return pd.DataFrame(list(List_DATA), columns=['guestId', 'recommendationId', 'SCORE_BEHAVIOR'])

    def get_Matrix_Categorie_Recommendation(self):
        List_of_category = self.repository.get_Category()
        DataFrame_Recommendation = self.repository.get_Recommendation_DataFrame({
        })
        print('GET ALL DATA DONE !')
        List_DATA = []
        for index, row_recommendation in DataFrame_Recommendation.iterrows():
            for category in List_of_category:
                # initialise sum to zero:
                DATA = {}
                if(category == row_recommendation['category']):
                    DATA['isInCategory'] = 1
                else:
                    DATA['isInCategory'] = 0
                # Add DATA
                DATA['recommendationId'] = row_recommendation['_id']
                DATA['category'] = category
                List_DATA.append(DATA)

        return pd.DataFrame(list(List_DATA), columns=['recommendationId', 'category', 'isInCategory'])

    def get_Matrix_Guest_x_Recommendation_on_Category(self):
        # Working on this , morrrre bug so far
        Matrix_Categorie_x_Recommendation = self.get_Matrix_Categorie_Recommendation()
        Matrix_Categorie_x_Guest = self.repository.get_guestCategory(
            {})[['guestId', 'category', 'nbClickCategory']]
        List_DATA = []
        for index, row_recommendation in Matrix_Categorie_x_Guest.iterrows():
            for index, row_recommendation in Matrix_Categorie_x_Recommendation.iterrows():
                # initialise sum to zero:
                DATA = {}

                # Add DATA
                DATA['guestId'] = row_recommendation['_id']
                DATA['recommendationId'] = ''
                DATA['SCORE_Category'] = ''
                List_DATA.append(DATA)

        return pd.DataFrame(list(List_DATA), columns=['guestId', 'recommendationId', 'SCORE_Category'])
