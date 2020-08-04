from Scraper import Scraper
import pandas as pd
import numpy as np
import csv

if __name__ == '__main__':
    scraper = Scraper()
    scraper.getpagenum()
    scraper.getlinklist()
    d = scraper.webscrape()
    new_d = {(k1, k2): v2 for k1, v1 in d.items()
             for k2, v2 in d[k1].items()}
    print(new_d)
    df = pd.DataFrame.from_dict(new_d, orient="index")

    df.to_csv("first_webscrape_result.csv")
