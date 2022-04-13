"""Performs simple MongoDB operations"""

#imports
from pymongo import MongoClient

class Mongo():

    def __init__(self, service_name='mongo', login='admin', password='password123', port='27017', database_name='coronavirusDB'):
        """Instanciate the instance of MongoDB client"""

        self.service_name = service_name
        self.login = login
        self.password = password
        self.port = port
        self.database_name = database_name
        self.client = MongoClient(f"mongodb://{self.login}:{self.password}@{self.service_name}:{self.port}")
        print('Mongo started within container')

    def create_database(self):
        """Creates Mongo database"""

        mydb = self.client[self.database_name]
        print(f'Database named {self.database_name} was created!')

        return mydb

    def delete_database(self):
        """Deletes Mongo database"""

        self.client.drop_database(self.database_name)
        print(f'Database {self.database_name} was deleted!')

    @staticmethod
    def create_collection(database, collection_name='coronavirusCollection'):
        """Creates Mongo collection"""

        mycol = database[collection_name]
        print(f'Collection {collection_name} was created!')

        return mycol

    @staticmethod
    def delete_collection(database, collection):
        """Deletes Mongo collection"""

        database.collection.drop()
        print('Collection was deleted!')

    @staticmethod
    def insert_data(df, database, collection):
        """Populates collection with data"""

        database.collection.insert_many(df.to_dict('records'))
        print(f'Data was inserted into database and collection!')

    @staticmethod
    def show_one(database, collection):
        """Prints the first row of Mongo collection"""

        print(database.collection.find_one())

    @staticmethod
    def show_all(database, collection):
        """Shows all items in Mongo collection"""

        cursor = database.collection.find({})
        for document in cursor:
            print(document)