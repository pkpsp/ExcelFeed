import requests
from bs4 import BeautifulSoup

class MoneyControl():

    valuation = "value_txtfr"

    def __init__(self, url):
        # super().__init__()
        response = requests.get(url)
        self.soup = BeautifulSoup(response.content, 'html.parser')
        self.standAloneSoup = self.soup.find(id="standalone_valuation")
        self.conSolidatedSoup = self.soup.find(id="consolidated_valuation")
        self.bseSoup = self.soup.find(id="div_bse_livebox_wrap")
        self.nseSoup = self.soup.find(id="div_nse_livebox_wrap")
    
    # div_bse_livebox_wrap
    def getBseHigh(self):
        soup2 = self.bseSoup.find(class_="clearfix lowhigh_band todays_lowhigh_wrap")
        temp = soup2.find(class_="low_high3").get_text()
        try:
            return float(temp)
        except:
            return None
    def getBseLow(self):
        soup2 = self.bseSoup.find(class_="clearfix lowhigh_band todays_lowhigh_wrap")
        temp = soup2.find(class_="low_high1").get_text()
        try:
            return float(temp)
        except:
            return None
    def getBse52High(self):
        soup2 = self.bseSoup.find(class_="clearfix lowhigh_band week52_lowhigh_wrap")
        temp = soup2.find(class_="low_high3").get_text()
        try:
            return float(temp)
        except:
            return None
    def getBse52Low(self):
        soup2 = self.bseSoup.find(class_="clearfix lowhigh_band week52_lowhigh_wrap")
        temp = soup2.find(class_="low_high1").get_text()
        try:
            return float(temp)
        except:
            return None
    def getBseClose(self):
        temp = self.soup.find(id="bprevclose").get('value')
        try:
            return float(temp)
        except:
            return None
    def getBseVwap(self):
        temp = self.bseSoup.find(class_="prive_avgp avgp").get_text()
        try:
            return float(temp)
        except:
            return None
    def getBseOpen(self):
        temp = self.bseSoup.find(class_="prev_open priceopen").get_text()
        try:
            return float(temp)
        except:
            return None
    def getBsePreClose(self):
        temp = self.bseSoup.find(class_="prev_open priceprevclose").get_text()
        try:
            return float(temp)
        except:
            return None
    def getBseVolume(self, removeComma = True):
        temp = self.bseSoup.find(class_="txt13_pc volume_data").get_text()
        if removeComma:
            try:
                return int(temp.replace(",",""))
            except:
                return None
        return temp
    def getBseID(self):
        return self.soup.find(id="bseid").get('value')

    # div_nse_livebox_wrap
    def getNseHigh(self):
        soup2 = self.nseSoup.find(class_="clearfix lowhigh_band todays_lowhigh_wrap")
        temp = soup2.find(class_="low_high3").get_text()
        try:
            return float(temp)
        except:
            return None
    def getNseLow(self):
        soup2 = self.nseSoup.find(class_="clearfix lowhigh_band todays_lowhigh_wrap")
        temp = soup2.find(class_="low_high1").get_text()
        try:
            return float(temp)
        except:
            return None
    def getNse52High(self):
        soup2 = self.nseSoup.find(class_="clearfix lowhigh_band week52_lowhigh_wrap")
        temp = soup2.find(class_="low_high3").get_text()
        try:
            return float(temp)
        except:
            return None
    def getNse52Low(self):
        soup2 = self.nseSoup.find(class_="clearfix lowhigh_band week52_lowhigh_wrap")
        temp = soup2.find(class_="low_high1").get_text()
        try:
            return float(temp)
        except:
            return None
    def getNseClose(self):
        temp = self.soup.find(id="nprevclose").get('value')
        try:
            return float(temp)
        except:
            return None
    def getNseVwap(self):
        temp = self.nseSoup.find(class_="prive_avgp avgp").get_text()
        try:
            return float(temp)
        except:
            return None
    def getNseOpen(self):
        temp = self.nseSoup.find(class_="prev_open priceopen").get_text()
        try:
            return float(temp)
        except:
            return None
    def getNsePreClose(self):
        temp = self.nseSoup.find(class_="prev_open priceprevclose").get_text()
        try:
            return float(temp)
        except:
            return None
    def getNseVolume(self, removeComma = True):
        temp = self.nseSoup.find(class_="txt13_pc volume_data").get_text()
        if removeComma:
            try:
                return int(temp.replace(",",""))
            except:
                return None
        return temp    
    def getNseID(self):
        return self.soup.find(id="nseid").get('value')
        
    def getSCID(self):
        return self.soup.find(id="scid").get('value')
    def getName(self):
        return self.soup.find(class_="pcstname").get_text()

    def getMarketCaptureStandalone(self, removeComma = True):
        temp = self.standAloneSoup.find_all(class_ = self.valuation)[0].get_text()
        if removeComma:
            try:
                return float(temp.replace(",",""))
            except:
                return None
        return temp    
    def getPEStandalone(self, removeComma = True):
        temp = self.standAloneSoup.find_all(class_ = self.valuation)[1].get_text()
        if removeComma:
            try:
                return float(temp.replace(",",""))
            except:
                return None
        return temp    
    def getBookValueStandalone(self, removeComma = True):
        temp = self.standAloneSoup.find_all(class_ = self.valuation)[2].get_text()
        if removeComma:
            try:
                return float(temp.replace(",",""))
            except:
                return None
        return temp    
    def getDividentStandalone(self, removeComma = True):
        temp = self.standAloneSoup.find_all(class_ = self.valuation)[3].get_text()
        if removeComma:
            try:
                return float(temp.replace(",",""))
            except:
                return None
        return temp    
    def getMarketLotStandalone(self):
        temp = self.standAloneSoup.find_all(class_ = self.valuation)[4].get_text()
        return int(temp)
    def getIndustryPEStandalone(self, removeComma = True):
        temp = self.standAloneSoup.find_all(class_ = self.valuation)[5].get_text()
        if removeComma:
            try:
                return float(temp.replace(",",""))
            except:
                return None
        return temp    
    def getEPSStandalone(self, removeComma = True):
        temp = self.standAloneSoup.find_all(class_ = self.valuation)[6].get_text()
        if removeComma:
            try:
                return float(temp.replace(",",""))
            except:
                return None
        return temp    
    def getPCStandalone(self, removeComma = True):
        temp = self.standAloneSoup.find_all(class_ = self.valuation)[7].get_text()
        if removeComma:
            try:
                return float(temp.replace(",",""))
            except:
                return None
        return temp    
    def getPriceBookRatioStandalone(self, removeComma = True):
        temp = self.standAloneSoup.find_all(class_ = self.valuation)[8].get_text()
        if removeComma:
            try:
                return float(temp.replace(",",""))
            except:
                return None
        return temp    
    def getDividentYieldStandalone(self, removeComma = True):
        temp = self.standAloneSoup.find_all(class_ = self.valuation)[9].get_text()
        if removeComma:
            try:
                return float(temp.replace(",",""))
            except:
                return None
        return temp    
    def getFaceValueStandalone(self, removeComma = True):
        temp = self.standAloneSoup.find_all(class_ = self.valuation)[10].get_text()
        if removeComma:
            try:
                return float(temp.replace(",",""))
            except:
                return None
        return temp    
    def getDeliverablesStandalone(self):
        soup2 = self.standAloneSoup.find_all(class_ = self.valuation)[11]
        try:
            temp = soup2.find('a').get_text()
            return float(temp)
        except:
            soup2.get_text()
        
    def getMarketCaptureConsolidated(self, removeComma = True):
        temp = self.conSolidatedSoup.find_all(class_ = self.valuation)[0].get_text()
        if removeComma:
            try:
                return float(temp.replace(",",""))
            except:
                return None
        return temp    
    def getPEConsolidated(self, removeComma = True):
        temp = self.conSolidatedSoup.find_all(class_ = self.valuation)[1].get_text()
        if removeComma:
            try:
                return float(temp.replace(",",""))
            except:
                return None
        return temp    
    def getBookValueConsolidated(self, removeComma = True):
        temp = self.conSolidatedSoup.find_all(class_ = self.valuation)[2].get_text()
        if removeComma:
            try:
                return float(temp.replace(",",""))
            except:
                return None
        return temp    
    def getDividentConsolidated(self, removeComma = True):
        temp = self.conSolidatedSoup.find_all(class_ = self.valuation)[3].get_text()
        if removeComma:
            try:
                return float(temp.replace(",",""))
            except:
                return None
        return temp    
    def getMarketLotConsolidated(self):
        temp = self.conSolidatedSoup.find_all(class_ = self.valuation)[4].get_text()
        return int(temp)
    def getIndustryPEConsolidated(self, removeComma = True):
        temp = self.conSolidatedSoup.find_all(class_ = self.valuation)[5].get_text()
        if removeComma:
            try:
                return float(temp.replace(",",""))
            except:
                return None
        return temp    
    def getEPSConsolidated(self, removeComma = True):
        temp = self.conSolidatedSoup.find_all(class_ = self.valuation)[6].get_text()
        if removeComma:
            try:
                return float(temp.replace(",",""))
            except:
                return None
        return temp    
    def getPCConsolidated(self, removeComma = True):
        temp = self.conSolidatedSoup.find_all(class_ = self.valuation)[7].get_text()
        if removeComma:
            try:
                return float(temp.replace(",",""))
            except:
                return None
        return temp    
    def getPriceBookRatioConsolidated(self, removeComma = True):
        temp = self.conSolidatedSoup.find_all(class_ = self.valuation)[8].get_text()
        if removeComma:
            try:
                return float(temp.replace(",",""))
            except:
                return None
        return temp    
    def getDividentYieldConsolidated(self, removeComma = True):
        temp = self.conSolidatedSoup.find_all(class_ = self.valuation)[9].get_text()
        if removeComma:
            try:
                return float(temp.replace(",",""))
            except:
                return None
        return temp    
    def getFaceValueConsolidated(self, removeComma = True):
        temp = self.conSolidatedSoup.find_all(class_ = self.valuation)[10].get_text()
        if removeComma:
            try:
                return float(temp.replace(",",""))
            except:
                return None
        return temp    
    def getDeliverablesConsolidated(self):
        soup2 = self.conSolidatedSoup.find_all(class_ = self.valuation)[11]
        try:
            temp = soup2.find('a').get_text()
            return float(temp)
        except:
            return None

