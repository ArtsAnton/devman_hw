import os
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
    average_salary = int(current_salary_sum / vacancies_processed) if vacancies_processed else 0
    return average_salary, vacancies_processed


def get_salary_statistics_table(statistics, title):
    table = [["Язык программирования", "Вакансий найдено", "Вакансий обработано", "Средняя зарплата"]]
    for language, stat in statistics.items():
        table.append([language,
                      stat["vacancies_found"],
                      stat["vacancies_processed"],
                      stat["average_salary"]])
    return AsciiTable(table, title).table


def get_salary_statistics_hh(base_url, headers, payload, pages, api_func):
    hh_payload = {**payload}
    hh_payload["page"] = 0
    tmp_storage_vacancies = []
    while hh_payload["page"] < pages:

        api_response = get_api_response(base_url=base_url,
                                        headers=headers,
                                        payload=hh_payload)
        tmp_storage_vacancies.extend(api_response["items"])
        if hh_payload["page"] == api_response["pages"]:
            break
        hh_payload["page"] += 1
    average_salary, vacancies_processed = get_aver_salary_metrics(tmp_storage_vacancies, api_func)
    salary_statistics = {"vacancies_found": api_response["found"],
                         "average_salary": average_salary,
                         "vacancies_processed": vacancies_processed}
    return salary_statistics


def get_salary_statistics_sj(base_url, headers, payload, api_func):
    sj_payload = {**payload}
    tmp_storage_vacancies = []
    sj_payload["page"] = 0
    while True:
        api_response = get_api_response(base_url=base_url,
                                        headers=headers,
                                        payload=sj_payload)
        tmp_storage_vacancies.extend(api_response["objects"])
        if not api_response["more"]:
            break
        sj_payload["page"] += 1
    average_salary, vacancies_processed = get_aver_salary_metrics(tmp_storage_vacancies, api_func)
    salary_statistics = {"vacancies_found": api_response["total"],
                         "average_salary": average_salary,
                         "vacancies_processed": vacancies_processed}
    return salary_statistics


def main():
    load_dotenv()
    languages = ["Java", "Php", "Python", "Scala", "Swift", "Kotlin", "C++", "JavaScript", "C#"]
    pages, per_page = 20, 100

    hh_url = "https://api.hh.ru/vacancies/"
    hh_profession_id = 1.221
    hh_moscow_id = 1
    hh_period = 30
    hh_payload = {"specialization": hh_profession_id,
                  "per_page": per_page,
                  "area": hh_moscow_id,
                  "period": hh_period}
    hh_headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                "Chrome/80.0.3987.163 Safari/537.36"}
    hh_title = "HeadHunter Moscow"

    sj_url = "https://api.superjob.ru/2.0/vacancies/"
    sj_profession_id = 48
    sj_moscow_id = 4
    sj_period = 0
    sj_payload = {"catalogues": sj_profession_id,
                  "town": sj_moscow_id,
                  "period": sj_period,
                  "count": per_page}
    sj_headers = {"X-Api-App-Id": os.getenv("SJ_TOKEN")}
    sj_title = "SuperJob Moscow"

    salary_statistics_hh, salary_statistics_sj = dict(), dict()
    for language in languages:
        hh_payload["text"], sj_payload["keyword"] = language, language
        try:
            salary_statistics_hh[language] = get_salary_statistics_hh(base_url=hh_url,
                                                                      headers=hh_headers,
                                                                      payload=hh_payload,
                                                                      pages=pages,
                                                                      api_func=predict_rub_salary_for_hh)

            salary_statistics_sj[language] = get_salary_statistics_sj(base_url=sj_url,
                                                                      headers=sj_headers,
                                                                      payload=sj_payload,
                                                                      api_func=predict_rub_salary_for_sj)
        except requests.HTTPError as error:
            logger.exception(error)
    tables = f"{get_salary_statistics_table(salary_statistics_hh, title=hh_title)} \n " \
             f"{get_salary_statistics_table(salary_statistics_sj, title=sj_title)}"
    print(tables)


if __name__ == '__main__':
    main()
