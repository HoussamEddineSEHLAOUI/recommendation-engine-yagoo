
from tabulate import tabulate
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np


def Recommend(df):
    global result
    print(type(df))


    new_features = ['fullAddress', 'title', 'category', 'description']

    df = df[new_features]
    df1=df[new_features]

    print(tabulate(df, headers='keys', tablefmt='psql'))

    for new_feature in new_features:
        df[new_feature] = df[new_feature].apply(clean_data)




    print(tabulate(df, headers='keys', tablefmt='psql'))


    df['soup'] = df.apply(create_soup, axis=1)

    print(tabulate(df, headers='keys', tablefmt='psql'))

    count = CountVectorizer(stop_words='english')
    count_matrix = count.fit_transform(df['soup'])
    cosine_sim2 = cosine_similarity(count_matrix, count_matrix)

    netflix_data = df.reset_index()

    indices = pd.Series(netflix_data.index, index=netflix_data['title'])

    print(indices)

    print("##########################################################################")
    print(get_recommendations_new('Boulangerie Daumesnil', cosine_sim2 , indices , df,df1))

def clean_data(x):
    return str.lower( str(x).replace(" ", ""))


def create_soup(x):
    return x['fullAddress']+ ' ' + x['title'] + ' ' + x['category'] + ' ' +x['description']




def get_recommendations_new(title, cosine_sim, indices, df, df1):
    global result
    title=title.replace(' ','').lower()
    idx = indices[title]

    # Get the pairwsie similarity scores of all recommendations with that recommendation
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the movies based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores of the 10 most similar recommendations
    sim_scores = sim_scores[1:11]

    # Get the movie indices
    recommendation_indices = [i[0] for i in sim_scores]

    # Return the top 10 most similar recommendation
    result =  df1['title'].iloc[recommendation_indices]
    result = result.to_frame()
    result = result.reset_index()
    del result['index']

    return result
