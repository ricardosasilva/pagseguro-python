# -*- coding: utf-8 -*-
from pagseguro.api.base_payment import BasePaymentRequest
from pagseguro.api.v2 import settings, settings_sandbox
from pagseguro.api.v2.schemas import item_schema, client_schema, shipping_schema
from pagseguro.exceptions import PagSeguroApiException, \
    PagSeguroPaymentException
from pagseguro.validators import Email
from voluptuous import Schema, Object, Required, All, Length, Range, Url
from xml.etree import ElementTree
import dateutil.parser
import logging
import requests

logger = logging.getLogger(__name__)


class Payment(BasePaymentRequest):
    ''' Classe que implementa a requisição à API do PagSeguro versão 2
    
    .. todo:: Adicionar suporte à metadata no checkout 

    Args:
        email (str): (obrigatório) O email da sua conta no PagSeguro
        token (str): (obrigatório) O seu token de acesso ao PagSeguro
        receiver_email (str): (opcional)
        currency (str): (opcional) A moeda a ser utilizada. Nesta versão apenas o valor BRL é aceito
            e ele é definido por padrão. Não se preocupe com este parâmetro.
        reference (str): (opcional) Um identificador para a transação. Você irá utilizar este valor 
            posteriormente para identificar as transações.
        extra_amount (float): (opcional) Um valor extra que deve ser adicionado ou subtraído ao valor
            total do pagamento.
        redirect_url (str): (opcional)  URL para a qual o comprador será redirecionado após o final
            do fluxo de pagamento. Tamanho máximo de 255 caracteres.
        notification_url (str): (opcional)  URL para a qual o PagSeguro enviará os códigos de
            notificação relacionados ao pagamento. Toda vez que houver uma mudança no status da
            transação e que demandar sua atenção, uma nova notificação será enviada para este endereço.
        max_uses (int): Determina o número máximo de vezes que o código de pagamento criado pela chamada
            à API de Pagamentos poderá ser usado. Este parâmetro pode ser usado como um controle de segurança.        
        max_age (int): (opcional) Determina o prazo (em segundos) durante o qual o código de pagamento
            criado pela chamada à API de Pagamentos poderá ser usado. Este parâmetro pode ser usado
            como um controle de segurança

    '''

    def __init__(self,
                 email,
                 token,
                 receiver_email=None,
                 currency='BRL',
                 reference=None,
                 extra_amount=None,
                 redirect_url=None,
                 notification_url=None,
                 max_uses=None,
                 max_age=None,
                 sandbox=False,
                 **kwargs):

        self.email = email
        self.token = token
        self.receiver_email = receiver_email
        self.currency = currency
        self.reference = reference

        self.extra_amount = extra_amount
        self.redirect_url = redirect_url
        self.notification_url = notification_url
        self.max_uses = max_uses
        self.max_age = max_age
        self.sandbox = sandbox
        if sandbox:
            self.PAGSEGURO_API_URL = settings_sandbox.PAGSEGURO_API_URL
            self.PAGSEGURO_PAYMENT_URL = settings_sandbox.PAGSEGURO_PAYMENT_URL
            # self.PAGSEGURO_NOTIFICATION_URL = settings_sandbox.PAGSEGURO_NOTIFICATION_URL
        else:
            self.PAGSEGURO_API_URL = settings.PAGSEGURO_API_URL
            self.PAGSEGURO_PAYMENT_URL = settings.PAGSEGURO_PAYMENT_URL
            # self.PAGSEGURO_NOTIFICATION_URL = settings.PAGSEGURO_NOTIFICATION_URL


        self.items = []
        self.client = {}
        self.shipping = {}
        self.response = None
        self.params = None

    def api_version(self):
        return u'2.0'

    def add_item(self, item_id, description, amount, quantity, shipping_cost=None, weight=None):
        item = {}
        item['item_id'] = item_id
        item['description'] = description
        item['amount'] = float(amount)
        item['quantity'] = quantity
        if shipping_cost:
            item['shipping_cost'] = shipping_cost
        if weight:
            item['weight'] = weight
        # Validar dados
        item_schema(item)
        self.items.append(item)

    def set_client(self, *args, **kwargs):
        ''' Se você possui informações cadastradas sobre o comprador você pode utilizar
        este método para enviar estas informações para o PagSeguro. É uma boa prática pois
        evita que seu cliente tenha que preencher estas informações novamente na página
        do PagSeguro.

        Args:
            name (str): (opcional) Nome do cliente
            email (str): (opcional) Email do cliente
            phone_area_code (str): (opcional) Código de área do telefone do cliente. Um número com 2 digitos.
            phone_number (str): (opcional) O número de telefone do cliente.
            cpf: (str): (opcional) Número do cpf do comprador
            born_date: (date): Data de nascimento no formato dd/MM/yyyy

        Exemplo:
            >>> from pagseguro import Payment
            >>> from pagseguro import local_settings
            >>> payment = Payment(email=local_settings.PAGSEGURO_ACCOUNT_EMAIL, token=local_settings.PAGSEGURO_TOKEN, sandbox=True)
            >>> payment.set_client(name=u'Adam  Yauch', phone_area_code=11)
        '''
        self.client = {}      
        for arg, value in kwargs.iteritems():
            if value:
                self.client[arg] = value
        client_schema(self.client)

    def set_shipping(self, *args, **kwargs):
        ''' Define os atributos do frete

        Args:
            type (int): (opcional) Tipo de frete. Os valores válidos são: 1 para 'Encomenda normal (PAC).',
                2 para 'SEDEX' e 3 para 'Tipo de frete não especificado.'
            cost (float): (opcional) Valor total do frete. Deve ser maior que 0.00 e menor ou igual a 9999999.00.
            street (str): (opcional) Nome da rua do endereço de envio do produto
            address_number: (opcional) Número do endereço de envio do produto. 
            complement: (opcional) Complemento (bloco, apartamento, etc.) do endereço de envio do produto. 
            district: (opcional) Bairro do endereço de envio do produto.
            postal_code: (opcional) CEP do endereço de envio do produto.
            city: (opcional) Cidade do endereço de envio do produto.
            state: (opcional) Estado do endereço de envio do produto.
            country: (opcional) País do endereço de envio do produto. Apenas o valor 'BRA' é aceito.
        
        '''
        self.shipping = {}
        for arg, value in kwargs.iteritems():
            self.shipping[arg] = value
        shipping_schema(self.shipping)

    def request(self):
        '''
        Faz a requisição de pagamento ao servidor do PagSeguro.
        '''
