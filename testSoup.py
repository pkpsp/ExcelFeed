import requests
from bs4 import BeautifulSoup


page = requests.get("https://www.moneycontrol.com/india/stockpricequote/finance-housing/indiabullshousingfinance/IHF01")
soup = BeautifulSoup(page.content, 'html.parser')

# soup.find_all('p')
# soup.find_all('p', class_='prive_avgp avgp')
# soup.find_all(id="first")   

# try:
#     print(soup.find_all(class_='prive_avgp avgp')[2].get_text())
# except:
#     print("Error")
#     pass

# print(soup.find(id="bprevclose").get('value'))

# soup2 = soup.find_all(class_="clearfix lowhigh_band todays_lowhigh_wrap")[0]
# text = soup2.find(class_="low_high1")
# print(text.get_text())

# soup2 = soup.find(id="standalone_valuation")
# soup3 = soup.find(id="consolidated_valuation")

# value_txtfr = soup3.find_all(class_="value_txtfr")

# i = 0
# while i < len(value_txtfr) -1 :
#     te = value_txtfr[i].get_text().replace(",","")
#     try:
#         print(float(te))
#     except:
#         print(te)
#     print()
#     i += 1
# print(value_txtfr[11].find('a').get_text())

quickLinks = soup.find(class_='clearfix quick_wraplink PT20')
# print(quickLinks)

tag = "Yearly Results"
link = quickLinks.find('a', {"title": tag}).get("href")
print(link)

newPage = requests.get(link)
newSoup = BeautifulSoup(str(newPage.content), 'html.parser')

# print(type(newPage.content), str(newPage.content))

# table = newSoup.find(id='standalone-new').find(class_='mctable1')
table = newSoup.find(class_='mctable1')

def tableToArray(htmlTable):
    result = []
    rows = htmlTable.find_all('tr')

    for eachRow in rows:
        result.append([])
        cols = eachRow.find_all('td')
        if(cols == None):
            cols = eachRow.find_all('th')
        for eachCol in cols:
            result[-1].append(eachCol.get_text)
            # print(eachCol.get_text())

    return result

tableToArray(table)

# linkTag = quickLinks.find('a', {"title": tag})["href"]
# print(linkTag)

# quickLinkDB = {
#     'Business': 'Business',
#     'Earnings': 'Earnings',
#     'Mgmt Interviews': 'Mgmt Interviews',
#     'Announcements': 'Announcements',
#     'Stock Views': 'Stock Views',
#     'Brokerage Reports': 'Brokerage Reports',
#     'Sector': 'Sector',
#     'Board Meetings': 'Board Meetings',
#     'AGM/EGM': 'AGM/EGM',
#     'Bonus': 'Bonus',
#     'Rights': 'Rights',
#     'Splits': 'Splits',
#     'Dividends': 'Dividends',
#     'Company History': 'Company History',
#     'Listing Info': 'Listing Info',
#     'Locations': 'Locations',
#     'Bulk Deals': 'Bulk Deals',
#     'Large Deals': 'Large Deals',
#     'Shareholding': 'Shareholding',
#     'MF Holding': 'MF Holding',
#     'Top Shareholders': 'Top Shareholders',
#     'Promoter Holding': 'Promoter Holding',
#     'Balance Sheet': 'Balance Sheet',
#     'Profit & Loss': 'Profit & Loss',
#     'Quarterly Results': 'Quarterly Results',
#     'Half Yearly Results': 'Half Yearly Results',
#     'Nine Monthly Results': 'Nine Monthly Results',
#     'Yearly Results': 'Yearly Results',
#     'Cash Flow': 'Cash Flow',
#     'Ratios': 'Ratios',
#     'Directors Report': 'Directors Report',
#     'Chairman\'s Speech': 'Chairman\'s Speech',
#     'Auditors Report': 'Auditors Report',
#     'Notes to Accounts': 'Notes to Accounts',
#     'Finished Goods': 'Finished Goods',
#     'Raw Materials': 'Raw Materials',
#     'Background': 'Background',
#     'Board of Directors': 'Board of Directors',
#     'Capital Structure': 'Capital Structure',
#     'Competition': 'Competition',
#     'Price': 'Price',
#     'Price Performance': 'Price Performance',
#     'Market Cap': 'Market Cap',
#     'Net Sales': 'Net Sales',
#     'Net Profit': 'Net Profit',
#     'Total Assets': 'Total Assets',
#     'Historical Prices': 'Historical Prices',
#     'Price of SBI on previous budgets': 'Price of SBI on previous budgets'
# }

# print("-"*50)
# for i in quickLinkDB.keys():
#     try:
#         linkTag = quickLinks.find('a', {"title": quickLinkDB[i]})["href"]
#         print(linkTag)
#     except:
#         print("Error at ("+ i +")")
    
# print("-"*50)