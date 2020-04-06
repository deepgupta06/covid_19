# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 16:31:35 2020

@author: Deep
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

    
class web_scrap:
    def __init__(self, url):
        self.url = url      
    
    def get_soup(self):
        html = requests.get(self.url)
        soup = BeautifulSoup(html.content, "html.parser")
        return soup
    
    def get_last_updated_time(self):
        soup_for_last_update_time = self.get_soup()
        for_time = soup_for_last_update_time.findAll("div",{"class":"content-inner"})
        last_updated_time = for_time[0].findAll('div')[1].text
        return last_updated_time
    
    def all_country_dataframe(self):
        soup_for_country_data=self.get_soup()
        table = soup_for_country_data.tbody.findAll("tr")
        single_contry_info = []
        for row in table:
            country_data_list = []
            country_info = row.findAll("td")
            for value in country_info:
                country_data = value.text.strip().replace(",","")
                if (country_data ==''):
                    country_data  = 0
                country_data_list.append(country_data)
            country_data_list
            single_contry_info.append(country_data_list)
        header = ["country", "total_cases", "new_cases", "total_deaths", "new_deaths", "total_recovered", "active_cases",
                  "serious_condition","total_cases_per1mpop", "total_death_per1mpop", "total_test", "Testper1m"]
        df = pd.DataFrame(np.array(single_contry_info), columns = header)
        df.drop(["total_cases_per1mpop","total_death_per1mpop", "total_test","Testper1m" ], axis =1,inplace = True)
        cols = df.columns.drop(["country"])
        df[cols] = df[cols].apply(pd.to_numeric)
        df["death_rate"]=df['total_deaths']/df['total_cases']*100
        return df
    
    def global_dataframe(self):
        df = self.all_country_dataframe()
        global_sum = df.sum().drop(["country","death_rate"])
        global_dataframe= pd.DataFrame(global_sum).transpose()
        global_dataframe.insert(loc = 0, column = "country", value = 'Global')
        global_dataframe.insert(loc = 8, column = "death_rate", value = (global_dataframe['total_deaths'][0]/global_dataframe['total_cases'][0]*100))
        return global_dataframe
    
    def top_country_dataframe(self, number):
        self.number = number
        df = self.all_country_dataframe()
        df_sorted = df.sort_values(by = "total_cases", ascending = False)
        top_country_data = df_sorted.head(number)
        return top_country_data
    
    def top_country_dataframe_by_deathe_rate(self, number):
       self.number = number
       df = self.all_country_dataframe()
       df_sorted = df.sort_values(by = "death_rate", ascending = False)
       top_country_data = df_sorted.head(number)
       return top_country_data






