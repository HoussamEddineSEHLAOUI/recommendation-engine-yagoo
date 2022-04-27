

class Profiling:
    def __init__(self, Geust, DataFrameOnLigneChek):
        print('INITIALISE DATA')
        self.Geust = Geust
        self.DataFrameOnLigneChek = DataFrameOnLigneChek

    def get_Profiles(self):
        print('GET SIMILAR PROFILE')

        GUEST = self.Geust
        SCORE_AGE_GEUST = self.get_ScoreAge(GUEST)
        SCORE_GENDRE = self.get_ScoreGendre(GUEST)
        SCORE_RESERVATION_DATE = self.get_ScoreDateReservation(GUEST)

        # 1  faire une seule iteration sur la date frame de online chek    for row in dataframe :
        # 2  fair cette conndition if Guest match the row of your iteration
        # if( SCORE_AGE_GEUST == self.ScoreAge(row)  & SCORE_GENDRE== self.get_ScoreGendre(row)  & SSCORE_RESERVATION_DATE ==self.get_ScoreDateReservation(row)):
        #     add to list profile

    def get_ScoreAge(self, USER):
        print('RETURN THE SCORE OF AGE ')

    def get_ScoreDateReservation(self, USER):
        print('RETURN THE MONTH OF THE USER : GUEST OR ROW')

    def get_ScoreGendre(self, USER):
        print('RETURN THE 0 if man 1 if women')
