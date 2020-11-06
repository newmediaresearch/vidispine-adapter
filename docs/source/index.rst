.. Vidispine Adapter documentation master file, created by
   sphinx-quickstart on Mon Nov  2 11:31:19 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Vidispine Adapter's documentation!
=============================================

A python (3.6+) wrapper around the `Vidispine API <https://apidoc.vidispine.com/latest/>`_.

Note: This is a work in progress and not all of the Vidispine endpoints have been implemented yet.

This is currently tested with Vidispine API 4.17, however, should work with most Vidispine 4.x API's. We will soon configure this to work with many different versions of Vidispine.

Quick Start
===========

Installation
------------

To install::

    pip install vidispine-adapter

Basic Usage
------------
To use the Vidispine API you will need a to know the URL, user and password. The user does not need to be the admin user but does need the correct roles for any API call you make::

    from vidispine import Vidispine

    vs = Vidispine(
        url='http://localhost:8080', user='admin', password='admin'
    )
    vs.collection.create(name='test_collection_1')

If `url`, `user` and `password` are not passed through when initialising, Vidispine will fall back and try and use environmental variables called `VIDISPINE_URL`, `VIDISPINE_USER` and `VIDISPINE_PASSWORD`::

    export VIDISPINE_URL="http://localhost:8080"
    export VIDISPINE_USER="admin"
    export VIDISPINE_PASSWORD="admin"

In your code::

    from vidispine import Vidispine

    vs = Vidispine()
    vs.collection.create(name='test_collection_1')


Contributing
============

All contributions are welcome and appreciated. Please see the :doc:`contributing` guide for more details including details on how to run tests etc.


Roadmap
=======

- [ ] Ability to work with other Vidispine API versions
- [ ] Complete API
- [x] Publish to PyPi
- [x] Publish Documentation
- [x] Implement tests using PyVCR
- [x] Configure CircleCI


.. toctree::
   :maxdepth: 2
   :caption: Guide:

   contributing


.. toctree::
   :maxdepth: 2
   :caption: API Reference:

   API/client
   API/collections
   API/items
   API/jobs
   API/metadata
   API/search

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
