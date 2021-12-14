# BlogWeb
A Social Blogging Application by Multilevel Association team with python
# Initial setup
### install virtual environment
***install virtualenv lib***
```
pip install virtualenv
python -m venv Fakebook
```
***create Fakebook virtual environment***
```
python -m venv Fakebook
```
***enter virtual environment***
```
Fakebook\Scripts\activate
```
***install dependencies***
```
pip install Flask
pip install flask_sqlalchemy
pip install flask_login     
pip install werkzeug
```
**First Run will create a new database**
```
python wsgi.py
```