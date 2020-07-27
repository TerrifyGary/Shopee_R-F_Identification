import sqlite3
import jieba
from collections import Counter
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
#https://towardsdatascience.com/overview-of-text-similarity-metrics-3397c4601f50
jieba.set_dictionary('./dict.txt.big.txt')

def get_star_words(star, data):
    conn = sqlite3.connect('./'+data)
    df = pd.read_sql_query("SELECT * FROM rating", conn)
    df = pd.read_sql_query("SELECT * FROM rating WHERE star == (?)", conn, params=(star,))
    stopwords = ['的']
    comment_ = df['comment']
    comment_ = ''.join(e for e in comment_ if e not in stopwords)
    words = jieba.lcut(comment_)
    comment_ = ' '.join(e for e in words)
    return comment_

def get_all_words(data):
    conn = sqlite3.connect('./'+data)
    df = pd.read_sql_query("SELECT * FROM rating", conn)
    stopwords = ['的']
    comment_ = df['comment']
    comment_ = ''.join(e for e in comment_ if e not in stopwords)
    words = jieba.lcut(comment_)
    comment_ = ' '.join(e for e in words)
    return comment_

def get_cosine_sim(*strs): 
    vectors = [t for t in get_vectors(*strs)]
    return cosine_similarity(vectors)[0][1]
    
def get_vectors(*strs):
    text = [t for t in strs]
    vectorizer = CountVectorizer(text)
    vectorizer.fit(text)
    return vectorizer.transform(text).toarray()

for x in range(5):
    strs = [get_star_words(x+1, 'Data.db'), get_star_words(x+1, 'Data2.db')]
    print(x+1, 'Star Comments: Similarity', get_cosine_sim(*strs)*100,'%')
    
strs = [get_all_words('Data.db'), get_all_words('Data2.db')]
print('Total Comments: Similarity', get_cosine_sim(*strs)*100,'%')