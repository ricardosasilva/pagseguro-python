.. _pagseguro_python-desenvolvimento:

===============
Desenvolvimento
===============

Testes
------

  Você pode executar os testes com o Nose::

    $ nosetests --with-doctest --with-coverage

.. note::
	
  	Os testes que estão sendo executados no `coveralls.io`_ não estão executando DocTests. 
  	Como o PagSeguro não possui ambiente de testes seria preciso deixar publicos algum
  	email e token válidos. Por isso os testes que necessitam de autenticação foram
  	implementados como DocTests. Eles serão executados no seu ambiente com o comando
  	acima. 

.. _coveralls.io: https://coveralls.io/r/ricardosasilva/pagseguro-python

Sobre a Documentação do projeto
-------------------------------

  Esta documentação foi gerada utilizando o `Sphinx`_ e publicada no `Read the Docs`_ .
  Qualquer ajuda em mante-la é muito bem vinda ;)
  
  Os arquivos fontes ficam no diretório docs/source e possuem a extensão
  .rst. Você pode gerar uma versão local da documentação em HTML com o comando::

    $ cd docs
    $ make html

  Depois disso você pode navegar pela documentação abrindo o arquivo que foi
  criado em docs/build/html/index.html

.. _Sphinx: http://sphinx-doc.org/tutorial.html
.. _Read the Docs: http://readthedocs.org
