from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

from initial import create_app

app = create_app()

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404/index.html'), 404

@app.errorhandler(500)
def something_go_wrong(e):
    return render_template('500/index.html'), 500

if __name__ == '__main__':
   app.run(debug = True, port = 80)