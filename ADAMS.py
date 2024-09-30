import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd


class Scraping:

    def scrap(self, url):
        # Send an HTTP GET request to the URL
        response = requests.get(url)
        data = {"Date": None, "Open":None, "High":None, "Low":None, "Close":None ,"Volume": None}
        values = []
            # Get the current date for the file name
        current_date = datetime.now().strftime("%d-%m-%Y")
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            table = soup.find(class_="stats stats--noborder")
            close = soup.find(class_ = "numRange")["data-current"]

            for i in table.find_all(class_="stats_value"):
                values.append(float(i.get_text().replace(',', '')))  # Remove commas and convert to float

            data.update({"Date": current_date, "Open":values[0], "High":values[1], "Low":values[2], "Close": close, "Volume":values[3]})
            # Define the CSV file
            df_existing = pd.read_csv('stock_price_data.csv')
            # Create a DataFrame from the data
            df = pd.DataFrame([data])


            # Append the new data to the existing DataFrame
            df_updated = pd.concat([df_existing, df], ignore_index=True)

            # Save the updated DataFrame back to the same CSV file
            df_updated.to_csv('stock_price_data.csv', index=False)

        else:
            print('Scraping not allowed')
