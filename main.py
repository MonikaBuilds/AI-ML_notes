import pymongo
from urllib.parse import quote_plus

username = quote_plus("monikabhati")
password = quote_plus("Monika@25")

uri = f"mongodb+srv://{username}:{password}@cluster0.ppjlfru.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = pymongo.MongoClient(uri)

dataBase = client["neurolabDB"]
collection = dataBase["Products"]

d = {
    'CompanyName': 'iNeuron',
    'Product': 'Affordable AI',
    'CourseOffered': 'Machine learning with Deployment'
}

rec = collection.insert_one(d)

# Show all records
for idx, record in enumerate(collection.find()):
    print(f"{idx}: {record}")
