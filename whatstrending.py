import pandas as pd
from pytrends.request import TrendReq
import os
import schedule
import time

pytrend = TrendReq()

credible = []
badwords = []

try:
    from googlesearch import search
except ImportError:
    print("No module named 'google' found")


def getLinks():
    df = pytrend.trending_searches(pn="new zealand")
    df.head()
    print(df.head(20))
    with open("crediblelist.txt", "r") as crediblelist:
        credible = crediblelist.read().splitlines()
    with open("badwords.txt", "r") as badwords:
        badwords = badwords.read().splitlines()
    list = df.values.tolist()
    os.remove("links.txt")
    for x in list:
        y = str(x).replace("['", "").replace("']", "")
        for result in search(y, tld="co.in", num=10, stop=10, pause=2):
            if any(cred in result
                   for cred in credible or any(badword in result
                                               for badword in badwords)):
                print(y, result)
            with open("links.txt", "a+") as linkstxt:
                linkstxt.write(y + ": " + result + "\n")
        else:
            with open("notcredible.txt", "a+") as notcredibletxt:
                notcredibletxt.write(y + " " + result + "\n")
            continue


schedule.every(60).minutes.do(getLinks)

while True:
    schedule.run_pending()
    time.sleep(1)
