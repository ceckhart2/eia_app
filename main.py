import requests
import json
import matplotlib.pyplot as plt
import tkinter as tk


# data = requests.get(url)
# datajson = json.loads(data.text)
# print(datajson)


# sort by different states, fuel type, year, make graphs showing percantage of each fuel type for certain years.

class MasterTK:
    def __init__(self, master):
        self.master = master

        self.master.mainloop()


class Data:
    def __init__(self, request):
        api_request = requests.get(request)

        self.json = json.loads(api_request.text)['response']['data']
        self.data = {}
        self.labels = ['All fuels', 'Natural Gas', 'Coal', 'Petroleum']

        for item in self.json:
            if item['sector-name'] not in self.data.keys():
                self.data[item['sector-name']] = {}
            self.data[item['sector-name']][item['fuel-name']] = item['value']

    def residential(self):
        sizes = [size for size in self.data['Residential carbon dioxide emissions'].values()]



def make_request(state, year, api_key):
    base_url = 'https://api.eia.gov/v2/co2-emissions/co2-emissions-aggregates/data/?'
    filters = f'frequency=annual&data[0]=value&facets[stateId][]={state}&start={year}&end={year}'
    url = f'{base_url}api_key={api_key}&{filters}'
    return url


if __name__ == '__main__':
    request = make_request('CO', '2018', 'tsK21n7UIzROgvie9e4Gd38vcubcSUsJeWjxHOWQ')
    d1 = Data(request)

    print(d1.residential())

    # root = tk.Tk()
    # MasterTK(root)
