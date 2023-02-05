import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
import lxml
import json


def get_headers():
    headers = Headers(browser="firefox", os="win")
    return headers.generate()


response = requests.get(
    "https://spb.hh.ru/search/vacancy?text=python+django+flask&salary=&area=1&area=2&ored_clusters=true&enable_snippets=true",
    headers=get_headers(),
)

hh_page = response.text

soup = BeautifulSoup(hh_page, features="lxml")

vacancy_list = soup.find(attrs={"data-qa": "vacancy-serp__results"})
vacancies = vacancy_list.find_all(class_="serp-item")
data = []
for vacancy in vacancies:
    link_elements = vacancy.find("a", class_="serp-item__title")
    link = link_elements.attrs.get("href")
    salary_elements = vacancy.find(
        attrs={"data-qa": "vacancy-serp__vacancy-compensation"}
    )
    if salary_elements is not None:
        salary = str(salary_elements.text.strip())
    else:
        salary = "None"
    company_elements = vacancy.find("a", {"data-qa": "vacancy-serp__vacancy-employer"})
    company = company_elements.text.strip()
    address_elements = vacancy.find(attrs={"data-qa": "vacancy-serp__vacancy-address"})
    address = address_elements.text.strip()
    data.append(
        {"link": link, "salary": salary, "company": company, "address": address}
    )

with open("vacancy.json", "w", encoding="UTF-8") as file:
    json.dump(data, file, indent=4, ensure_ascii=False)
