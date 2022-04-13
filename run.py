"""This file runs the script = webscraping + mongo database"""

# imports
import time
from webscraping import Webscraping
from mongo import Mongo

# runs the script
if __name__ == "__main__":
    with Webscraping() as scrap:
        scrap.land_coronavirus_data_website()
        data = scrap.scrape_data()
        df = scrap.create_dataframe(data)
        print(df)
        mongo = Mongo()
        db = mongo.create_database()
        col = mongo.create_collection(db)
        mongo.insert_data(df, db, col)
        mongo.show_one(db, col)
        mongo.show_all(db, col)
