
from turtle import color
from cleaningData import CleaningData
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.recommendation import ALS
from pyspark.sql import Row
from pyspark.sql import SparkSession
from pyspark.ml.feature import StringIndexer
from pyspark.ml import Pipeline
from pyspark.sql.types import StructType, StructField, IntegerType
from bson.objectid import ObjectId
from pyspark.sql.functions import col
from termcolor import colored
import pandas as pd
import findspark
findspark.init("D:/Spark/spark-3.0.3-bin-hadoop2.7/bin")


# # initialize the spark session
# spark = SparkSession.builder.appName(appName).getOrCreate()
appName = "Collaborative Filtering"


class Engine:
    def __init__(self):
        self.cleaningData = CleaningData()

    def get_MatrixPlein_Guest_x_Recommendation_Behavior(self):

        # initialize the spark session
        spark = SparkSession.builder.appName(appName).getOrCreate()

        Matrix_Guest_x_Recommendation_Behavior_withNone_pd = self.cleaningData.get_Matrix_Guest_x_Recommendation_Behavior()
        print('GET ALL DATA IS DONE  SUCCES  !')
        # Create PySpark DataFrame from Pandas
        Matrix_Guest_x_Recommendation_Behavior_withNone_spark = spark.createDataFrame(
            Matrix_Guest_x_Recommendation_Behavior_withNone_pd)
        Matrix_Guest_x_Recommendation_Behavior_withNone_spark.printSchema()
        Matrix_Guest_x_Recommendation_Behavior_withNone_spark.show()

        print('START CONVERT PANDA TO SPARK ')
        # Matrix_Guest_x_Recommendation_Behavior_withNone_spark = Matrix_Guest_x_Recommendation_Behavior_withNone_spark.withColumn(
        #     'guestId', array('guestId'))

        print('CONVERT STRING TO INDEX')
        indexer = [StringIndexer(inputCol=column, outputCol=column+"_index")
                   for column in ['guestId', 'recommendationId']]
        pipeline = Pipeline(stages=indexer)
        transformed = pipeline.fit(Matrix_Guest_x_Recommendation_Behavior_withNone_spark).transform(
            Matrix_Guest_x_Recommendation_Behavior_withNone_spark)
        transformed.select(
            ['guestId', 'recommendationId', 'recommendationId_index', 'guestId_index'])

        transformed.show()

        print('GET 0.8 0.2 from date')
        (training, test) = transformed.randomSplit(
            [0.8, 0.2])

        print('SATRT')
        # ratings = spark.createDataFrame(
        #     Matrix_Guest_x_Recommendation_Behavior_withNone)
        print('GET ALL DATA IS DONE  SUCCES  0.8 AND 0.2 !')

        # Build the recommendation model using ALS on the training data
        # Note we set cold start strategy to 'drop' to ensure we don't get NaN evaluation metrics
        als = ALS(maxIter=5, regParam=0.01, userCol="guestId_index", itemCol="recommendationId_index", ratingCol="rating",
                  coldStartStrategy="drop", nonnegative=True)

        print('\n\n\n\n\n\n\n\n\n\n  LET S GET INSIDE ALS  \n\n\n\n\n\n\n\n\n\n')
        model = als.fit(training)

        print('\n\n\n\n\n\n\n\n\n\n  CREATION OF THE MODEL IS DONE  \n\n\n\n\n\n\n\n\n\n')
        # Evaluate the model by computing the RMSE on the test data
        predictions = model.transform(test)
        evaluator = RegressionEvaluator(metricName="rmse", labelCol="rating",
                                        predictionCol="prediction")
        rmse = evaluator.evaluate(predictions)
        print("Root-mean-square error = " + str(rmse))

        print('\n\n\n TRANSFORMED MATRIX :')
        model.recommendForAllUsers(10).show()

        print('\n\n\n\n Visuialise recommendations \n\n\n\n\n')
        test = model.recommendForAllUsers(10).filter(
            col('guestId_index') == 3).select("recommendations").collect()
        TopRECOMMENDATION = []
        for item in test[0][0]:
            TopRECOMMENDATION.append(item.recommendationId_index)

        schema = StructType(
            [StructField("recommendationId_index", IntegerType(), True)])
        RECOMMENDATION_FIN = spark.createDataFrame(
            TopRECOMMENDATION, IntegerType()).toDF("recommendationId_index")

        print(colored('\n\n\n Old Data : \n\n\ns', 'red'))
        transformed\
            .select(['guestId', 'recommendationId', 'rating', 'SCORE_BEHAVIOR'])\
            .filter(col('guestId') == '6217efa3d8eaa414b9052470')\
            .show()
        print('\n\n\n\n Recommendation : \n\n\n')
        RECOMMENDATION_FIN\
            .join(transformed, on='recommendationId_index', how='inner')\
            .select(['recommendationId', 'rating'])\
            .show()

        # stop spark session
        spark.stop()
        return RECOMMENDATION_FIN

    def get_Recommendation_Behavior(self, guestId):
        # initialize the spark session
        spark = SparkSession.builder.appName(appName).getOrCreate()

        get_Matrix_Guest_x_Recommendation_Behavior = self.cleaningData.get_Matrix_Guest_x_Recommendation_Behavior()

        RECOMMENDATION_DATAFRAME = get_Matrix_Guest_x_Recommendation_Behavior[1]
        Matrix_Guest_x_Recommendation_Behavior_withNone_pd = get_Matrix_Guest_x_Recommendation_Behavior[
            0]
        print('GET ALL DATA IS DONE  SUCCES  !')
        # Create PySpark DataFrame from Pandas
        Matrix_Guest_x_Recommendation_Behavior_withNone_spark = spark.createDataFrame(
            Matrix_Guest_x_Recommendation_Behavior_withNone_pd)
        Matrix_Guest_x_Recommendation_Behavior_withNone_spark.printSchema()
        Matrix_Guest_x_Recommendation_Behavior_withNone_spark.show()

        print('CONVERT STRING TO INDEX')
        indexer = [StringIndexer(inputCol=column, outputCol=column+"_index")
                   for column in ['guestId', 'recommendationId']]
        pipeline = Pipeline(stages=indexer)
        transformed = pipeline.fit(Matrix_Guest_x_Recommendation_Behavior_withNone_spark).transform(
            Matrix_Guest_x_Recommendation_Behavior_withNone_spark)
        transformed.select(
            ['guestId', 'recommendationId', 'recommendationId_index', 'guestId_index']).show(truncate=False)

        # Get the index of the
        index_of_our_guest_DATAFRAME = transformed.select(
            ['guestId', 'guestId_index']).filter(col('guestId') == guestId)

        # Convert it to Data frame panda
        PANDA_DATA_FRAME = index_of_our_guest_DATAFRAME.toPandas()

        for index, row_guest in PANDA_DATA_FRAME.iterrows():
            print(row_guest)
            index_of_our_guest = row_guest['guestId_index']
            break

        print(index_of_our_guest)
        print("GUESSSST INDEX :" + str(index_of_our_guest))

        print('GET 0.8 0.2 from date')
        (training, test) = transformed.randomSplit(
            [0.8, 0.2])
        # Build the recommendation model using ALS on the training data
        # Note we set cold start strategy to 'drop' to ensure we don't get NaN evaluation metrics
        als = ALS(maxIter=5, regParam=0.01, userCol="guestId_index", itemCol="recommendationId_index", ratingCol="rating",
                  coldStartStrategy="drop", nonnegative=True)

        print('\n\n\n\n\n\n\n\n\n\n  LET S GET INSIDE ALS  \n\n\n\n\n\n\n\n\n\n')
        model = als.fit(training)

        print('\n\n\n\n Visuialise recommendations \n\n\n\n\n')
        test = model.recommendForAllUsers(20).filter(
            col('guestId_index') == index_of_our_guest).select("recommendations").collect()
        TopRECOMMENDATION = []
        for item in test[0][0]:
            TopRECOMMENDATION.append(item.recommendationId_index)

        schema = StructType(
            [StructField("recommendationId_index", IntegerType(), True)])
        RECOMMENDATION_FIN = spark.createDataFrame(
            TopRECOMMENDATION, IntegerType()).toDF("recommendationId_index")

        print(colored('\n\n\n Old Data : \n\n\ns', 'red'))
        transformed\
            .select(['guestId', 'recommendationId', 'rating', 'SCORE_BEHAVIOR'])\
            .filter(col('guestId') == guestId)\
            .show()
        print('\n\n\n\n Recommendation : \n\n\n')
        RESULT = RECOMMENDATION_FIN\
            .join(transformed, on='recommendationId_index', how='inner')\
            .select(['recommendationId', 'rating'])
        SORT_RESULT = RESULT.toPandas()
        SORT_RESULT = SORT_RESULT.sort_values(
            by='rating', ascending=False, na_position='last')
        # stop spark session
        spark.stop()

        print('RECOMENDATION with all details :')
        List_DATA = []
        for index, row_recommendation_sort in SORT_RESULT.iterrows():
            recommendationId = row_recommendation_sort['recommendationId']
            for index, row_recommendation in RECOMMENDATION_DATAFRAME.iterrows():
                if(str(recommendationId) == str(row_recommendation['_id'])):
                    print(row_recommendation_sort)
                    List_DATA.append(row_recommendation)
                    break
        ALL_DATA_ABOUT_RECOMMENDATION_SORT = pd.DataFrame(
            list(List_DATA))

        print(ALL_DATA_ABOUT_RECOMMENDATION_SORT)

        # return RESULT.sort_values(["rating"], ascending=True)
        return ALL_DATA_ABOUT_RECOMMENDATION_SORT

    def get_MatrixPlein_Guest_x_Recommendation_on_Category(self):
        return 'get_MatrixPlein_Guest_x_Recommendation_on_Category'

    def get_MatrixPlein_Guest_x_Recommendation_on_Tags(self):
        return 'get_MatrixPlein_Guest_x_Recommendation_on_Tags'
