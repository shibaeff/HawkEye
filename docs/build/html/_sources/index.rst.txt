.. HawkEye documentation master file, created by
   sphinx-quickstart on Thu Apr 21 01:04:52 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

HawkEye:
==========
the world's first intelligent blockchain transaction analyzer
===================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   modules

Usage
=============
.. code-block::
   :caption: Simple run to analyze the transaction
       from src.hawk_eye.hawk_eye import HawkEye
       he = HawkEye()
       print(he.parse("0xade227c3ad59395cf7a15ceb56085a77c61a29216858fc789d8413ef929a5fbe"))

*Run*

* To see our datascience in action:
* To see our model testing in action:

*Become our stargazer on github.com*
<link>

*Query our test API here*
<link>
.. code-block::
       from requests import get
       print(get(...))

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
