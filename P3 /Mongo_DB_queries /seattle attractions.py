def get_db(db_name):
    from pymongo import MongoClient
    client = MongoClient('localhost:27017')
    db = client[db_name]
    return db

    
def make_pipeline():
    pipeline = [ ] 
    pipeline =  [
                  {"$match":{"tourism":{"$exists":1}}},
                  {"$group":{ "_id":"$tourism", "count":{"$sum":1}}},
                  {"$sort":{"count":-1}},{"$limit":10}
                 ]
    return pipeline

def aggregate(db, pipeline):
    return [doc for doc in db.maps.aggregate(pipeline)]
    
if __name__ == '__main__':
    db = get_db('mdb')
    pipeline = make_pipeline()
    attractions = aggregate(db, pipeline)
    import pprint
    print "list of attractions"
    pprint.pprint(attractions)


