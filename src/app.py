from flask import jsonify, Flask
import engine
import data
app = Flask(__name__)


@app.route("/api/v1.0/recommendations/<int:id>", methods=["GET"])
def get_recomendations(id):
    print("product_id: " + str(id))
    return engine.get_recommendations(id)


@app.route("/data", methods=["GET"])
def getdata():
    return data.get_recommendation()


if __name__ == "__main__":
    app.run()


# test in POST MAN :
# http://127.0.0.1:5000/data
