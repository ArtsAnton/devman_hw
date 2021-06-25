import os
import sys
import logging

import requests

from dotenv import load_dotenv
from terminaltables import AsciiTable


logger = logging.getLogger(__file__)


def get_api_response(base_url, headers, payload):
    response = requests.get(base_url, headers=headers, params=payload)
    response.raise_for_status()
    return response.json()


def predict_salary(salary_from, salary_to):
    if salary_from and salary_to:
        return (salary_from + salary_to) / 2
    elif salary_from:
        return salary_from * 1.2
    elif salary_to:
        return salary_to * 0.8
    return None


def predict_rub_salary_for_hh(vacancy):
    if vacancy["salary"] and vacancy["salary"]["currency"] == "RUR":
        return predict_salary(salary_from=vacancy["salary"]["from"], salary_to=vacancy["salary"]["to"])
    return None


def predict_rub_salary_for_sj(vacancy):
    if vacancy["currency"] == "rub":
        return predict_salary(salary_from=vacancy["payment_from"], salary_to=vacancy["payment_to"])
    return None


def get_aver_salary_metrics(vacancies, predict_rub_salary):
    vacancies_processed = 0
    current_salary_sum = 0
    for vacancy in vacancies:
        salary = predict_rub_salary(vacancy=vacancy)
        if salary:
            current_salary_sum += salary
            vacancies_processed += 1
    if vacancies_processed != 0:
        average_salary = int(current_salary_sum/vacancies_processed)
    else:
        average_salary = 0
    return {"aver_salary": average_salary, "vac_proc": vacancies_processed}


def get_pivot_table_salaries(salaries, title):
    table_data = [["Язык программирования", "Вакансий найдено", "Вакансий обработано", "Средняя зарплата"]]
    for key, value in salaries.items():
        table_data.append([key, value["vacancies_found"], value["vacancies_processed"], value["average_salary"]])
    table = AsciiTable(table_data, title)
    return table.table


def get_salary_statistics_hh(base_url, headers, payload, pages, per_page, api_func):
    page = 0
    tmp_storage_vacancies = []
    while page < pages:
        payload["page"] = page
        api_response = get_api_response(base_url=base_url,
                                        headers=headers,
                                        payload=payload)
        tmp_storage_vacancies.extend(api_response["items"])
        if per_page * page > api_response["found"]:
            break
        page += 1
    aver_salary_metrics = get_aver_salary_metrics(tmp_storage_vacancies, api_func)
    salary_statistics = {"vacancies_found": api_response["found"],
                         "average_salary": f"{aver_salary_metrics['aver_salary']}",
                         "vacancies_processed": f"{aver_salary_metrics['vac_proc']}"}
    return salary_statistics


def get_salary_statistics_sj(base_url, headers, payload, pages, per_page, api_func):
    page = 0
    tmp_storage_vacancies = []
    while page < pages:
        api_response = get_api_response(base_url=base_url,
                                        headers=headers,
                                        payload=payload)
        tmp_storage_vacancies.extend(api_response["objects"])
        if per_page * page > api_response["total"]:
            break
        page += 1
    aver_salary_metrics = get_aver_salary_metrics(tmp_storage_vacancies, api_func)
    salary_statistics = {"vacancies_found": api_response["total"],
                         "average_salary": f"{aver_salary_metrics['aver_salary']}",
                         "vacancies_processed": f"{aver_salary_metrics['vac_proc']}"}
    return salary_statistics


def main():
    load_dotenv()
    languages = ["Java", "Php", "Python", "Scala", "Swift", "Kotlin", "C++", "JavaScript", "C#"]
    pages, per_page = 20, 100
    hh = {"base_urls": "https://api.hh.ru/vacancies/",
          "payload": {"specialization": "1.221",
                      "page": "0",
                      "per_page": "100",
                      "area": "1",
                      "period": "30",
                      "text": "language"},
          "headers": {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                    "Chrome/80.0.3987.163 Safari/537.36"},
          "title": "HeadHunter Moscow"
          }
    sj = {"base_urls": "https://api.superjob.ru/2.0/vacancies/",
          "payload": {"catalogues": "48",
                      "town": "4",
                      "period": "1",
                      "page": "0",
                      "count": "100",
                      "keyword": "language"},
          "headers": {"X-Api-App-Id": os.getenv("SECRET_KEY")},
          "title": "SuperJob Moscow"
          }

    salary_statistics_hh, salary_statistics_sj = dict(), dict()
    for language in languages:
        hh["payload"]["text"], sj["payload"]["keyword"] = language, language
        try:
            salary_statistics_hh[language] = get_salary_statistics_hh(base_url=hh["base_urls"],
                                                                      headers=hh["headers"],
                                                                      payload=hh["payload"],
                                                                      pages=pages,
                                                                      per_page=per_page,
                                                                      api_func=predict_rub_salary_for_hh)

            salary_statistics_sj[language] = get_salary_statistics_sj(base_url=sj["base_urls"],
                                                                      headers=sj["headers"],
                                                                      payload=sj["payload"],
                                                                      pages=pages,
                                                                      per_page=per_page,
                                                                      api_func=predict_rub_salary_for_sj)
        except requests.HTTPError as error:
            logger.exception(error)
    tables = get_pivot_table_salaries(salary_statistics_hh, title=hh["title"]) + "\n" + \
             get_pivot_table_salaries(salary_statistics_sj, title=sj["title"])
    print(tables)


if __name__ == '__main__':
    main()
