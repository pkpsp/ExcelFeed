import requests
from bs4 import BeautifulSoup


page = requests.get("https://www.moneycontrol.com/india/stockpricequote/auto-lcvshcvs/tatamotors/TM03")
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

soup2 = soup.find(id="standalone_valuation")
soup3 = soup.find(id="consolidated_valuation")

value_txtfr = soup3.find_all(class_="value_txtfr")

i = 0
while i < len(value_txtfr) -1 :
    te = value_txtfr[i].get_text().replace(",","")
    try:
        print(float(te))
    except:
        print(te)
    print()
    i += 1
print(value_txtfr[11].find('a').get_text())
