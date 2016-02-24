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
    articles = np.loadtxt(file, delimiter=',', skiprows=1, usecols=(0,), dtype='str')


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


for i in range(len(articles)):
    print(str(articles[i])[1:])     # remove b' from beginning when printing

print('Jaccard:')
print(metrics.pairwise_distances(data, metric='jaccard'))
jac = metrics.pairwise_distances(data, metric='jaccard')
print(sort_matrix(jac))

print('Cosine:')
print(metrics.pairwise_distances(data, metric='cosine'))
cos = metrics.pairwise_distances(data, metric='cosine')

print('Euclidean:')
print(100 - metrics.pairwise_distances(data, metric='euclidean'))
euc = 1 - metrics.pairwise_distances(data, metric='euclidean')/100

# build output
sorted_similarities = [sort_matrix(jac), sort_matrix(cos), sort_matrix(euc)]
sorted_similarities = list(zip(*sorted_similarities))

table = [['Article A', 'Article B', 'Jaccard Similarity', 'Article A', 'Article B', 'Cosine Similarity',
         'Article A', 'Article B', 'Euclidean Similarity']]
for sim in sorted_similarities:
    new_row = []
    for attr in sim:
        for x in attr:
            new_row.append(x)
    table.append(new_row)

print('Writing to file')
with open('sorted_similarity.csv', 'w') as output:
    doc_csv = csv.writer(output, lineterminator='\n')
    doc_csv.writerows(table)

