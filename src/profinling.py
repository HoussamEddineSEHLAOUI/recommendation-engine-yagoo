import numpy as np
from bson import ObjectId

from service import Service
import pandas as pd
from datetime import datetime
from datetime import date
from database import Database
import environement

class Profiling:
    def __init__(self, Geust, DataFrameOnLigneChek):
        print('INITIALISE DATA')
        self.ServiceData = Service()
        self.Geust = Geust
        self.DataFrameOnLigneChek = DataFrameOnLigneChek


    def get_Profiles(self):
        print('GET SIMILAR PROFILE')

        GUEST = self.Geust
        print(GUEST)
        SCORE_AGE_GEUST = self.get_ScoreAge(GUEST['guestBirthDate'])

        SCORE_GENDRE = self.get_ScoreGendre(GUEST['guestGender'])
        SCORE_RESERVATION_DATE = self.get_ScoreDateReservation(GUEST['startDate'])
        SCORE_NATIONALITY = self.get_ScoreNatinality(GUEST['guestCountry'])

        ListProfiles = []

        # 1  faire une seule iteration sur la date frame de online chek    for row in dataframe :
        for index, row in self.DataFrameOnLigneChek.iterrows():
         # 2  fair cette conndition if Guest match the row of your iteration
         if (SCORE_AGE_GEUST == self.get_ScoreAge(row['guestBirthDate']) and SCORE_GENDRE == self.get_ScoreGendre(
                row['guestGender']) and SCORE_NATIONALITY==self.get_ScoreNatinality(row['guestCountry']) and SCORE_RESERVATION_DATE==self.get_ScoreDateReservation(self.get_DateFromPropertyBooking(row['propertyBookingId']))  ):
                DATA={}
                DATA['propertyBookingId']=row['propertyBookingId']
                DATA['guestGender'] = row['guestGender']
                DATA['guestBirthDate'] = row['guestBirthDate']
                DATA['guestCountry'] = row['guestCountry']
                DATA['firstName'] = row['firstName']
                DATA['lastName'] = row['lastName']

                print( self.get_DateFromPropertyBooking(row['propertyBookingId']))


                ListProfiles.append(DATA)

        return pd.DataFrame(list(ListProfiles), columns=['propertyBookingId','firstName','lastName', 'guestGender','guestBirthDate','guestCountry'])


    def get_ScoreAge(self, guestBirthDate):

        if (isinstance(guestBirthDate, str)):
            Age = abs(date.today().year -
                      datetime.strptime(guestBirthDate, '%Y-%m-%d').year)
            if (Age < 20):
                 return 1
            elif (Age < 30 and Age >= 20):
                return 2
            elif (Age < 40 and Age >= 30):
                return  3
            else:
                return  4
        else:
            return  2


    def get_ScoreNatinality(self, guestCountry):

        return guestCountry

    def get_ScoreDateReservation(self, startDate):
       
        return datetime.strptime(startDate, '%Y-%m-%d').month
    
    

    def get_ScoreGendre(self, guestGender):

        if guestGender==environement.GEUST_GENDER_MALE:
            return 0
        elif    guestGender==environement.GEUST_GENDER_FEMALE:
            return 1
        else:
            return 2

    def get_DateFromPropertyBooking(self , propertBookingId):

       return self.ServiceData.get_PropretBooking_DataFrame({'_id': ObjectId(propertBookingId) })['startDate'][0]
