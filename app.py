from flask import Flask, render_template, request, redirect, session, url_for
from view import main

app = Flask(__name__)
app.register_blueprint(main)

if __name__ ==('__main__'):
    app.run(debug=True)