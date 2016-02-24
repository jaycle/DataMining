import requests
import re
from lxml import html
from urllib import request
import csv

USE_LOCAL = False        # Use a local web page instead of network (for testing)
LOCAL_SITE_DIR = 'local_sites'


def build_dict(tree):
    """
    Builds a dictionary with [key] corresponding to lowercase words occurring in article and value
     as number of occurrences.
    :param tree: Element Tree of html retrieved from CNN
    :return: dict()
    """

    # At the time of this script, CNN content was placed in a div with attribute itemprop="articleBody"
    # We select all the paragraph tags under this div to trim to the article content
    content = tree.xpath('//div[@itemprop="articleBody"]//p')

    # if above comes back empty, try this
    if not content:
        content = tree.xpath('//div[@id="storytext"]//p')

    word_dictionary = dict()

    print('Building dictionary')
    for line in content:
        for word in re.finditer('[a-z]+', line.text_content(), re.IGNORECASE):
            w = word.group().lower()
            if w not in word_dictionary:
                word_dictionary[w] = 1
            else:
                word_dictionary[w] += 1

    return word_dictionary

if __name__ == '__main__' or 'builtins':
    dict_list = [] # list to hold tuple containing (website, dictionary)

    # Open list of sites to parse from correct location
    if USE_LOCAL:
        with open('local_site_list.txt') as site_list:
            for site in site_list:
                local_site = 'file:' + '/'.join([LOCAL_SITE_DIR, site.rstrip('\n')])
                page = request.urlopen(local_site).read()
                tree = html.fromstring(page)
                dict_list.append((local_site, build_dict(tree)))
    else:
        with open('cnn_site_list.txt') as site_list:
            for site in site_list:
                print('Requesting ', site.rstrip('\n'))
                page = requests.get(site.rstrip('\n'))
                print('Creating tree')
                tree = html.fromstring(page.text)
                dict_list.append((page.url, build_dict(tree)))

    # Loop through list of dictionaries and build super dictionary for all sites
    print('Building super dictionary')
    full_reference = []
    for article in dict_list:
        for word in article[1]:
            if word not in full_reference:
                full_reference.append(word)

    # Build table
    print('Creating Table')
    document_data = [['ARTICLE']]

    for column in range(len(full_reference)):
        # build new column with first position as the word
        new_col = [full_reference[column]]

        for article in dict_list:
            # if this is the first word, also add the article name
            if column == 0:
                document_data[0].append(article[0])
            if full_reference[column] in article[1]:
                new_col.append(article[1][full_reference[column]])
            else:
                new_col.append(0)

        document_data.append(new_col)

    print('Writing to file')
    with open('doc_data.csv', 'w') as output:
        doc_csv = csv.writer(output, lineterminator='\n')
        doc_csv.writerows(list(zip(*document_data)))