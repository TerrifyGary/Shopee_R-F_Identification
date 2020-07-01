from bs4 import BeautifulSoup
# from fake_useragent import UserAgent
import requests
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
import time
import random
import json
import sqlite3
import timeit
import time


start_time = time.time() # Recording the time of running the code

seller_comment = []
num_of_comment = []
headers = {'user-agent': 'Googlebot','From': 'YOUR EMAIL ADDRESS'}

one_star_len2_stopwords = ["糟糕","仿冒","山寨","假貨"]
one_star_len1_stopwords = ["假","仿","F","f","爛"]

def scraping_comments(seller_name, star_of_comment):
    
    result = requests.get(f"https://shopee.tw/api/v2/shop/get?username={seller_name}")
    data = json.loads(result.text)
    userid = data['data']['userid']
    shopid = data['data']['shopid']

    result = requests.get(f"https://shopee.tw/api/v2/user/get_rating_summary?userid={userid}")
    data = json.loads(result.text)
    rating_count = data['data']['seller_rating_summary']['rating_count'][star_of_comment-1]
    # print(rating_count)
    num_of_comment.append(rating_count)

    # offset = 0
    rating_count = rating_count//100
    # yu_ = rating_count%100

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
    # finding the substring
    star_1_comment = 0
    for x in comments:
        for c in one_star_len2_stopwords:
            if c in x:
                x.replace(c,'')
                star_1_comment +=1
    for y in comments:       
        for d in one_star_len1_stopwords:
            if d in y:
                y.replace(d,'')
                star_1_comment +=1 

    return int(star_1_comment)

def rating_bad(seller_name):
    result = requests.get(f"https://shopee.tw/api/v2/shop/get?username={seller_name}")
    data = json.loads(result.text)
    n_rating_bad = int(data['data']['rating_bad'])

    return n_rating_bad

def response_rate(seller_name):
    result = requests.get(f"https://shopee.tw/api/v2/shop/get?username={seller_name}")
    data = json.loads(result.text)
    n_response_rate = float(data['data']['response_rate'])
    
    return n_response_rate/100

def rating_star(seller_name):
    result = requests.get(f"https://shopee.tw/api/v2/shop/get?username={seller_name}")
    data = json.loads(result.text)
    n_rating_star = float(data['data']['rating_star'])

    return n_rating_star

def get_mall_price(url):
    all_price = []
    # url = "https://shopee.tw/mall/search?keyword=yeezy boost"

    r = requests.get(url,headers=headers)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'html.parser')
        # contents = soup.find_all("div",class_ = '_1NoI8_ _16BAGk')
        prices = soup.find_all("span", class_='_341bF0')

        for p in prices:
            price_ = p.text.replace(',','')
            all_price.append(int(price_))
        # print(all_price)

        avg_official_price = float(sum(all_price)/len(all_price))
        return avg_official_price
    else: 
        return 0

def get_web_info(url):
    check = True
    p_, s_ = '',''
    r_item_page = requests.get(url,headers=headers)

    if r_item_page.status_code == 200:
        soup_item_page = BeautifulSoup(r_item_page.text,'html.parser')
        # contents_item_page = soup_item_page.find_all("div",class_ = 'qaNIZv')
        price_item_page = soup_item_page.find_all("div",class_ = '_3n5NQx')
        seller_name = soup_item_page.find_all("div",class_ = '_3Lybjn')

        # print(seller_name)
        for p,s in zip(price_item_page,seller_name):
            p_ = p.text.replace('$','').replace(',','')
            for word in p_:
                if(word == '-'): # handling multiple price on same page.
                    check = False
                    break
            if(check == True):
                p_ = int(p_) 
            else:
                a_,b_ = p_.split('-')
                p_ = (int(a_.replace(' ',''))+int(b_.replace(' ','')))/2
            s_ = s.text
            # print(p_,s_)
        
        return p_,s_ # p_ stands for the price of the website, s_ stands for the seller name of the website

    else:
        return 0
    
if __name__ == '__main__':

    # text = input("Enter Seller Name : ")
    product = input("Enter Product Name : ")
    product_webpage_url = input("Enter Your Product Page URL : ")

    price,text = get_web_info(product_webpage_url)
    mall_price = get_mall_price(f"https://shopee.tw/mall/search?keyword={product}")
    for x in range(1,6,1):
        scraping_comments(text,x)

    # print(len(seller_comment))
    print('The Number of comments from 1~5 star = ',num_of_comment)
    print('Numbers of Fake Detected = ',checking(seller_comment))
    print('Numbers of Rating Bad = ',rating_bad(text))
    print('The avg raring star = ',rating_star(text))
    print('The response rate = ',response_rate(text))
    print('Official Shopee Price is :',mall_price)
    print('The Price of this site is :',price)
    print('Delta Price = ',abs(mall_price-price))
    print("It takes %s seconds to finish the code." % (time.time() - start_time))