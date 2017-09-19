.. Relational Linear Programming documentation master file, created by
   sphinx-quickstart on Thu Dec 11 10:09:08 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. |br| raw:: html

   <br />


.. toctree::
   :hidden:
   :maxdepth: 1

   installation
   tutorial 
   examples
   quick_reference
   reference
   bibliography
   contact

|br| |br|

.. image:: images/reloop.svg
   :width:  50%
   :alt: woot!
   :align: right

RELOOP: A Toolkit for Relational Convex Optimization 
=========================================================
|br| |br|
Welcome to reloop! This is the web home of the Relational Optimization project of the Data Mining group at TU-Dortmund. Here you will find software and theory produced in our research efforts. 


Modern social and technological trends result in an enormous increase in the amount of accessible data,
with a significant portion of the resources being interrelated in a complex way and having inherent uncertainty.
Such data, to which we may refer to as relational data, arise for instance in social
network and media mining, natural language processing, open information extraction,
the web, bioinformatics, and robotics, among others, and typi- cally features substantial
social and/or business value if become amenable to computing machinery. Therefore it is not
surprising that probabilistic logical languages and **statistical relational learning** are currently provoking a lot of new AI research
with tremendous theoretical and practical implications. By combining aspects of logic and probabilities
— a dream of AI dating back to at least the late 1980s
when Nils Nilsson introduced the term probabilistic logics — they help to effectively manage
both complex interactions and uncertainty in the data.

However, instead of looking at AI through the glasses of probabilities over possible worlds, we may also approach
it using optimization. That is, we have a preference relation over possible worlds, and we want a best possible
world according to the preference. The preference is often to minimize some objective function. Consider for example
a typical machine learning user in action solving a problem for some data. She selects a model for the underlying
phenomenon to be learned (choosing a learning bias), formats the raw data according to the chosen model, and then
tunes the model parameters by minimizing some objective function induced by the data and the model assumptions.
In the process of model selection and validation, the core optimization problem in the last step may be solved many times.
Ideally, the optimization problem solved in the last step falls within a class of mathematical programs for which efficient
and robust solvers are available. For example, linear, semidefinite and quadratic programs, found at the heart of many popular AI
and learning algorithms, can be solved efficiently by commercial-grade software packages.

From here you can:

* get an overall picture of what RELOOP is about by checking out the :ref:`introduction <introduction>`;

* get started with our code -- head over to :ref:`download <download>`, :ref:`installation <installation>` and then to our quickstart :ref:`tutorial <tutorial>`;

* navigate the complete code :ref:`documentation <reference>`;

* find a list of all related papers on our :ref:`bibliography <bibliography>` page. 

|br| |br|

News
----
 * 02.06.2015: Version 0.1.0. Check out the :ref:`tutorial <tutorial>`
	* Major language update: Rlp2 based on `sympy <http://www.sympy.org/en/index.html>`_
	* Support for **PostgreSQL** added
	* Increased extensibility: Add your own LogKB or LP-solver

 * 16.02.2015: **Reloop** -- first release!

Acknowledgements
----------------
The research presented was partly supported by the Fraunhofer ATTRACT fellowship STREAM, by the EC under contract number FP-248258-First-MM, by the German-Israeli Foundation (GIF) for Scientific Research and Development, 1180-218.6/2011, and by the German Science Foundation (DFG), KE 1686/2-1.
