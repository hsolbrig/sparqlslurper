import unittest

import io
from contextlib import redirect_stdout

from rdflib import Namespace, Graph
from sparql_slurper import SlurpyGraph
from sparql_slurper._graphdb_slurpygraph import GraphDBSlurpyGraph

endpoint = 'https://graph.fhircat.org/repositories/fhirontology'


class GraphDBBnodeTestCase(unittest.TestCase):

    def test_bnodes(self):
        FHIR = Namespace("http://hl7.org/fhir/")
        P = Namespace("http://hl7.org/fhir/Patient/")
        g = GraphDBSlurpyGraph(endpoint)
        g.debug_slurps = False
        obj = g.value(P.pat4, FHIR['Resource.id'])
        v = g.value(obj, FHIR.value)
        self.assertEqual(str(v), "pat4")

if __name__ == '__main__':
    unittest.main()
