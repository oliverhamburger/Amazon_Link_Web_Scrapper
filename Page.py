class Page:

    def __init__(self,url,wanted_price):
        self.url = url
        self.wanted_price = wanted_price

    def getWantedPrice(self):
        return self.wanted_price

    def getUrl(self):
        return self.url