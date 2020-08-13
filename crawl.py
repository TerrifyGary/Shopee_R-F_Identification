import sqlite3
from collections import Counter

import jieba
import pandas as pd

# Create your connection.
conn = sqlite3.connect('./Data.db')
jieba.set_dictionary('./dict.txt.big.txt')
def top_words(star, num):
    df = pd.read_sql_query("SELECT * FROM rating", conn)
    df = pd.read_sql_query("SELECT * FROM rating WHERE star == (?)", conn, params=(star,))
    stopwords = ['的','n','我','有','了']
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
    # return Counter(words).most_common(num)
    return res



num = 20
for x in range(5):
    print('Number of star:',x+1,'Top 10 comments: ',top_words(x+1, num))
    
# conn.commit()
# conn.close()
