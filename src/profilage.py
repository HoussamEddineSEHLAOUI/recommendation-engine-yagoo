from service import Service
import pandas as pd
from datetime import datetime
from datetime import date
import environement
class profilage:

    def profilage_byAge(self , guestBirthDate):

        DataFrame_OnlineChek = Service.get_OnLineChek_DataFrame({})
        List_DATA = []
        DATA_Guest={}
        if (isinstance(guestBirthDate, str)):
            Age = abs(date.today().year -
                      datetime.strptime(guestBirthDate, '%Y-%m-%d').year)
            if (Age < 20):
                DATA_Guest['SCORE_guestAge'] = 1
            elif (Age < 30 and Age >= 20):
                DATA_Guest['SCORE_guestAge'] = 2
            elif (Age < 40 and Age >= 30):
                DATA_Guest['SCORE_guestAge'] = 3
            else:
                DATA_Guest['SCORE_guestAge'] = 4
        else:
            DATA_Guest['SCORE_guestAge'] = 2

        for index, row in DataFrame_OnlineChek.iterrows():
            DATA= {}

            # Get Guest ID
            DATA['guestId'] = row['propertyBookingId']
            # Get age
            guestBirthDate = row['guestBirthDate']
            if (isinstance(guestBirthDate, str)):
                Age = abs(date.today().year -
                          datetime.strptime(guestBirthDate, '%Y-%m-%d').year)
                if (Age < 20):
                    DATA['SCORE_guestAge'] = 1
                elif (Age < 30 and Age >= 20):
                    DATA['SCORE_guestAge'] = 2
                elif (Age < 40 and Age >= 30):
                    DATA['SCORE_guestAge'] = 3
                else:
                    DATA['SCORE_guestAge'] = 4
            else:
                DATA['SCORE_guestAge'] = 2

            List_DATA.append(DATA)

        #on utilise le score Age pour identifier chaque tranche d'age(meme score equivalent tranche d'age)
        guestScoreAge = DATA_Guest['SCORE_guestAge']

        #on cherche les voyageurs avec le meme score
        SimilarProfiles_ByAge = pd.DataFrame(list(List_DATA), columns=['guestId', 'SCORE_guestAge']).query('SCORE_guestAge== @guestScoreAge')

        #on change le nom de l acomlumns guestId pour faciliter les jointure apres
        SimilarProfiles_ByAge.rename(columns={'guestId': 'propertyBookingId'}, inplace=True)

        #Liste des profiles qui ont la meme tracnhe d'age que le voaygeur en question
        return SimilarProfiles_ByAge


    def profilage_byGender(self , guestGender):

  
        DataFrame_OnlineChek = Service.get_OnLineChek_DataFrame({})

        #on cherchre les voyageur qui ont le meme genre
        SimilarProfiles_ByGender = DataFrame_OnlineChek.query('guestGender== @guestGender')

        #list des voaygeurs avec le meme genre
        return SimilarProfiles_ByGender


    def profilage_byNationalte(self, guestCountry):


        DataFrame_OnlineChek = Service.get_OnLineChek_DataFrame({})

        # on cherchre les voyageur qui ont la meme nationalite
        SimilarProfiles_ByNationality = DataFrame_OnlineChek.query('guestCountry== @guestCountry')

        # list des voaygeurs avec la meme nationalite
        return SimilarProfiles_ByNationality


    def profilage_ByDate(self):
        return "Septempbre"


    #Cette fonction permet d'avoir la list des profiles similaire selon les 3 critères (je vais ajouter la data apres )
    def getProfilage_List(self , SimilarProfiles_ByAge , SimilarProfiles_ByGender ,  SimilarProfiles_ByNationality ):

        #jointure entre les profiles similaire par age et par genre
        Similar_Profiles = pd.merge(SimilarProfiles_ByAge, SimilarProfiles_ByGender, on=['propertyBookingId', 'propertyBookingId'])

        #jointure entre les profiles similaire par age , genre et nationlaite
        Similar_Profiles = pd.merge(    Similar_Profiles ,  SimilarProfiles_ByNationality,
                                    on=['propertyBookingId', 'propertyBookingId'])


        return Similar_Profiles
