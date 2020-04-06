import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from webscraping import web_scrap
import pandas as pd
import numpy as np
from time import sleep
from Adafruit_IO import Client
import os

LARGE_FONT= ("Verdana", 12)
SMALL_FONT= ("Verdana", 6)
custome_country = ""

root = tk.Tk()

my_url = "https://www.worldometers.info/coronavirus/"
web = web_scrap(my_url)
last_time = web.get_last_updated_time()
all_country_df = web.all_country_dataframe()
df_global = web.global_dataframe()
df_global_pi = [df_global["active_cases"][0],
                df_global["total_recovered"][0],
                df_global["total_deaths"][0]]
all_dataframe = web.all_country_dataframe()
top_country_df = web.top_country_dataframe(10)

top_country_df_20_by_death = web.top_country_dataframe_by_deathe_rate(20)
mqtt_sending_data = top_country_df
top_country_df_bar = top_country_df
top_country_df_bar.drop(top_country_df_bar[top_country_df_bar["country"]=="World"].index, axis = 0, inplace = True)
mqtt_sending_data = mqtt_sending_data.append(df_global, ignore_index = True)
root.iconbitmap('covid.ico')
root.wm_title("COVID-19 Live Tracker")

bordwesize = 2
frame_for_data = tk.Frame(root)
frame_for_data.grid(row = 0, column = 0)

frame_for_plot = tk.Frame(root)
frame_for_plot.grid(row = 0, column = 1)

frame_for_time = tk.Frame(frame_for_data, relief="groove")
frame_for_time.grid(row= 0,column =0)


frame_for_split = tk.Frame(frame_for_data)
frame_for_split.grid(row=1,column=0)

frame_for_mqtt = tk.Frame(frame_for_split)
frame_for_mqtt.grid(row=0, column=1)
 
frame_for_datatable_1 = tk.Frame(frame_for_split)
frame_for_datatable_1.grid(row=0,column=0)


frame_for_datatable_2 = tk.Frame(frame_for_data)
frame_for_datatable_2.grid(row=2,column=0)



frame_dataseve = tk.Frame(frame_for_datatable_2)
frame_dataseve.grid(row=4,column=0)

labe_last_time = tk.Label(frame_for_time, text ="Covid 19 Tracker by yobots-"+ last_time, font = LARGE_FONT, height = 2,width = 60,  borderwidth=bordwesize, relief="groove")
labe_last_time.grid(row = 0, column = 0)

custome_country_name=tk.StringVar()

check_mqtt = tk.IntVar()
check_value = tk.Checkbutton(frame_for_mqtt, 
                                  text = "Data To MQTT",
                                  variable = check_mqtt,
                                  onvalue = 1,
                                  offvalue = 0,
                                  height= 1,
                                  width = 12,
                                  relief="groove")
check_value.grid(row = 0, column = 0)
mqtt_username_lable = tk.Label(frame_for_mqtt, text = "Adafrut Username",height = 1,width = 15,relief="groove", borderwidth = bordwesize)
mqtt_username_lable.grid(row = 1,column=0)
mqtt_username = tk.StringVar()
mqtt_entry = tk.Entry(frame_for_mqtt,text = "UserName",textvariable=mqtt_username, width = 30,relief="groove", borderwidth = bordwesize)
mqtt_entry.grid(row=1,column=1)
mqtt_api_key_lable = tk.Label(frame_for_mqtt, text = "Adafrut API Key",height = 1,width = 15,relief="groove", borderwidth = bordwesize)
mqtt_api_key_lable.grid(row = 2,column=0)
mqtt_api_key = tk.StringVar()
mqtt_api_key_entry = tk.Entry(frame_for_mqtt,text = "API Key",textvariable=mqtt_api_key, width = 30, relief="groove", borderwidth = bordwesize)
mqtt_api_key_entry.grid(row=2,column=1)


custome_country_name.set("--Select Custome Country--")
all_country_name = []
for country in all_country_df['country']:
    all_country_name.append(country)
custome_country_select = tk.OptionMenu(frame_for_datatable_1, custome_country_name,*all_country_name )
custome_country_select.config(width=26, font = LARGE_FONT, bg = "red", borderwidth=2, relief="groove")
custome_country = custome_country_name.get()
custome_country_select.grid(row=0, column = 2)

tree = ttk.Treeview(frame_for_datatable_1, columns = (1,2,3), show="headings", height = "8" )
tree.grid(row = 1,column=2)
tree.heading(1, text = "Data")
tree.column(1,minwidth=0,width=100)
tree.heading(2, text = "Global")
tree.column(2,minwidth=0,width=100)
tree.heading(3, text = custome_country)
tree.column(3,minwidth=0,width=100)

