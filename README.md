# Amazon_Link_Web_Scrapper

Web scrapper to alert user when amazon product price has fallen below threshold

Note: Uses BeautifulSoup which needs to be installed manualy (pip-install available)
Program scraps amazon.com links for the price and checks that price with a wanted price given by the user. If the original price has fallen below the given price, the program will send an email alert to notify the user the price has changed. The program will do this for a list of Page objects, which are created with a URL and a wanted price. Thanks and Enjoy!

In order for program to send an email when a price has dropped a sending email and password must be given on line 73. The sending and receiving email must also be given at lines 80 and 81. Sending email is set up to be a gmail (line 68). Browser header will depend on your browser (line 11). 
