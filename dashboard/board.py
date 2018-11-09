# -*- coding: utf-8 -*-
"""
Created on Wed Nov  7 20:35:14 2018

@author: JulioCaye
"""

import pandas as pd
import functools

from .db import get_engine, get_session
from .model import Ocorrencia, Recomendacao, Fator, Aeronave
from datetime import datetime, timedelta
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint('board', __name__, url_prefix='/board')

@bp.route('/', methods=('GET',))
def serve_data():
    empresa = get_empresa()
    tipo_operacao = get_tipo_operacao()
    tipo_aeronave = get_tipo_aeronave()
    
    render_this = {
            'chart1': {'title': 'Ocorrencias por empresa no ultimo ano', 'labels': [str(date.year) + "-" + str(1 + date.month//3) + "T" for date in empresa[-16:].index], 'values': empresa[-16:].to_dict('list')},
            'chart2': {'title': 'Total de ocorrencias (eixo esquerdo) e proporcao por tipo de voo (eixo direito)', 'labels': [str(date.year) + "-" + str(1 + date.month//3) + "T" for date in tipo_operacao[-16:].index], 'values': tipo_operacao[-16:].to_dict('list')},
            'chart3': {'title': '180', 'labels': [str(date.year) + "-" + str(1 + date.month//3) + "T" for date in tipo_aeronave[-16:].index], 'values': tipo_aeronave[-16:].to_dict('list')}
            }
    return render_template('line_chart.html', render_this=render_this)

def get_bar():
    df =(
        pd.read_sql(get_session().query(Ocorrencia.codigo_ocorrencia, Ocorrencia.ocorrencia_dia, Aeronave.aeronave_fabricante).join(Aeronave).statement, get_engine())
            .apply(lambda x: x if x.name != 'ocorrencia_dia' else pd.to_datetime(x))
            .set_index('ocorrencia_dia'))
    return (df.loc[df.index > datetime.today() - timedelta(days=180)]
            .groupby('aeronave_fabricante')
            .size()
            .sort_values(ascending=False))

def get_line():
    df =(
        pd.read_sql(get_session().query(Ocorrencia.codigo_ocorrencia, Ocorrencia.ocorrencia_dia, Aeronave.aeronave_fabricante).join(Aeronave).statement, get_engine())
            .apply(lambda x: x if x.name != 'ocorrencia_dia' else pd.to_datetime(x))
            .set_index('ocorrencia_dia'))
    bar = get_bar()
    return (pd.get_dummies(df.drop(columns='codigo_ocorrencia').loc[df.aeronave_fabricante.isin(list(bar[:5].keys())) & (df.index > datetime.today() - timedelta(days=365))],
                                  prefix="",
                                  prefix_sep="")
                .resample('M')
                .agg('sum')
                )
def get_overtime():
    return (pd.read_sql(get_session().query(Ocorrencia.codigo_ocorrencia, Ocorrencia.ocorrencia_dia).statement, get_engine())
            .apply(lambda x: x if x.name != 'ocorrencia_dia' else pd.to_datetime(x, yearfirst=True))
            .set_index('ocorrencia_dia')
            .resample('3M')
            .agg('count'))

def get_empresa():
    df = (pd.read_sql(get_session().query(Ocorrencia.ocorrencia_dia, Aeronave.aeronave_fabricante).join(Aeronave).statement, get_engine())
            .apply(lambda x: x if x.name != 'ocorrencia_dia' else pd.to_datetime(x, yearfirst=True))
            .apply(lambda x: x if x.name != 'aeronave_fabricante' else x.apply(lambda y: 'OUTROS' if y not in ['CESSNA AIRCRAFT', 'EMBRAER', 'PIPER AIRCRAFT', 'AIRBUS INDUSTRIE', 'NEIVA INDUSTRIA AERONAUTICA', 'BEECH AIRCRAFT', 'HELIBRAS', 'AERO BOERO', 'BOEING COMPANY', 'RAYTHEON AIRCRAFT', 'CIRRUS DESIGN', 'AEROSPATIALE AND ALENIA', 'EUROCOPTER FRANCE', 'DIAMOND AIRCRAFT'] else y))
            .set_index('ocorrencia_dia'))
    return (pd.get_dummies(df, prefix="", prefix_sep="")
            .resample('3M')
            .agg('sum'))

def get_tipo_operacao():
    df = (pd.read_sql(get_session().query(Ocorrencia.ocorrencia_dia, Aeronave.aeronave_tipo_operacao).join(Aeronave).statement, get_engine())
            .apply(lambda x: x if x.name != 'ocorrencia_dia' else pd.to_datetime(x, yearfirst=True))
            .apply(lambda x: x if x.name != 'aeronave_tipo_operacao' else x.apply(lambda y: 'OUTROS' if y not in ['VOO PRIVADO', 'VOO REGULAR', 'VOO DE INSTRUÇÃO', 'TÁXI AÉREO', 'OPERAÇÃO AGRÍCOLA', 'VOO EXPERIMENTAL'] else y))
            .set_index('ocorrencia_dia'))
    return (pd.get_dummies(df, prefix="", prefix_sep="")
            .resample('3M')
            .agg('sum'))

def get_tipo_aeronave():
     df = (pd.read_sql(get_session().query(Ocorrencia.ocorrencia_dia, Aeronave.aeronave_nivel_dano).join(Aeronave).statement, get_engine())
            .apply(lambda x: x if x.name != 'ocorrencia_dia' else pd.to_datetime(x, yearfirst=True))
            .apply(lambda x: x if x.name != 'aeronave_tipo_operacao' else x.apply(lambda y: 'OUTROS' if y not in ['VOO PRIVADO', 'VOO REGULAR', 'VOO DE INSTRUÇÃO', 'TÁXI AÉREO', 'OPERAÇÃO AGRÍCOLA', 'VOO EXPERIMENTAL'] else y))
            .set_index('ocorrencia_dia'))
     return (pd.get_dummies(df, prefix="", prefix_sep="")
             .resample('3M')
             .agg('sum'))