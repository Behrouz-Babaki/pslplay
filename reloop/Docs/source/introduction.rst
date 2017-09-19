.. _introduction:

============
Introduction
============

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

This is an instance of the declarative **“Model+Solver”** paradigm currently observed a lot in AI, machine learning and also data mining:
instead of outlining how a solution should be computed, we specify what the problem is using some high-level modeling language and
solve it using general solvers. Unfortunately, however, today’s solvers for mathematical programs typically require that the
mathematical program is presented in some canonical algebraic form or offer only some very restricted modeling environment.

To overcome these downsides and triggered by the success of probabilistic logical languages, **relational optimization aims at lifting
optimization to the relational level**, too. Using a Relational Mathematical Programming Language, **RAMPL** for short, mathematical programs can be modelled using relational languages that
feature the notions of **objects** and **relations** among them.

Indeed, the induced mathematical programs can become rather large. Next to exploiting efficient solvers, we could also try to
exploit symmetries within the ground programs to reduce their dimensionalities, if possible. For linear programs, e.g.,
the reduced program can be much smaller and still be solved using any off-the-shelf LP solver. This is sometimes called
**lifted optimization** or **compressed optimization**.