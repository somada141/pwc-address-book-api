====================
pwc-address-book-api
====================

API backend for a simple address book implemented for the PwC interview process.

This is a simple implementation of an address book API. The API is primarily implemented via the falcon_ framework, which in turn interacts with a MySQL server via SQLAlchemy_.

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

Features
--------

* RESTful API implemented via falcon_.
* API endpoint to retrieve all contacts from the database.
* API endpoint to add new contacts to the database.
* API endpoint to update contacts in the database.
* API endpoint to upload a CSV file with contacts and receive a JSON response with the contents.

Provisioning
------------

Provisioning of this project is performed via Ansible_.

A provisioning role has been defined under ``roles/app-pwc-address-book-api`` while another role (``mysql``) has been pulled in as a Git subtree to facilitate the provisioning of the MySQL server.

The ``app-pwc-address-book-api`` role can be used to provision and deploy the role both to the local Vagrant_ VM (see below) and a remote server.

Deployment
----------

Deployment to a remote server can be done via Ansible_ as such::

    >>> ansible-playbook -i path/to/ansible/inventory app-pwc-address-book-api.yaml

Configuration
-------------

The application configuration is defined under the ``vars/main.yml`` file in the Ansible_ role in a YAML format.

Configuration accounts for:

* MySQL Server databases and users along with credentials under the ``mysql_databases`` and ``mysql_users`` respectively. These settings override the defaults ones defined in the ``mysql`` role mentioned prior.
* Application user/group and directory settings under the ``app_pwc_address_book_api`` key.
* Gunicorn_ settings determining how the API is served behind Gunicorn_ under the ``app_pwc_address_book_api.gunicorn`` key.
* Application-specific settings under the ``app_pwc_address_book_api.config`` key.

The application-specific under the ``app_pwc_address_book_api.config`` key are rendered into a JSON file which is in turn used to execute the application (see below).

Development
-----------

Setup
^^^^^

This project is entirely developed within a local Vagrant_ VM based on the official ubuntu/trusty64_ base image.

The VM can be spun up through::

    >>> vagrant up

Virtual Environment
^^^^^^^^^^^^^^^^^^^

Upon provisioning the application via Ansible_, a virtual-environment is created under the application folder, which
by default is located under ``/usr/local/share/pwc-address-book-api/venvs/pwc-address-book-api``.

The virtual-environment needs to be activated prior to running, debugging, or testing the application as such::

    >>> source /usr/local/share/pwc-address-book-api/venvs/pwc-address-book-api/bin/activate

Execution
^^^^^^^^^

The API application can be executed by switching to the application user, enabling the virtual-environment, and serving the API through Gunicorn_::

    >>> sudo -Hu pwc-address-book-api bash
    >>> source /usr/local/share/pwc-address-book-api/venvs/pwc-address-book-api/bin/activate
    >>> PYTHONPATH="/home/vagrant/pwc-address-book-api/" gunicorn --bind 0.0.0.0:8000 "pabapi.pabapi:build_app('/etc/pwc-address-book-api/pwc-address-book-api.json')" --timeout 600

Unit-tests
^^^^^^^^^^

Unit-tests for the application have been written under the `tests` subpackage.

These can be executed via the included `Makefile` as such::

    >>> make test

while unit-testing and coverage can be inspected with::

    >>> make coverage

Documentation
^^^^^^^^^^^^^

The codebase adheres closely to the Google Python Style Guide (https://google.github.io/styleguide/pyguide.html) which is applied to the code comments and docstrings.

The project documentation is generated automatically via Sphinx_ using the napoleon_  extension which can parse Google-style docstrings and improve their legibility prior to rendering.

Documentation can be built via the included Makefile as such::

    >>> make docs

.. _falcon: https://falconframework.org/
.. _SQLAlchemy: https://www.sqlalchemy.org/
.. _Ansible: https://www.ansible.com/
.. _Vagrant: https://www.vagrantup.com/
.. _ubuntu/trusty64: https://app.vagrantup.com/ubuntu/boxes/trusty64
.. _Sphinx: http://www.sphinx-doc.org/en/stable/
.. _napoleon: https://pypi.python.org/pypi/sphinxcontrib-napoleon
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _Gunicorn: http://gunicorn.org/

