import unittest

from rdflib import Namespace, Graph

from sparql_slurper import TM_NS
from sparql_slurper._graphdb_slurpygraph import GraphDBSlurpyGraph

# Note: this endpoint is not terribly stable.  We really need to find a stable graphdb instance to switch to
endpoint = 'https://graph.fhircat.org/repositories/fhirontology'

FHIR = Namespace("http://hl7.org/fhir/")
P = Namespace("http://hl7.org/fhir/Patient/")

class GraphDBBnodeTestCase(unittest.TestCase):
    g: Graph = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.g = GraphDBSlurpyGraph(endpoint)

    def test_bnodes(self):
        self.debug_slurps = False
        obj = self.g.value(P.pat4, FHIR['Resource.id'])
        v = self.g.value(obj, FHIR.value)
        self.assertEqual(str(v), "pat4")

    def test_bnode_mapping(self):
        bd_list = list(self.g.objects(P.pat4, FHIR['Patient.birthDate']))
        self.assertEqual(3, len(bd_list))
        for e in bd_list:
            self.assertTrue(str(e).startswith(TM_NS))


if __name__ == '__main__':
    unittest.main()
