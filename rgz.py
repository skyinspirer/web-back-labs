from flask import Blueprint, url_for, request, redirect, abort, render_template, make_response, session, current_app, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash
from os import path
from db import db
from db.models import users, articles
from flask_login import login_user, login_required, current_user, logout_user
from sqlalchemy import or_

rgz = Blueprint('rgz', __name__)


@rgz.route("/rgz/")
def rgz():
    return render_template('rgz/rgz.html')