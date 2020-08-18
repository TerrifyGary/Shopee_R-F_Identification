import json
import requests
import urllib.parse
#Reference:https://freelancerlife.info/zh/blog/python-web-scraping-user-agent-for-shopee/
#Reference:https://stackoverflow.com/questions/59557071/how-can-i-crawl-the-product-items-from-shopee-website
def get_shopids(query):
    parsed_query = urllib.parse.quote(query)
    url = f"https://shopee.tw/api/v2/search_items/?by=relevancy&keyword={parsed_query}&limit=50&newest=0&order=desc&page_type=search&version=2"
    headers = {
        'User-Agent': 'Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'referer': 'https://shopee.tw',
        #'if-none-match-': '55b03-35a627b0a83e6dd326f4ed6e81484fc9',
        }
    result = requests.get(url, headers = headers, allow_redirects=False)
    data = json.loads(result.text)
    print(result.status_code)
    for x in range(50):
        print(data['items'][x]['shopid'])

query = 'yeezy boost'
get_shopids(query)