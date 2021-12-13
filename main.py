from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

from initial import create_app

app = create_app()

if __name__ == '__main__':
   app.run(debug = True, port = 80)