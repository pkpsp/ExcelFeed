import requests
from bs4 import BeautifulSoup
import os

class MoneyControl():

    valuation = "value_txtfr"
    tempFolder = "temp"

    quickLinkDB = {
        'Balance Sheet': 'Balance Sheet',
        'Profit & Loss': 'Profit & Loss',
        'Quarterly Results': 'Quarterly Results',
        'Half Yearly Results': 'Half Yearly Results',
        'Nine Monthly Results': 'Nine Months Results',
        'Yearly Results': 'Yearly Results',
        'Cash Flow': 'Cash Flows',
        'Ratios': 'Ratios',
        'Capital Structure': 'Captial Structure'
        # 'Business': 'Business',
        # 'Earnings': 'Earnings',
        # 'Mgmt Interviews': 'Mgmt Interviews',
        # 'Announcements': 'Announcements',
        # 'Stock Views': 'Stock Views',
        # 'Brokerage Reports': 'Brokerage Reports',
        # 'Sector': 'Sector',
        # 'Board Meetings': 'Board Meetings',
        # 'AGM/EGM': 'AGM/EGM',
        # 'Bonus': 'Bonus',
        # 'Rights': 'Rights',
        # 'Splits': 'Splits',
        # 'Dividends': 'Dividends',
        # 'Company History': 'Company History',
        # 'Listing Info': 'Listing Info',
        # 'Locations': 'Locations',
        # 'Bulk Deals': 'Bulk Deals',
        # 'Large Deals': 'Large Deals',
        # 'Shareholding': 'Shareholding',
        # 'MF Holding': 'MF Holding',
        # 'Top Shareholders': 'Top Shareholders',
        # 'Promoter Holding': 'Promoter Holding',
        # 'Directors Report': 'Directors Report',
        # 'Chairman\'s Speech': 'Chairman\'s Speech',
        # 'Auditors Report': 'Auditors Report',
        # 'Notes to Accounts': 'Notes to Accounts',
        # 'Finished Goods': 'Finished Goods',
        # 'Raw Materials': 'Raw Materials',
        # 'Background': 'Background',
        # 'Board of Directors': 'Board of Directors',
        # 'Competition': 'Competition',
        # 'Price': 'Price',
        # 'Price Performance': 'Price Performance',
        # 'Market Cap': 'Market Cap',
        # 'Net Sales': 'Net Sales',
        # 'Net Profit': 'Net Profit',
        # 'Total Assets': 'Total Assets',
        # 'Historical Prices': 'Historical Prices',
        # 'Price of SBI on previous budgets': 'Price of SBI on previous budgets'
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

    def getLifeTimeStandaloneData(self, url):
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
    def getLifeTimeConsodilatedData(self, url):
        response = requests.get(url)
        temp = BeautifulSoup(response.content, 'html.parser')
        consolidatedURL = temp.find(id="#consolidated").get("href")
        return self.getLifeTimeStandaloneData(consolidatedURL)

    def __init__(self, url):
        # super().__init__()
        response = requests.get(url)
        self.soup = BeautifulSoup(response.content, 'html.parser')
        # self.standAloneSoup = self.soup.find(id="standalone_valuation")
        # self.conSolidatedSoup = self.soup.find(id="consolidated_valuation")

        self.bseSoup = self.soup.find(id="inp_bse")
        self.nseSoup = self.soup.find(id="inp_nse")

        # self.valuations = self.soup.find(id="stk_overview")
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
        try:
            return self.soup.find(id="bseid").get('value')
        except:
            return None

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
                temp = self.soup.find(class_="nseopn bseopn").get_text().replace(",","")
                return float(temp)
            except:
                return None
    def getNsePreClose(self, bypass = False):
        if self.nseSoup or bypass:
            try:
                temp = self.soup.find(class_="nseprvclose bseprvclose").get_text().replace(",","")
                return float(temp)
            except:
                return None
    def getNseID(self):
        try:
            return self.soup.find(id="nseid").get('value')
        except:
            return None
        
    def getSCID(self):
        try:
            return self.soup.find(id="scid").get('value')
        except:
            return None
    def getName(self):
        try:
            temp = self.soup.find(id="stockName")
            return temp.find('h1').get_text().strip()
        except:
            return None
    def getSector(self):
        temp = self.soup.find(id="stockName")
        return temp.find('a').get_text().strip()

    def getMarketCapitalizationInCr(self, removeComma = True):
        temp = self.soup.find(class_="nsemktcap bsemktcap").get_text()
        if removeComma:
            try:
                return float(temp.replace(",",""))
            except:
                return None
        return temp
    def getPE(self, removeComma = True):
        temp = self.soup.find(class_="nsepe bsepe").get_text()
        if removeComma:
            try:
                return float(temp.replace(",",""))
            except:
                return None
        return temp    
    def getIndustryPE(self, removeComma = True):
        temp = self.soup.find(class_="nsesc_ttm bsesc_ttm").get_text()
        if removeComma:
            try:
                return float(temp.replace(",",""))
            except:
                return None
        return temp    
    def getBookValue(self, removeComma = True):
        temp = self.soup.find(class_="nsebv bsebv").get_text()
        if removeComma:
            try:
                return float(temp.replace(",",""))
            except:
                return None
        return temp    
    def getEPS(self, removeComma = True):
        temp = self.soup.find(class_="nseceps bseceps").get_text()
        if removeComma:
            try:
                return float(temp.replace(",",""))
            except:
                return None
        return temp    
    def getPC(self, removeComma = True):
        temp = self.soup.find(class_="nsep_c bsep_c").get_text()
        if removeComma:
            try:
                return float(temp.replace(",",""))
            except:
                return None
        return temp    
    def getPriceBookRatio(self, removeComma = True):
        temp = self.soup.find(class_="nsepb bsepb").get_text()
        if removeComma:
            try:
                return float(temp.replace(",",""))
            except:
                return None
        return temp    
    def getDividentYield(self, removeComma = True):
        temp = self.soup.find(class_="nsedy bsedy").get_text()
        if removeComma:
            try:
                return float(temp.replace(",",""))
            except:
                return None
        return temp    
    def getFaceValue(self, removeComma = True):
        temp = self.soup.find(class_="nsefv bsefv").get_text()
        if removeComma:
            try:
                return float(temp.replace(",",""))
            except:
                return None
        return temp    
    def calculateDividentPerCent(self):
        currCost = self.getNseClose()
        if currCost == None:
            currCost = self.getBseClose()
        
        if currCost:
            divYield = self.getDividentYield()

            temp = int((divYield * currCost) / 100)
            return (temp * 100) / self.getFaceValue()

    def getQuickLink(self, ref):
        soup2 = self.soup.find(class_='quick_links clearfix')
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
    # stock = MoneyControl("https://www.moneycontrol.com/india/stockpricequote/refineries/relianceindustries/RI")


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
    printLL(stock.getSector(),"SECTOR")
    # print()
    print("========================== Valuation ==========================")
    printLL(stock.getMarketCapitalizationInCr(),"MARKET CAPTURE")
    printLL(stock.getMarketCapitalizationInCr(False),"MARKET CAPTURE (,)")
    printLL(stock.getPE(),"P/E")
    printLL(stock.getBookValue(),"BOOK VALUE")
    printLL(stock.getIndustryPE(),"INDUSTRY P/E")
    printLL(stock.getEPS(),"EPS")
    printLL(stock.getPC(),"P/C")
    printLL(stock.getPriceBookRatio(),"PRICE/BOOK")
    printLL(stock.getDividentYield(),"DIVIDENT YIELD")
    printLL(stock.getFaceValue(),"FACE VALUE")
    # printLL(stock.calculateDividentPerCent(),"DIVIDENT")
    # print()
    print("===========================================================================")
    print("============================= Quick Links =============================")
    keys = list(MoneyControl.quickLinkDB.keys())
    for i in range(9):
        printLL(stock.getQuickLink(i),keys[i])
    print("--")
    for i in range(9):
        printLL(stock.getQuickLink(keys[i]),keys[i])
    print("===========================================================================")
    print("============================= Data =============================")
    
    import csv

    link = stock.getQuickLink("Balance Sheet")
    temp = stock.getLifeTimeStandaloneData(link)

    with open("standalone.csv","w+") as my_csv:
        csvWriter = csv.writer(my_csv,delimiter=',')
        csvWriter.writerows(temp)
        
    temp = stock.getLifeTimeConsodilatedData(link)

    try:
        with open("consolidated.csv","w+") as my_csv:
            csvWriter = csv.writer(my_csv,delimiter=',')
            csvWriter.writerows(temp)
    except:
        print("--None--")

    # print(temp)
    print("===========================================================================")

if __name__ == "__main__":
    main()