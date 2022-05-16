from time import sleep
from requests_html import HTMLSession
from discord_webhook import DiscordWebhook, DiscordEmbed
import schedule
import os
from dotenv import load_dotenv


# Soon to be env vars:
load_dotenv()
webhookurl = os.getenv('webhookurl')
timer = os.getenv('timer')

# Not used at the moment 
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
        r = session.get('https://www.alaragames.se/pages/advanced-search?q=' + cardname.replace(" ", "+") + '&game=mtg&availabilty=true&condition=&printing=&setNames=&colors=&rarities=&types=&pricemin=&pricemax=&page=' + str(p) + '&order=price-descending')
        r.html.render(sleep=5)
        products = r.html.links
        session.close()
        for i in products:
            if i.startswith("/products/"):
                el=r.html.find('a[href="' + i + '"] div.product-detail div.grid-view-item__title', clean = True)
                if el[0].text.lower().startswith(cardname + " (") or el[0].text.lower().startswith(cardname + " ["):
                    resultArr.append("https://www.alaragames.se" + i)
        if not resultArr:
            break
    return resultArr

def runFilecheck():
    cardsfile = open('cards.txt', 'r')
    fileLines = cardsfile.readlines()
    count = 0
    cardsfile.close()
    for line in fileLines:
        count += 1
        cardurls = listUrls(line.strip())
        if not cardurls:
            print(line.strip().title() + " is not in stock")
        else:
            print(line.strip().title() + " is in stock! " + "\n" + "\n".join(cardurls))
            sendDiscord(line.strip().title() + " is in stock! " + "\n" + "\n".join(cardurls))
            newfile = open("cards.txt", "w")
            del fileLines[count - 1]
            for line in fileLines:
                newfile.write(line)
            newfile.close()
            statusDiscord()

def statusDiscord():
    cardsfile = open('cards.txt', 'r')
    fileLines = cardsfile.readlines()
    cardsfile.close()

    webhook = DiscordWebhook(url=webhookurl, username="Autolara")

    embed = DiscordEmbed(title='Tracked cards', description="".join(fileLines).title(), color='03b2f8')
    embed.set_author(name='Autolara', url='https://alaragames.se', icon_url='https://cdn.shopify.com/s/files/1/0275/0146/1640/files/Alara_Games_Gradient_32x32.png')
    #embed.set_timestamp()
    #embed.add_embed_field(name='______', value='Lightningbolt' + "\n" + "Endurance")

    webhook.add_embed(embed)
    response = webhook.execute()

def sendDiscord(message):
    webhook = DiscordWebhook(url=webhookurl, content=message)
    sent_webhook = webhook.execute()
    webhook.remove_embeds()

def main():
    #global checkRunning

    if checkRunning:
        print("Check is already running. Skipping this run... ")
    else:
        #checkRunning = True
        runFilecheck()
        #checkRunning = False

checkRunning = False

statusDiscord()
main()

schedule.every(int(timer)).hours.do(main)

while True:
    schedule.run_pending()
    sleep(50)