tree_all_view = tk.Label(frame_for_datatable_2, text = "All Country Data",height = 2,width = 20, relief="groove")
tree_all_view.grid(row = 0,column=0)
tree_all = ttk.Treeview(frame_for_datatable_2, columns = (1,2,3,4,5,6,7,8,9), show="headings", height = "15" )
tree_all.grid(row =1,column=0)
tree_all.heading(1, text = "Country")
tree_all.column(1,minwidth=0,width=100)
tree_all.heading(2, text = "Total Cases")
tree_all.column(2,minwidth=0,width=100)
tree_all.heading(3, text = "New Cases")
tree_all.column(3,minwidth=0,width=100)
tree_all.heading(4, text = "Total Deaths")
tree_all.column(4,minwidth=0,width=100)
tree_all.heading(5, text = "New Deaths")
tree_all.column(5,minwidth=0,width=100)
tree_all.heading(6, text = "Total Recovered")
tree_all.column(6,minwidth=0,width=100)
tree_all.heading(7, text = "Active Cases")
tree_all.column(7,minwidth=0,width=100)
tree_all.heading(8, text = "Serious Condition")
tree_all.column(8,minwidth=0,width=100)
tree_all.heading(9, text = "Death Rate(%)")
#df = web.all_country_dataframe()
tree_all.column(9,minwidth=0,width=100)
for row in range(len(all_country_df)):
    data =  str(all_country_df.loc[row][0])+str("       ")+str(all_country_df.loc[row][1])+str("       ")+str(all_country_df.loc[row][2])+str("       ")+str(all_country_df.loc[row][3])+str("       ")+str(all_country_df.loc[row][4])+str("       ")+str(all_country_df.loc[row][5])+str("       ")+str(all_country_df.loc[row][6])+str("       ")+str(all_country_df.loc[row][7])+str("       ")+str(all_country_df.loc[row][8])
    tree_all.insert('','end', value = data)

custome_country = custome_country_name.get()

f1 = Figure(figsize=(5,2), dpi=100)
a1 = f1.add_subplot(111)
wedges, texts,  autotexts = a1.pie(df_global_pi, autopct='%1.2f%%', textprops=dict(color="w"))
a1.legend(wedges, ["Active Cases", "Total Recovered", "Total Death"],
      loc="upper left",
      bbox_to_anchor=(1, 0, 0.5, 1),
      fontsize= 5)
a1.set_title('Pie Chart of Global Data of Active Cases, Recovered, Death', fontsize = 8)
canvas_pie = FigureCanvasTkAgg(f1, frame_for_plot)
canvas_pie.draw()
canvas_pie.get_tk_widget().grid(row=0, column=0)
canvas_pie._tkcanvas.grid(row=0, column=0)

f2 = Figure(figsize=(5,2), dpi=100)
a2 = f2.add_subplot(111)
x1 = np.arange(len((top_country_df_bar['country'])))  # the label locations
width = 0.3  # the width of the bars
rects1 = a2.bar(x1 - width- width/2, top_country_df_bar['active_cases'], width, facecolor = 'Black', label='Active Cases')
rects2 = a2.bar(x1 - width/2 , top_country_df_bar['total_recovered'], width, facecolor = 'gray', label='Recovered')
rects3 = a2.bar(x1 + width/2, top_country_df_bar['total_deaths'], width, facecolor = 'blue', label='Death')
a2.set_ylabel('Number of People')
a2.set_title('Bar Chart of Active Cases, Recovered, Death of top 10 country', fontsize = 8)
a2.set_xticks(x1)
a2.set_xticklabels(top_country_df_bar['country'], rotation = 30, fontsize =6)
a2.legend()
canvas_three_bar = FigureCanvasTkAgg(f2, frame_for_plot)
canvas_three_bar.draw()
canvas_three_bar.get_tk_widget().grid(row=1,column=0)
canvas_three_bar._tkcanvas.grid(row=1,column=0)

x2 = np.arange(len((top_country_df_20_by_death['country'])))  # the label locations
width = .7  # the width of the bars

f3 = Figure(figsize=(5,3), dpi=100)
a3 = f3.add_subplot(111)

rects4 = a3.bar(x2, top_country_df_20_by_death['death_rate'], width, facecolor = 'Black', label='Death Rate')

# Add some text for labels, title and custom x-axis tick labels, etc.
a3.set_ylabel('Death Rate (%)')
a3.set_title('Bar Chart of Top 20 country by Death rate(%)', fontsize = 8)
a3.set_xticks(x2)
a3.set_xticklabels(top_country_df_20_by_death['country'], rotation = 60, fontsize = 6)
a3.legend()

canvas_for_death_rate = FigureCanvasTkAgg(f3, frame_for_plot)
canvas_for_death_rate.draw()
canvas_for_death_rate.get_tk_widget().grid(row=2,column=0)
canvas_for_death_rate._tkcanvas.grid(row=2,column=0)

