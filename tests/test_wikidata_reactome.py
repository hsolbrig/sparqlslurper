import unittest

from rdflib import Namespace
from sparql_slurper import SlurpyGraph

endpoint = 'https://query.wikidata.org/sparql'


class ReactomeTestCase(unittest.TestCase):

    def test_reactome(self):
        WD = Namespace("http://www.wikidata.org/entity/")
        P = Namespace("http://www.wikidata.org/prop/")
        g = SlurpyGraph(endpoint)
        gpo = list(g.predicate_objects(WD.Q29017194))
        orig_len = len(gpo)
        # Test that we get something
        self.assertTrue(30 < orig_len < 60)                 # Current value is 33
        # Test that it is reproducable
        self.assertEqual(orig_len, len(list(g.predicate_objects((WD.Q29017194)))))
        # Test that it is cached
        self.assertEqual(orig_len, len(g))
        # Add a path
        added_length = 0
        for s in g.objects(WD.Q29017194, P.P31):
            gp31s = list(g.predicate_objects(s))
            added_length += len(gp31s)
        self.assertEqual(orig_len + added_length, len(g))


if __name__ == '__main__':
    unittest.main()
