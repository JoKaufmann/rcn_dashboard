import pandas as pd
from src.scrape import scrape

# URL of the webpage
url = 'https://www.rcnonline.de/rcnlive/gesamt.php'

# Scrape the webpage and get the dataframe
df = scrape(url)

# get index, where 'Fahrer' == 'Schall'
index = df.index[df['Fahrer'] == 'Schall'][0]
print(df.iloc[index])