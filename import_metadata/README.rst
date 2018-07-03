Import Metadata
===============

Allow you to import metadata on every record. The metadata are the create_uid,
create_date, write_uid, write_date. You need to call create or write (or load
method) as admin with the following value in the context: {'write_metadata':
True}.

Note that write_date and write_uid may not be set as you want since other write
can be trigger directly after yours in the same transaction. Like on
res.partner. Those two value will change soon anyway. 

Contributors
------------

* Hugo Adan <hugo@vauxoo.com>

Maintainer
----------

.. image:: https://www.vauxoo.com/logo.png
    :alt: Vauxoo
    :target: https://vauxoo.com

This module is maintained by Vauxoo.

a latinamerican company that provides training, coaching,
development and implementation of enterprise management
sytems and bases its entire operation strategy in the use
of Open Source Software and its main product is odoo.

To contribute to this module, please visit http://www.vauxoo.com.
