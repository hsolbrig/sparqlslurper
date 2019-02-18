# SPARQL Slurper for `rdflib`

[![Pyversions](https://img.shields.io/pypi/pyversions/sparql_slurper.svg)](https://pypi.python.org/pypi/sparql_slurper)
[![PyPi](https://img.shields.io/pypi/v/sparql_slurper.svg)](https://pypi.python.org/pypi/sparql_slurper)


## Revision History
* 0.1.0 - Initial drop
* 0.1.1 - Added debug_slurps parameter
* 0.1.2 - Added diagnostic parameters
* 0.1.3 - Lock out sparql access during serialize
* 0.1.4 - Add persistent_bnodes parameter 
* 0.2.0 - Switch over to pbr and pipenv
* 0.2.1 - Add ability to supply a named graph and diagnostic/debug query results

An implementation of a [`rdflib`](https://github.com/RDFLib/rdflib)[`Graph`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html#rdflib.graph.Graph) that acts as a cache for a SPARQL endpoint.  
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
  * Release 0.1.4: you can now ask the slurper to assume BNodes persist across calls - a potentially dangerous option as mostly they don't
