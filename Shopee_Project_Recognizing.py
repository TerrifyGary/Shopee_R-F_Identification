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


fake_one_len1_words = ["假","仿"]
fake_one_len2_words = ["仿冒","山寨","假貨"]

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
    start_time = time.time() # Recording the time of running the code
    price,text = get_web_info(product_webpage_url)
    mall_price = get_mall_price(f"https://shopee.tw/mall/search?keyword={product}")
    for x in range(1,6,1):
        scraping_comments(text,x)

    # print(len(seller_comment))
    print('The Number of comments from 1~5 star = ',num_of_comment)
    print('Numbers of Fake Detected = ',couting_times(seller_comment))
    print('Fake Words appearence times = ',couting_fake(seller_comment))
    print('Numbers of Rating Bad = ',rating_bad(text))
    print('The avg raring star = ',rating_star(text))
    print('The response rate = ',response_rate(text))
    print('Official Shopee Price is :',mall_price)
    print('The Price of this site is :',price)
    print('Delta Price = ',abs(mall_price-price))
    print("It takes %s seconds to finish the code." % (time.time() - start_time))