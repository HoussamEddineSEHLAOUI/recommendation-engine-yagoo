from flask import jsonify, Flask, request
import engine
from service import Service
from IPython.display import display
from tabulate import tabulate
import collaborative
import Profile
import pandas as pd
import matplotlib.pyplot as plt
from tabulate import tabulate
import clustring

app = Flask(__name__)

# Service data
ServiceData = Service()


@app.route("/api/v1.0/recommendations/<int:id>", methods=["GET"])
def get_recomendations(id):
    print("Profile_id: " + str(id))
    # return engine.get_recommendations(id)
    return {'recommendation': 'DONE'}

@app.route("/profile", methods=['POST'])
def get_profile():
    dummy_df = pd.read_csv("./MOCK_DATA (4).csv")
    cols = ['guestGender', 'guestBirthDate', 'adults', 'children', 'babies', 'doubleBeds', 'singleBeds', 'startDate',
            'endDate', 'Location']

    dummy_df = dummy_df[cols]

    request_data = request.get_json()
    genre = request_data['gender']
    age = request_data['age']
    adultNumber=request_data['adults']
    childrenNumber=request_data['children']
    babiesNumber=request_data['babies']

    clustring.getProfile(genre ,age ,adultNumber ,childrenNumber , babiesNumber )


    for i in range(len(dummy_df['guestBirthDate'])):

        dummy_df['guestBirthDate'][i]= str(Profile.age(dummy_df['guestBirthDate'][i]))


    female = 0
    for i in range(len(dummy_df['guestGender'])):
        if dummy_df['guestGender'][i]=='Female':
            female+=1

    labels = ['Female', 'Male']
    values = [female  , len(dummy_df['guestGender'])-female]
    explode = (0.2, 0)
    colors = ['b', 'g']
    plt.pie(values, colors=colors, labels=labels,
            explode=explode, autopct='%1.1f%%',
            counterclock=False, shadow=True)
    plt.title('Profile Gender ')
    plt.legend(labels, loc=3)
    plt.show()

    dummy_df_male= dummy_df.groupby('guestGender').get_group(genre)

    print(tabulate(dummy_df_male, headers='keys', tablefmt='psql'))

    labels = ['17-25', '26-35' , '35-50' , '>50']
    v1 , v2 , v3 , v4 =0 ,0 ,0 ,0


    dummy_df_male_age = dummy_df_male.groupby("guestBirthDate").get_group(age)

    dummy_df_male_age_country = dummy_df_male.groupby("Location")

    print(tabulate(dummy_df_male_age_country , headers='keys', tablefmt='psql'))

    print(tabulate(dummy_df_male_age, headers='keys', tablefmt='psql'))

    dummy_df_male_age_status = dummy_df_male_age.groupby("adults").get_group(adultNumber)

    print("exemple de  classe/Niveau de profile : ")

    print(tabulate(dummy_df_male_age_status, headers='keys', tablefmt='psql'))

    return "Done"






if __name__ == "__main__":

    # Get all tags , type Data Frame
    print('##############   tags :')
   # print(tabulate(ServiceData.get_Tags_DataFrame({}), headers='keys', tablefmt='psql'))
    input()



    # get guest tags :
   # print('##############  Guest tags :')
   # print(tabulate(ServiceData.get_guestTag({}), headers='keys', tablefmt='psql'))
   # input()

    # get_guestReviews
    #print('##############  Guest Reviews :')
    #display(ServiceData.get_guestReviews({}))
    #print(tabulate(ServiceData.get_guestReviews({}), headers='keys', tablefmt='psql'))
    #input()

    # Recommendations :
    """""

    print('##############  Recommendation:')
    display(ServiceData.get_Recommendation_DataFrame({}))
    print(tabulate(ServiceData.get_guestReviews({}), headers='keys', tablefmt='psql'))
    input()

    print(tabulate(ServiceData.get_OnLineChek_DataFrame({}), headers='keys', tablefmt='psql'))
    profile_df = ServiceData.get_OnLineChek_DataFrame({})

    print( Profile.age(profile_df['guestBirthDate'][5]))

    for i in range(len(profile_df['guestBirthDate'])):

        if profile_df['checkStatus'][i]!='EMPTY':

          print(type(profile_df['guestBirthDate'][i]))
          profile_df['guestBirthDate'][i]= str(Profile.age(profile_df['guestBirthDate'][i]))



    print(tabulate(profile_df, headers='keys', tablefmt='psql'))
    Reseravtion = ServiceData.get_PropretBooking_DataFrame({})
    print(tabulate(Reseravtion , headers='keys', tablefmt='psql'))

    reseveravtionFeature=["_id","adults","children","babies","doubleBeds","singleBeds" , "startDate","endDate"]

    Reseravtion = Reseravtion[reseveravtionFeature]
    print(tabulate(Reseravtion, headers='keys', tablefmt='psql'))
    count=0
    for i in range(len(profile_df['checkStatus'])):
          for j in range(len(Reseravtion['_id'])):
              if  Reseravtion['_id'][j]== profile_df['propertyBookingId'][j]:
                  count+=1

    print("count ===> :" , count)

    Reseravtion.rename(columns={'_id': 'propertyBookingId'}, inplace=True)
    print(tabulate(Reseravtion, headers='keys', tablefmt='psql'))

    print(tabulate(profile_df, headers='keys', tablefmt='psql'))

   # engine.Recommend(ServiceData.get_Recommendation_DataFrame({}))

   # collaborative.getData(ServiceData.get_Recommendation_DataFrame({}), ServiceData.get_guestReviews({}))

    profile_df= profile_df[["propertyId" , "propertyBookingId" ,"guestGender","guestBirthDate"]]

    # get all category type data frame
    newdf=  pd.merge(profile_df, Reseravtion, on=['propertyBookingId','propertyBookingId'])
    print(newdf.columns)
    print(tabulate(newdf, headers='keys', tablefmt='psql'))

        """""
    #Let's load dummy Data
    dummy_df = pd.read_csv("./MOCK_DATA (4).csv")



    cols = ['guestGender',   'guestBirthDate' ,   'adults',   'children',   'babies' ,   'doubleBeds' ,   'singleBeds' ,'startDate', 'endDate' , 'Location']

    dummy_df = dummy_df[cols]

    print(tabulate(dummy_df, headers='keys', tablefmt='psql'))


    print("ok")



    #collaborative.getData(ServiceData.get_Recommendation_DataFrame({}), ServiceData.get_guestReviews({}))






    app.run(debug=False)


# test in POST MAN :
# http://127.0.0.1:5000/data