######################################################################################################################



# stock = MoneyControl("https://www.moneycontrol.com/india/stockpricequote/domestic-appliances/hawkinscooker/HC02")
# stock = MoneyControl("https://www.moneycontrol.com/india/stockpricequote/pharmaceuticals/glenmarkpharma/GP08")
# stock = MoneyControl("https://www.moneycontrol.com/india/stockpricequote/oil-drillingexploration/oilnaturalgascorporation/ONG")
stock = MoneyControl("https://www.moneycontrol.com/india/stockpricequote/finance-housing/indiabullshousingfinance/IHF01")


ml = []
mSpace = 20
def printLL(s, t = ""):
    # ml.append(s)
    s = s if s != None else ""
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
printLL(stock.getBseVolume(), "VOLUME (,)")
printLL(stock.getBseVolume(False), "VOLUME")
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
printLL(stock.getNseVolume(), "VOLUME")
printLL(stock.getNseVolume(False), "VOLUME (,)")
printLL(stock.getNseID(), "ID")
# print()
print("============================= Company Details =============================")
printLL(stock.getSCID(),"SCID")
printLL(stock.getName(),"NAME")
# print()
print("========================== Standalone  Valuation ==========================")
printLL(stock.getMarketCaptureStandalone(),"MARKET CAPTURE")
printLL(stock.getMarketCaptureStandalone(False),"MARKET CAPTURE (,)")
printLL(stock.getPEStandalone(),"P/E")
printLL(stock.getBookValueStandalone(),"BOOK VALUE")
printLL(stock.getDividentStandalone(),"DIVIDENT")
printLL(stock.getMarketLotStandalone(),"MARKET LOT")
printLL(stock.getIndustryPEStandalone(),"INDUSTRY P/E")
printLL(stock.getEPSStandalone(),"EPS")
printLL(stock.getPCStandalone(),"P/C")
printLL(stock.getPriceBookRatioStandalone(),"PRICE/BOOK")
printLL(stock.getDividentYieldStandalone(),"DIVIDENT YIELD")
printLL(stock.getFaceValueStandalone(),"FACE VALUE")
printLL(stock.getDeliverablesStandalone(),"DELIVERABLES")
# print()
print("========================= Consolidated  Valuation =========================")
printLL(stock.getMarketCaptureConsolidated(),"MARKET CAPTURE")
printLL(stock.getMarketCaptureConsolidated(False),"MARKET CAPTURE (,)")
printLL(stock.getPEConsolidated(),"P/E")
printLL(stock.getBookValueConsolidated(),"BOOK VALUE")
printLL(stock.getDividentConsolidated(),"DIVIDENT")
printLL(stock.getMarketLotConsolidated(),"MARKET LOT")
printLL(stock.getIndustryPEConsolidated(),"INDUSTRY P/E")
printLL(stock.getEPSConsolidated(),"EPS")
printLL(stock.getPCConsolidated(),"P/C")
printLL(stock.getPriceBookRatioConsolidated(),"PRICE/BOOK")
printLL(stock.getDividentYieldConsolidated(),"DIVIDENT YIELD")
printLL(stock.getFaceValueConsolidated(),"FACE VALUE")
printLL(stock.getDeliverablesConsolidated(),"DELIVERABLES")
# print()
print("===========================================================================")
print("============================= Financial Links =============================")
print("===========================================================================")
