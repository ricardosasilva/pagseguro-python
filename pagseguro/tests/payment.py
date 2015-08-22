# -*- coding: utf-8 -*-
from pagseguro import Payment
from pagseguro.exceptions import PagSeguroApiException
from unittest.case import TestCase
from voluptuous import MultipleInvalid


class PaymentTest(TestCase):

    def setUp(self):
        self.payment = Payment(email='vendedor@domain.tld', token='seutokendeaacessocom32caracteres', version=2)

    def test_request(self):
        self.payment.add_item(item_id=u'id-do-item-1', description=u'Desc. do produto', amount=7, quantity=2)
        self.payment.add_item(item_id=u'id-do-item-2', description=u'Um outro produto', amount=24.1, quantity=2)
        self.payment.set_client(name=u'Adam Yauch', phone_area_code=11, phone_number=12341234, cpf='93537621701')
        self.payment.set_shipping(cost=1.2)
        self.assertRaisesRegexp(PagSeguroApiException, 'Erro ao fazer request para a API: HTTP Status=401 - Response: Unauthorized', self.payment.request)

    def test_client_phone_area_code(self):
        self.payment.set_client(phone_area_code='11')
        self.assertRaises(MultipleInvalid, self.payment.set_client, phone_area_code=3)

    def test_client_phone_number(self):
        self.payment.set_client(phone_number='12341234')
        self.assertRaises(MultipleInvalid, self.payment.set_client, phone_number=3)

    def test_client_email(self):
        self.payment.set_client(email='email-valido@dominio.tld')
        self.assertRaises(MultipleInvalid, self.payment.set_client, email='invalido')

    def test_shipping(self):
        self.payment.set_shipping(state='SP', district=u'São Paulo', street=u'Baker Street', number=u'19')
        self.assertRaisesRegexp(PagSeguroApiException, 'Erro ao fazer request para a API: HTTP Status=401 - Response: Unauthorized', self.payment.request)
        self.assertRaises(MultipleInvalid, self.payment.set_shipping, state='aa')
        self.assertRaises(MultipleInvalid, self.payment.set_shipping, district='1234567890123456789012345678901234567890123456789012345678901')
