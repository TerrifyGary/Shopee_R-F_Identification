import sqlite3
import pandas as pd
import jieba
from collections import Counter
# Create your connection.
conn = sqlite3.connect('C:/Users/user/Desktop/Shopee_R-F_Identification/Data.db')
jieba.set_dictionary('C:/Users/user/Desktop/Shopee_R-F_Identification/dict.txt.big.txt')
def top_words(star):
    df = pd.read_sql_query("SELECT * FROM rating", conn)
    df = pd.read_sql_query("SELECT * FROM rating WHERE star == (?)", conn, params=(star,))
    stopwords = ['的']
    comment_ = df['comment'].to_string()
    comment_ = ''.join(e for e in comment_ if e.isalpha())
    comment_ = ''.join(e for e in comment_ if e not in stopwords)
    words = jieba.lcut(comment_)
    #words.remove('n')
    #print(words)
    res = [] 
    for ele in words: 
        if ele.strip('n'): 
            res.append(ele)     
    return Counter(words).most_common(20)

for x in range(5):
    print('Number of star:',x+1,'Top 10 comments: ',top_words(star = x+1))
    
conn.commit()
conn.close()