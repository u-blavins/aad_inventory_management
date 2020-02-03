from flask import Blueprint, request, render_template, redirect, session, url_for
from utils import Database
from models import User

users = Blueprint('users', __name__)

@user.route('/users/user/{id}')
def get_user(id):
