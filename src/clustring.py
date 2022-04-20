import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from tabulate import tabulate
from sklearn.decomposition import PCA
import Profile
import service
from sklearn.cluster import KMeans
from kmeans_numpy_improved import *
from sklearn.cluster import MeanShift

def getProfile(genre ,age ,adultNumber ,childrenNumber , babiesNumber):
    guest_data = pd.read_csv("./MOCK_DATA (4).csv")



    cols = ['guestGender', 'guestBirthDate', 'adults', 'children', 'babies', 'doubleBeds', 'singleBeds']

    guest_data = guest_data[cols]
    print(tabulate(guest_data, headers='keys', tablefmt='psql'))

    encode = LabelEncoder()
    encoded_sex = encode.fit_transform(guest_data.iloc[:, 0])

    print(encoded_sex)
    guest_data['guestGender'] = encoded_sex

    print(tabulate(guest_data, headers='keys', tablefmt='psql'))

    #caluclate age from bithdate
    for i in range(len(guest_data['guestBirthDate'])):
        guest_data['guestBirthDate'][i] = str(Profile.age(guest_data['guestBirthDate'][i]))

    new_guest_data = guest_data.astype({"guestBirthDate": float}, errors='raise')

    print(tabulate(new_guest_data, headers='keys', tablefmt='psql'))
    print(new_guest_data.dtypes)
    input()

    pca_reducer = PCA(n_components=2)
    reduced_data = pca_reducer.fit_transform(new_guest_data)

    print(tabulate(reduced_data, headers='keys', tablefmt='psql'))
    """""
    km = KMeans(n_clusters=30)
    cluster = km.fit(reduced_data)

    plt.scatter(reduced_data[:, 0], reduced_data[:, 1], label='Datapoints')
    plt.scatter(cluster.cluster_centers_[:, 0], cluster.cluster_centers_[:, 1], label='Clusters')
    plt.title("Sklearn version of KMeans")
    plt.legend()
    plt.show()
    """""
    """""
    km_numpy = KMeans_numpy(n_clusters=5, tolerance=0.0001)
    clusters, clusterd_data = km_numpy.fit(reduced_data)
    clusters = np.array(clusters)
    cluster_one_data = np.array(clusterd_data[0])
    cluster_two_data = np.array(clusterd_data[1])
    cluster_three_data = np.array(clusterd_data[2])
    cluster_four_data = np.array(clusterd_data[3])
    cluster_five_data = np.array(clusterd_data[4])

    plt.figure(figsize=(12, 6))
    plt.scatter(cluster_one_data[:, 0], cluster_one_data[:, 1], c='r', label='Cluster One')
    plt.scatter(cluster_two_data[:, 0], cluster_two_data[:, 1], c='b', label='Cluster two')
    plt.scatter(cluster_three_data[:, 0], cluster_three_data[:, 1], c='g', label='Cluster three')
    plt.scatter(cluster_four_data[:, 0], cluster_four_data[:, 1], c='y', label='Cluster four')
    plt.scatter(cluster_five_data[:, 0], cluster_five_data[:, 1], c='orange', label='Cluster five')

    plt.scatter(clusters[:, 0], clusters[:, 1], marker='*', s=200, c='black', label='Centroids')
    plt.title("Custom KMeans results")
    plt.legend()
    plt.show()

  
    mshift = MeanShift(bandwidth=25)
    cluster_mean = mshift.fit(reduced_data)
    plt.scatter(reduced_data[:, 0], reduced_data[:, 1], label='Datapoints')
    plt.scatter(cluster_mean.cluster_centers_[:, 0], cluster_mean.cluster_centers_[:, 1], label='Clusters')
    plt.title("Sklearn version of KMeans")
    plt.legend()
    plt.show()
    """""

    full_data_kmeans = KMeans_numpy(n_clusters=5)
    centroids, clus_data = full_data_kmeans.fit(new_guest_data.values)

    cluster_1 = pd.DataFrame(clus_data[0],
                             columns=['guestGender', 'guestBirthDate', 'adults', 'children', 'babies', 'doubleBeds',
                                      'singleBeds'])
    cluster_2 = pd.DataFrame(clus_data[1],
                             columns=['guestGender', 'guestBirthDate', 'adults', 'children', 'babies', 'doubleBeds',
                                      'singleBeds'])
    cluster_3 = pd.DataFrame(clus_data[2],
                             columns=['guestGender', 'guestBirthDate', 'adults', 'children', 'babies', 'doubleBeds',
                                      'singleBeds'])
    cluster_4 = pd.DataFrame(clus_data[3],
                             columns=['guestGender', 'guestBirthDate', 'adults', 'children', 'babies', 'doubleBeds',
                                      'singleBeds'])


    print(tabulate(cluster_1, headers='keys', tablefmt='psql'))
    print(tabulate(cluster_2, headers='keys', tablefmt='psql'))
    print(tabulate(cluster_3, headers='keys', tablefmt='psql'))
    print(tabulate(cluster_4, headers='keys', tablefmt='psql'))

    print("Average age for guest in cluster four: {}".format(np.array(cluster_4['guestBirthDate']).mean()))
    print("Average number of adults {} ".format(np.array(cluster_4['adults']).mean()))
    print("Average number of children {} ".format(np.array(cluster_4['children']).mean()))
    print("Average number of babies {}".format(np.array(cluster_4['babies']).mean()))

    list_cluster1 = [np.array(cluster_1['guestBirthDate']).mean(), np.array(cluster_1['adults']).mean(),
                     np.array(cluster_1['children']).mean(), np.array(cluster_1['babies']).mean()]
    list_cluster2 = [np.array(cluster_2['guestBirthDate']).mean(), np.array(cluster_2['adults']).mean(),
                     np.array(cluster_2['children']).mean(), np.array(cluster_2['babies']).mean()]
    list_cluster3 = [np.array(cluster_3['guestBirthDate']).mean(), np.array(cluster_3['adults']).mean(),
                     np.array(cluster_3['children']).mean(), np.array(cluster_3['babies']).mean()]
    list_cluster4 = [np.array(cluster_1['guestBirthDate']).mean(), np.array(cluster_4['adults']).mean(),
                     np.array(cluster_4['children']).mean(), np.array(cluster_4['babies']).mean()]
    list_newGuest = [ float(age) ,adultNumber ,childrenNumber , babiesNumber]

    # print("Deviation of the mean for annual income (in thousends) for customers in cluster one: {}".format(np.array(cluster_1['Annual Income (k$)']).std()))
    print("In cluster one we have: {} guest".format(cluster_4.shape[0]))
    print("From those guest we have {} male and {} female".format(
        cluster_4.loc[(cluster_4['guestGender'] == 1.0)].shape[0],
        cluster_4.loc[(cluster_4['guestGender'] == 0.0)].shape[0]))

    def jaccard_binary(x, y):
        """A function for finding the similarity between two binary vectors"""
        intersection = np.logical_and(x, y)
        union = np.logical_or(x, y)
        similarity = intersection.sum() / float(union.sum())
        return similarity

    print("Jaccard Similarity with cluster 1 :  ", jaccard_binary(list_newGuest, list_cluster1))

    Jaccard_Similarities = [jaccard_binary(list_newGuest, list_cluster1), jaccard_binary(list_newGuest, list_cluster2),
                            jaccard_binary(list_newGuest, list_cluster3), jaccard_binary(list_newGuest, list_cluster4)]

    print("ce voyageur apartient au profile :", Jaccard_Similarities.index(max(Jaccard_Similarities)) + 1 , "with value of " , max(Jaccard_Similarities))



