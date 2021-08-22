import requests
import json
import time
import re
from .models import *
from django.http import HttpResponse


class HHapi:
    def __init__(self, page, name_vac, name_region):
        self.name_vac = name_vac
        self.name_region = name_region
        self.page = page

    def getarea(self):
        req = requests.get('https://api.hh.ru/suggests/areas', {'text': self.name_region})
        data = req.content.decode()
        req.close()
        jsobj = json.loads(data)
        try:
            return jsobj["items"][0]["id"]
        except IndexError:
            pass

    def getpage(self):
        params = {
            'text': 'NAME:' + self.name_vac,
            'area': self.getarea(),
            'page': self.page,  #
        }

        req = requests.get('https://api.hh.ru/vacancies', params)  # Посылаем запрос к API
        data = req.content.decode()  # Декодируем его ответ, чтобы Кириллица отображалась корректно
        req.close()
        return data


class Results:
    def __init__(self, name_vac, name_region, pk):
        self.name_v = name_vac
        self.name_r = name_region
        self.pk = pk

    def name_vac_hh(self, jsobj, vacancy):
        return jsobj['items'][vacancy]['name']

    def desc(self, jsobj_api):  # Получаем Описание вакансии
        return jsobj_api['description']

    def salary(self, jsobj_api):  # Получаем З/П
        if jsobj_api['salary'] is not None:
            if jsobj_api['salary']['from'] is not None and jsobj_api['salary']['to'] is not None :
                salary_res = f"{jsobj_api['salary']['from']} - {jsobj_api['salary']['to']} {jsobj_api['salary']['currency']}"
            else:
                salary_res = f"от {jsobj_api['salary']['from']} {jsobj_api['salary']['currency']}"
        else:
            salary_res = "Не указана"
        return salary_res

    def skills(self, jsobj_api):
        if len(jsobj_api["key_skills"]) != 0:
            skills_res = []
            for key_skills in range(0, len(jsobj_api["key_skills"])):
                skills_res.append(jsobj_api["key_skills"][key_skills]["name"])
            skills_res = '; '.join(skills_res)
        else:
            skills_res = "Не указаны"
        return skills_res

    def name_company(self, jsobj_api):
        return jsobj_api['employer']['name']

    def address_company(self, jsobj, vacancy):  # Получаем адрес компании:

        if jsobj['items'][vacancy]['address'] is not None:
            address_res = jsobj['items'][vacancy]['address']['raw']
        else:
            address_res = "Не указан"

        return address_res

    def url_vac(self, jsobj_api):
        return jsobj_api['alternate_url']

    def parsing(self):
        #s1 = Search.objects.create(input_vacancy=self.name_v, city=self.name_r)
        for page in range(0, 10):
            hh_req = HHapi(page, self.name_v, self.name_r)
            jsobj = json.loads(hh_req.getpage())
            for vacancy in range(0, len(jsobj["items"])):
                req_desc_api = requests.get(jsobj['items'][vacancy]['url'])  # Посылаем запрос к API для детальной информации по вакансии
                data_api = req_desc_api.content.decode()  # Декодируем его ответ, чтобы Кириллица отображалась корректно
                req_desc_api.close()
                jsobj_api = json.loads(data_api)


                Output_data.objects.create(
                    vacancy=self.name_vac_hh(jsobj, vacancy),
                    description=self.desc(jsobj_api),
                    salary=self.salary(jsobj_api),
                    skills=self.skills(jsobj_api),
                    company=self.name_company(jsobj_api),
                    address=self.address_company(jsobj, vacancy),
                    url_link=self.url_vac(jsobj_api),
                    input_vac_id=self.pk
                    )

            if (jsobj['pages'] - page) <= 1:
                break

        #return Output_data.objects.filter(input_vac_id=self.pk)

    # Необязательная задержка, но чтобы не нагружать сервисы hh, оставим. 5 сек мы может подождать
    time.sleep(0.25)
