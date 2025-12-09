from flask import Blueprint, url_for, request, redirect, abort, render_template, make_response, session
import datetime
lab7 = Blueprint('lab7', __name__)

@lab7.route("/lab7/")
def main():
    return render_template('lab7/index.html')