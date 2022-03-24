from flask import jsonify, Flask
import engine
from service import Service
from IPython.display import display

app = Flask(__name__)

# Service data
ServiceData = Service()


@app.route("/api/v1.0/recommendations/<int:id>", methods=["GET"])
def get_recomendations(id):
    print("Profile_id: " + str(id))
    # return engine.get_recommendations(id)
    return {'recommendation': 'DONE'}


if __name__ == "__main__":

    # Get all tags , type Data Frame
    print('##############   tags :')
    display(ServiceData.get_Tags_DataFrame({}))
    input()

    # get guest tags :
    print('##############  Guest tags :')
    display(ServiceData.get_guestTag({}))
    input()

    # get_guestReviews
    print('##############  Guest Reviews :')
    display(ServiceData.get_guestReviews({}))
    input()

    # Recommendations :
    print('##############  Recommendation:')
    display(ServiceData.get_Recommendation_DataFrame({}))
    input()

    # get all category type data frame

    app.run(debug=False)


# test in POST MAN :
# http://127.0.0.1:5000/data
