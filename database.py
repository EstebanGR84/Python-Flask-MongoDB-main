from pymongo import MongoClient
import certifi

uri = "mongodb+srv://a:Ovh0zTlX5voR3aEg@cluster0.kljgjmo.mongodb.net/?retryWrites=true&w=majority"
ca = certifi.where()

def dbConnection():
    try:
        client = MongoClient(uri, tlsCAFile=ca)
        db = client["dbb_users_app"]
    except ConnectionError:
        print('Error de conexión con la bdd')
    return db
