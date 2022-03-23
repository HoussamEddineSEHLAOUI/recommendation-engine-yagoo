from flask import jsonify, Flask
import engine
import data

from IPython.display import display

app = Flask(__name__)


@app.route("/api/v1.0/recommendations/<int:id>", methods=["GET"])
def get_recomendations(id):
    print("Profile_id: " + str(id))
    # return engine.get_recommendations(id)
    return data.get_Recommendation_DataFrame().to_json()


if __name__ == "__main__":

    # Get data base collection names :
    data.get_database()
    input()
    # Get all tags , type Data Frame
    display(data.get_Tags_DataFrame())
    input()

    # Get all recomendation , type data frame
    display(data.get_Recommendation_DataFrame())
    input()

    # get all category type data frame

    app.run(debug=False)


# test in POST MAN :
# http://127.0.0.1:5000/data
