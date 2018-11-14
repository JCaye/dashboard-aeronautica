# -*- coding: utf-8 -*-

import pandas as pd

from . import service
from flask import Blueprint, render_template

bp = Blueprint('board', __name__, url_prefix='/board')

@bp.route('/', methods=('GET',))
def serve_data():
    empresa = service.get_empresa()
    tipo_e_dano = service.get_tipo_e_dano()
    tipo_aeronave = service.get_tipo_aeronave()
    
    render_this = {
            'chart1': {
				'title':'Ocorrencias por empresa e trimestre',
				'labels': [str(date.year) + "-" + str(1 + date.month//3) + "T" for date in empresa[-16:].index],
				'values': empresa[-16:].to_dict('list')
				},
            'chart2': {
				'title': 'Ocorrências por tipo de operação e dano sofrido',
				'labels': tipo_e_dano.index,
				'values': tipo_e_dano.to_dict('list')
				},
            'chart3': {
				'title': 'Ocorrências por trimestre e dano sofrido',
				'labels': [str(date.year) + "-" + str(1 + date.month//3) + "T" for date in tipo_aeronave[-10:-1].index],
				'values': tipo_aeronave[-10:-1].to_dict('list')
				}
            }
    return render_template('board.html', render_this=render_this)