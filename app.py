from flask import Flask, render_template, request
import Shopee_Project_Recognizing as sp
from bs4 import BeautifulSoup
import requests
import time
import random
import json
import sqlite3
import timeit
import time

app = Flask(__name__)


@app.route('/')
def main():
    return render_template('app.html', static_url_path='/static')


@app.route('/send', methods=['POST','GET'])
def send(sum=sum):
    if request.method == 'POST':
        product_url = request.form['Product_URL']
        product_name = request.form['Product_Name']
        operation = request.form['operation']

        seller_comment = []
        num_of_comment = []

        price, text = sp.get_web_info(product_url)

        for x in range(1,6,1):
            sp.scraping_comments(text,x)
        
        sum = 0


        if operation == 'fake_words':

            sum = int(sp.couting_fake(seller_comment))
            return render_template('app.html', sum=sum)

        elif operation == 'shipping_time':

            sum = float(product_url) - float(product_name)
            return render_template('app.html', sum=sum)

        elif operation == 'rating_stars':
            sum = float(product_url) * float(product_name)

            return render_template('app.html', sum=sum)

        elif operation == 'delta_price':
            # sum = float(product_url) / float(product_name)
            sum = sp.get_mall_price(
                f"https://shopee.tw/mall/search?keyword={product_name}"
                ) - price

            return render_template('app.html', sum=sum)
        else:
            return render_template('app.html')

#⚠️⚠️⚠️------ Here Starts All Functions -------⚠️⚠️⚠️#


if __name__ == ' __main__':
    app.debug = True
    app.run()
