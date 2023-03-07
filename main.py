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
        self.canvas = None
        label_main = tk.Label(self.master, text='Carbon Emissions in the USA', font=('Arial', 25))


        #Creating frames
        self.frame1 = tk.Frame(self.master)
        self.frame2 = None
        #Creating frame contents
        self.label_state = tk.Label(self.frame1, text='State')
        label_year = tk.Label(self.frame1, text='Year')
        label_sector = tk.Label(self.frame1, text='Sector')

        self.strvar_year = tk.StringVar()
        self.strvar_sector = tk.StringVar()
        self.strvar_state = tk.StringVar()

        years = [str(i) for i in range(1980,2020)]
        sectors = ["Residential", "Commercial", "Industrial", "Electric", "Transportation", "All"]
        states = ['AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA',
           'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME',
           'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM',
           'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
           'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY']


        option_year = tk.OptionMenu(self.frame1, self.strvar_year, *years)
        option_sector = tk.OptionMenu(self.frame1, self.strvar_sector, *sectors)
        option_state = tk.OptionMenu(self.frame1, self.strvar_state, *states)


        button_retrieve = tk.Button(self.frame1, text='Retrieve Data', command=self.plot_data)

        #packing items to plot frame
        self.label_state.grid(column=0, row=0, padx=5, pady=5)
        label_year.grid(column=1, row=0, padx=5, pady=5)
        label_sector.grid(column=2, row=0, padx=5, pady=5)

        option_state.grid(column=0, row=1, padx=5)
        option_year.grid(column=1, row=1, padx=5,)
        option_sector.grid(column=2, row=1, padx=5,)

        button_retrieve.grid(column=3, row=1, padx=5)

        #Packing frames to main
        label_main.pack(side='top', pady = 5)
        self.frame1.pack(side='top', pady=5)
        self.master.mainloop()

    def plot_data(self):
        #Creates Search Query
        state = self.strvar_state.get()
        year = self.strvar_year.get()
        api_key = 'tsK21n7UIzROgvie9e4Gd38vcubcSUsJeWjxHOWQ'
        base_url = 'https://api.eia.gov/v2/co2-emissions/co2-emissions-aggregates/data/?'
        filters = f'frequency=annual&data[0]=value&facets[stateId][]={state}&start={year}&end={year}'
        url = f'{base_url}api_key={api_key}&{filters}'

        #Sends request to retrieve data
        d1 = Data(url)
        data_dict = getattr(d1, self.strvar_sector.get().lower())

        fig = plt.figure(figsize=(5,5) , dpi=100)
        values = [value for key, value in data_dict.items() if key !="All Fuels"]
        plot = plt.pie([value for key, value in data_dict.items() if key !="All Fuels"], shadow=True,
                       labels =[round(value, 3) for key, value in data_dict.items() if key !="All Fuels"] )
        plt.title(f"{state} {self.strvar_sector.get()} C02 Emissions - {year} (Metric Tons)")
        plt.figlegend(['Petroleum', 'Natural Gas', "Coal"],loc='lower right')

        try:
            self.canvas.get_tk_widget().destroy()
        except AttributeError:
            pass

        self.canvas = FigureCanvasTkAgg(master=self.frame1, figure=fig)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(rowspan=5, columnspan=5, pady=5)


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
