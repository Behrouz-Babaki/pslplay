.. _installation:

============
Installation
============


The first step is to download the latest reloop distribution from the :ref:`download <download>` section and unpack it in a directory of choice. E.g.:: 

	$ wget https://bitbucket.org/reloopdev/reloop/get/reloop-1.1.0.tar.gz
	$ tar zxvf ŕeloop-1.1.0.tar.gz

Main dependencies
*****************
Before you can build and run reloop, you need to take care of a bunch of dependencies. In particular, reloop depends on the following Python modules:

* `Sympy <http://docs.sympy.org/dev/install.html>`_

* `Cython <https://pypi.python.org/pypi/Cython/>`_

* `scipy <http://www.scipy.org/scipylib/download.html>`_

* `numpy <http://www.scipy.org/scipylib/download.html>`_

* `cvxopt <http://cvxopt.org/install/index.html>`_

* `PICOS <http://picos.zib.de/intro.html#installation>`_

* `PuLP <http://www.coin-or.org/PuLP/main/installing_pulp_at_home.html>`_

* `pyDatalog <https://sites.google.com/site/pydatalog/installation>`_

* `pyparsing <http://pyparsing.wikispaces.com/Download+and+Installation>`_

as well as libglpk. To simplify the installation of the Python modules, we provide a requirements file that can be installed with `pip <https://pip.pypa.io/en/latest/installing.html>`_. To install the Python dependencies with pip, type ::

    $ pip install -r requirements.txt --upgrade

in the directory where you extracted reloop. 

.. DANGER::
   If you already have or want to install some of these packages with custom build parameters (e.g. numpy or cvxopt), doing the above is not advisable. In this case, install all packages one by one or remove the packages in question from requirements.txt and build them manually.

To install libglpk, head on over to `glpk <http://en.wikibooks.org/wiki/GLPK/Linux_OS>`_.

Optional dependencies
*********************
Coming soon. 

Installing reloop
*****************

Once all the requirements are taken care of run ::

    $ pip install .

Upon successful completion, reloop should be installed. To verify that reloop is running correctly, run ::

    $ something
