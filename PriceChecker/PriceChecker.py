import bs4, requests, sys

url = sys.argv[1]

def AmazonPriceCheck(productUrl):
    try:
        res = requests.get(productUrl)
        res.raise_for_status()

        soup = bs4.BeautifulSoup(res.text, 'html.parser')
        elem = soup.select('#priceblock_ourprice')
        return float(elem[0].text[1:]) #returns the float value of the price
    
    except requests.exceptions.HTTPError:
        print('503 Error: Try Again')

price = AmazonPriceCheck(url)

if not price == None:
    print("The price is: $" + str(price))

