# Data base params
DATA_BASE_NAME = 'yaago-staging'
URL_DATA_BASE = 'mongodb+srv://stage:password1234$@yaago-prod-cluster-pri.hq5rg.mongodb.net/yaago-staging?authSource=admin&replicaSet=atlas-i9ni26-shard-0&w=majority&readPreference=primary&appname=MongoDB%20Compass&retryWrites=true&ssl=true'
#URL_DATA_BASE='mongodb+srv://root:T8GRF2_uB4/?qCvq@149.202.107.243:29517/yaago-prod-clone?retryWrites=true&ssl=false?authSource=admin'

# Name of collection :

COLLECTION_TAGS = 'tags'
COLLECTION_RECOMMENDATION = 'recommendation'
COLLECTION_GUEST_TAG = 'guestTag'
COLLECTION_GUEST_CATEGORY = 'guestCategory'
COLLECTION_GUEST_REVIEWS = 'guestReviews'
COLLECTION_ONLINECHECK='onLineCheck'
COLLECTION_PROPRETYBOOKING='propertyBooking'


#Data Scoring
SCORE_nbClickRecoCard = 1
SCORE_nbClickRecoMarker = 2
SCORE_nbClickRecoWebSite = 4
SCORE_nbClickRecoDirection = 10
SCORE_clickOnSliderPictures = 3
