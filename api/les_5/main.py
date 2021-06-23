import logging

import requests

from terminaltables import AsciiTable

import settings


logger = logging.getLogger(__file__)


def get_api_response(base_url, headers, payload, language, page, api_name):
    if api_name == "hh":
        payload["text"] = language
    else:
        payload["keyword"] = language
    payload["page"] = page
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
    else:
        return None


def predict_rub_salary_for_hh(vacancy):
    if vacancy["salary"] and vacancy["salary"]["currency"] == "RUR":
        return predict_salary(salary_from=vacancy["salary"]["from"], salary_to=vacancy["salary"]["to"])
    return None


def predict_rub_salary_for_sj(vacancy):
    if vacancy["currency"] == "rub":
        return predict_salary(salary_from=vacancy["payment_from"], salary_to=vacancy["payment_to"])
    return None


def get_aver_salary_metrics(vacancies, api_name):
    vacancies_processed = 0
    current_salary_sum = 0
    for vacancy in vacancies:
        if api_name == "hh":
            salary = predict_rub_salary_for_hh(vacancy=vacancy)
        else:
            salary = predict_rub_salary_for_sj(vacancy=vacancy)
        if salary:
            current_salary_sum += salary
            vacancies_processed += 1
    average_salary = int(current_salary_sum/vacancies_processed)
    return {"aver_salary": average_salary, "vac_proc": vacancies_processed}


def get_pivot_table_salaries(salaries, title):
    table_data = [["Язык программирования", "Вакансий найдено", "Вакансий обработано", "Средняя зарплата"]]
    for key, value in salaries.items():
        table_data.append([key, value["vacancies_found"], value["vacancies_processed"], value["average_salary"]])
    table = AsciiTable(table_data, title)
    return table.table


def get_salary_statistics(languages, base_url, headers, payload, pages, per_page, api_name, max_value, batch):
    salary_statistics = dict()
    for language in languages:
        page = 0
        tmp_storage_vacancies = []
        while page < pages:
            try:
                api_response = get_api_response(base_url=base_url,
                                                headers=headers,
                                                payload=payload,
                                                language=language,
                                                page=page,
                                                api_name=api_name)
                tmp_storage_vacancies.extend(api_response[batch])
            except requests.HTTPError as error:
                logger.exception(error)
            if per_page * page > api_response[max_value]:
                break
            page += 1
        aver_salary_metrics = get_aver_salary_metrics(vacancies=tmp_storage_vacancies, api_name=api_name)
        salary_statistics[language] = {"vacancies_found": api_response[max_value],
                                       "average_salary": f"{aver_salary_metrics['aver_salary']}",
                                       "vacancies_processed": f"{aver_salary_metrics['vac_proc']}"}
    return salary_statistics


def main():
    languages = ["Java", "Php", "Python", "Scala", "Swift", "Kotlin", "C++", "JavaScript", "C#"]
    pages, per_page = 20, 100
    api_names = ["hh", "sj"]
    tables = str()
    for api in api_names:
        salary_statistics = get_salary_statistics(languages,
                                                  base_url=settings.BASE_URLS[api],
                                                  headers=settings.HEADERS[api],
                                                  payload=settings.PAYLOAD[api],
                                                  pages=pages,
                                                  per_page=per_page,
                                                  api_name=api,
                                                  max_value=settings.MAX_VALUE_KEY[api],
                                                  batch=settings.BATCH_VACANCIES_KEY[api])
        tables += get_pivot_table_salaries(salary_statistics, title=settings.TABLE_TITLE[api]) + "\n"
    print(tables)


if __name__ == '__main__':
    main()
