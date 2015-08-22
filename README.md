# PagSeguro-Python


[![Build Status](https://api.travis-ci.org/ricardosasilva/pagseguro-python.png)](https://travis-ci.org/ricardosasilva/pagseguro-python) [![Coverage Status](https://coveralls.io/repos/ricardosasilva/pagseguro-python/badge.png?branch=master)](https://coveralls.io/r/ricardosasilva/pagseguro-python?branch=master)

## O que é ?

Uma biblioteca Python para acesso à API versão 2.0 do PagSeguro. Este projeto foi desenvolvido inicialmente para uso 
no site [Pizze.me](http://pizze.me) mas está disponível como Software Livre sobre a licença Apache 2.0. Sua ajuda para
torná-lo melhor é muito bem vinda!

## Guia rápido

Para os impacientes:

```python
>>> from pagseguro import Payment
>>> pagamento = Payment(email=u'emaildasuaconta@dominio.tld', token='seutokendeaacessocom32caracteres')
>>> pagamento.add_item(item_id=u'id-do-item-1', description=u'Desc. do produto', amount=7, quantity=2)
>>> pagamento.set_client(name=u'Adam Yauch', phone_area_code=11, phone_number=12341234, cpf='93537621701')
>>> pagamento.set_shipping(cost=1.2)
>>> pagamento.request()
>>> url = pagamento.payment_url

```

## Instalação

Utilize a boa e velha CheeseShop:

```bash
$ pip install pagseguro-python

```

## Documentação

A documentação completa está em:
[http://pagseguro-python.readthedocs.org](http://pagseguro-python.readthedocs.org/en/latest/)

