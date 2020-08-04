#   Imports

from bs4 import BeautifulSoup
import requests
from selenium import webdriver

#   Global Variables
BASE_URL = "https://www.lijepa.hr/za-muskarce_k2/miris_k1541/parfemska-voda_k1355/"
URL = "https://www.lijepa.hr"
dict = {}
PAGE_NUM = "#stranica="
EXECUTABLE_PATH = ".\geckodriver.exe"


class Scraper:
    def __init__(self):
        self.base_url = requests.get(BASE_URL)
        self.soup = BeautifulSoup(self.base_url.text, 'html.parser')
        self.linklist = []
        self.pagelist = []
        self.browser = webdriver.Firefox(executable_path=EXECUTABLE_PATH)

    #   Number on the pagination

    def getpagenum(self):
        max_page = 1
        self.pagelist.append("")
        for pagenum in self.soup.select(".pagination li a"):
            if int(pagenum["data-filter-page"]) > max_page:
                max_page += 1
                self.pagelist.append(PAGE_NUM + str(max_page))
        return self.pagelist

    #   Products that match what is searched //there are top sold, ad products and such which are avoided

    def getlinklist(self):
        for i in range(len(self.pagelist)):
            url = BASE_URL + self.pagelist[i]

            self.browser.get(url)
            html = self.browser.page_source
            self.soup = BeautifulSoup(html, 'html.parser')
            for link in self.soup.select(".catalog a"):
                if link["href"][0:15] == "/parfemska-voda":
                    self.linklist.append(link["href"])
        return self.linklist

    #   Webscraping and saving it into a class global dict

    def webscrape(self):
        display_counter = 0
        newlinklist = []
        for i in self.linklist:
            if i not in newlinklist:
                newlinklist.append(i)

        for link in newlinklist:
            display_counter += 1
            print(f"Scraping {str(display_counter)}/{str(len(newlinklist))}")
            self.browser.get(URL + link)
            html = self.browser.page_source
            self.soup = BeautifulSoup(html, 'html.parser')
            model = self.soup.select("h1.product-h1")[0].text.split("\n")[0]
            dict[model] = {}
            pricelist = []
            productlist = []
            n = 0
            for price in self.soup.select("p.price-final"):
                pricelist.append(price.get_text().split()[0])
                n += 1

            for table in self.soup.select("div.display-cell.table-variations-cell.variation-title"):
                for title in table.select("p.title"):
                    productlist.append(' '.join(title.text.replace('\n', '').replace('  ', ' ').strip().split()))

            for i in range(len(pricelist)):
                dict[model][productlist[i]] = pricelist[i]

        return dict
