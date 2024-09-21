import streamlit as st
import pandas as pd
from src.scrape import scrape
from converter import str_to_timedelta, str_to_sec
import numpy as np

# URL of the webpage
url = 'https://www.rcnonline.de/rcnlive/gesamt.php'
# Scrape the webpage and get the dataframe
df = scrape(url)

# # debug
# # Define the columns
# columns = ['Rg', 'StNr', 'Fahrer', 'Gesamtzt', 'RD', 'GesPkt', 'Strafe', 
#            'AB1', 'AB2', 'AB3', 'AB4', 'AB5', 'AB6', 'AB7', 'AB8', 'AB9', 
#            'AB10', 'AB11', 'AB12', 'AB13', 'AB14']

# # Create sample data
# data = [
#     [1, 16, 'Driver A', '01:30.00', 5, 100, 0, 
#      '00:10.00', '00:09.50', '00:09.45', '07:49.40', '07:59.35', '00:09.30', 
#      '00:09.25', '00:09.20', '00:09.15', '00:09.10', pd.NaT, pd.NaT, 
#         pd.NaT, pd.NaT],
#     [2, 17, 'Driver B', '01:32.00', 5, 95, 0, 
#      '00:10.10', '00:10.00', '00:09.55', '00:09.50', '00:09.45', '00:09.40', 
#      '00:09.35', '00:09.30', '00:09.25', pd.NaT, pd.NaT, pd.NaT, 
#      pd.NaT, pd.NaT]
# ]

# # Create the DataFrame
# df = pd.DataFrame(data, columns=columns)

with st.sidebar:
    st.title('RCN Dashboard')
    own_n = int(st.text_input('Enter your start number', '16'))
    comp1_n = int(st.text_input('Compare against first start number', '16'))
    comp2_n = int(st.text_input('Compare against second start number', '16'))

# get own data
try:
    own_i = df.index[df['StNr'] == own_n].tolist()[0]
    own_data = df.iloc[own_i]
    current_round = int(own_data['RD'])

    # Display overview data
    st.title('RCN Overview - '+own_data['Fahrer'])
    col1, col2, col3 = st.columns([1,1,1])  # 1:1:1 ratio
    if current_round > 1:
        col1.metric(label='Current Round: '+str(current_round), value=own_data['AB'+str(current_round)], delta=round(str_to_sec(own_data['AB'+str(current_round)])-str_to_sec(own_data['AB'+str(current_round-1)]), 2), delta_color='inverse')
    else: 
        col1.metric(label='Current Round: '+str(current_round), value=own_data['AB'+str(current_round)])
    laps = ['AB1', 'AB2', 'AB3', 'AB4', 'AB5', 'AB6', 'AB7', 'AB8', 'AB9', 'AB10', 'AB11', 'AB12', 'AB13', 'AB14']
    # st.write(own_data['AB1'])
    fastest_lap_i = own_data[laps].apply(str_to_sec).idxmin()
    col3.metric(label='Fastest Lap', value=own_data[fastest_lap_i])
    # for lap in laps:
    #     df[lap] = df[lap].apply(str_to_timedelta)
    # df['StNr'] = pd.to_numeric(df['StNr'], errors='coerce')
    # df['Rg'] = pd.to_numeric(df['Rg'], errors='coerce')
    # df['GesPkt'] = pd.to_numeric(df['GesPkt'], errors='coerce')
    # df['RD'] = pd.to_numeric(df['RD'], errors='coerce')
    
    st.text('Current Standings')
    st.write(df[['Rg', 'StNr', 'Fahrer', 'Gesamtzt', 'RD', 'GesPkt', 'Strafe', 'AB1', 'AB2', 'AB3', 'AB4', 'AB5', 'AB6', 'AB7', 'AB8', 'AB9', 'AB10', 'AB11', 'AB12', 'AB13', 'AB14']])

except IndexError:
    st.error('Start number '+str(own_n)+' not found')