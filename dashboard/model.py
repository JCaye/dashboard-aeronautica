# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 23:59:46 2018

@author: JulioCaye
"""

from sqlalchemy import Column, Float, ForeignKey, Integer, BigInteger, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Ocorrencia(Base):
    __tablename__ = 'ocorrencias'
    
    id = Column(Integer, primary_key=True)
    codigo_ocorrencia = Column(String)
    ocorrencia_classificacao = Column(String)
    ocorrencia_tipo = Column(String)
    ocorrencia_tipo_categoria = Column(String)
    ocorrencia_tipo_icao = Column(String)
    ocorrencia_latitude = Column(Float)
    ocorrencia_longitude = Column(Float)
    ocorrencia_cidade = Column(String)
    ocorrencia_uf = Column(String)
    ocorrencia_pais = Column(String)
    ocorrencia_aerodromo = Column(String)
    ocorrencia_dia = Column(String)
    ocorrencia_horario = Column(String)
    investigacao_aeronave_liberada = Column(String)
    investigacao_status = Column(String)
    divulgacao_relatorio_numero = Column(String)
    divulgacao_relatorio_publicado = Column(String)
    divulgacao_dia_publicacao = Column(String)
    total_recomendacoes = Column(Integer)
    total_aeronaves_envolvidas = Column(Integer)
    ocorrencia_saida_pista = Column(String)
    ocorrencia_dia_extracao = Column(String)
    

class Recomendacao(Base):
    __tablename__ = 'recomendacoes'
    
    id = Column(Integer, primary_key=True)
    codigo_ocorrencia = Column(String, ForeignKey('ocorrencias.codigo_ocorrencia'))
    recomendacao_numero = Column(String)
    recomendacao_dia_assinatura = Column(String)
    recomendacao_dia_encaminhamento = Column(String)
    recomendacao_feedback = Column(String)
    recomendacao_conteudo = Column(String)
    recomendacao_status = Column(String)
    recomendacao_destinatario_sigla = Column(String)
    recomendacao_destinatario_nome = Column(String)
    dia_extracao_recomendacao = Column(String)
    
    ocorrencias = relationship('Ocorrencia', back_populates='recomendacoes')

class Fator(Base):
    __tablename__ = 'fatores'
    
    id = Column(Integer, primary_key=True)
    codigo_ocorrencia = Column(String, ForeignKey('ocorrencias.codigo_ocorrencia'))
    fator_nome = Column(String)
    fator_aspecto = Column(String)
    fator_condicionante = Column(String)
    fator_area = Column(String)
    fator_detalhe_fator = Column(String)
    fator_dia_extracao = Column(String)
    
    ocorrencias = relationship('Ocorrencia', back_populates='fatores')
    
class Aeronave(Base):
    __tablename__ = 'aeronaves'
    
    id = Column(Integer, primary_key=True)
    codigo_ocorrencia = Column(String, ForeignKey('ocorrencias.codigo_ocorrencia'))
    aeronave_matricula = Column(String)
    aeronave_operador_categoria = Column(String)
    aeronave_tipo_veiculo = Column(String)
    aeronave_fabricante = Column(String)
    aeronave_modelo = Column(String)
    aeronave_tipo_icao = Column(String)
    aeronave_motor_tipo = Column(String)
    aeronave_motor_quantidade = Column(String)
    aeronave_pmd = Column(Integer)
    aeronave_pmd_categoria = Column(String)
    aeronave_assentos = Column(Integer)
    aeronave_ano_fabricacao = Column(Integer)
    aeronave_pais_fabricante = Column(String)
    aeronave_pais_registro = Column(String)
    aeronave_registro_categoria = Column(String)
    aeronave_registro_segmento = Column(String)
    aeronave_voo_origem = Column(String)
    aeronave_voo_destino = Column(String)
    aeronave_fase_operacao = Column(String)
    aeronave_fase_operacao_icao = Column(String)
    aeronave_tipo_operacao = Column(String)
    aeronave_nivel_dano = Column(String)
    total_fatalidades = Column(Integer)
    aeronave_dia_extracao = Column(String)
    
    ocorrencias = relationship('Ocorrencia', back_populates='aeronaves')

Ocorrencia.recomendacoes = relationship('Recomendacao', order_by=Recomendacao.id, back_populates='ocorrencias')
Ocorrencia.aeronaves = relationship('Aeronave', order_by=Aeronave.id, back_populates='ocorrencias')
Ocorrencia.fatores = relationship('Fator', order_by=Fator.id, back_populates='ocorrencias')