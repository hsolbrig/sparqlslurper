# SPARQL Slurper for `rdflib`
[![Pyversions](https://img.shields.io/pypi/pyversions/sparql_slurper.svg)](https://pypi.python.org/pypi/sparql_slurper)

[![PyPi](https://version-image.appspot.com/pypi/?name=sparql_slurper)](https://pypi.python.org/pypi/sparql_slurper)

An implementation of a [`rdflib`](https://github.com/RDFLib/rdflib)[`Graph`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html#rdflib.graph.Graph) that acts as a "cache" for a SPARQL endpoint.  
SPARQL Slurper translates the `Graph.triples()` function into the corresponding SPARQL
query and resolves it against an endpoint.  

## Requirements
* Python 3.6 -- this module uses the new typing annotations
* [`rdflib`](https://github.com/RDFLib/rdflib) -- a Python library for working with RDF
* [`sparqlwrapper`](https://github.com/RDFLib/sparqlwrapper) -- A wrapper for a remot SPARQL endpoint

## Use
See [Jupyter notebook](README.ipynb)

## Issues and notes
* We still need to add BNode reification -- at the moment this code generates a ValueError if it crosses a BNode boundary