from database import Database
from bson.objectid import ObjectId
import pandas as pd
import environement
Database.initialize()


class Service:
    def __init__(self):
        Database.initialize()

    def convert_cursorWithObjID_to_ListWithoutObjID(self, cursor):
        return map(lambda row: {i: str(row[i]) if isinstance(row[i], ObjectId) else row[i] for i in row}, cursor)

    def convert_to_dataFrame(self, ListWithoutOId):
        return pd.DataFrame(list(ListWithoutOId)[:50])

    def get_Tags_DataFrame(self, query):
        Cursor_Tags = Database.find(environement.COLLECTION_TAGS, query)
        return self.convert_to_dataFrame(Cursor_Tags)

    def get_Recommendation_DataFrame(self, query):
        return self.convert_to_dataFrame(Database.find(environement.COLLECTION_RECOMMENDATION, query))

    def get_OnLineChek_DataFrame(self, query):
        return self.convert_to_dataFrame(Database.find(environement.COLLECTION_ONLINECHECK, query))

    def get_PropretBooking_DataFrame(self , query):
        return self.convert_to_dataFrame(Database.find(environement.COLLECTION_PROPRETYBOOKING , query))

    def get_guestTag(self, query):
        Cursor_Guest_Tag = Database.find(
            environement.COLLECTION_GUEST_TAG, query)
        list_guest_tag = []
        for row in Cursor_Guest_Tag:
            row['guestId'] = row['_id']['guestId']
            row['tagId'] = row['_id']['tagId']
            list_guest_tag.append(row)
        return self.convert_to_dataFrame(list_guest_tag)

    def get_guestCategory(self, query):
        Cursor_Guest_category = Database.find(
            environement.COLLECTION_GUEST_CATEGORY, query)
        list_guest_category = []
        for row in Cursor_Guest_category:
            row['guestId'] = row['_id']['guestId']
            row['category'] = row['_id']['category']
            list_guest_category.append(row)
        return self.convert_to_dataFrame(list_guest_category)

    def get_guestReviews(self, query):
        Cursor_Guest_Reviews = Database.find(
            environement.COLLECTION_GUEST_REVIEWS, query)
        list_guest_reviews = []
        for row in Cursor_Guest_Reviews:
            row['guestId'] = row['_id']['guestId']
            row['recommendationId'] = row['_id']['recommendationId']
            list_guest_reviews.append(row)
        return self.convert_to_dataFrame(list_guest_reviews)