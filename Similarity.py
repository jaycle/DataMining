import re
import numpy as np
from sklearn import metrics
import csv


with open('doc_data.csv') as file:
    # grab header then convert to list from first line in file
    headers = file.readline()
    headers = re.split(',', headers)
    # import data but skip first column containing website
    data = np.loadtxt(file, delimiter=',', usecols=range(1, len(headers)), dtype='int')
    # reset buffer to start and read article names
    file.seek(0)
    articles = np.loadtxt(file, delimiter=',', skiprows=1, usecols=(0,), dtype='S')


def sort_matrix(array):
    """
    Sorts the input array of articles from most to least similar
    :param array: numpy array of similarities between articles (2d)
    :return: list of tuples as (article_number_1, article_number_2, similarity_measurement)
    """
    size = len(array)

    l = []
    for row in range(size):
        for col in range(row+1, size):
            l.append((row, col, array[row][col]))

    # sort by third value in tuple
    return sorted(l, key=lambda sim: sim[2], reverse=True)


jac = metrics.pairwise_distances(data, metric='jaccard')
cos = metrics.pairwise_distances(data, metric='cosine')
euc = 1 - metrics.pairwise_distances(data, metric='euclidean')/100

# build similarity table output
sorted_similarities = list(zip(*[sort_matrix(jac), sort_matrix(cos), sort_matrix(euc)]))

similarity_table = [['Article A', 'Article B', 'Jaccard Similarity', 'Article A', 'Article B', 'Cosine Similarity',
                    'Article A', 'Article B', 'Euclidean Similarity']]
for sim in sorted_similarities:
    similarity_table.append(list(sum(sim, ())))

# build article reference table
reference_table = [['Article number', 'Site Address']]
for i in range(len(articles)):
    reference_table.append([i, articles[i].decode()])

print('Writing to file')
with open('sorted_similarity.csv', 'w') as output:
    sim_csv = csv.writer(output, lineterminator='\n')
    sim_csv.writerows(similarity_table)

with open('article_numbers.csv', 'w') as output:
    articles_csv = csv.writer(output, lineterminator='\n')
    articles_csv.writerows(reference_table)
