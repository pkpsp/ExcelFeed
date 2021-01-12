import requests
from bs4 import BeautifulSoup
import os

class MoneyControl():

    valuation = "value_txtfr"
    tempFolder = "temp"

    quickLinkDB = {
        'Business': 'Business',
        'Earnings': 'Earnings',
        'Mgmt Interviews': 'Mgmt Interviews',
        'Announcements': 'Announcements',
        'Stock Views': 'Stock Views',
        'Brokerage Reports': 'Brokerage Reports',
        'Sector': 'Sector',
        'Board Meetings': 'Board Meetings',
        'AGM/EGM': 'AGM/EGM',
        'Bonus': 'Bonus',
        'Rights': 'Rights',
        'Splits': 'Splits',
        'Dividends': 'Dividends',
        'Company History': 'Company History',
        'Listing Info': 'Listing Info',
        'Locations': 'Locations',
        'Bulk Deals': 'Bulk Deals',
        'Large Deals': 'Large Deals',
        'Shareholding': 'Shareholding',
        'MF Holding': 'MF Holding',
        'Top Shareholders': 'Top Shareholders',
        'Promoter Holding': 'Promoter Holding',
        'Balance Sheet': 'Balance Sheet',
        'Profit & Loss': 'Profit & Loss',
        'Quarterly Results': 'Quarterly Results',
        'Half Yearly Results': 'Half Yearly Results',
        'Nine Monthly Results': 'Nine Monthly Results',
        'Yearly Results': 'Yearly Results',
        'Cash Flow': 'Cash Flow',
        'Ratios': 'Ratios',
        'Directors Report': 'Directors Report',
        'Chairman\'s Speech': 'Chairman\'s Speech',
        'Auditors Report': 'Auditors Report',
        'Notes to Accounts': 'Notes to Accounts',
        'Finished Goods': 'Finished Goods',
        'Raw Materials': 'Raw Materials',
        'Background': 'Background',
        'Board of Directors': 'Board of Directors',
        'Capital Structure': 'Capital Structure',
        'Competition': 'Competition',
        'Price': 'Price',
        'Price Performance': 'Price Performance',
        'Market Cap': 'Market Cap',
        'Net Sales': 'Net Sales',
        'Net Profit': 'Net Profit',
        'Total Assets': 'Total Assets',
        'Historical Prices': 'Historical Prices',
        'Price of SBI on previous budgets': 'Price of SBI on previous budgets'
    }

    # quickLinkSoups = {

    # }

    def createFolder(self):
        if not os.path.exists(self.tempFolder):
            os.makedirs(self.tempFolder)

    def getHtmlTable(self, url):
        #Pre process on URL
        temp = url
        temp = temp.replace("http://www.moneycontrol.com/", "")
        temp = temp.replace("https://www.moneycontrol.com/", "")
        temp = temp.replace("/", "").replace(":","").replace("\\","")
        temp = self.tempFolder + "/" + temp
        page = ""
        
        if not os.path.isfile(temp):
            # print("Hitting Request")
            page = str(requests.get(url).content)
            f = open(temp, "w")
            f.write(page)
            f.close()
        else:
            # print("Reading File")
            f = open(temp, "r")
            page = f.read()
            f.close()

        tempSoup = BeautifulSoup(page, 'html.parser')

        return tempSoup.find(class_='mctable1')

    def getTableAs2DArray(self, htmlTable):
        if htmlTable == None:
            return None

        result = []
        rows = htmlTable.find_all('tr')

        for eachRow in rows:
            result.append([])
            cols = eachRow.find_all('td')
            if(cols == None):
                cols = eachRow.find_all('th')
            first = True
            for eachCol in cols:
                temp = eachCol.get_text()
                if temp != '\xa0':
                    if not first:
                        if temp == "--":
                            temp = 0.00
                        elif temp != "":
                            try:
                                temp = float(temp.replace(",", ""))
                            except:
                                pass
                    
                    result[-1].append(temp)
                
                if first:
                    first = False
        
                # print(temp)

        return result

    def getLifeTimeData(self, url):
        index = url.index("#")
        leftLink = url[:index]
        rightLink = url[index:]

        counter = 1
        finalResult = None

        while True:
            table = self.getHtmlTable(leftLink + "/" + str(counter) + rightLink)
            result = self.getTableAs2DArray(table)

            if table == None:
                break

            if finalResult == None:
                finalResult = result
            else:
                for row in range(len(result)):
                    for col in range(1, len(result[row])):
                        finalResult[row].append(result[row][col])

            counter += 1

        return finalResult

    def __init__(self, url):
        # super().__init__()
        response = requests.get(url)
        self.soup = BeautifulSoup(response.content, 'html.parser')
        # self.standAloneSoup = self.soup.find(id="standalone_valuation")
        # self.conSolidatedSoup = self.soup.find(id="consolidated_valuation")

        self.bseSoup = self.soup.find(id="inp_bse")
        self.nseSoup = self.soup.find(id="inp_nse")

        self.financials = self.soup.find(id="stk_overview")
        self.createFolder()
        
        self.quickLinkDBIndex = []
        for i in self.quickLinkDB.keys():
            self.quickLinkDBIndex.append(self.quickLinkDB[i])
    
    # div_bse_livebox_wrap
    def getBseHigh(self):
        try:
            temp = self.bseSoup.find(id="sp_high").get_text()
            return float(temp)
        except:
            return None
    def getBseLow(self):
        try:
            temp = self.bseSoup.find(id="sp_low").get_text()
            return float(temp)
        except:
            return None
    def getBse52High(self):
        try:
            temp = self.bseSoup.find(id="sp_yearlyhigh").get_text() 
            return float(temp)
        except:
            return None
    def getBse52Low(self):
        try:
            temp = self.bseSoup.find(id="sp_yearlylow").get_text()
            return float(temp)
        except:
            return None
    def getBseClose(self):
        try:
            temp = self.soup.find(id="bsecp").get_text().replace(",","")
            return float(temp)
        except:
            return None
    def getBseVolume(self, removeComma = True):
        temp = None
        try:
            temp = self.bseSoup.find(id="bse_vol").get_text()
        except:
            return None

        if removeComma:
            try:
                return int(temp.replace(",",""))
            except:
                return None
        return temp
    def getBseVwap(self):
        if self.bseSoup and self.nseSoup:
            return "ND"
        elif self.bseSoup:
            # return self.getNseVwap(True)
            return None
    def getBseOpen(self):
        if self.bseSoup and self.nseSoup:
            return "ND"
        elif self.bseSoup:
            # return self.getNseOpen(True)
            return None
    def getBsePreClose(self):
        if self.bseSoup and self.nseSoup:
            return "ND"
        elif self.bseSoup:
            # return self.getNsePreClose(True)
            return None

    def getBseID(self):
        return self.soup.find(id="bseid").get('value')

    # div_nse_livebox_wrap
    
    def getNseHigh(self):
        try:
            temp = self.nseSoup.find(id="sp_high").get_text()
            return float(temp)
        except:
            return None
    def getNseLow(self):
        try:
            temp = self.nseSoup.find(id="sp_low").get_text()
            return float(temp)
        except:
            return None
    def getNse52High(self):
        try:
            temp = self.nseSoup.find(id="sp_yearlyhigh").get_text()
            return float(temp)
        except:
            return None
    def getNse52Low(self):
        try:
            temp = self.nseSoup.find(id="sp_yearlylow").get_text()
            return float(temp)
        except:
            return None
    def getNseClose(self):
        try:
            temp = self.soup.find(id="nsecp").get_text().replace(",","")
            return float(temp)
        except:
            return None
    def getNseVolume(self, removeComma = True):
        temp = None
        try:
            temp = self.nseSoup.find(id="nse_vol").get_text()
        except:
            return None
            
        if removeComma:
            try:
                return int(temp.replace(",",""))
            except:
                return None
        return temp
    def getNseVwap(self, bypass = False):
        if self.nseSoup or bypass:
            try:
                temp = self.soup.find(class_="nsevwap bsevwap").get_text().replace(",","")
                return float(temp)
            except:
                return None
    def getNseOpen(self, bypass = False):
        if self.nseSoup or bypass:
            try:
                temp = self.financials.find(class_="nseopn bseopn").get_text().replace(",","")
                return float(temp)
            except:
                return None
    def getNsePreClose(self, bypass = False):
        if self.nseSoup or bypass:
            try:
                temp = self.financials.find(class_="nseprvclose bseprvclose").get_text().replace(",","")
                return float(temp)
            except:
                return None

    def getNseID(self):
        if self.nseSoup:
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

    def getQuickLink(self, ref):
        soup2 = self.soup.find(class_='clearfix quick_wraplink PT20')
        try:
            index = int(ref)
            try:
                return soup2.find('a', {"title": self.quickLinkDBIndex[index]}).get("href")
            except:
                return None
        except:
            try:
                return soup2.find('a', {"title": self.quickLinkDB[ref]}).get("href")
            except:
                return None

