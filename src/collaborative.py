from tabulate import tabulate
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import environement


from collections import defaultdict #data colector

#Surprise: https://surprise.readthedocs.io/en/stable/
import surprise

from surprise.reader import Reader
from surprise import Dataset
from surprise.model_selection import GridSearchCV

  ##CrossValidation
from surprise.model_selection import cross_validate


  ##Matrix Factorization Algorithms
from surprise import SVD
from surprise import NMF

np.random.seed(42) # replicating results



def getData(df , ratingdf):
    print(type(df))

    new_features = ['_id','fullAddress', 'title', 'category', 'description']
    global_rating = ratingdf

    new_features1=['guestId' , 'recommendationId','nbClickRecoDirection']

    df = df[new_features]
    ratingdf = ratingdf[new_features1]
    NB_score = environement.SCORE_nbClickRecoCard + environement.SCORE_nbClickRecoMarker + environement.SCORE_nbClickRecoWebSite + \
               environement.SCORE_nbClickRecoDirection + \
               environement.SCORE_clickOnSliderPictures
    for i in range(len(ratingdf['nbClickRecoDirection'])):
        pictureScore = 0
        if (global_rating['clickOnSliderPictures'])[i]:
            pictureScore=1


        ratingdf['nbClickRecoDirection'][i]= global_rating['nbClickRecoDirection'][i]* environement.SCORE_nbClickRecoDirection  + global_rating['nbClickRecoCard'][i] * environement.SCORE_nbClickRecoCard   +global_rating['nbClickRecoMarker'][i]* environement.SCORE_nbClickRecoMarker  +global_rating['nbClickRecoWebSite'][i]* environement.SCORE_nbClickRecoWebSite \
        +  pictureScore*environement.SCORE_clickOnSliderPictures
        ratingdf['nbClickRecoDirection'][i]=(ratingdf['nbClickRecoDirection'][i]/NB_score)*10+1

    #print(tabulate(df, headers='keys', tablefmt='psql'))

    #We still don't have enough data !

    print(df.columns)
    print(ratingdf.columns)
    ratingdf.columns = ratingdf.columns.str.replace('nbClickRecoDirection', 'scoreBehaviour')

    #ratings_flrd_df = ratingdf.groupby("recommendationId")
    #ratings_flrd_df =ratings_flrd_df.groupby("guestId")

    reader = Reader(rating_scale=(0.5, 5))  # line_format by default order of the fields
    data = Dataset.load_from_df(ratingdf[["guestId", "recommendationId", "scoreBehaviour"]], reader=reader)

    final_dataset = ratingdf.pivot(index='recommendationId', columns='guestId', values='scoreBehaviour')
    print(tabulate(ratingdf, headers='keys', tablefmt='psql'))
    print("Matrice de Factorisation :")
    print(tabulate( final_dataset, headers='keys', tablefmt='psql'))

    final_dataset.fillna(0, inplace=True)
    print(tabulate( final_dataset, headers='keys', tablefmt='psql'))




    trainset = data.build_full_trainset()

    testset = trainset.build_anti_testset()

    algo_SVD = SVD(n_factors=4)
    algo_SVD.fit(trainset)

    # Predict ratings for all pairs (i,j) that are NOT in the training set.
    testset = trainset.build_anti_testset()

    predictions = algo_SVD.test(testset)

    print("valeur en nan : ", len(predictions) , "from " , final_dataset.shape)


    rmse_svd = rmse_vs_factors(SVD, data)
    plot_rmse(rmse_svd, "SVD")

    pred = algo_SVD.predict('621649c3c8162045849f2ff9', '5ecd191d250fc36d81996c07', r_ui=4, verbose=True)

    print(predictions)
    print("Example ===>:  " , pred)







def rmse_vs_factors(algorithm, data):
    """Returns: rmse_algorithm i.e. a list of mean RMSE of CV = 5 in cross_validate() for each  factor k in range(1, 101, 1)
    100 values
    Arg:  i.) algorithm = Matrix factoization algorithm, e.g SVD/NMF/PMF, ii.)  data = surprise.dataset.DatasetAutoFolds
    """

    rmse_algorithm = []

    for k in range(1, 101, 1):
        algo = algorithm(n_factors=k)

        # ["test_rmse"] is a numpy array with min accuracy value for each testset
        loss_fce = cross_validate(algo, data, measures=['RMSE'], cv=5, verbose=False)["test_rmse"].mean()
        rmse_algorithm.append(loss_fce)

    return rmse_algorithm


def plot_rmse(rmse, algorithm):
    """Returns: sub plots (2x1) of rmse against number of factors.
       Vertical line in the second subplot identifies the arg for minimum RMSE

       Arg: i.) rmse = list of mean RMSE returned by rmse_vs_factors(), ii.) algorithm = STRING! of algo
    """

    plt.figure(num=None, figsize=(11, 5), dpi=80, facecolor='w', edgecolor='k')

    plt.subplot(2, 1, 1)
    plt.plot(rmse)
    plt.xlim(0, 100)
    plt.title("{0} Performance: RMSE Against Number of Factors".format(algorithm), size=20)
    plt.ylabel("Mean RMSE (cv=5)")

    plt.subplot(2, 1, 2)
    plt.plot(rmse)
    plt.xlim(0, 50)
    plt.xticks(np.arange(0, 52, step=2))

    plt.xlabel("{0}(n_factor = k)".format(algorithm))
    plt.ylabel("Mean RMSE (cv=5)")
    plt.axvline(np.argmin(rmse), color="r")
    plt.show()


def encode_column(column):
        """ Encodes a pandas column with continous IDs"""
        keys = column.unique()
        key_to_id = {key: idx for idx, key in enumerate(keys)}
        return key_to_id, np.array([key_to_id[x] for x in column]), len(keys)

def encode_df(anime_df):
        """Encodes rating data with continuous user and anime ids"""

        anime_ids, anime_df['anime_id'], num_anime = encode_column(anime_df['anime_id'])
        user_ids, anime_df['user_id'], num_users = encode_column(anime_df['user_id'])
        return anime_df, num_users, num_anime, user_ids, anime_ids