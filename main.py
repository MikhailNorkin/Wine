from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime

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
    time_word = time_word
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()


# from http.server import HTTPServer, SimpleHTTPRequestHandler


# server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
# server.serve_forever()