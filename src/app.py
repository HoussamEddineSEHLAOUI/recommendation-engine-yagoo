from flask import jsonify, Flask, request

from service import Service

from profiling import Profiling

app = Flask(__name__)

# Service data
ServiceData = Service()




@app.route("/profiling", methods=['POST'])
def get_profiles():
    request_data = request.get_json()
    #get data from post request
    guestGender= request_data['guestGender']
    guestBirthDate = request_data['guestBirthDate']
    guestCountry= request_data['guestCountry']
    startDate = request_data['startDate']

    #guest object
    Guest = {'guestGender': guestGender, 'guestBirthDate': guestBirthDate, 'guestCountry': guestCountry,
             'startDate': startDate}

    #initializing profiling class
    profiling = Profiling(Guest, ServiceData.get_OnLineChek_DataFrame({}))

    #return list of similar profiles
    return  str(profiling.get_Profiles())


if __name__ == "__main__":

    print(" test to run ")

    Guest = {'guestGender': 'homme', 'guestBirthDate': '1995-05-10', 'guestCountry': 'FR',
             'startDate': '2000-05-10'}


    profiling = Profiling(Guest, ServiceData.get_OnLineChek_DataFrame({}))


    print(profiling.get_Profiles())


    app.run(debug=False)

    # test in POST MAN :
    # http://127.0.0.1:5000/data
