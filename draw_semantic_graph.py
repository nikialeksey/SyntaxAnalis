import networkx as nx

A = nx.to_agraph(nx.Graph())
A.read('semantic.dot')
A.draw('semantic.png', prog='dot')