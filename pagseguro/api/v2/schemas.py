# -*- coding: utf-8 -*-
from pagseguro.validators import Email, PhoneArea, PhoneNumber, BrState
from voluptuous import Schema, Required, All, Length, Range, Optional, Match, \
    Any

item_schema = Schema({
    Required('item_id'): All(unicode, Length(min=1, max=100)),
    Required('description'): All(unicode, Length(min=1, max=100)),
    Required('amount'): All(float, Range(min=0.01, max=9999999)),
    Required('quantity'): All(int, Range(min=1, max=999)),
    Optional('weight'): All(int, Range(max=30000)),
})

#: .. todo:: Validar born_date e CPF
client_schema = Schema({
    'name': unicode,
    'email': All(Email(), Length(max=60)),
    'phone_area_code': All(PhoneArea(), Length(min=2, max=2)),
    'phone_number': All(PhoneNumber(), Length(min=7, max=9)),
    'cpf': All(Match('[\d]{11}', msg='CPF invalido. Informe um numero com 11 digitos'), Length(min=11, max=11)),
    'born_date': str 
})

shipping_schema = Schema({
    'type': Any(1, 2, 3),
    'cost': All(float, Range(min=0.01, max=9999999)),
    'street': All(unicode, Length(max=80)),
    'number': All(unicode, Length(max=20)),
    'complement': All(unicode, Length(max=40)),
    'district': All(unicode, Length(max=60)),
    'postal_code': All(Match('[\d]{8,8}', msg=u'PostalCode invalido. Informe um numero com oito digitos'), 
                         Length(min=8, max=8)),
    'city': All(unicode, Length(min=2, max=60)),
    'state': All(BrState(), Length(min=2, max=2)),
    'country': 'BRA',
})
