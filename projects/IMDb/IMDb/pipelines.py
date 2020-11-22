# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import pymongo
import sqlite3


class ImdbPipeline:
    collection_name = "best_movies"

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(port=27017)
        self.db = self.client["IMDb"]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(item)
        return item


class SQLitePipeline:

    def open_spider(self, spider):
        self.connection = sqlite3.connect("imdb.db")
        self.cursor = self.connection.cursor()
        try:
            self.cursor.execute('''
                        CREATE TABLE best_movies(
                            title TEXT,
                            director TEXT,
                            year TEXT,
                            run_time TEXT,
                            genre TEXT,
                            rating FLOAT,
                            movie_url TEXT, 
                            movie_imdb_id TEXT
                        )

                    ''')
            self.connection.commit()
        except sqlite3.OperationalError:
            pass

    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        self.cursor.execute('''
            INSERT INTO best_movies (title, director, year, run_time, genre, rating, movie_url, movie_imdb_id) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)        
        ''', (
            item.get("title"),
            item.get("director"),
            item.get("year"),
            item.get("run_time"),
            item.get("genre"),
            item.get("rating"),
            item.get("movie_url"),
            item.get("movie_imdb_id"),
        ))
        self.connection.commit()
        return item
