import requests
from bs4 import BeautifulSoup
import os

tempFolder = "temp"


def getHtmlTable(url):
    #Pre process on URL
    temp = url
    temp = temp.replace("http://www.moneycontrol.com/", "")
    temp = temp.replace("https://www.moneycontrol.com/", "")
    temp = temp.replace("/", "").replace(":","").replace("\\","")
    temp = tempFolder + "/" + temp
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

def getTableAs2DArray(htmlTable):
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

def getLifeTimeData(url):
    index = url.index("#")
    leftLink = url[:index]
    rightLink = url[index:]

    counter = 1
    finalResult = None

    while True:
        table = getHtmlTable(leftLink + "/" + str(counter) + rightLink)
        result = getTableAs2DArray(table)

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

link = "https://www.moneycontrol.com/financials/glenmarkpharma/results/quarterly-results/GP08/1#GP08"
link = "https://www.moneycontrol.com/financials/relianceindustries/balance-sheetVI/RI#RI"



# table = getHtmlTable(link)
# result = getTableAs2DArray(table)
result = getLifeTimeData(link)

ttt = 0
for i in result:
    print(i)
    # ttt += 1
    # if ttt > 5:
    #     break