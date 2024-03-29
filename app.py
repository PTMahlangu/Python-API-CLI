
import sys
import requests
import json
import colorama
import datetime
from termgraph import termgraph as tg  # To plot on the terminal
import pandas as pd  # To filter by dates
from colorama import Fore, Back, Style
colorama.init(autoreset=True)

sys.tracebacklimit = 0
USERS_URL = 'http://sam-user-activity.eu-west-1.elasticbeanstalk.com/'

def getData():
    """
    Get perfom get  request
    return response
    """
    response_API = requests.get(USERS_URL)

    if(response_API.ok):
        return response_API
    else:
        return None


def formatData(response):
    """
    format data to json list
    return date , number of users
    """
    if(response == None):
            raise Exception(f"{Fore.RED}Server Error!")
    try:
        if(response.status_code == 200):
            data = response.text
            parse_json = json.loads(data)
            labels = list(parse_json.keys())
            values = list( [x] for x in parse_json.values())
            return labels,values
        else:
            raise Exception(f"{Fore.RED}Server Error!\n code:{response.status_code}")

    except Exception as e:
	    print("ERROR : "+str(e))


def plotData(labels,data):
    """
    Get plot data on at the terminal
    return none
    """
    len_categories = 1
    args = {'filename': None, 'title': None, 'width': 50,
            'format': '{:<5.2f}', 'suffix': '', 'no_labels': False,
            'color': None, 'vertical': False, 'stacked': False,
            'different_scale': False, 'calendar': False,
            'start_dt': None, 'custom_tick': '', 'delim': '',
            'verbose': False, 'version': False}

    colors = [91]

    normal_data = tg.normalize(data, 120)
    print("\nUserbase Statistics\n")
    tg.stacked_graph(labels, data, normal_data, len_categories, args, colors)
    print("")



def filterData(data,labels,arguments,dateRange=[]):
    """
    Filter data between two dates
    return filtered data
    """
    try:
        df = pd.DataFrame({'users': data,'date': labels})
        # Convert the date to datetime64
        df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')

        maxDate = datetime.datetime(int(labels[-1].split("-")[2]), int(labels[-1].split("-")[1]), int(labels[-1].split("-")[0]))
        minDate = datetime.datetime(int(labels[0].split("-")[2]), int(labels[-1].split("-")[1]), int(labels[0].split("-")[0]))
        if (arguments):
            queryMax = datetime.datetime(int(dateRange[1].split("-")[0]), int(dateRange[1].split("-")[1]), int(dateRange[1].split("-")[2]))
            queryMin = datetime.datetime(int(dateRange[0].split("-")[0]), int(dateRange[0].split("-")[1]), int(dateRange[1].split("-")[2]))

            if((maxDate < queryMax) or (minDate > queryMin )):
                raise Exception(f"{Fore.RED}Date out of range!\n min date: {labels[0]}\n max date: {labels[-1]}\n Choose date between min and max.")
                
            filtered_df = df.loc[(df['date'] >= dateRange[0])
                                & (df['date'] <= dateRange[1])]
        else:
             filtered_df = df['date']          

        return  [labels[i] for i in filtered_df.index],[data[i] for i in filtered_df.index]
    except Exception as e:
	    print("ERROR : "+str(e))
        


if __name__ == "__main__":

    if(len(sys.argv) >= 2):
        datesRange = sys.argv[1:3]
        labels , data = formatData(getData())
        filteredLabels, filteredData= filterData(data,labels,True,datesRange)
        plotData(filteredLabels, filteredData)
    else:
        labels , data = formatData(getData())
        filteredLabels, filteredData= filterData(data,labels,False)
        plotData(filteredLabels, filteredData)

