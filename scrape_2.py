import os
import urllib.request
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import json

# PROXY = "9ca8fa4022504c39a85426ec941406ec"

# Set up the Chrome options
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--proxy-server=%s' % PROXY)

# Set the path for the Chrome driver
driver_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
driver = webdriver.Chrome()

# Navigate to the main URL
url = "https://khaadi.com/"
driver.get(url)
driver.implicitly_wait(10)

# Select the country
# dropdown = driver.find_element(By.ID, 'countrydropdown')
# dropdown = dropdown.find_element(By.CLASS_NAME, 'select-items select-hide')
#
#
# dropdown.select_by_value('pk')

# Click the "ENTER" button
enter_button = driver.find_element(By.CLASS_NAME, 'splash-btn')
enter_button.click()

# Get the current URL after the redirect
homepage = driver.current_url
driver.get(homepage)

# Find the navigation bar
nav_bar = driver.find_element(By.CLASS_NAME, 'menu-group')

# Extract all the links within the navigation bar
nav_links = nav_bar.find_elements(By.TAG_NAME, 'a')

links = []
product_links = []
count = 0
khaadi_data = pd.read_csv("Khaadi_data.csv")

# Extract href attributes from the links
for link in nav_links:
    href = link.get_attribute("href")
    if href:
        links.append(href)
    driver.implicitly_wait(2)

driver.implicitly_wait(5)
# print(links)
# # Extract product links
for link in links:
    product_links.clear()
    print(product_links)
    print("link", link)
    #
    driver.get(link)
    #
    #     # Extract JSON data from the script tag
    script_element = driver.find_element(By.XPATH, "/html/body/script[8]")
    json_data = script_element.get_attribute("innerHTML")

    data = json.loads(json_data)
    #
    #
    #
    #     # Access the "itemListElement" and extract the URLs
    item_list = data.get("itemListElement")
    for item in item_list:
        #         #position = item.get("position")
        url = item.get("url")
        if url:
            product_links.append(url)
        driver.implicitly_wait(3)
    #
    driver.implicitly_wait(15)
    print(product_links)

    for product in product_links:
        #         # Visit the product link
        driver.get(product)
        #         print(product)
        #
        #
        #         # Extract all the required attributes
        sku = driver.find_element(By.CLASS_NAME, 'product-number').text
        id = sku.split(":")[-1].strip()
        if id not in khaadi_data['ID'].values:
            #
            product_name = driver.find_element(By.CLASS_NAME, 'product-name').text
            product_description = driver.find_element(By.CLASS_NAME, 'product-brand').text
            price_element = driver.find_element(By.CLASS_NAME, 'cc-price')
            price = price_element.get_attribute('content')
            availability = driver.find_element(By.CLASS_NAME, 'null').text

            #             # Find the section containing pictures
            pictures_section = driver.find_element(By.CLASS_NAME, 'inner')
            pictures_div = pictures_section.find_elements(By.CLASS_NAME, "item")
            image_urls = []
            #
            #             # Extract and print the image URLs
            for div_element in pictures_div:
                img_element = div_element.find_element(By.TAG_NAME, 'img')
                image_url = img_element.get_attribute("src")
                image_urls.append(image_url)
                driver.implicitly_wait(5)

            base_path = "images"
            #             # Creating the folder structure
            product_folder_path = os.path.join(base_path, id)
            #
            #             # Checking if the directory already exists
            if not os.path.exists(product_folder_path):
                os.makedirs(product_folder_path)
            else:
                print(f"Folder '{id}' already exists in '{base_path}' directory.")
            #
            #             # Iterate through the image URLs and download them
            for i, url in enumerate(image_urls):
                #                 # Create the file path for saving the image
                file_path = os.path.join(product_folder_path, f'image_{i}.jpg')
                driver.implicitly_wait(2)
                #                 # Use urllib to download the image
                urllib.request.urlretrieve(url, file_path)
                driver.implicitly_wait(2)
            #
            driver.implicitly_wait(5)
            #             # Create a new DataFrame for the current product
            df = pd.DataFrame({"ID": [id], "Product Name": [product_name], "Product Description": [product_description],
                               "Price": [price],
                               "Availability": [availability], "Img Path": product_folder_path,
                               "Product Link": product})
            #
            #             # Append the new data to the existing DataFrame
            khaadi_data = pd.concat([khaadi_data, df], ignore_index=True)
            #
            #             # Save the updated DataFrame back to the same CSV file
            khaadi_data.to_csv('khaadi_data.csv', index=False)
            #             print(product, " scrapped successfully")
            count = count + 1
            driver.implicitly_wait(15)
        #
        else:
            print(f"Product with id {id} and url {product} alreday available in csv")
            driver.implicitly_wait(15)
        driver.implicitly_wait(300)
    print(count)
#
#         # Quit the driver
driver.quit()
#
#
#
