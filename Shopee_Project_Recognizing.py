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




seller_comment = []
num_of_comment = []
headers = {'user-agent': 'Googlebot','From': 'YOUR EMAIL ADDRESS'}

one_star_len2_words = ["糟糕","惡劣","低端"] #change name later
one_star_len1_words = ["爛","糟","慘","臭","醜"]
two_star_len2_words = []
two_star_len1_words = []
three_star_len2_words = []
three_star_len1_words = []
four_star_len2_words = []
four_star_len1_words = [] 
five_star_len2_words = []
five_star_len1_words = []




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
            if (comment != None and len(comment)>0 and comment != 'None'): # basic filter
                seller_comment.append(comment)
    return seller_comment

def get_word_times_in_sentence(sentence,words,n):
    
    for c in words:
        if c in sentence:
            sentence.replace(c,'')
            n+=1

    return n

def couting_times(comments):
    # finding the substring
    star_comment_times = [0,0,0,0,0]
    
    for x in comments:
        star_comment_times[0] = get_word_times_in_sentence(x,one_star_len2_words,star_comment_times[0])
        star_comment_times[0] = get_word_times_in_sentence(x,one_star_len1_words,star_comment_times[0])

    return star_comment_times

def couting_fake(comments):

    f_word_times = 0

    fake_one_len1_words = ["假","仿"]
    fake_one_len2_words = ["仿冒","山寨","假貨"]
    for x in comments:
        f_word_times  = get_word_times_in_sentence(x,fake_one_len2_words,f_word_times)
        f_word_times  = get_word_times_in_sentence(x,fake_one_len1_words,f_word_times)
    return f_word_times

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
    shopid, itemid = url.split('.')[-2],url.split('.')[-1] # From the url, we can get the shopid first.

    reseult = requests.get(f"https://shopee.tw/api/v2/shop/get?is_brief=1&shopid={shopid}")
    data = json.loads(reseult.text)
    seller_name = data['data']['account']['username']

    r_ = requests.get(f"https://shopee.tw/api/v2/item/get?itemid={itemid}&shopid={shopid}")

    data_ = json.loads(r_.text)
    price_max = int(data_['item']['price_max'])/100000
    price_min = int(data_['item']['price_min'])/100000
    print((price_max+price_min)/2.0)
    avg_price = (price_max+price_min)/2.0
        
    return avg_price,seller_name # No More BS4 shit!!!
    

def scoring(delta_price, fake_time, rating_bad, rating_star):
    
    score = (delta_price+fake_time*200+rating_bad*100+rating_star*10)

    return score

if __name__ == '__main__':

    # text = input("Enter Seller Name : ")
    product = input("Enter Product Name : ")
    product_webpage_url = input("Enter Your Product Page URL : ")
    start_time = time.time() # Recording the time of running the code
    price,text = get_web_info(product_webpage_url)
    print(text)
    mall_price = get_mall_price(f"https://shopee.tw/mall/search?keyword={product}")
    for x in range(1,6,1):
        scraping_comments(text,x)

    # print(len(seller_comment))
    print('The Number of comments from 1~5 star = ',num_of_comment)
    # print('Numbers of Fake Detected = ',couting_times(seller_comment))
    print('Fake Words appearence times = ',couting_fake(seller_comment))
    print('Numbers of Rating Bad = ',rating_bad(text))
    print('The avg raring star = ',rating_star(text))
    print('The response rate = ',response_rate(text))
    print('Official Shopee Price is :',mall_price)
    print('The Price of this site is :',price)
    print('Delta Price = ',abs(mall_price-price)/price)
    print("It takes %s seconds to finish the code." % (time.time() - start_time))
    print('The score of the seller being real is ',scoring(cabs(mall_price-price)/price),outing_fake(seller_comment),rating_bad(text),response_rate(text)),'/1000')