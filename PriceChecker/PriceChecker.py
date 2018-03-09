import bs4, requests, sys, re

def priceCheck(productUrl, cssSel):
    try:
        priceFilter = re.compile(r'(\d){1,5}.(\d){2}')
        res = requests.get(productUrl)
        res.raise_for_status()

        soup = bs4.BeautifulSoup(res.text, 'html.parser')
        elem = soup.select(cssSel)
        priceStr = priceFilter.search(elem[0].text).group(0)
        return float(priceStr) #returns the float value of the price

    except requests.exceptions.HTTPError:
        print('503 Error: Try Again')

def getPriceSelector(url):
    urlDomainName = re.search(r'www.(\w)+.com', url).group(0)
    if urlDomainName == 'www.ebay.com':
        return '#prcIsum'
    elif urlDomainName == 'www.amazon.com':
        return '#priceblock_ourprice'
    else:
        return

#Returns all product and their prices of the first search page
def getEbaySearch(productName):
    itemDesc = []
    url = 'https://www.ebay.com/sch/'+productName
    res = requests.get(url)
    res.raise_for_status()
    nameFilter = re.compile(r'#item')

    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    for listItem in soup.find_all('li', {'class' : 'sresult'}): #li 'sresult' is each item on search page
        nameAttr = listItem.findChild('a',{'class':'vip'}) #a tag includes title of product
        priceAttr = listItem.findChild('span',{'class': 'bold'})
        if priceAttr is None: #Avoid special listing/styles of products
            continue
        name = nameAttr.text
        price = re.search(r'(\d)+.\d\d', priceAttr.text).group(0)
        itemDesc.append([name, float(price)])
    print(itemDesc)
    return itemDesc
        

def getAmazonSearch():
    # TODO: Get list of products and their prices
    return
    

def main():
    productName = ' '.join(sys.argv[1:])
    getEbaySearch(productName)
        
# TODO: Allow users to select items from product list
# TODO: Notify user if price changes

if __name__ == '__main__':
  main()
