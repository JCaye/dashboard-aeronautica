import pandas as pd

from . import db
from . import model
from datetime import datetime, timedelta


def get_empresa():
    df = (pd.read_sql(db.get_session().query(model.Ocorrencia.ocorrencia_dia, model.Aeronave.aeronave_fabricante).join(model.Aeronave).statement, db.get_engine())
            .apply(lambda x: x if x.name != 'ocorrencia_dia' else pd.to_datetime(x, yearfirst=True))
            .apply(lambda x: x if x.name != 'aeronave_fabricante' else x.apply(lambda y: 'OUTROS' if y not in ['CESSNA AIRCRAFT', 'EMBRAER', 'PIPER AIRCRAFT', 'AIRBUS INDUSTRIE', 'NEIVA INDUSTRIA AERONAUTICA', 'BEECH AIRCRAFT', 'HELIBRAS', 'AERO BOERO', 'BOEING COMPANY', 'RAYTHEON AIRCRAFT', 'CIRRUS DESIGN', 'AEROSPATIALE AND ALENIA', 'EUROCOPTER FRANCE', 'DIAMOND AIRCRAFT'] else y))
            .set_index('ocorrencia_dia'))
    return (pd.get_dummies(df, prefix="", prefix_sep="")
            .resample('3M')
            .agg('sum'))

def get_tipo_operacao():
    df = (pd.read_sql(db.get_session().query(model.Ocorrencia.ocorrencia_dia, model.Aeronave.aeronave_tipo_operacao).join(model.Aeronave).statement, db.get_engine())
            .apply(lambda x: x if x.name != 'ocorrencia_dia' else pd.to_datetime(x, yearfirst=True))
            .apply(lambda x: x if x.name != 'aeronave_tipo_operacao' else x.apply(lambda y: 'OUTROS' if y not in ['VOO PRIVADO', 'VOO REGULAR', 'VOO DE INSTRUÇÃO', 'TÁXI AÉREO', 'OPERAÇÃO AGRÍCOLA', 'VOO EXPERIMENTAL'] else y))
            .set_index('ocorrencia_dia'))
    return (pd.get_dummies(df, prefix="", prefix_sep="")
            .resample('3M')
            .agg('sum'))

def get_tipo_aeronave():
     df = (pd.read_sql(db.get_session().query(model.Ocorrencia.ocorrencia_dia, model.Aeronave.aeronave_nivel_dano).join(model.Aeronave).statement, db.get_engine())
            .apply(lambda x: x if x.name != 'ocorrencia_dia' else pd.to_datetime(x, yearfirst=True))
            .apply(lambda x: x if x.name != 'aeronave_tipo_operacao' else x.apply(lambda y: 'OUTROS' if y not in ['VOO PRIVADO', 'VOO REGULAR', 'VOO DE INSTRUÇÃO', 'TÁXI AÉREO', 'OPERAÇÃO AGRÍCOLA', 'VOO EXPERIMENTAL'] else y))
            .set_index('ocorrencia_dia'))
     return (pd.get_dummies(df.loc[df.aeronave_nivel_dano != 'INDETERMINADO'], prefix="", prefix_sep="")
             .resample('3M')
             .agg('sum')
             .reindex(columns=['DESTRUÍDA', 'SUBSTANCIAL', 'LEVE', 'NENHUM']))

def get_tipo_e_dano():
    df = pd.read_sql(db.get_session().query(model.Ocorrencia.ocorrencia_dia,
                                   model.Aeronave.aeronave_nivel_dano,
                                   model.Aeronave.aeronave_tipo_operacao,
                                   model.Aeronave.codigo_ocorrencia
                                   ).join(model.Aeronave).statement, db.get_engine()
         ).apply(lambda x: x if x.name != 'ocorrencia_dia' else pd.to_datetime(x, yearfirst=True)).set_index('ocorrencia_dia')
    return (df.loc[(df.index > (datetime.today() - timedelta(days=365)))
                   & (df.aeronave_nivel_dano != 'INDETERMINADO')
                   & (df.aeronave_tipo_operacao != 'INDETERMINADA')]
             .groupby(['aeronave_tipo_operacao', 'aeronave_nivel_dano'])
             .size()
             .unstack()
             .fillna(0)
             .apply(lambda x: x/x.sum(), axis=1)
             .reindex(columns=['DESTRUÍDA', 'SUBSTANCIAL', 'LEVE', 'NENHUM']))#.reindex(columns=['DESTRUIDA', 'SUBSTANCIAL', 'LEVE', 'NENHUM']))