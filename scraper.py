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
    #enter sending email and passwrod
    server.login('email@email.com', 'emailpassword')

    subject = 'Price fell down'
    body = 'Check the amazon link ' + URL

    msg = f"Subject: {subject}\n\n{body}"
    server.sendmail(
        'sendingEmail@email.com',
        'recevingEmail@email.com',
        msg
    )
    print('Email has been sent')
    server.quit()





#create list of pages
pages = []

#create amazon.com pages and add them to the list
headphones = Page('https://www.amazon.com/Powerbeats-Pro-Totally-Wireless-Earphones/dp/B07R5QD598/ref=sr_1_3?crid=1P13WRASZMXBL&keywords=beats+workout+earbuds&qid=1576214123&sprefix=beats+work%2Caps%2C147&sr=8-3', 50)
pages.append(headphones)
computer = Page('https://www.amazon.com/Apple-MacBook-16-inch-512GB-Storage/dp/B081FZV45H/ref=sr_1_4?crid=30VE2VXC6RFMW&keywords=apple+macbook+pro&qid=1578025208&s=electronics&sprefix=apple+mac%2Celectronics%2C193&sr=1-4', 2000)
pages.append(computer)
adapter = Page('https://www.amazon.com/Belkin-Charge-Rockstar-Adapter-Charging/dp/B074WDWVX1/ref=sr_1_3?crid=30PHZFKKYQDQE&keywords=lightning+to+headphone+jack+belkin&qid=1576480494&s=electronics&sprefix=lightning+to+head%2Celectronics%2C159&sr=1-3',10)
pages.append(adapter)


#check to see if the price has changed every hour
while(len(pages) != 0):
    for page in pages:
        if(check_price(page.getUrl(), page.getWantedPrice()) == True):
            pages.remove(page)
    time.sleep(60)

