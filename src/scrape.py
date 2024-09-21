import requests
import pandas as pd
from bs4 import BeautifulSoup
import streamlit as st

@st.fragment(run_every="2s")
def scrape(url):
    # Send a GET request to the webpage
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Read the HTML content
        html_content = response.content

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find the specific table element (you may need to adjust the selector)
        table = soup.find_all('table')

        # Use pandas to read the tables
        df1 = pd.read_html(str(table))[0]
        df1.columns = df1.iloc[0]                   # Set the first row as the column headers
        df1 = df1[1:]                               # Remove the first row
        df1.reset_index(drop=True, inplace=True)    # Reset the index

        df2 = pd.read_html(str(table))[1]
        df2.columns = df2.iloc[0]
        df2 = df2[1:]
        df2.reset_index(drop=True, inplace=True)
        # Drop unnecessary columns
        df2 = df2.drop(columns=['Rg', 'StNr', 'Fahrer', 'Gesamtzt', 'RD', 'GesPkt', 'Strafe'])

        # concatenate the two tables
        return pd.concat([df1, df2], axis=1)
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
