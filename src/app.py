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
    # print('##############   guest category :')
    # display(ServiceData.get_guestCategory({}))
    # input()

    print('############# guest reviews :')
    display(ServiceData.get_guestReviews({}))

    # app.run(debug=False)


# test in POST MAN :
# http://127.0.0.1:5000/data
