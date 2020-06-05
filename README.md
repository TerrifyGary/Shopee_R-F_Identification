# Shopee_R-F_Identification
NO MORE FAKE STUFF!

## Code Explain

## Getting What We Need
### createDataStruct()
```python=
def createDataStruct():
    
    c = conn.cursor()
    c.execute('''CREATE TABLE rating
                (comment text, star int, sellname text, realorfake text)''') # REAL_0 FAKE_1
    conn.commit()
    # conn.close()
```
This fuction is to create a sqlite (.db) file. By setting the comment(text), star(integer), sellname(text), and realorfake(text).

### getComments(star)
```python=
def getComments(star):
    t = (star,)
    c = conn.cursor()
    c.execute('SELECT * FROM rating WHERE star=? AND comment <> \'\'', t)

    return c.fetchall()
```

This is the part we search all the comment of a kind of rating star, which is convenient for usage in the future.

### scraping_comments(sellername, star_of_comment, fake_or_not)
```python=
def   scraping_comments(seller_name, star\_of\_comment, fake\_or\_not):

    c = conn.cursor()



    result = requests.get(f"https://shopee.tw/api/v2/shop/get?username={seller_name}")

    data = json.loads(result.text)

    userid = data['data']['userid']

    shopid = data['data']['shopid']



    result = requests.get(f"https://shopee.tw/api/v2/user/get_rating_summary?userid={userid}")

    data = json.loads(result.text)

    rating_count = data['data']['seller_rating_summary']['rating_count'][star_of_comment-1]

     print(rating_count)



    offset = 0

    rating_count = rating_count//100

    yu_ = rating_count%100



    for x in range(rating_count+1):

    result = requests.get(

     f"https://shopee.tw/api/v2/shop/get_ratings?filter=0&limit=100&offset={x*100}&shopid={shopid}&type={star_of_comment}&userid={userid}"

    )

    data = json.loads(result.text)

    for y in range(len(data['data']['items'])):

    item = data['data']['items'][y]

    comment = item['comment']

     if (comment != None and len(comment)>0 and comment != 'None'):

     # c.execute(f"INSERT INTO rating VALUES ('{comment}','{star_of_comment}','{seller_name}')")

    temp_list = [comment,star_of_comment,seller_name,fake_or_not]

    c.execute('INSERT INTO rating VALUES (?,?,?,?)', temp_list)

     print(comment)

```
First, we get the userid and shopeeid by scraping down the css on the shopee website. By doing so, we can scrape the css comment page.
After getting getting all the comments of a kind of star of the userpage, we are able to insert the data into the sqlite file.

```python=
name = "ruihuaa"
for x in range(5):
    scraping_comments(seller_name = name,star_of_comment = x+1,fake_or_not = 'Fake')
    # human_check.update({name:"FAKE"})


conn.commit()
conn.close()
```
Finally, by typying the shopee seller name, we are now able to insert the comment data into our "Data.db".

---

## Go Further

```python=
import jieba

all_comment = []
for x in range(len(df['comment'])):
    seg_list = jieba.cut_for_search(df['comment'][x])  # 搜索引擎模式
    jieba.set_dictionary('./dict.txt.big.txt')
    all_comment.append(",".join(seg_list))
# print(", ".join(seg_list))
print(all_comment)
```
By using JieBa, now we have the abilty to slice the comment data into single words.
Furthermore, we can use TfidfVectorizer to analyize how possitive or negative a comment is. 
PS. dict.txt.big.txt file is the comparison text file of Tradional Chinese.
```python=
from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer()
vectorizer.fit(all_comment)

# print("查看對應表")
# print(vectorizer.vectorizer.vocabulary_)

print(vectorizer.get_feature_names())
x_ = vectorizer.get_feature_names()
print(type(x_))
print("\n查看IDF對應的分數")
# print(vectorizer.idf_)
# 
# 編碼
vector = vectorizer.transform(all_comment)

print(vector.shape)

print("\n查看編碼後結果")
print(vector.toarray())
```
[ get_feature_names() ] : Array mapping from feature integer indices to feature name.
[ transform(self, raw_documents[, copy]) ] : Transform documents to document-term matrix.
