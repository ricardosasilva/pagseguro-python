# -*- coding: utf-8 -*-
from pagseguro.api.v2.payment import Payment as PaymentV2


class Payment(object):
    '''
    Esta é a classe principal do PagSeguro-Python. Todo o processo de pagamento é
    realizado através dela. 
    
    O mínimo necessário para fazer uma solicitação de pagamento é: 

    - Criar uma instância de Payment passando o seu email e token.
    - Adicionar um ou mais itens.
    - Chamar o método request()
    - Ler o atributo payment_url para obter a URL para a qual o comprador deve
      ser redirecionado 

    Mas é possível também definir outros atributos:
    
    .. autofunction:: pagseguro.api.v2.payment.Payment

    Exemplos:

        >>> payment = Payment(email=local_settings.PAGSEGURO_ACCOUNT_EMAIL, token=local_settings.PAGSEGURO_TOKEN, sandbox=True)
        >>> payment.add_item(item_id=u'id-do-item-1', description=u'Desc. do produto', amount=7, quantity=2)
        >>> payment.add_item(item_id=u'id-do-item-2', description=u'Um outro produto', amount=24.1, quantity=2)
        >>> payment.set_client(name=u'Adam Yauch', phone_area_code=11, phone_number=12341234, cpf='93537621701')
        >>> payment.set_shipping(cost=1.2)
        >>> payment.request()
        >>> url = payment.payment_url
    
    '''

    @staticmethod
    def _payment_factory(version=2, **kwargs):
        if version == 2:
            return PaymentV2(**kwargs)
        else:
            raise NotImplementedError()

    def __init__(self, **kwargs):
        self._payment = self._payment_factory(**kwargs)

    def add_item(self, *args, **kwargs):
        '''
        Método proxy para a classe que implementa o método add_item na
        versão da API escolhida
        '''
        return self._payment.add_item(*args, **kwargs)

    def set_client(self, *args, **kwargs):
        '''
        Método proxy para a classe que implementa o método set_client na
        versão da API escolhida

        Exemplo:
        >>> payment = Payment(email=local_settings.PAGSEGURO_ACCOUNT_EMAIL, token=local_settings.PAGSEGURO_TOKEN, sandbox=True)
        >>> payment.set_client(name=u'Adam Yauch', phone_area_code=11)

        '''
        return self._payment.set_client(*args, **kwargs)

    def set_shipping(self, *args, **kwargs):
        '''
        Método proxy para a classe que implementa o método set_shipping na
        versão da API escolhida
        '''
        return self._payment.set_shipping(*args, **kwargs)

    def request(self):
        ''' Método proxy para a classe que implementa o método request na
        versão da API escolhida

        :returns: PaymentResponse object
        '''
        return self._payment.request()

    @property
    def response(self):
        ''' Objeto com resposta à requisição '''
        return self._payment.response

    @property
    def payment_url(self):
        ''' URL para redirecionar o usuário para completar o pagamento '''
        return self._payment.payment_url()
