# -*- coding: utf-8 -*-
"""
Created on Wed Nov  7 20:35:14 2018

@author: JulioCaye
"""

import pandas as pd
import dbService

from flask import Blueprint, render_template


bp = Blueprint('board', __name__, url_prefix='/board')

@bp.route('/', methods=('GET',))
def serve_data():
    empresa = dbService.get_empresa()
    tipo_operacao = dbService.get_tipo_operacao()
    tipo_aeronave = dbService.get_tipo_aeronave()
    
    render_this = {
            'chart1': {'title': 'Ocorrencias por empresa no ultimo ano', 'labels': [str(date.year) + "-" + str(1 + date.month//3) + "T" for date in empresa[-16:].index], 'values': empresa[-16:].to_dict('list')},
            'chart2': {'title': 'Total de ocorrencias (eixo esquerdo) e proporcao por tipo de voo (eixo direito)', 'labels': [str(date.year) + "-" + str(1 + date.month//3) + "T" for date in tipo_operacao[-16:].index], 'values': tipo_operacao[-16:].to_dict('list')},
            'chart3': {'title': '180', 'labels': [str(date.year) + "-" + str(1 + date.month//3) + "T" for date in tipo_aeronave[-16:].index], 'values': tipo_aeronave[-16:].to_dict('list')}
            }
    return render_template('board.html', render_this=render_this)