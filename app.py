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
        # num_of_comment = []

        price, sellername = sp.get_web_info(product_url)

        for x in range(1,6,1):
            sp.scraping_comments(sellername,x)
        
        sum = 0


        if operation == 'fake_words':
            
            sum = operation + ' = ' + str(sp.couting_fake(seller_comment)) + ' times.'
            return render_template('app.html', sum=sum)

        elif operation == 'response_rate':

            sum = operation + ' = ' + str(sp.response_rate(sellername)*100) + '%'
            return render_template('app.html', sum=sum)
        
        elif operation == 'rating_bad':

            sum = operation + ' = ' + str(sp.rating_bad(sellername)) + ' times.'
            return render_template('app.html', sum=sum)

        elif operation == 'rating_stars':

            sum = operation + ' = ' + str(sp.rating_star(sellername)) + ' stars.'
            return render_template('app.html', sum=sum)

        elif operation == 'delta_price':
            # sum = float(product_url) / float(product_name)
            sum = operation + ' = ' +str(int(sp.get_mall_price(
                f"https://shopee.tw/mall/search?keyword={product_name}"
                ) - price))+' $NTD'

            return render_template('app.html', sum=sum)
        else:
            return render_template('app.html')

#⚠️⚠️⚠️------ Here Starts All Functions -------⚠️⚠️⚠️#  


if __name__ == ' __main__':
    app.debug = True
    app.run()
