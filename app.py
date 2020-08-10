from flask import Flask, render_template, request
import Shopee_Project_Recognizing as sp

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
        sum = 0

        if operation == 'fake_words':
            sum = float(product_url) + float(product_name)

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
                f"https://shopee.tw/mall/search?keyword={product_name}")

            return render_template('app.html', sum=sum)
        else:
            return render_template('app.html')

#⚠️⚠️⚠️------ Here Starts All Functions -------⚠️⚠️⚠️#


if __name__ == ' __main__':
    app.debug = True
    app.run()
