import pymongo

def get_conn():
    client = pymongo.MongoClient(host='localhost', port=27017)
    return client

def get_db(client):
    db = client['hz_lottery_house']
    return db
