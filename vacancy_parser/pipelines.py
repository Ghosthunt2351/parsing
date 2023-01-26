from itemadapter import ItemAdapter
from pymongo import MongoClient


class VacancyParserPipeline:
    '''При инициализации сразу запускаем клиент mongo'''
    def __init__(self):
        client = MongoClient('localhost:27017')
        self.mongo_db = client.vacancy_parser

    '''В пайплайне создаем коллекцию по имени паука и добавляем туда спарсенные данные'''
    def process_item(self, item, spider):
        collection = self.mongo_db[spider.name]
        collection.insert_one(item)
        return item
