import requests
from bs4 import BeautifulSoup

# Product page link(Change to the desired link)
URL = "https://example.com/products"
# Header, to prevent blocking
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
}
# Send a request to the site
response = requests.get("https://shoeseller.in/", headers=headers)
if response.status_code == 200:
    # Check and adjust page encoding
    response.encoding = response.apparent_encoding  # تشخیص خودکار کدگذاری صفحه
    soup = BeautifulSoup(response.text, "html.parser")
    # Find all product blocks
    products = soup.find_all("div", class_="product")  # تغییر کلاس بسته به سایت مورد نظر
    for product in products:
        # Product name
        name = product.find(["h1", "h2", "h3"])
        product_name = name.get_text(strip=True) if name else "Not found"
        # Price
        price = product.find("bdi")
        product_price = price.get_text(strip=True) if price else "Not found"
        # Description
        description = product.find("div")
        product_description = description.get_text(strip=True) if description else "Not found"
        # Photo link
        image = product.find("img")
        product_image = image["src"] if image else "Not found"
        # Display product information
        print(f"Product Name: {product_name}")
        print(f"Price: {product_price}")
        print(f"Description: {product_description}")
        print(f"Image URL: {product_image}")
        print("-" * 50)
else:
    print(f"Failed to retrieve the page, Status Code: {response.status_code}")
