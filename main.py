from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import URLField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_bootstrap import Bootstrap
import requests
from bs4 import BeautifulSoup


class Form(FlaskForm):
    url = URLField('URL', validators=[URL(), DataRequired()])
    submit = SubmitField()

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

@app.route('/', methods = ['POST', 'GET'])
def home():
    form = Form()
    if form.validate_on_submit():
        hrefs = []
        html_data = requests.get(form.url.data).text
        soup = BeautifulSoup(html_data, 'html.parser')
        for x in soup.find_all('a'):
            a = x.get('href')
            if a and a[0] == 'h':
                hrefs.append(a)
        form.url.data = ''
        return render_template('index.html', form=form, all_href=hrefs)
    return render_template('index.html', form=form)

app.run(debug=True)