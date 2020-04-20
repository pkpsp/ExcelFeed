import requests
from bs4 import BeautifulSoup

class MoneyControl():

    def __init__(self, url):
        # super().__init__()
        response = requests.get(url)
        self.soup = BeautifulSoup(response.content, 'html.parser')
        self.data = response.text

    def getBseHigh(self):
        soup2 = self.soup.find_all(class_="clearfix lowhigh_band todays_lowhigh_wrap")[0]
        return float(soup2.find(class_="low_high3").get_text())
    def getBseLow(self):
        soup2 = self.soup.find_all(class_="clearfix lowhigh_band todays_lowhigh_wrap")[0]
        return float(soup2.find(class_="low_high1").get_text())

    def getBse52High(self):
        soup2 = self.soup.find_all(class_="clearfix lowhigh_band week52_lowhigh_wrap")[0]
        return float(soup2.find(class_="low_high3").get_text())
    def getBse52Low(self):
        soup2 = self.soup.find_all(class_="clearfix lowhigh_band week52_lowhigh_wrap")[0]
        return float(soup2.find(class_="low_high1").get_text())


    def getBseClose(self):
        return float(self.soup.find(id="bprevclose").get('value'))
    def getBseVwap(self):
        return float(self.soup.find_all(class_="prive_avgp avgp")[0].get_text())
    def getBseOpen(self):
        return float(self.soup.find_all(class_="prev_open priceopen")[0].get_text())
    def getBsePreClose(self):
        return float(self.soup.find_all(class_="prev_open priceprevclose")[0].get_text())
    def getBseVolume(self, removeComma = False):
        temp = self.soup.find_all(class_="txt13_pc volume_data")[0].get_text()
        if removeComma:
            return int(temp.replace(",",""))
        return temp
    def getBseID(self):
        return self.soup.find(id="bseid").get('value')

    def getNseHigh(self):
        soup2 = self.soup.find_all(class_="clearfix lowhigh_band todays_lowhigh_wrap")[1]
        return float(soup2.find(class_="low_high3").get_text())
    def getNseLow(self):
        soup2 = self.soup.find_all(class_="clearfix lowhigh_band todays_lowhigh_wrap")[1]
        return float(soup2.find(class_="low_high1").get_text())

    def getNse52High(self):
        soup2 = self.soup.find_all(class_="clearfix lowhigh_band week52_lowhigh_wrap")[1]
        return float(soup2.find(class_="low_high3").get_text())
    def getNse52Low(self):
        soup2 = self.soup.find_all(class_="clearfix lowhigh_band week52_lowhigh_wrap")[1]
        return float(soup2.find(class_="low_high1").get_text())


    def getNseClose(self):
        return float(self.soup.find(id="nprevclose").get('value'))
    def getNseVwap(self):
        return float(self.soup.find_all(class_="prive_avgp avgp")[1].get_text())
    def getNseOpen(self):
        return float(self.soup.find_all(class_="prev_open priceopen")[1].get_text())
    def getNsePreClose(self):
        return float(self.soup.find_all(class_="prev_open priceprevclose")[1].get_text())
    def getNseVolume(self, removeComma = False):
        temp = self.soup.find_all(class_="txt13_pc volume_data")[1].get_text()
        if removeComma:
            return int(temp.replace(",",""))
        return temp    
    def getNseID(self):
        return self.soup.find(id="nseid").get('value')
        
    def getSCID(self):
        return self.soup.find(id="scid").get('value')
    def getName(self):
        return self.soup.find(class_="pcstname").get_text()

stock = MoneyControl("https://www.moneycontrol.com/india/stockpricequote/oil-drillingexploration/oilnaturalgascorporation/ONG")

ml = []
mSpace = 15
def printLL(s, t = ""):
    # ml.append(s)
    temp = " "*(mSpace - len(t))
    print(t, temp, "==>", s)

print("=============================== BSE Details ===============================")
printLL(stock.getBseHigh(),"HIGH")
printLL(stock.getBseLow(),"LOW")
printLL(stock.getBse52High(),"52 WEEK HIGH")
printLL(stock.getBse52Low(), "52 WEEK LOW")
printLL(stock.getBseClose(), "CLOSE")
printLL(stock.getBseVwap(), "VWAP")
printLL(stock.getBseOpen(), "OPEN")
printLL(stock.getBsePreClose(), "PREVIOUS CLOSE")
printLL(stock.getBseVolume(True), "VOLUME (,)")
printLL(stock.getBseVolume(), "VOLUME")
printLL(stock.getBseID(), "ID")
# print()
print("=============================== NSE Details ===============================")
printLL(stock.getNseHigh(),"HIGH")
printLL(stock.getNseLow(),"LOW")
printLL(stock.getNse52High(),"52 WEEK HIGH")
printLL(stock.getNse52Low(), "52 WEEK LOW")
printLL(stock.getNseClose(), "CLOSE")
printLL(stock.getNseVwap(), "VWAP")
printLL(stock.getNseOpen(), "OPEN")
printLL(stock.getNsePreClose(), "PREVIOUS CLOSE")
printLL(stock.getNseVolume(True), "VOLUME (,)")
printLL(stock.getNseVolume(), "VOLUME")
printLL(stock.getNseID(), "ID")
# print()
print("============================= Company Details =============================")
printLL(stock.getSCID(),"SCID")
printLL(stock.getName(),"NAME")
print("===========================================================================")