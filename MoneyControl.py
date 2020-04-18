import requests
# <!--<section class="price_overview_wrap" id="sec_quotes">-->
class MoneyControl():

    def __init__(self, url):
        # super().__init__()
        response = requests.get(url)
        self.data = response.text

    def oneLevelBse(self, className):
        startIndex = self.data.index(className)

        while(data[startIndex] != '>'):
            startIndex += 1
        startIndex += 1

        endIndex = startIndex

        while(data[endIndex] != '<'):
            endIndex += 1

        return data[startIndex:endIndex]

    def getBseVwap(self):
        return self.oneLevelBse("prive_avgp avgp")

    def getBseHigh(self):
        # clearfix lowhigh_band todays_lowhigh_wrap  >> low_high3
        pass
    def getBseLow(self):
        # clearfix lowhigh_band todays_lowhigh_wrap 
        # Two level or low_high1
        pass
    def getBseClose(self):
        return self.oneLevelBse("bprevclose")
        
    def getBseOpen(self):
        return self.oneLevelBse("prev_open priceopen")
    def getBsePreClose(self):
        return self.oneLevelBse("prev_open priceprevclose")
    def getBseVolume(self):
        return self.oneLevelBse("txt13_pc volume_data")

    def getNseVwap(self):
        startIndex = self.data.rindex("prive_avgp avgp")

        while(data[startIndex] != '>'):
            startIndex += 1
        startIndex += 1

        endIndex = startIndex

        while(data[endIndex] != '<'):
            endIndex += 1

        return data[startIndex:endIndex]

    def getNseHigh(self):
        pass
    def getNseLow(self):
        pass
    def getNseOpen(self):
        pass
    def getNseClose(self):
        pass
    def getNsePreClose(self):
        # nprevclose
        pass
    def getNseVolume(self):
        pass