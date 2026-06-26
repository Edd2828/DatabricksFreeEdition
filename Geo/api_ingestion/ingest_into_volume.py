# Databricks notebook source
import requests


class RestCountries:

    BASE_URL = 'https://api.restcountries.com/countries/v5'
    PAGE_LIMIT = 100

    def __init__(self, token: str):
        self._token = token
        self.header = {'Authorization': f'Bearer {self._token}'}

    def get_page(self, offset: int):
        params = {
            "response_fields": ["names.common", "names.official", "population", "currencies", "languages"],
            "limit": self.PAGE_LIMIT,
            "offset": offset,
        }
        return requests.get(
            self.BASE_URL,
            headers=self.header,
            params=params
        )
    
    @staticmethod
    def store_data(response):
        data = response.json()
        print(data['data']['meta'])
        request_id = data['data']['meta']['request_id']
        spark.sql(f"CREATE VOLUME IF NOT EXISTS workspace.default.rest_countries;")
        dbutils.fs.put(f"/Volumes/workspace/default/rest_countries/request_id_{request_id}.json", response.text, True)
    
    def get_pages(self):
        
        offset = 0

        response = self.get_page(offset=offset)
        
        data = response.json()
        more_pages: bool = data['data']['meta']['more']

        self.store_data(response=response)

        offset += self.PAGE_LIMIT

        while more_pages:
            response = self.get_page(offset=offset)

            data = response.json()
            more_pages: bool = data['data']['meta']['more']

            self.store_data(response=response)

            offset += self.PAGE_LIMIT

if __name__ == "__main__":
    token = "<insert token>"
    rest_countries = RestCountries(token)

    rest_countries.get_pages()