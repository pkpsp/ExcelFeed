import matplotlib.pyplot as plt
from MoneyControl import MoneyControl

# stock = MoneyControl("https://www.moneycontrol.com/india/stockpricequote/refineries/relianceindustries/RI")
stock = MoneyControl("https://www.moneycontrol.com/india/stockpricequote/bearings/skfindia/SKF01")
# can club
balanceSheet = stock.getLifeTimeData(stock.getQuickLink(22))
# profitNloss = stock.getLifeTimeData(stock.getQuickLink(23))

# single
# yearlyResult = stock.getLifeTimeData(stock.getQuickLink(27))
# print(balanceSheet)
# print(profitNloss)
# print(yearlyResult)

# parameters = [4, 20, 33, 41]
parameters = [4, 6, 16, 38, 14, 20, 33, 41]
db = {}

period = balanceSheet[0][1:]

for i in parameters:
    db[balanceSheet[i][0]] = balanceSheet[i][1:]
    db[balanceSheet[i][0]].reverse()
    print(db[balanceSheet[i][0]], balanceSheet[i][0])

print(db)

# esc = balanceSheet[4][1:]
# tcl = balanceSheet[20][1:]
# tca = balanceSheet[41][1:]
# besc = balanceSheet[33][1:]

period.reverse()
# esc.reverse()
# tcl.reverse()
# tca.reverse()
# besc.reverse()

# print(len(period), period)
# print(len(esc), esc)
# print(len(tcl), tcl)
# print(len(tca), tca)
# print(len(besc), besc)


for i in db.keys():
    plt.plot(period, db[i], label = i)



# plotting the line 1 points 
# plt.plot(period, esc, label = "Equity Share Capital")
# plt.plot(period, tcl, label = "Total Current Libalities")
# plt.plot(period, tca, label = "Total Current Assets")
# plt.plot(period, besc, label = "Bonus Equity Share Capital")

# period = ["MAR '20", "DEC '19", "SEP '19", "JUN '19", "MAR '19"]
# netProfit = [349.19, 345.53, 431.99, 227.84, 281.29]
# otherIncome = [251.29, 94.49, 192.47, 68.54, 168.39]

# period.reverse()
# netProfit.reverse()
# otherIncome.reverse()


plt.xlabel('Period')
plt.ylabel('Rs. in crore')

plt.title(stock.getName() + ' Balance Sheet')
# show a legend on the plot
plt.legend()
# Display a figure.
plt.show()