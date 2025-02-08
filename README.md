import requests
from bs4 import BeautifulSoup
from collections import namedtuple

# Initial settings
URL = "https://shoeseller.in/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(HTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
}
PRODUCT_CLASS = "product"          # Class for each product ((may change depending on the site))
PRODUCT_NAME_TAGS = ["h1", "h2", "h3"]
PRICE_TAG = "bdi"
DESCRIPTION_TAG = "div"
IMAGE_TAG = "img"

# Product definition for data retention
Product = namedtuple("Product", ["name", "price", "description", "image"])

def fetch_page(url):
    """ Retrieving page contents with requests and handling errors """
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        return response.text
    except requests.RequestException as e:
        print(f"Error retrieving page: {e}")
        return None

def extract_text(element):
    """ Extract text from element, if there is no default value 'Not found' """
    return element.get_text(strip=True) if element else "Not found"

def find_product_name(product):
    """ Search for product name among multiple possible tags """
    for tag in PRODUCT_NAME_TAGS:
        name_tag = product.find(tag)
        if name_tag:
            return name_tag.get_text(strip=True)
    return "Not found"

def parse_products(html):
    """ HTML processing and product information extraction """
    soup = BeautifulSoup(html, "html.parser")
    products_html = soup.find_all("div", class_=PRODUCT_CLASS)
    products = []

    for product in products_html:
        name = find_product_name(product)
        price = extract_text(product.select_one(PRICE_TAG))
        description = extract_text(product.select_one(DESCRIPTION_TAG))
        image_tag = product.select_one(IMAGE_TAG)
        image = (image_tag.get("src") or image_tag.get("data-src") or "Not found") if image_tag else "Not found"

        products.append(Product(name, price, description, image))
    return products

def display_products(products):
    """ Displaying products in the console """
    for product in products:
        print(f"Product Name: {product.name}")
        print(f"Price: {product.price}")
        print(f"Description: {product.description}")
        print(f"Image URL: {product.image}")
        print("-" * 50)

def main():
    html = fetch_page(URL)
    if html:
        products = parse_products(html)
        display_products(products)
    else:
        print("Page not received")

if __name__ == "__main__":
    main()
