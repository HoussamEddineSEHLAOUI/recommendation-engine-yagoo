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
    print("DONE ! WITH GET DATA !")
    #DB = data.get_database()
    return jsonify(data.GETDATA())


if __name__ == "__main__":
    print(data.get_database())
    print(data.get_collection('tags'))
    app.run()
