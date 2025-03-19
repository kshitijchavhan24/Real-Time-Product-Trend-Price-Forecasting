import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
from kafka import KafkaProducer

# Setup Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Specify the path to your ChromeDriver if not added to PATH
service = Service("C:\\chromedriver\\chromedriver.exe")  # adjust path if needed
driver = webdriver.Chrome(service=service)

# Open a sample Amazon product page (example product URL)
driver.get("https://www.amazon.com/Positioning-Adjustable-Three-Layer-Dampening-Touchscreen/dp/B0D45ZHYZJ/ref=sxin_16_pa_sp_search_thematic_sspa?_encoding=UTF8&cv_ct_cx=gaming&sbo=RZvfv%2F%2FHxDF%2BO5021pAnSA%3D%3D&sr=1-4-2c727eeb-987f-452f-86bd-c2978cc9d8b9-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9zZWFyY2hfdGhlbWF0aWM")  # Replace with a valid product URL
time.sleep(3)  # wait for the page to load

# Initialize an empty dictionary to store product data
product_data = {}

# Extract the product title
try:
    title = driver.find_element(By.ID, "productTitle").text.strip()
    product_data['title'] = title
    print("Product Title:", title)
except Exception as e:
    print("Error extracting title:", e)

# Extract the product price
try:
    price = driver.find_element(By.CSS_SELECTOR, ".a-price .a-offscreen").text.strip()
    product_data['price'] = price
    print("Price:", price)
except Exception as e:
    print("Error extracting price:", e)

# Publish the product data to Kafka if data is collected
if product_data:
    producer.send('amazon_products', product_data)
    producer.flush()  # Ensure the message is sent
    print("Data published to Kafka.")

# Close the browser
driver.quit()
