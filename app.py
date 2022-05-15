import re
import time
from time import sleep
from unittest import result
from requests_html import HTMLSession


#url="https://www.alaragames.se/pages/advanced-search?q=endurance&game=mtg&availabilty=false&condition=&printing=&setNames=&colors=&rarities=&types=&pricemin=&pricemax=&page=1&order=price-descending"
def inStock(url):
    session = HTMLSession()
    r = session.get(url)
    soldout = r.html.find(".product-info",clean = True)

    for x in soldout[0].attrs['class']:
        if x == "product-soldout":
            return False
    return True

def listUrls(cardname,page=3):
    resultArr = []
    for p in range(1,page):
        sleep(5)
        session = HTMLSession()
        r = session.get('https://www.alaragames.se/pages/advanced-search?q=' + cardname.replace(" ", "+") + '&game=mtg&availabilty=false&condition=&printing=&setNames=&colors=&rarities=&types=&pricemin=&pricemax=&page=' + str(p) + '&order=price-descending')
        r.html.render(sleep=5)
        products = r.html.links
        session.close()
        for i in products:
            if i.startswith("/products/"):
                el=r.html.find('a[href="' + i + '"] div.product-detail div.grid-view-item__title', clean = True)
                if el[0].text.lower().startswith(cardname + " (") or el[0].text.lower().startswith(cardname + " ["):
                    resultArr.append("https://www.alaragames.se" + i)
    return resultArr
            

            
#inStock("https://www.alaragames.se/collections/mtgsingles/products/endurance-modern-horizons-2?variant=40240083239112")

#if inStock("https://www.alaragames.se/collections/karusell-singles-1/products/tainted-indulgence-streets-of-new-capenna"):
#    print("In stock")
#else:
#    print("Not in stock")

urlList = listUrls("grief")

print(urlList)