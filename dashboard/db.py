# -*- coding: utf-8 -*-
"""
Created on Wed Nov  7 20:08:02 2018

@author: JulioCaye
"""

import click
import pandas as pd

from flask import current_app, g
from flask.cli import with_appcontext
from .model import Ocorrencia, Recomendacao, Fator, Aeronave, Base
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

def init_db():
    engine = get_engine()
    Base.metadata.create_all(engine)
    s = get_session()
    
    data_oco = pd.read_csv('oco.csv', sep='~')
    data_rec = pd.read_csv('rec.csv', sep='~')
    data_anv = pd.read_csv('anv.csv', sep='~')
    data_ftc = pd.read_csv('ftc.csv', sep='~')
    
    data_oco['codigo_ocorrencia'] = data_oco['codigo_ocorrencia'].apply(lambda x: str(x))
    
    data_rec['codigo_ocorrencia'] = data_rec['codigo_ocorrencia'].apply(lambda x: str(x))
    data_anv['codigo_ocorrencia'] = data_anv['codigo_ocorrencia'].apply(lambda x: str(x))
    data_ftc['codigo_ocorrencia'] = data_ftc['codigo_ocorrencia'].apply(lambda x: str(x))
    
    data_oco['recomendacoes'] = (data_oco['codigo_ocorrencia']
                                    .apply(lambda codigo:
                                        list(data_rec[data_rec['codigo_ocorrencia'] == codigo]
                                            .apply(lambda row:
                                                Recomendacao(**row.to_dict()), axis = 1))))
    data_oco['fatores'] = (data_oco['codigo_ocorrencia']
                                    .apply(lambda codigo:
                                        list(data_ftc[data_ftc['codigo_ocorrencia'] == codigo]
                                            .apply(lambda row:
                                                Fator(**row.to_dict()), axis = 1))))
    data_oco['aeronaves'] = (data_oco['codigo_ocorrencia']
                                    .apply(lambda codigo:
                                        list(data_anv[data_anv['codigo_ocorrencia'] == codigo]
                                            .apply(lambda row:
                                                Aeronave(**row.to_dict()), axis = 1))))
    
    
    
    [s.add(Ocorrencia(**data_oco.iloc[i].to_dict())) for i in range(data_oco.shape[0])]
    s.commit()
    close_session()

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_session)
    app.cli.add_command(init_db_command)