f3.tight_layout()

def data_update():
    custome_country = custome_country_name.get()
    if any(custome_country in country for country in all_country_name ):
        custome_country = custome_country_name.get()
        tree.heading(3, text = custome_country)
        row_name = ["Total_Cases", "New_Cases", "Total_Deaths", "New_Deaths", "Total_Recovered", "Active_Cases", "Serious_Condition", "Death_Rate"]
        for i in tree.get_children():
                tree.delete(i)
        for row in range(0,len(row_name)):
            df_custome = all_country_df[all_country_df["country"] == custome_country]
            marge = [df_global, df_custome]
            df_global_custome = pd.concat(marge).transpose()
            df_global_custome.columns = ["Global", custome_country]
            #data = "Active Cases"+"         "+str(df_global_custome["Global"][1])+"         "+str(df_global_custome[custome_country][1])+"New Cases"+"         "+str(df_global_custome["Global"][2])+"         "+str(df_global_custome[custome_country][2])+"Total Death"+"         "+str(df_global_custome["Global"][3])+"         "+str(df_global_custome[custome_country][3])+"New Death"+"         "+str(df_global_custome["Global"][4])+"         "+str(df_global_custome[custome_country][4)+"Total Recovered"+"         "+str(df_global_custome["Global"][5])+"         "+str(df_global_custome[custome_country][6])+"Total Recovered"+"         "+str(df_global_custome["Global"][6])+"         "+str(df_global_custome[custome_country][6])
            
            data = str(row_name[row])+"           "+str(df_global_custome["Global"][row+1])+"           "+str(df_global_custome[custome_country][row+1])
            tree.insert('','end', value = data)
            print(any(custome_country in country for country in all_country_name ))

def mqtt_send():
    if ((check_mqtt.get() == 1)):
        aio = Client(mqtt_username.get(), mqtt_api_key.get())
        mqtt_sending_df = mqtt_sending_data.append(all_country_df[all_country_df['country'] == custome_country], ignore_index=True)
        for country in mqtt_sending_df["country"]:
            country_pos = pd.Index(list(mqtt_sending_df.country))
            mqtt_sending_df_transpose = mqtt_sending_df[mqtt_sending_df["country"]==country].transpose()
            mqtt_sending_df_transpose.columns = ['Data']
            data_for_send = str(country_pos.get_loc(country)+1)+"_"+str(mqtt_sending_df_transpose['Data'][0])+"_"+str(mqtt_sending_df_transpose['Data'][1])+"_"+str(mqtt_sending_df_transpose['Data'][2])+"_"+str(mqtt_sending_df_transpose['Data'][3])+"_"+str(mqtt_sending_df_transpose['Data'][4])+"_"+str(mqtt_sending_df_transpose['Data'][5])+"_"+str(mqtt_sending_df_transpose['Data'][6])+"_"+str('{0:.2f}'.format(mqtt_sending_df_transpose['Data'][8]))
            aio.send('covid-19', data_for_send)
            aio.send('last-updated-time', last_time)
            sleep(1)
            print(mqtt_sending_df_transpose)
            print(data_for_send)

save_file_path = tk.Text(frame_dataseve, height =1, width = 20,relief="groove", borderwidth = bordwesize)
save_file_path.grid(row=0,column=2)
save_file_lable = tk.Label(frame_dataseve, text = "File Saved in:", width = 15,relief="groove" ,borderwidth = bordwesize)
save_file_lable.grid(row=0,column=1)


                                                           

def save_data():
    save_file_path.delete(1.0,tk.END)
    csv_file_name = last_time.lstrip("Last updated: ").replace(" ", "_").replace(",", "_").replace(":", "_") + ".csv"
    all_country_df.to_csv(csv_file_name)
    save_file_path.insert(tk.END, str(os.getcwd()))

btn = tk.Button(frame_for_datatable_1, text = 'Show Data',height = 1,width = 40, borderwidth = bordwesize, relief="raised",command = data_update)
btn.grid(row = 2, column = 2)
save_bttn = tk.Button(frame_dataseve, text = "Save Data",relief="groove", command=save_data)
save_bttn.grid(row=0,column=0)

btn_mqtt = tk.Button(frame_for_mqtt, text = 'Send Data',height = 1,width = 15,borderwidth = bordwesize, relief="raised",command = mqtt_send)
btn_mqtt.grid(row = 3, column = 0)

i=3600000
root.after(i,mqtt_send)
root.after(i*2,mqtt_send)
root.after(i*3,mqtt_send)
root.after(i*4,mqtt_send)
root.after(i*5,mqtt_send)
root.after(i*6,mqtt_send)
root.after(i*7,mqtt_send)
root.after(i*8,mqtt_send)


root.mainloop()

