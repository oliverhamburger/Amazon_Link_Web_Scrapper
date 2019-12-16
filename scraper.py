import requests
from Page import Page
from bs4 import BeautifulSoup
import smtplib
import time


#checks the name and price of the item
#returns true if the price has droped, meaning the email is sent and the program no longer has to check the price
def check_price(URL, wantedPrice):
    headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'}
    page = requests.get(URL, headers=headers)

    #workaround with two Beautiful soup objects becuse amazon.com makes html with javascroipt.
    soup = BeautifulSoup(page.content, 'html.parser')
    realSoup = BeautifulSoup(soup.prettify(), 'html.parser')

    #gets the title from URL and prints the data if no exceptions were thrown
    try:
        title = realSoup.find(id="productTitle").getText()
    except Exception:
        print("Error with getting the title")
    else:
        print(title.strip())

    #gets the price from URL and prints the data if no exceptions were thrown
    try:
        price = realSoup.find(id="priceblock_ourprice").getText()
    except Exception:
        #see if price replaced by a deal price
        try:
            price = realSoup.find(id="priceblock_dealprice").getText()
        except Exception:
            print("Error with getting the price(Item could be out of stock and not have a price at the moment)")
        else:
            price = price.replace(',', '')
            converted_price = float(price.strip()[1:])
            print(converted_price)

            # compare the price and determine if an email shoud be sent
            if (converted_price == 0.0):
                print('There is a problem with the price')
            elif (converted_price < wantedPrice):
                send_mail(URL)
                return True
            else:
               return False
        print("Error with getting the price(Item could be out of stock and not have a price at the moment)")
    else:
        price = price.replace(',', '')
        converted_price = float(price.strip()[1:])
        print(converted_price)

        #compare the price and determine if an email shoud be sent
        if(converted_price == 0.0):
            print('There is a problem with the price')
        elif (converted_price < wantedPrice):
            send_mail(URL)
            return True
        else:
            return False




#sends the notification email that the price has fallen
def send_mail(URL):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login('hamburger.soccer@gmail.com', 'vixxjbwhdjewwqqa')

    subject = 'Price fell down'
    body = 'Check the amazon link ' + URL

    msg = f"Subject: {subject}\n\n{body}"
    server.sendmail(
        'hamburger.soccer@gmail.com',
        'oliver.hamburger@uvm.edu',
        msg
    )
    print('Email has been sent')
    server.quit()





#create list of pages
pages = []

#create amazon.com pages and add them to the list
headphones = Page('https://www.amazon.com/Powerbeats-Pro-Totally-Wireless-Earphones/dp/B07R5QD598/ref=sr_1_3?crid=1P13WRASZMXBL&keywords=beats+workout+earbuds&qid=1576214123&sprefix=beats+work%2Caps%2C147&sr=8-3', 50)
pages.append(headphones)
computer = Page('https://www.amazon.com/Apple-MacBook-15-inch-512GB-Storage/dp/B07S58MHXF/ref=pd_rhf_dp_s_vtp_ses_clicks_shared_1_3/146-3009192-6710615?_encoding=UTF8&pd_rd_i=B07S58MHXF&pd_rd_r=bdc4f451-eab4-4f00-b7ef-c44aeaceb57b&pd_rd_w=YOqqT&pd_rd_wg=xwLZW&pf_rd_p=016ff402-c614-45c8-b1eb-3e2e77f84f7c&pf_rd_r=1198CHGY3TT6TASMM8MX&psc=1&refRID=1198CHGY3TT6TASMM8MX', 2000)
pages.append(computer)
adapter = Page('https://www.amazon.com/Belkin-Charge-Rockstar-Adapter-Charging/dp/B074WDWVX1/ref=sr_1_3?crid=30PHZFKKYQDQE&keywords=lightning+to+headphone+jack+belkin&qid=1576480494&s=electronics&sprefix=lightning+to+head%2Celectronics%2C159&sr=1-3',10)
pages.append(adapter)


#check to see if the price has changed every hour
while(len(pages) != 0):
    for page in pages:
        if(check_price(page.getUrl(), page.getWantedPrice()) == True):
            pages.remove(page)
    time.sleep(60)


#upload to git