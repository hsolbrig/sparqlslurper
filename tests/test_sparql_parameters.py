import unittest

import io
from contextlib import redirect_stdout

from rdflib import Namespace, Graph
from sparql_slurper import SlurpyGraph
from sparql_slurper._graphdb_slurpygraph import GrapphDBSlurpyGraph

endpoint = 'https://graph.fhircat.org/repositories/fhirontology'


class SparqlParametersTestCase(unittest.TestCase):

    def test_parms(self):
        """ Show how to pass a parameter to a wrapper instance

            This test assumes a GraphDB SPARQL endpoint
            loaded with the fhir.ttl w/ the inference option on.
            We are testing that the parameter makes it through and
            changes the behavior of the server.

            Note that a copy of fhir.ttl can be found in tests/data.
        """
        FHIR = Namespace("http://hl7.org/fhir/")
        g = GrapphDBSlurpyGraph(endpoint)
        self.assertLess(85, len(list(g.predicate_objects(FHIR.Patient))))
        g = GrapphDBSlurpyGraph(endpoint)
        g.sparql.addParameter("infer", "false")
        self.assertGreater(60, len(list(g.predicate_objects(FHIR.Patient))))

        g = GrapphDBSlurpyGraph(endpoint + '?infer=false')
        self.assertGreater(60, len(list(g.predicate_objects(FHIR.Patient))))


if __name__ == '__main__':
    unittest.main()
