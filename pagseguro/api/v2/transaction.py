# -*- coding: utf-8 -*-
'''
Created on Nov 17, 2013

@author: Ricardo Silva
'''
from pagseguro.validators import PhoneArea, PhoneNumber, BrState
from voluptuous import Schema, Required, All, Length, Coerce, Range, Optional, \
    Any

TRANSACTION_TYPE_PAGAMENTO = 1

TRANSACTION_TYPES = {
    TRANSACTION_TYPE_PAGAMENTO: u'Pagamento',
}

STATUS_AGUARDANDO_PAGAMENTO = 1
STATUS_EM_ANALISE = 2
STATUS_PAGA = 3
STATUS_DISPONIVEL = 4
STATUS_EM_DISPUTA = 5
STATUS_DEVOLVIDA = 6
STATUS_CANCELADA = 7

STATUS = {
  STATUS_AGUARDANDO_PAGAMENTO: u'Aguardando Pagamento',
  STATUS_EM_ANALISE: u'Em Análise',
  STATUS_PAGA: u'Paga',
  STATUS_DISPONIVEL: u'Disponível',
  STATUS_EM_DISPUTA: u'Em Disputa',
  STATUS_DEVOLVIDA: u'Devolvida',
  STATUS_CANCELADA: u'Cancelada',
}

PAYMENT_TYPE_CARTAO_CREDITO = 1
PAYMENT_TYPE_BOLETO = 2
PAYMENT_TYPE_TEF = 3
PAYMENT_TYPE_SALDO_PAGSEGURO = 4
PAYMENT_TYPE_OI_PAGGO = 5
PAYMENT_TYPE_DEPOSITO_EM_CONTA = 7

PAYMENT_TYPES = {
    PAYMENT_TYPE_CARTAO_CREDITO: u'Cartão de Crédito',
    PAYMENT_TYPE_BOLETO: u'Boleto',
    PAYMENT_TYPE_TEF: u'Débito online (TEF)',
    PAYMENT_TYPE_SALDO_PAGSEGURO: u'Saldo PagSeguro',
    PAYMENT_TYPE_OI_PAGGO: u'Oi Paggo',
    PAYMENT_TYPE_DEPOSITO_EM_CONTA: u'Depósito em Conta'
}


# Validador do dicionário construido com base no XML de notificação do PagSeguro
transaction_schema = Schema({
    Required('transaction'):  {
        Required('date'): unicode, #TODO: Validar
        Required('code'): All(unicode, Length(min=36, max=36)),
        'reference': All(unicode, Length(min=0, max=200)),
        Required('type'): Coerce(int),
        Required('status'): All(Coerce(int), Range(min=1,max=7)),
        'cancellationSource': ('INTERNAL', 'EXTERNAL'),
        Required('lastEventDate'): unicode, # TODO: Validar
        Required('paymentMethod'): {
            Required('type'): Coerce(int),
            Required('code'): Coerce(int),
        },
        Required('grossAmount'): Coerce(float),
        Required('discountAmount'): Coerce(float),
        Required('feeAmount'): Coerce(float),
        Required('netAmount'): Coerce(float),
        'escrowEndDate': unicode, # TODO: Validar
        Required('extraAmount'): Coerce(float),
        Required('installmentCount'): Coerce(int),
        Required('itemCount'): Coerce(int),
        Required('items'): {
            Required('item'): Any([{
                Required('id'): unicode,
                Required('description'): unicode,
                Required('amount'): Coerce(float),
                Required('quantity'): All(Coerce(int), Range(min=1, max=999))
            }], {
                Required('id'): unicode,
                Required('description'): unicode,
                Required('amount'): Coerce(float),
                Required('quantity'): All(Coerce(int), Range(min=1, max=999))
            }),
        },
        Required('sender'): {
            Required('email'): All(unicode, Length(max=60)),
            'name': All(unicode, Length(min=0, max=50)),
            'phone': {
                'areaCode': PhoneArea(),
                'number': PhoneNumber()
            }
        },
        Required('shipping'): {
            Required('type'): All(Coerce(int), Range(min=1, max=3)),
            'cost': Coerce(float),
            'address': {
                'country': 'BRA',
                'state': BrState(),
                'city': unicode,
                Optional('postalCode'): All(Coerce(int), Range(max=99999999)),
                Optional('district'): Any(unicode, None),
                Optional('street'): Any(unicode, None),
                Optional('number'): Any(unicode, None),
                Optional('complement'): Any(unicode, None), 
            }
        }
    }
}, extra=True)
