
from flask import jsonify, Flask, Response
from tabulate import tabulate
from engine import Engine
from repository import Repository
import json
from bson.objectid import ObjectId
from flask import request
#
from repository import Repository
from profiling import Profiling
from recommendation import Recommendation


app = Flask(__name__)
engine = Engine()
repo = Repository()


@app.route("/api/v1.0/recommendations/<int:id>", methods=["GET"])
def get_recomendations(id):
    print("Profile_id: " + str(id))
    return engine.get_Recommendatio_Behavior()


@app.route("/api/recommendations", methods=["GET"])
def getRecommendation():
    # get the id of the guest
    guestId = request.args.get('guestId')

    RecommendationFinale = Engine().get_Recommendation_Behavior(guestId)
    list_recommendation = []
    for index, row_recommendation in RecommendationFinale.iterrows():
        DATA = {}
        DATA['_id'] = str(row_recommendation['_id'])
        DATA['title'] = row_recommendation['title']
        DATA['category'] = row_recommendation['category']
        DATA['googlePlaceId'] = row_recommendation['googlePlaceId']
        DATA['photos'] = row_recommendation['photos']
        list_recommendation.append(DATA)
    return {
        'DATA': "DONE",
        "list": list(list_recommendation)
    }


if __name__ == "__main__":

    print('########## Behavior : Recommendation X Profile :\n')
    # dt = engine.get_MatrixPlein_Guest_x_Recommendation_Behavior()
    # print(tabulate(dt, headers='keys', tablefmt='psql'))

    app.run(host="127.0.0.1", port=5055, debug=False)

    # test in POST MAN :
    # http://127.0.0.1:5000/data

    # commande to run the code : spark-submit app.py

    # repo = Repository()

    # print('START IN GEOLOCALISATION :')
    # DataFrameRecommendation = repo.get_Recommendation_DataFrame({})
    # Recommendation = Recommendation(DataFrameRecommendation)
    # dt = Recommendation.get_Recommendation()
    # print(tabulate(dt, headers='keys', tablefmt='psql'))

    # print('GET LIST OF RECOMMENDATION :')
    # RecommendationFinale = Engine().get_Recommendation_Behavior(
    #     '622f5a0ec025410ff5e5efd0')
    # # RecommendationFinale.join()
    # print(RecommendationFinale)

    # print(Repository.get_guest_byId('61fa61b2f2605e47c844b918'))
