import requests
from bs4 import BeautifulSoup
import smtplib

url = 'https://www.amazon.com/gp/product/B085Z4P89R/ref=ppx_yo_dt_b_asin_title_o08_s04?ie=UTF8&psc=1'
headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'}

def check_price():
    page = requests.get(url,headers=headers)
    soup = BeautifulSoup(page.content,'html.parser')

    title = soup.find('span',id="productTitle").get_text()
    price = soup.find('span',id="priceblock_ourprice").get_text()
    converted_price = float(price[1])

    if(converted_price < .8*converted_price):
        send_mail()

def send_mail(username = '',password = '',destination = ''):
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login(username,password)

    subject = 'Buy Seagate IronWolf 6TB!!!'
    body = 'Click the amazon link https://www.amazon.com/gp/product/B085Z4P89R/ref=ppx_yo_dt_b_asin_title_o08_s04?ie=UTF8&psc=1'
    msg = f"Subject: {subject}\n\n{body}"
    server.sendmail(username,destination,msg)
    server.quit()

check_price()