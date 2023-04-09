import requests
import pandas as pd
import time
from pymongo import MongoClient

def get_weather(zipcode):

    url = "https://weatherapi-com.p.rapidapi.com/current.json"

    q_param = {"q":zipcode}

    headers = {
        "X-RapidAPI-Key": "API-KEY",
        "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=q_param)
    data_to_store = {
        'zip':zipcode,
        'city': response.json()['location']['name'],
        'created_at': time.time(),
        'weather':  response.json()['current']
    }
    return data_to_store

def create_list_of_weather_per_zipcode(zipcodes):
    list = []
    for zip in zipcodes['Zip']:
        print(zip)
        list.append(get_weather(zip))
    return list

def load_zipcodes():
    return pd.read_csv('Top100-US.csv',delimiter=';',converters={'Zip': str})

def write_weather_to_db(weather_per_zipcode):
    client = MongoClient("mongodb://db:27017/")
    db = client['mydatabase']
    collection = db['mycollection']           
    result = collection.insert_many(weather_per_zipcode)
    return result

def get_all_documents():
    client = MongoClient("mongodb://db:27017/")
    # Select the database and collection
    db = client["mydatabase"]
    collection = db["mycollection"]
    documents = collection.find()
    # Close the MongoDB connection
    x = list(documents).copy()
    blah = client.close()
    # Return the documents as a lis q t
    return x
    

if __name__ == '__main__':
    zips = load_zipcodes()
    weather_per_zipcode = create_list_of_weather_per_zipcode(zips)
    print('SUCCESSFULLY GOT ALL WEATHER INFORMATION')
    write_weather_to_db(weather_per_zipcode)
    print('SUCCESSFULLY WROTE RECORDS TO DB')
    all_records = get_all_documents()
    print(all_records)
    print('NUMBER OF RECORDS AFTER RUN:', len(all_records))
    