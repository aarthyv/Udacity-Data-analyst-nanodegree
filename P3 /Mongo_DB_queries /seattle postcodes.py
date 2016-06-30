def get_db(db_name):
    from pymongo import MongoClient
    client = MongoClient('localhost:27017')
    db = client[db_name]
    return db

    
def make_pipeline():
    pipeline = [ ] 
    pipeline =  [
                  {"$match":{"address.postcode":{"$exists":1}}},
                  {"$group":{ "_id":"$address.postcode", "count":{"$sum":1}}},
                  {"$sort":{"count":-1}}
                 ]
    return pipeline

def aggregate(db, pipeline):
    return [doc for doc in db.maps.aggregate(pipeline)]
    
if __name__ == '__main__':
    db = get_db('mdb')
    pipeline = make_pipeline()
    postcodes = aggregate(db, pipeline)
    import pprint
    print "list of postcodes"
    pprint.pprint(postcodes)
