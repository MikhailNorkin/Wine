from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import pandas
import collections
from pprint import pprint

excel_wine = pandas.read_excel('wine.xlsx',sheet_name='Лист1')
name_wine = excel_wine['Название'].tolist()

excel_kat = pandas.read_excel('wine3.xlsx')
kat_wine = list(set(excel_kat['Категория'].tolist()))
excel_data_df = pandas.read_excel('wine3.xlsx', sheet_name='Лист1',na_values=['N/A', 'NA'], keep_default_na=False)
data_shot = excel_data_df.to_dict(orient='record')
dict_of_lists = collections.defaultdict(list)

for i in data_shot:
    dict_of_lists[i['Категория']].append(i)

pprint(dict_of_lists)

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

event1 = datetime.datetime.now().year
time_years = event1-1902

if time_years % 10 == 1:
    time_word = "год"
elif (time_years % 10 >= 2) and (time_years % 10 <= 4):
    time_word = "года"    
else:
    time_word = "лет"

rendered_page = template.render(
    time_years = time_years,
    time_word = time_word,
    name_wine = name_wine,
    list_wine = dict_of_lists
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()