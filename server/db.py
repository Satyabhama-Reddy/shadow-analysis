
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime, timedelta

uri = "mongodb+srv://cluster0.jy04cjp.mongodb.net/?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"
client = MongoClient(uri,
                     tls=True,
                     tlsCertificateKeyFile='X509-cert-8481942796777629104.pem',
                     server_api=ServerApi('1'))

db = client['shadow-analyzer']
collection = db['shadow-matrices']

def insert(timestamp, matrix):
    try:
        data_to_insert = {
            "timestamp": timestamp,
            "shadow-matrix": matrix,
        }
        inserted_id = collection.insert_one(data_to_insert).inserted_id
        data_to_insert["_id"] = str(inserted_id)
        # print(data_to_insert)
        return data_to_insert
    except Exception as e:
        print("Exception occured while inserting record", e)
        return -1

def get_records(start, end):
    print(start, end)
    query = {
        "timestamp": {
            "$gte": start,
            "$lte": end
        }
    }

    # Use the find() method to retrieve records that match the query
    matching_records = collection.find(query)
    return matching_records

    

#get_records(datetime.now() - timedelta(days=12), datetime.now())