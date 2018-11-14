# -*- coding: utf-8 -*-
"""
Created on Wed Nov  7 20:08:02 2018

@author: JulioCaye
"""

import click
import pandas as pd

from . import model

from flask import g
from flask.cli import with_appcontext
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def get_engine():
    if 'engine' not in g:
        g.engine = create_engine('sqlite:///./dashboard/registro.db')
    return g.engine

def get_session():
    if 'session' not in g:
        g.session = (sessionmaker(bind = get_engine()))()
    return g.session

def close_session(e=None):
    session = g.pop('session', None)

    if session is not None:
        session.close()