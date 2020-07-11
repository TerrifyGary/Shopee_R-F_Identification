from bs4 import BeautifulSoup
# from fake_useragent import UserAgent
import requests
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
import time
import random
import json
import sqlite3

# human_check = {}

conn = sqlite3.connect('./Shopee_R-F_Identification/Data2.db')
 
def createDataStruct():
    
    c = conn.cursor()
    c.execute('''CREATE TABLE rating
                (comment text, star int, sellname text, realorfake text)''') # REAL_0 FAKE_1
    conn.commit()
    # conn.close()


def getComments(star):
    t = (star,)
    c = conn.cursor()
    c.execute('SELECT * FROM rating WHERE star=? AND comment <> \'\'', t)

    return c.fetchall()


def scraping_comments(seller_name, star_of_comment, fake_or_not):
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
    
    
# createDataStruct()

name = "ninesofficial"
for x in range(5):
    scraping_comments(seller_name = name,star_of_comment = x+1,fake_or_not = 'Fake')
    # human_check.update({name:"FAKE"})


conn.commit()
conn.close()


# print(getComments(star = 5))