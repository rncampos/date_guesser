Date Guesser
============

|Build Status| |Coverage| 

Adapted from `on date_guesser <https://pypi.org/project/date-guesser/>`_, project (as a part of the `mediacloud project <https://mediacloud.org/>`_,). Contrary to the initial project, we only focus on extracting dates from URLs.

Installation
------------

This adapted version can be installed as follows:

.. code-block:: bash

    pip install git+https://github.com/rncampos/date_guesser

Quickstart
----------
This adapted version extracts dates from the URL.

.. code-block:: python
    
    from date_guesser import guess_date
    
    # Uses url slugs when available
    guess = guess_date(url='https://arquivo.pt/noFrame/replay/20160509184307/https://tvi24.iol.pt/internacional/24/04/2021/iraque-incendio-em-unidade-de-cuidados-intensivos-faz-23-mortos')

    #  Returns a Guess object with three properties
    guess.date      # datetime.datetime(2017, 10, 13, 0, 0, tzinfo=<UTC>)


.. |Build Status| image:: https://travis-ci.org/mitmedialab/date_guesser.png?branch=master
   :target: https://travis-ci.org/mitmedialab/date_guesser
.. |Coverage| image:: https://coveralls.io/repos/github/mitmedialab/date_guesser/badge.svg?branch=master
   :target: https://coveralls.io/github/mitmedialab/date_guesser?branch=master
