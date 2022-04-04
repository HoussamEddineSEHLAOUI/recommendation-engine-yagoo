from database import Database
from bson.objectid import ObjectId
import pandas as pd
import environement


class Repository:
    def __init__(self):
        Database.initialize()

    def convert_cursorWithObjID_to_ListWithoutObjID(self, cursor):
        return map(lambda row: {i: str(row[i]) if isinstance(row[i], ObjectId) else row[i] for i in row}, cursor)

    def convert_to_dataFrame(self, ListWithoutOId):
        return pd.DataFrame(list(ListWithoutOId))

    def get_Guest_DataFrame(self, query):
        Cursor_Guest = Database.find(environement.COLLECTION_GUEST, query)
        return self.convert_to_dataFrame(Cursor_Guest)

    def get_Tags_DataFrame(self, query):
        Cursor_Tags = Database.find(environement.COLLECTION_TAGS, query)
        return self.convert_to_dataFrame(Cursor_Tags)

    def get_Category(self):
        Tags_data_frame = Database.find(environement.COLLECTION_TAGS, {})
        list_Categorie = []
        for row in Tags_data_frame:
            if str(row['category']) not in list_Categorie:
                list_Categorie.append(row['category'])
        return list_Categorie

    def get_Recommendation_DataFrame(self, query):
        return self.convert_to_dataFrame(Database.find(environement.COLLECTION_RECOMMENDATION, query))

    def get_OnLineChek_DataFrame(self, query):
        return self.convert_to_dataFrame(Database.find(environement.COLLECTION_ONLINECHECK, query))

    def get_guestTag(self, query):
        Cursor_Guest_Tag = Database.find(
            environement.COLLECTION_GUEST_TAG, query)
        list_guest_tag = []
        for row in Cursor_Guest_Tag:
            row['guestId'] = row['_id']['guestId']
            row['tagId'] = row['_id']['tagId']
            list_guest_tag.append(row)
        return self.convert_to_dataFrame(list_guest_tag)

    def get_guestTag_byId(self, query):
        Cursor_Guest_Tag = Database.find_one(
            collection=environement.COLLECTION_GUEST_TAG, query=query)
        if(Cursor_Guest_Tag != None):
            return Cursor_Guest_Tag['nbClickTag']
        return None

    def get_guestTag_byId_new(self, query, _id):
        Cursor_Guest_Tag = Database.find(
            collection=environement.COLLECTION_GUEST_TAG, query=query)
        for row in Cursor_Guest_Tag:
            if(_id == row['_id']):
                return row['nbClickTag']
        return -100

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
            if row['clickOnSliderPictures']:
                row['clickOnSliderPicturesScore'] = 1
            else:
                row['clickOnSliderPicturesScore'] = 0
            list_guest_reviews.append(row)
        return self.convert_to_dataFrame(list_guest_reviews)
