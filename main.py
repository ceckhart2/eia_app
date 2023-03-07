import requests
import json
import matplotlib.pyplot as plt
import tkinter as tk
import tkintermapview
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)


# data = requests.get(url)
# datajson = json.loads(data.text)
# print(datajson)


# sort by different states, fuel type, year, make graphs showing percantage of each fuel type for certain years.

class MasterTK:
    def __init__(self):

        self.master = tk.Tk()
        self.master.geometry('1200x600')

        self.master.bind('<Return>', self.set_map)

        self.canvas = None
        label_main = tk.Label(self.master, text='Carbon Emissions in the USA', font=('Arial', 25))


        #Creating frames
        frame_map = tk.Frame(self.master)
        self.frame_plot = tk.Frame(self.master)

        #Map Frame contents
        label_location = tk.Label(frame_map, text='Enter or choose a state within the United States')
        self.strvar_entry = tk.StringVar()
        entry_location = tk.Entry(frame_map, textvariable=self.strvar_entry)



        self.map_widget = tkintermapview.TkinterMapView(frame_map, width=600, height=450)
        self.map_widget.set_address('Colorado')
        self.map_widget.add_left_click_map_command(self.add_marker_event)

        #Plot Frame contents
        label_year = tk.Label(self.frame_plot, text='Year')
        label_sector = tk.Label(self.frame_plot, text='Sector')

        self.strvar_year = tk.StringVar()
        self.strvar_sector = tk.StringVar()

        years = [str(i) for i in range(1980,2020)]
        sectors = ["Residential", "Commercial", "Industrial", "Electric", "Transportation", "All"]

        option_year = tk.OptionMenu(self.frame_plot, self.strvar_year, *years)
        option_sector = tk.OptionMenu(self.frame_plot, self.strvar_sector, *sectors)

        button_data = tk.Button(self.frame_plot, text='Retrieve Data', command=self.plot_data)


        #Packing items to map frame
        label_location.pack()
        entry_location.pack()
        self.map_widget.pack(side='left', padx=5)

        #packing items to plot frame
        label_year.grid(column=0, row=0, padx=5, pady=5)
        label_sector.grid(column=1, row=0, padx=5, pady=5)

        option_year.grid(column=0, row=1, padx=5,)
        option_sector.grid(column=1, row=1, padx=5,)

        button_data.grid(column=3, row=1, padx=5)

        #Packing frames to main
        label_main.pack(side='top', pady = 5)
        frame_map.pack(side='left', pady=5)
        self.frame_plot.pack(side='top', pady=5)
        self.master.mainloop()

    def plot_data(self):
        #Creates Search Query
        state = 'CO'
        year = self.strvar_year.get()
        api_key = 'tsK21n7UIzROgvie9e4Gd38vcubcSUsJeWjxHOWQ'
        base_url = 'https://api.eia.gov/v2/co2-emissions/co2-emissions-aggregates/data/?'
        filters = f'frequency=annual&data[0]=value&facets[stateId][]={state}&start={year}&end={year}'
        url = f'{base_url}api_key={api_key}&{filters}'

        #Sends request to retrieve data
        d1 = Data(url)
        data_dict = getattr(d1, self.strvar_sector.get().lower())

        fig = plt.figure(figsize=(5,4.5) , dpi=101)
        values = [value for key, value in data_dict.items() if key !="All Fuels"]
        plot = plt.pie([value for key, value in data_dict.items() if key !="All Fuels"], shadow=True,
                       labels =[round(value, 3) for key, value in data_dict.items() if key !="All Fuels"] )
        plt.title(f"{state} {self.strvar_sector.get()} C02 Emissions in {year} (Metric Tons)")
        plt.legend(['Petroleum', 'Natural Gas', "Coal"],loc='upper left')

        try:
            self.canvas.get_tk_widget().destroy()
        except AttributeError:
            pass

        self.canvas = FigureCanvasTkAgg(master=self.frame_plot, figure=fig)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(rowspan=5, columnspan=5, pady=10)


    def set_map(self, call):
        location = self.strvar_entry.get()
        self.marker_1 = self.map_widget.set_address(location, marker=True)

    def add_marker_event(self, coords):
        self.map_widget.delete_all_marker()

        location = tkintermapview.convert_coordinates_to_address(coords[0], coords[1])[0]
        marker = self.map_widget.set_marker(coords[0], coords[1])
        marker.set_text(location)
        self.strvar_entry.set(location.state)















class Data:
    def __init__(self, request):
        self.request = request
        api_request = requests.get(self.request)

        self.json = json.loads(api_request.text)['response']['data']
        self.data = {}
        self.labels = ['All fuels', 'Natural Gas', 'Coal', 'Petroleum']

        for item in self.json:
            if item['sector-name'] not in self.data.keys():
                self.data[item['sector-name']] = {}
            self.data[item['sector-name']][item['fuel-name']] = item['value']
    @property
    def residential(self):
        sizes = {sector:size for sector, size in self.data['Residential carbon dioxide emissions'].items()}
        return sizes
    @property
    def commercial(self):
        sizes = {sector:size for sector, size in self.data['Commercial carbon dioxide emissions'].items()}
        return sizes
    @property
    def electric(self):
        sizes = {sector:size for sector, size in self.data['Electric Power carbon dioxide emissions'].items()}
        return sizes
    @property
    def industrial(self):
        sizes = {sector:size for sector, size in self.data["Industrial carbon dioxide emissions"].items()}
        return sizes
    @property
    def transportation(self):
        sizes = {sector:size for sector, size in self.data["Transportation carbon dioxide emissions"].items()}
        return sizes
    @property
    def all(self):
        sizes = {sector:size for sector, size in self.data['Total carbon dioxide emissions from all sectors'].items()}
        return sizes


def make_request(state, year, api_key):
    base_url = 'https://api.eia.gov/v2/co2-emissions/co2-emissions-aggregates/data/?'
    filters = f'frequency=annual&data[0]=value&facets[stateId][]={state}&start={year}&end={year}'
    url = f'{base_url}api_key={api_key}&{filters}'
    return url


if __name__ == '__main__':
    request = make_request('CO', '1988', 'tsK21n7UIzROgvie9e4Gd38vcubcSUsJeWjxHOWQ')

    m1 = MasterTK()
