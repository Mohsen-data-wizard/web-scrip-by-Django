import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
from .models import Product

URL = "https://shoeseller.in/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(HTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
}
PRODUCT_CLASS = "product"
PRODUCT_NAME_TAGS = ["h1", "h2", "h3"]
PRICE_TAG = "bdi"
DESCRIPTION_TAG = "div"
IMAGE_TAG = "img"

def extract_text(element):
    return element.get_text(strip=True) if element else "Not found"

def scrape_products():
    response = requests.get(URL, headers=HEADERS)
    if response.status_code != 200:
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    products_html = soup.find_all("div", class_=PRODUCT_CLASS)

    for product in products_html:
        name = extract_text(product.find(PRODUCT_NAME_TAGS))
        price = extract_text(product.find(PRICE_TAG))

        description = extract_text(product.find(DESCRIPTION_TAG))
        image_tag = product.find(IMAGE_TAG)
        image = image_tag["src"] if image_tag and image_tag.has_attr("src") else "Not found"

        # Save to database
        Product.objects.create(name=name, price=price, description=description, image=image)

    return Product.objects.all()

def product_list(request):
    products = scrape_products()
    return render(request, "scraper/product_list.html", {"products": products})
