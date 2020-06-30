from bs4 import BeautifulSoup
# from fake_useragent import UserAgent
import requests
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
import time
import random
import json
import sqlite3

seller_comment = []

def scraping_comments(seller_name, star_of_comment):
    
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
                seller_comment.append(comment)
    return seller_comment

def checking(comments):
    
    f_word_times = 0

    for x in comments:
        for y in x:
            if(y=='假' or y=='仿' or y=='爛'):
                f_word_times +=1
    return float(f_word_times/len(comments)*100)

def rating_bad(seller_name):
    result = requests.get(f"https://shopee.tw/api/v2/shop/get?username={seller_name}")
    data = json.loads(result.text)
    n_rating_bad = data['data']['rating_bad']

    return n_rating_bad

def response_rate(seller_name):
    result = requests.get(f"https://shopee.tw/api/v2/shop/get?username={seller_name}")
    data = json.loads(result.text)
    n_response_rate = data['data']['response_rate']
    
    return n_response_rate

def rating_star(seller_name):
    result = requests.get(f"https://shopee.tw/api/v2/shop/get?username={seller_name}")
    data = json.loads(result.text)
    n_rating_star = data['data']['rating_star']

    return n_rating_star

if __name__ == '__main__':

    text = input("Enter Seller Name ")
    
    for x in range(1,6,1):
        scraping_comments(text,x)

    # print(len(seller_comment))
    print('Numbers of Fake Detected = ',checking(seller_comment),'%')
    print('Numbers of Rating Bad = ',rating_bad(text))
    print('The avg raring star = ',rating_star(text))
    print('The response rate = ',response_rate(text))
