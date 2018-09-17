.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

===============
company_country
===============

This module allow set a country to main company in order to use the hook of 
account that install l10n_** based on country of main company.

Installation
============

To install this module, you need to:

#. Add as depends from your main module.

Configuration
=============

To configure this module, you need to:

#. Set the environment variable COUNTRY using 2 letter of ISO 3166 codes.

Odoo-sh
=======

In case you need to configure odoo-sh:

- Go to your project
- Under settings go to **Module installation**
- Write down the modules you want to install, but make sure the localization is in that line along with the module you want to install

.. image:: https://user-images.githubusercontent.com/4094256/45762860-ef89cd00-bbf4-11e8-9902-9421b4163e81.png

Usage
=====

To use this module, you need to:

#. Just start server installing your main module.

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/{repo_id}/{branch}


Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/OCA/{project_repo}/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smashing it by providing a detailed and welcomed feedback.

Credits
=======

Vauxoo

Images
------

* Odoo Community Association: `Icon <https://github.com/OCA/maintainer-tools/blob/master/template/module/static/description/icon.svg>`_.

Contributors
------------

* Moisés López <moylop260@vauxoo.com>

Maintainer
----------

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit https://odoo-community.org.
