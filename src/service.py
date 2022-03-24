from database import Database
import environement
Database.initialize()


class Service:
    def __init__(self):
        Database.initialize()

    def get_Tags_DataFrame(self, query):
        return Database.convert_to_dataFrame(environement.COLLECTION_TAGS, query)

    def get_Recommendation_DataFrame(self, query):
        return Database.convert_to_dataFrame(environement.COLLECTION_RECOMMENDATION, query)

    def get_guestTag(self, query):
        return Database.convert_to_dataFrame(environement.COLLECTION_GUEST_TAG, query)

    def get_guestCategory(self, query):
        return Database.convert_to_dataFrame(environement.COLLECTION_GUEST_CATEGORY, query)

    def get_guestReviews(self, query):
        return Database.convert_to_dataFrame(environement.COLLECTION_GUEST_REVIEWS, query)
