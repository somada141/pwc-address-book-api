=======
History
=======

0.2.1 (2017-09-02)
------------------

* Made configuration changes to the Ansible role.
* ``resources.py``: Fixed bug in the ``read_uploaded_file`` method of the ``ResourceUploadCsv`` class where ``request.get_param("file")`` wasn't evaluating to ``True`` if a file was uploaded. This bug was causing browser uploaded files to not be processed correctly.

0.2.0 (2017-09-02)
------------------

* Updated the Python dependencies.
* ``docs/config.py``: Enabled ``sphinxcontrib.napoleon`` in the Sphinx extensions to allow for parsing Google-style docstrings as opposed to reST ones which make the code hard to read.
* Fixed typo in the service-configuration template filename.
* ``main.yml``: Fixed bug in the Ansible tasks which was using HTTP to clone the Git repo.
* ``README.rst``: Cleaned up and updated.
* Cleanup superfluous documentation files.
* Fixed a couple bugs in the Ansible role.

0.1.0 (2017-08-26)
------------------

* Initial release.
