.. highlight:: python

.. |br| raw:: html

    <br />

Quick Reference
================

Reloop
-----------

This Quick Reference will provide you with an overview about the available language features of Relational Linear Programming. For a more in depth code documentation, please visit our :ref:`reference page<reference>`.

Reloop comes with a powerful modelling language for relational linear programs: RLP. 

RLP aims to bridge the gap between powerful relational reasoning tools and efficient numerical optimization algorithms in a hassle-free way.
When defining a model with RLP, you are able to use logically parameterized definitions for the index sets within arithmetic expressions. 
A 'Logical Knowledge Base' contains all your data and will be queried in order to ground the RLP into a plain LP, that can then be solved by an arbitrary numerical solver. 


.. image:: images/rlp_diagram.png
    :align: center
    :alt: RLP Diagram

RLP and Sympy
--------------
RLP is built on top of Sympy, a Python library for symbolic mathematics. That means you are able to use most of SymPy's features, such as simplification, expansion and functions.


Predicates
...........
Predicates represent relational data inside our model definitions. If your data contains e.g. a relation ``R(String, String, Integer)``, it is possible to define a predicate inside RLP that maps to this specific relation. RLP distinguishes between two types of predicates:

1. **BooleanPredicates** 
   can be used to determine if a tuple is part of the relation. It will return True or False |br|
   ``boolean_predicate(name, arity)``
2. **NumericPredicates**
   can be used to get numerical data from a LogKb for using it in mathematical expressions. It can also be interpreted as a function. |br|
   ``numeric_predicate(name, arity)`` 

Algebraic Expressions
---------------------
All defined Numeric Predicates can be used in algebraic expressions inside constraints and the objective function. An example for such an expression is ``3 * flow(X,Y) + cost(X,Y)**3`` 


SubSymbols
............

SubSymbols in RLP are placeholders in expressions. They behave similarly to `Sympys Symbols <http://docs.sympy.org/latest/modules/core.html#id17>`_, since SubSymbol subclasses Symbol.
They can only be used inside a `Forall` or `RlpSum` statement, because the Grounder will try to substitute those SubSymbols with answers from the LogKB. 

While ``X = SubSymbol('X')`` will instantiate a SubSymbol with value 'X' and store it inside the variable *X* we provide a convenience function to create multiple symbols at once:
``X, Y, Z = sub_symbols('X', 'Y', 'Z')`` 

Queries
........
Queries are logical expressions and can consist of BooleanPredicates and `Boolean Functions <http://docs.sympy.org/0.7.6/modules/logic.html#boolean-functions>`_. They can be built with the standard python operators ``&`` (And), ``|`` (Or) and ``~`` (Not).

A possible query with boolean predicates ``node`` and ``edge`` where ``node(X)`` indicates that ``X`` is a node and ``edge(X, Y)`` indicates that there is an endge between nodes ``X`` and ``Y`` would be:
``node(X) & edge(X, Y)`` over ``X, Y``. |br| The answer from the LogKB would contain all tuples (X,Y) that satisfy the query.

Queries are used in

1. **ForAll** 
   statements: These allow batch constraint generation, based on answers from the LogKB. |br|
   ``ForAll({X, Y}, edge(X,Y) & node(X), cost(X, Y) <= cost(Y, X) )``
2. **RlpSum** 's
   : A mathematical sum over an answer set from the LogKB. |br|
   ``RlpSum({X}, node(X), expr(X))``

Constraints
............

While there is no inherent datatype for constraints, we allow instances of ``ForAll`` that contain a sympy `Relation <http://docs.sympy.org/latest/modules/core.html#module-sympy.core.relational>`_ or directly such relations, which can be added to the model with the ``+=`` operator.

Furthermore we provide two additional ways to declare constraints, where ``ask = grounder.ask``:


.. code:: python

    for (x, y) in ask(edge(X,Y)):
        model += flow(x, y) |le| cost(x, y)
        
.. code:: python

    model += (flow(x, y) |ge| 0
        for (x,y) in ask(edge(X,Y))
    )

.. WARNING::

    For now, both ways won't create `ForAll`-constraints, but ground directly into a set of pure sympy Relations. That can be slow, since you can't benefit from the ``BlockGrounder``.


Logical Knowledge Base & Grounding
----------------------------------

When solving a RLP model, Reloop grounds the model definitions into a LP. It compiles the logical queries and queries the Logical Knowledge Base until everything is grounded. That includes nested queries, e.g. a RlpSum inside a ForAll constraint. Currently we provide interfaces to four differenct LogKBs:

1. pyDatalog
2. PostgreSQL
3. SWI Prolog
4. ProbLog

