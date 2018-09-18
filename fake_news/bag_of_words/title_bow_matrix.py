import nltk
import pickle
from collections import defaultdict
import time
from nltk.corpus import stopwords
import random
import numpy as np

#Computes the 10,000 most common words in the title and makes bag of words matrix for titles
def make_OED(processed):
    OED = defaultdict(int)

    for i in range(len(processed)):
        temp_dict = processed[i][10]
        for k in temp_dict:
            OED[k] += temp_dict[k]

    all_words = []
    for k, v in OED.items():
        temp = [k, v]
        all_words.append(temp)

    stop_words = set(stopwords.words('english'))
    all_but_stop_words = [t for t in all_words if not t[0] in stop_words]

    # got sorted_by_second from https://stackoverflow.com/questions/3121979/how-to-sort-list-tuple-of-lists-tuples
    sorted_by_second = sorted(all_but_stop_words, key=lambda tup: tup[1])

    top_5k = [None] * 5000
    index = len(sorted_by_second) - 1
    for i in range(len(top_5k)):
        top_5k[i] = sorted_by_second[index][0]
        index -= 1

    print(top_5k)

    return top_5k


def make_matrix(words, articles):
    list = [None] * len(articles)
    ids = [None] * len(articles)
    for i in range(len(articles)):
        temp_list = []
        #        print(type(articles[i][0]))
        ids[i] = articles[i][0]
        if len(articles[i][10]) != 0:
            for word in words:
                temp_list.append(articles[i][10][word])
        else:
            for word in words:
                temp_list.append(0)
            print(f"index {i} title bow: {articles[i][10]}")
            print(len(temp_list))
        list[i] = temp_list
    print(list[0])
    return (list, ids)


if __name__ == '__main__':
    start = time.time()
    nltk.download('stopwords')
    pickle_in = open('../data/sorted_collected.pkl', 'rb')
    processed = pickle.load(pickle_in)

    print(f"start of making OED = {time.time()}")
    mega_words = make_OED(processed)
    print(f"end of making OED = {time.time()}")

    print(f"start of making matrix = {time.time()}")
    matrix = make_matrix(mega_words, processed) # returns (list, ids)
    print(f"end of making OED = {time.time()}")

   # matrix = np.array(matrix)
    pickle_out = open('../data/5k_words_title_matrix.pkl', 'wb')
    descr = 'bow matrix for sorted_collected.pkl 5k columns, for most common words in all titles; 1 row for each article'
    # in the form (matrix, ids), desc when you unpickle
    pickle.dump((matrix, descr), pickle_out)
    pickle_out.close()

    end = time.time()
    print(f"runtime: {end-start}")