from flask import jsonify, Flask
from tabulate import tabulate
from cleaningData import CleaningData
from repository import Repository
from IPython.display import display
import pandas as pd

app = Flask(__name__)
cleaningData = CleaningData()


@app.route("/api/v1.0/recommendations/<int:id>", methods=["GET"])
def get_recomendations(id):
    print("Profile_id: " + str(id))
    # return engine.get_recommendations(id)
    return {'recommendation': 'DONE'}


if __name__ == "__main__":

    print('########## category Recommendation :')
    dg = cleaningData.get_Matrix_Categorie_Recommendation()
    print(tabulate(dg, headers='keys', tablefmt='psql'))

    # app.run(debug=False)

    # test in POST MAN :
    # http://127.0.0.1:5000/data
