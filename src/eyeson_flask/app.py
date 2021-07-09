from flask import Flask, render_template, redirect, url_for
from . import forms
from flask_wtf.csrf import CSRFProtect
from flask_wtf import csrf, Form
import argparse
import calendar
import datetime
import time
import os
import requests
import json

from concurrent.futures import ThreadPoolExecutor

# never used there if we need it later
# from concurrent.futures import as_completed

# search functionality
from . import core, translators

app = Flask(__name__)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

csrf = CSRFProtect(app)
csrf.init_app(app)


@app.route('/')
def index():
    form = forms.SearchForm()
    return render_template('index.html', form=form)


@app.route('/search', methods=['GET', 'POST'])
def search():
    #form handling
    form = forms.SearchForm()
    if not form.validate_on_submit():
        return redirect(url_for('index'))

    sys_name = form.search.data
    num_kills = 5
    print(f"System specified as: {sys_name}")
    sys_id = translators.name2id(sys_name)
    closest_match = translators.id2name(sys_id)
    print(f"Closest match is {closest_match}, using that...")
    kills_dict, kill_list, hash_list = core.get_kills_dict(sys_id, int(num_kills))

    obj_list = core.create_objects(num_kills)
    filled_vic_list = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_result = executor.map(
            core.fill_in_object, obj_list, kill_list, hash_list
        )
        for future in future_result:
            filled_vic_list.append(future)

    num_gates = core.num_stargates(sys_id)

    num_jumps = core.get_jumps(sys_id)

    interactions = core.get_recent_kills(sys_id)

    return render_template('post_search.html', closest_match=closest_match, form=form, interactions=interactions, num_jumps=num_jumps, num_gates=num_gates,
                           num_kills=num_kills, filled_vic_list=filled_vic_list)


