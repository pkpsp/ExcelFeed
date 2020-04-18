import requests
from bs4 import BeautifulSoup


page = requests.get("https://www.moneycontrol.com/india/stockpricequote/pharmaceuticals/sunpharmaceuticalindustries/SPI")
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

soup2 = soup.find_all(class_="clearfix lowhigh_band todays_lowhigh_wrap")[0]
text = soup2.find(class_="low_high1")
print(text.get_text())

# [0].get_text()