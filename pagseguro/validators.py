# -*- coding: utf-8 -*-
from voluptuous import Invalid
import re


def Email(msg=None):
    '''
    Valida endereços de email
    '''
    def f(v):
        if re.match("[\w\.\-]*@[\w\.\-]*\.\w+", str(v)):
            return str(v)
        else:
            raise Invalid(msg or ("Endereco de email invalido"))
    return f


def PhoneArea(msg=None):

    def f(v):
        if re.match("[\d]{2}", str(v)):
            return str(v)
        else:
            raise Invalid(msg or ("Codigo de area de telefone invalido"))
    return f


def PhoneNumber(msg=None):

    def f(v):
        if re.match("[\d]{7,9}", str(v)):
            return str(v)
        else:
            raise Invalid(msg or ("Numero de telefone invalido"))
    return f


def BrState(msg=None):
    def f(v):
        if str(v).upper() in ('AC',
                              'AL',
                              'AP',
                              'AM',
                              'BA',
                              'CE',
                              'DF',
                              'ES',
                              'GO',
                              'MA',
                              'MT',
                              'MS',
                              'MG',
                              'PA',
                              'PB',
                              'PR',
                              'PE',
                              'PI',
                              'RJ',
                              'RN',
                              'RS',
                              'RO',
                              'RR',
                              'SC',
                              'SP',
                              'SE',
                              'TO'):
            return str(v).upper()
        else:
            raise Invalid(msg or(
                u'State invalido. Informe a sigla de um estado brasileiro'))
    return f
