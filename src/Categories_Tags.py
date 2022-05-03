from bson import ObjectId
from flask import jsonify, Flask, request

from service import Service

from tabulate import tabulate

from src.app import ServiceData

app = Flask(__name__)


class Tag_Categories:

    def __init__(self):
        self.ServiceData = Service()



    ###Categoty
    def getCategory_Matrix(self):
        #Category DataFrame
        Category_df = ServiceData.get_guestCategory({})

        cols = ['guestId', 'category', 'nbClickCategory']
        Category_df= Category_df[cols]

        #Creation de la matrice de factorisation
        Category_Matrix = Category_df.pivot(index='category', columns='guestId', values='nbClickCategory')

        return Category_Matrix


    ####Tags
    def getTags_matrix(self):


        Tags_df= ServiceData.get_guestTag({})



        tag_cols= [ 'nbClickTag', 'guestId', 'tagId']

        Tags_df= Tags_df[tag_cols]

        Tags_Matrix = Tags_df.pivot(index='tagId' , columns='guestId', values='nbClickTag')

        return  Tags_Matrix