######################################################################################################################

def main():

    stock = MoneyControl("https://www.moneycontrol.com/india/stockpricequote/domestic-appliances/hawkinscooker/HC02")
    # stock = MoneyControl("https://www.moneycontrol.com/india/stockpricequote/pharmaceuticals/glenmarkpharma/GP08")
    # stock = MoneyControl("https://www.moneycontrol.com/india/stockpricequote/oil-drillingexploration/oilnaturalgascorporation/ONG")
    stock = MoneyControl("https://www.moneycontrol.com/india/stockpricequote/refineries/relianceindustries/RI")


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
    # printLL(stock.getBseID(), "ID")
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
    # printLL(stock.getNseID(), "ID")
    # print()
    print("============================= Company Details =============================")
    # printLL(stock.getSCID(),"SCID")
    # printLL(stock.getName(),"NAME")
    # print()
    print("========================== Standalone  Valuation ==========================")
    # printLL(stock.getMarketCaptureStandalone(),"MARKET CAPTURE")
    # printLL(stock.getMarketCaptureStandalone(False),"MARKET CAPTURE (,)")
    # printLL(stock.getPEStandalone(),"P/E")
    # printLL(stock.getBookValueStandalone(),"BOOK VALUE")
    # printLL(stock.getDividentStandalone(),"DIVIDENT")
    # printLL(stock.getMarketLotStandalone(),"MARKET LOT")
    # printLL(stock.getIndustryPEStandalone(),"INDUSTRY P/E")
    # printLL(stock.getEPSStandalone(),"EPS")
    # printLL(stock.getPCStandalone(),"P/C")
    # printLL(stock.getPriceBookRatioStandalone(),"PRICE/BOOK")
    # printLL(stock.getDividentYieldStandalone(),"DIVIDENT YIELD")
    # printLL(stock.getFaceValueStandalone(),"FACE VALUE")
    # printLL(stock.getDeliverablesStandalone(),"DELIVERABLES")
    # print()
    print("========================= Consolidated  Valuation =========================")
    # printLL(stock.getMarketCaptureConsolidated(),"MARKET CAPTURE")
    # printLL(stock.getMarketCaptureConsolidated(False),"MARKET CAPTURE (,)")
    # printLL(stock.getPEConsolidated(),"P/E")
    # printLL(stock.getBookValueConsolidated(),"BOOK VALUE")
    # printLL(stock.getDividentConsolidated(),"DIVIDENT")
    # printLL(stock.getMarketLotConsolidated(),"MARKET LOT")
    # printLL(stock.getIndustryPEConsolidated(),"INDUSTRY P/E")
    # printLL(stock.getEPSConsolidated(),"EPS")
    # printLL(stock.getPCConsolidated(),"P/C")
    # printLL(stock.getPriceBookRatioConsolidated(),"PRICE/BOOK")
    # printLL(stock.getDividentYieldConsolidated(),"DIVIDENT YIELD")
    # printLL(stock.getFaceValueConsolidated(),"FACE VALUE")
    # printLL(stock.getDeliverablesConsolidated(),"DELIVERABLES")
    # print()
    print("===========================================================================")
    print("============================= Quick Links =============================")
    # printLL(stock.getQuickLink(22),"Balance Sheet")
    # link = stock.getQuickLink(MoneyControl.quickLinkDB['Yearly Results'])
    # printLL(link,"Balance Sheet")
    # temp = stock.getLifeTimeData(link)
    print("===========================================================================")
    # print(temp)

main()