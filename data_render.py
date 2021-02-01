import requests

def daywise_data_nigeria():
    day_wise = requests.get("https://api.covid19api.com/dayone/country/nigeria")
    day_wise_data = day_wise.json()

    day = []
    confirmed = []
    deaths = []
    i = 1
    for item in day_wise_data:
        day.append(i)
        confirmed.append(item['Confirmed'])
        deaths.append(item['Deaths'])
        i += 1
    
    daywise_multi_list = [day[:-1], confirmed[:-1], deaths[:-1]]
    del day
    del confirmed
    del deaths
    return daywise_multi_list

