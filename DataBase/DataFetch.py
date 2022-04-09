import pymongo
from pymongo.server_api import ServerApi

def fetch(index):
    loc = "mongodb+srv://root-yash:J6mQZrPOietkgtpt@snakedataset.pheez.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    client = pymongo.MongoClient(
        loc,
        server_api=ServerApi('1')
    )
    db = client["SnakeDetails"]
    collection = db["SnakeDataset"]
    data = collection.find_one({'idx': index+1}, {"_id": 0, "idx": 0, "Genus": 0})
    return data