#        try:
        payment_v2_schema(self)
#        except MultipleInvalid as e:
#            raise PagSeguroPaymentValidationException(u'Erro na validação dos dados: %s' % e.msg)
        params = self._build_params()
#         logger.debug(u'Parametros da requisicao ao PagSeguro: %s' % params)
        req = requests.post(
            self.PAGSEGURO_API_URL,
            params=params,
            headers={
                'Content-Type':
                'application/x-www-form-urlencoded; charset=ISO-8859-1'
            }
        )
        if req.status_code == 200:
            self.params = params
            self.response = self._process_response_xml(req.text)
        else:
            raise PagSeguroApiException(
                u'Erro ao fazer request para a API:' +
                ' HTTP Status=%s - Response: %s' % (req.status_code, req.text))
        return

    def _build_params(self):
        ''' método que constrói o dicionario com os parametros que serão usados
        na requisição HTTP Post ao PagSeguro
        
        Returns:
            Um dicionário com os parametros definidos no objeto Payment.
        '''
        params = {}
        params['email'] = self.email
        params['token'] = self.token
        params['currency'] = self.currency

        # Atributos opcionais
        if self.receiver_email:
            params['receiver_email'] = self.receiver_email
        if self.reference:
            params['reference'] = self.reference
        if self.extra_amount:
            params['extra_amount'] = self.extra_amount
        if self.redirect_url:
            params['redirect_url'] = self.redirect_url
        if self.notification_url:
            params['notification_url'] = self.notification_url
        if self.max_uses:
            params['max_uses'] = self.max_uses
        if self.max_age:
            params['max_age'] = self.max_age

        #TODO: Incluir metadata aqui

        # Itens
        for index, item in enumerate(self.items, start=1):
            params['itemId%d' % index] = item['item_id']
            params['itemDescription%d' % index] = item['description']
            params['itemAmount%d' % index] = '%.2f' % item['amount']
            params['itemQuantity%s' % index] = item['quantity']
            if item.get('shipping_cost'):
                params['itemShippingCost%d' % index] = item['shipping_cost']
            if item.get('weight'):
                params['itemWeight%d' % index] = item['weight']

        # Sender
        if self.client.get('email'):
            params['senderEmail'] = self.client.get('email')
        if self.client.get('name'):
            params['senderName'] = ' '.join(self.client.get('name').split())
        if self.client.get('phone_area_code'):
            params['senderAreaCode'] = self.client.get('phone_area_code')
        if self.client.get('phone_number'):
            params['senderPhone'] = self.client.get('phone_number')
        if self.client.get('cpf'):
            params['senderCPF'] = self.client.get('cpf')
        if self.client.get('sender_born_date'):
            params['senderBornDate'] = self.client.get('sender_born_date')

        # Shipping
        if self.shipping.get('type'):
            params['shippingType'] = self.shipping.get('type')
        if self.shipping.get('cost'):
            params['shippingCost'] = '%.2f' % self.shipping.get('cost')
        if self.shipping.get('country'):
            params['shippingAddressCountry'] = self.shipping.get('country')
        if self.shipping.get('state'):
            params['shippingAddressState'] = self.shipping.get('state')
        if self.shipping.get('city'):
            params['shippingAddressCity'] = self.shipping.get('city')
        if self.shipping.get('postal_code'):
            params['shippingAddressPostalCode'] = self.shipping.get('postal_code')
        if self.shipping.get('district'):
            params['shippingAddressDistrict'] = self.shipping.get('district')
        if self.shipping.get('street'):
            params['shippingAddressStreet'] = self.shipping.get('street')
        if self.shipping.get('number'):
            params['shippingAddressNumber'] = self.shipping.get('number')
        if self.shipping.get('complement'):
            params['shippingAddressComplement'] = self.shipping.get('complement')

        return params

    def _process_response_xml(self, response_xml):
        '''
        Processa o xml de resposta e caso não existam erros retorna um
        dicionario com o codigo e data.

        :return: dictionary
        '''
        result = {}
        xml = ElementTree.fromstring(response_xml)
        if xml.tag == 'errors':
            logger.error(
                u'Erro no pedido de pagamento ao PagSeguro.' +
                ' O xml de resposta foi: %s' % response_xml)
            errors_message = u'Ocorreu algum problema com os dados do pagamento: '
            for error in xml.findall('error'):
                error_code = error.find('code').text
                error_message = error.find('message').text
                errors_message += u'\n (code=%s) %s' % (error_code,
                                                        error_message)
            raise PagSeguroPaymentException(errors_message)

        if xml.tag == 'checkout':
            result['code'] = xml.find('code').text

            try:
                xml_date = xml.find('date').text
                result['date'] = dateutil.parser.parse(xml_date)
            except:
                logger.exception(u'O campo date não foi encontrado ou é invalido')
                result['date'] = None
        else:
            raise PagSeguroPaymentException(
                u'Erro ao processar resposta do pagamento: tag "checkout" nao encontrada no xml de resposta')
        return result

    def payment_url(self):
        '''
        Retorna a url para onde o cliente deve ser redirecionado para
        continuar o fluxo de pagamento.

        :return: str, URL de pagamento
        '''
        if self.response:
            return u'%s?code=%s' % (self.PAGSEGURO_PAYMENT_URL, self.response['code'])
        else:
            return None


#: Schema utilizado para validar os atributos da classe Payment da versão 2 da API
#: ..todo:: Verificar porque a validação de URLs não está funcionando
payment_v2_schema = Schema(Object({
    Required('email'): All(Email(), Length(max=60)),
    'token': All(str, Length(min=32, max=32)),
    'receiver_email': All(Email(), Length(max=60)),
    'currency': 'BRL',
    'reference': All(str, Length(max=200)),
    'extra_amount': All(float, Range(min=-9999999.01, max=9999999)),
    'redirect_url': Url(),
    'notification_url':Url(),
    'max_uses': All(int, Range(min=1, max=999)),
    'max_age': All(int, Range(min=30,max=999999999)),
    'client': client_schema,
    'items': [ item_schema, ],
    'shipping' : shipping_schema,
    'response': str,
    'sandbox': bool,
    'PAGSEGURO_API_URL': str,
    'PAGSEGURO_PAYMENT_URL': str
},cls=Payment)
)
