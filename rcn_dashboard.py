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
#     [5, 16, 'Driver A', '01:30.00', 5, 100, 0, 
#      '08:09.50', '08:09.50', '08:09.45', '07:49.40', '07:59.35', '08:09.30', 
#      '08:09.25', '08:09.20', '08:09.15', '08:09.10', pd.NaT, pd.NaT, 
#         pd.NaT, pd.NaT],
#     [2, 17, 'Driver B', '01:32.00', 5, 95, 0, 
#      '08:10.10', '09:10.00', '10:09.55', '07:59.50', '08:09.45', '09:09.40', 
#      '10:09.35', '07:56.30', '07:49.25', pd.NaT, pd.NaT, pd.NaT, 
#      pd.NaT, pd.NaT],
#     [3, 18, 'Driver C', '01:32.00', 5, 95, 0, 
#      '08:10.10', '09:10.00', '10:09.55', '07:59.50', '08:09.45', '09:09.40', 
#      '10:09.35', '07:56.30', '07:49.25', pd.NaT, pd.NaT, pd.NaT, 
#      pd.NaT, pd.NaT],
#     [4, 19, 'Driver D', '01:32.00', 5, 95, 0, 
#      '08:10.10', '09:10.00', '10:09.55', '07:59.50', '08:09.45', '09:09.40', 
#      '10:09.35', '07:56.30', '07:49.25', pd.NaT, pd.NaT, pd.NaT, 
#      pd.NaT, pd.NaT]
# ]
# # Create the DataFrame
# df = pd.DataFrame(data, columns=columns)

with st.sidebar:
    st.title('RCN Dashboard')
    own_n = int(st.text_input('Enter your start number', '16'))
    comp_n = int(st.text_input('Compare against start number', '17'))

# get own data
try:
    own_i = df.index[df['StNr'] == own_n].tolist()[0]
    comp_i = df.index[df['StNr'] == comp_n].tolist()[0]
    own_data = df.iloc[own_i]
    comp_data = df.iloc[comp_i]

    # own current round
    current_round = int(own_data['RD'])

    # Display overview data
    # st.title('RCN Overview - '+own_data['Fahrer'])
    col1, col2, col3 = st.columns([1,1,1])  # 1:1:1 ratio
    if current_round > 1:
        col1.metric(label='Current Round: '+str(current_round), value=own_data['AB'+str(current_round)], delta=round(str_to_sec(own_data['AB'+str(current_round)])-str_to_sec(own_data['AB'+str(current_round-1)]), 2), delta_color='inverse')
    else: 
        col1.metric(label='Current Round: '+str(current_round), value=own_data['AB'+str(current_round)])
    if own_data['AB1'] is not pd.NaT:
        col2.metric(label='Set Time', value=own_data['AB1'])
    laps = ['AB1', 'AB2', 'AB3', 'AB4', 'AB5', 'AB6', 'AB7', 'AB8', 'AB9', 'AB10', 'AB11', 'AB12', 'AB13', 'AB14']
    # st.write(own_data['AB1'])
    fastest_lap_i = own_data[laps].apply(str_to_sec).idxmin()
    fastest_lap_comp_i = comp_data[laps].apply(str_to_sec).idxmin()
    col3.metric(label='Fastest Lap', value=own_data[fastest_lap_i])

    st.text('Sprint laps')
    if int(own_data['Rg']) is not 1: 
        st.write(st.write(df.iloc[[own_i-1, own_i, comp_i]][['Rg', 'StNr', 'Fahrer', 'AB2', 'AB3', 'AB4', 'AB5', 'AB7', 'AB8', 'AB9', 'AB10']]))
    else:
        st.write(st.write(df.iloc[[own_i, comp_i]][['Rg', 'StNr', 'Fahrer', 'AB2', 'AB3', 'AB4', 'AB5', 'AB7', 'AB8', 'AB9', 'AB10']]))
    sprint_laps = ['AB2', 'AB3', 'AB4', 'AB5', 'AB7', 'AB8', 'AB9', 'AB10']
    own_sprint_time = 0
    comp_sprint_time = 0
    for l in laps:
        if pd.isna(own_data[l]):
            own_sprint_time += str_to_sec(own_data[fastest_lap_i])
        else:
            own_sprint_time += str_to_sec(own_data[l])
        if pd.isna(comp_data[l]):
            comp_sprint_time += str_to_sec(comp_data[fastest_lap_comp_i])
        else:
            comp_sprint_time += str_to_sec(comp_data[l])
    col21, col22 = st.columns([1,1])
    col21.metric(label='Est. sprint time', value=round(own_sprint_time,2), delta=round(comp_sprint_time-own_sprint_time,2))
    col22.metric(label='Est. sprint time StNr '+str(comp_n), value=round(comp_sprint_time,2))

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