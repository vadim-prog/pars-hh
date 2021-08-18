# Библиотека для работы с HTTP-запросами. Будем использовать ее для обращения к API HH
import requests

# Пакет для удобной работы с данными в формате json
import json

# Модуль для работы со значением времени
import time

import re

from .models import Output_data, Search

# Модуль для работы с операционной системой. Будем использовать для работы с файлами
import os
'''
name_vac = input("Введите ваканси: ")
name_region = input("Введите регион: ")
'''

def getarea(name_region):
    req = requests.get('https://api.hh.ru/suggests/areas', {'text': name_region})
    data = req.content.decode()
    req.close()
    jsobj = json.loads(data)
    return jsobj["items"][0]["id"]


def getpage(page, name_region, name_vac):
    """
    Создаем метод для получения страницы со списком вакансий.
    Аргументы:
        page - Индекс страницы, начинается с 0. Значение по умолчанию 0, т.е. первая страница
    """

    # Справочник для параметров GET-запроса
    params = {
        # 'text': 'NAME:' + name_vac,  # Текст фильтра. В имени должно быть слово "Аналитик"
        'text': 'NAME:' + name_vac,
        # 'area': int(getarea(name_region)),  # Поиск ощуществляется по вакансиям города Москва
        'area': int(getarea(name_region)),
        'page': page,  # Индекс страницы поиска на HH
        # 'per_page': 50 # Кол-во вакансий на 1 странице
    }

    req = requests.get('https://api.hh.ru/vacancies', params)  # Посылаем запрос к API
    data = req.content.decode()  # Декодируем его ответ, чтобы Кириллица отображалась корректно
    req.close()
    return data


# Считываем первые 2000 вакансий
def results(name_region, name_vac, pk):
    for page in range(0, 10):

        # Преобразуем текст ответа запроса в справочник Python
        jsobj = json.loads(getpage(page, name_region, name_vac))
        for vacancy in range(0, len(jsobj["items"])):
            # Получаем название вакансии
            print(f"НАЗВАНИЕ ВАКАНСИИ: {jsobj['items'][vacancy]['name']}")

            # Получаем Описание вакансии
            req_desc_api = requests.get(jsobj['items'][vacancy]['url'])  # Посылаем запрос к API для детальной информации по вакансии
            data_api = req_desc_api.content.decode()  # Декодируем его ответ, чтобы Кириллица отображалась корректно
            req_desc_api.close()
            jsobj_api = json.loads(data_api)
            res_desc = re.sub('</?\w+\s?>', '', jsobj_api['description'])  # Исключаем теги из описания вакансии по регулярному выражению
            #print(f"Описание: {res_desc}")

            # Получаем З/П
            if jsobj_api['salary'] is not None:
                #print(f"Зарплата: от {jsobj_api['salary']['from']}", end=' ')
                salary_res = f"от {jsobj_api['salary']['from']}"
                if jsobj_api['salary']['to'] is not None:
                    #print(f"до {jsobj_api['salary']['to']} {jsobj_api['salary']['currency']}")
                    salary_res = salary_res + f"до {jsobj_api['salary']['to']} {jsobj_api['salary']['currency']}"
                else:
                    #print(jsobj_api['salary']['currency'])
                    salary_res = salary_res + jsobj_api['salary']['currency']
            else:
                #print("Зарплата: Не указано")
                salary_res = "Не указано"

            # Получаем ключевые навыки
            skills_res = []
            for key_skills in range(0, len(jsobj_api["key_skills"])):
                #print(f'Ключевые навыки: {jsobj_api["key_skills"][key_skills]["name"]}', end='; ')
                skills_res.append(jsobj_api["key_skills"][key_skills]["name"])
            else:
                #print('')
                skills_res.append("")

            # Получаем Название компании
            print(f"Название компании: {jsobj_api['employer']['name']}")

            # ПОлучаем адрес компании:
            if jsobj['items'][vacancy]['address'] is not None:
                #print(f"Адрес компании: {jsobj['items'][vacancy]['address']['raw']}")
                address_res = jsobj['items'][vacancy]['address']['raw']
            else:
                address_res = "Не указан"

            # Получаем ссылку на вакансию:
            #print(f"ССылка на вакансию: {jsobj_api['alternate_url']}")
            '''
            p = Output_data(vacancy = jsobj['items'][vacancy]['name'], description = res_desc, salary = salary_res,
                            skills = '; '.join(skills_res), company = jsobj_api['employer']['name'],
                            address = jsobj['items'][vacancy]['address']['raw'], url_link = jsobj_api['alternate_url'])
            '''
            p = Output_data(vacancy = jsobj['items'][vacancy]['name'], description = res_desc, salary = salary_res,
                            skills = '; '.join(skills_res), company = jsobj_api['employer']['name'],
                            url_link = jsobj_api['alternate_url'], address = address_res, input_vac_id = int(pk))
            p.save()
        if (jsobj['pages'] - page) <= 1:
            break
    # Необязательная задержка, но чтобы не нагружать сервисы hh, оставим. 5 сек мы может подождать
    time.sleep(0.25)

