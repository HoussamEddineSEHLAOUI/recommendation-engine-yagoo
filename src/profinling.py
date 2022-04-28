
import numpy as np

from service import Service
import pandas as pd
from datetime import datetime
from datetime import date
from database import Database

class Profiling:
    def __init__(self, Geust, DataFrameOnLigneChek , DataFramePropertyBooking):
        print('INITIALISE DATA')
        self.Geust = Geust
        self.DataFrameOnLigneChek = DataFrameOnLigneChek


    def get_Profiles(self):
        print('GET SIMILAR PROFILE')

        GUEST = self.Geust
        SCORE_AGE_GEUST = self.get_ScoreAge(GUEST.guestBirthDate)
        SCORE_GENDRE = self.get_ScoreGendre(GUEST.guestGender)
        SCORE_RESERVATION_DATE = self.get_ScoreDate(GUEST.startDate)
        SCORE_NATIONALITY = self.get_ScoreNatinality(GUEST.guestCountry)

        ListProfiles = []

        # 1  faire une seule iteration sur la date frame de online chek    for row in dataframe :
        for index, row in self.DataFrameOnLigneChek.iterrows():
         # 2  fair cette conndition if Guest match the row of your iteration
         if (SCORE_AGE_GEUST == self.ScoreAge(row['guestBirthdate']) and SCORE_GENDRE == self.get_ScoreGendre(
                row['guestGender']) and SCORE_NATIONALITY == self.get_ScoreNatinality(row['guestCountry']) ,   SCORE_RESERVATION_DATE == self.get_ScoreDatey(row['startDate']) ):

                ListProfiles.append(row['propertyBookingId'])

        return ListProfiles

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

        return float(guestCountry)

    def get_ScoreDateReservation(self, startDate):
        if(startDate=='nan'):
            startDate=np.NaN

        return datetime.strptime(startDate, '%Y-%m-%d').month

    def get_ScoreGendre(self, guestGender):

        if guestGender=='homme':
            return 0
        elif    guestGender=='femme':
            return 1
        else:
            return 2

