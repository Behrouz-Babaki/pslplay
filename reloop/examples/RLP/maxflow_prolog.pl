/* test.pl */

/*predicates*/

node(a).
node(b).
node(c).
node(d).
node(e).
node(f).
node(g).

edge(a,b).
edge(a,c).
edge(b,d).
edge(b,e).
edge(c,d).
edge(c,f).
edge(d,e).
edge(d,f).
edge(e,g).
edge(f,g).

cost(a,b,50).
cost(a,c,100).
cost(b,d,40).
cost(b,e,20).
cost(c,d,60).
cost(c,f,20).
cost(d,e,50).
cost(d,f,60).
cost(e,g,70).
cost(f,g,70).

source(a).
target(g).
