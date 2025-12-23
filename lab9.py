from flask import Blueprint, url_for, request, redirect, abort, render_template, make_response, session, current_app, jsonify


lab9 = Blueprint('lab9', __name__)


@lab9.route("/lab9/")
def main():
    return render_template('lab9/index.html')