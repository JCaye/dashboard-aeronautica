import pandas as pd

from db import get_engine, get_session
from model import Ocorrencia, Recomendacao, Fator, Aeronave

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

def get_tipo_dano():
     df = (pd.read_sql(get_session().query(Ocorrencia.ocorrencia_dia, Aeronave.aeronave_nivel_dano).join(Aeronave).statement, get_engine())
            .apply(lambda x: x if x.name != 'ocorrencia_dia' else pd.to_datetime(x, yearfirst=True))
            .apply(lambda x: x if x.name != 'aeronave_tipo_operacao' else x.apply(lambda y: 'OUTROS' if y not in ['VOO PRIVADO', 'VOO REGULAR', 'VOO DE INSTRUÇÃO', 'TÁXI AÉREO', 'OPERAÇÃO AGRÍCOLA', 'VOO EXPERIMENTAL'] else y))
            .set_index('ocorrencia_dia'))
     return (pd.get_dummies(df, prefix="", prefix_sep="")
             .resample('3M')
             .agg('sum'))