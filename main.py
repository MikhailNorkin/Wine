from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import pandas
import collections
import argparse
import sys


def get_time_name(time_years):
    if (time_years % 100 >= 12) and (time_years % 100 <= 14):
        time_word = "лет"
    elif time_years % 10 == 1:
        time_word = "год"
    elif (time_years % 10 >= 2) and (time_years % 10 <= 4):
        time_word = "года"    
    else:
        time_word = "лет"
    return time_word


def get_data_from_excel(name_excel):
    excel_data_df = pandas.read_excel(name_excel, sheet_name='Лист1',na_values=['N/A', 'NA'], keep_default_na=False)
    excel_data = excel_data_df.to_dict('record')
    category_wines = collections.defaultdict(list)
    for i in excel_data:
        category_wines[i['Категория']].append(i)
    return category_wines


def main():
    parser = argparse.ArgumentParser(
        description='Введите путь к файлу excel'
    )
    parser.add_argument('name', help='Путь к файлу')
    args = parser.parse_args()

    name_excel = args.name
    try:
        excel_wine = pandas.read_excel(name_excel,sheet_name='Лист1')
        name_wines = excel_wine['Название'].tolist()
    except IOError:
        print('Вы ввели неверное имя файла. Запустите программу заново')    
        sys.exit()

    category_wines = get_data_from_excel(name_excel)

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    event1 = datetime.datetime.now().year
    time_years = event1-1902

    time_word = get_time_name(time_years)

    rendered_page = template.render(
        time_years = time_years,
        time_word = time_word,
        name_wine = name_wines,
        list_wine = category_wines
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()