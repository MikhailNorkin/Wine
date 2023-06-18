from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import pandas

excel_data_df1 = pandas.read_excel('wine.xlsx',sheet_name='Лист1')
name_wine = excel_data_df1['Название'].tolist()
excel_data_df2 = pandas.read_excel('wine2.xlsx')
kat_wine = list(set(excel_data_df2['Категория'].tolist()))
# excel_data_df3 = pandas.read_excel('wine2.xlsx', sheet_name='Лист1', usecols=['Категория', 'Название'])
excel_data_df = pandas.read_excel('wine2.xlsx', sheet_name='Лист1')
df = excel_data_df.to_dict(orient='record')
for i in kat_wine:
    print(i)
    for j in df:
        if j['Категория'] == i:
            print(j)

# print(excel_data_df3)


# rec = excel_data_df3.to_dict(orient='record')
# print(rec)
# for i in excel_data_df3:
#     print([i])


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
    name_wine = name_wine
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()


# from http.server import HTTPServer, SimpleHTTPRequestHandler


# server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
# server.serve_forever()