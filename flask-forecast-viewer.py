import zipfile
from datetime import datetime as dt, timedelta

from flask import Flask, render_template

app = Flask(__name__)

def create_select(options, selected=0):
    action = 'window.location.href=this.value'
    options = '\n'.join([f'<option value={v}>{v}</option>' for v in options])
    return f'<select name="colour" method="GET" action="/" onchange=\'{action}\'>{options}</select>'


def create_img(field):
    return field


def tag(the_tag, txt, attributes=''):
    return '<{tag}{attributes}>{txt}</{tag}>'.format(tag=the_tag, txt=txt,
           attributes=(('' if attributes == '' else ' ') + attributes))


def read_zip():
    first_date = (dt.now() - timedelta(days=14)).strftime('%Y%m%d%H%M%S')
    zip_name = r"resources/forecasts.zip"
    forecasts = zipfile.ZipFile(zip_name, 'r')
    return ''.join([tag('tr',tag('td', file)) for file in forecasts.namelist()
                    if file > f'forecasts_{first_date}.json'])

def insert_css():
    return open('static/style.css').read()


@app.route('/')
def index():
    chart_select = create_select(range(20))
    return render_template('index.html', chart_select=chart_select)

@app.route('/<field>')
def pick_chart(field):
    chart_select = create_select(range(20))
    img_source = create_img(field)
    zip_files = read_zip()
    css = insert_css()
    return render_template('chart.html', chart_select=chart_select,
                           img_source=img_source, zip_files=zip_files, css=css)

