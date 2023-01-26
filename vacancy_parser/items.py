import scrapy
from itemloaders.processors import MapCompose, TakeFirst, Compose

'''Функция корректировки зарплаты. 
Из получаемого списка зарплаты извлекаем цифры, если таковые имеются, очищаем от
спецсимволов, переводим в числа. Валюта остается текстом. Возвращаем словарь зарплат.'''
def process_salary(value):
    if value:
        sal_min = 0
        sal_max = 0
        currency = 'None'
        if value[0] != 'з/п не указана':
            if value[0][0].isdecimal():
                sal_min = value[0].replace('\xa0', '')
                if value[2][0].isdecimal():
                    sal_max = value[2].replace('\xa0', '')
            elif value[0] == 'от ':
                sal_min = value[1].replace('\xa0', '')
                if value[3][0]:
                    if value[3][0].isdecimal():
                        sal_max = value[3].replace('\xa0', '')
            elif value[0] == 'до ':  
                sal_max = value[1].replace('\xa0', '')
            currency = value[-1]
        return {'Мин.плата': int(sal_min), 'Макс.плата': int(sal_max), 'Валюта': currency}

'''Функция корректировки названия компании.
При парсинге наименование(ия) задваивается(ются).'''
def process_company(value):
    if value:
        return ' '.join(value[0: -len(value)])

'''Функция корректировки описания.
Приводим получаемый список в единый текст.'''
def process_description(value):
    if value:
        return ' '.join(value) 

'''Функция корректировки даты.
Извлекаем дату, очищаем от спецсимволов.'''
def process_date(value):
    if value:
        return value[1].replace('\xa0', ' ')


'''При получении и записи данных используем пре- и пост-обработку с помощью функций.'''
class VacancyParserItem(scrapy.Item):
    name = scrapy.Field(output_processor=TakeFirst())
    salary = scrapy.Field(input_processor=Compose(process_salary), output_processor=TakeFirst())
    company = scrapy.Field(input_processor=Compose(process_company), output_processor=TakeFirst())
    location = scrapy.Field(output_processor=TakeFirst())
    description = scrapy.Field(input_processor=Compose(process_description), output_processor=TakeFirst())
    date = scrapy.Field(input_processor=Compose(process_date), output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    _id = scrapy.Field()
