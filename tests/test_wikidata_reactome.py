import unittest

import io
from contextlib import redirect_stdout

from rdflib import Namespace, Graph
from sparqlslurper import SlurpyGraph
from tests import UserAgent

endpoint = 'https://query.wikidata.org/sparql'


class ReactomeTestCase(unittest.TestCase):

    def test_reactome(self):
        WD = Namespace("http://www.wikidata.org/entity/")
        P = Namespace("http://www.wikidata.org/prop/")
        g = SlurpyGraph(endpoint, agent=UserAgent)
        g.debug_slurps = False
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
        print(f"{g.total_calls}, {g.total_queries}, {g.total_slurptime}, {g.total_triples}")
        self.assertEqual((5, 3, 41), (g.total_calls, g.total_queries, g.total_triples))
        self.assertTrue(g.total_slurptime > 0.1)

    def test_debug_slurps(self):
        WD = Namespace("http://www.wikidata.org/entity/")
        g = SlurpyGraph(endpoint, agent=UserAgent)
        g.debug_slurps = True
        output = io.StringIO()
        with redirect_stdout(output):
            _ = list(g.predicate_objects(WD.Q29017194))
        if not output.getvalue().startswith("SPARQL: "
                                            "(SELECT ?s ?p ?o {<http://www.wikidata.org/entity/Q29017194> ?p ?o})"):
            print("Unexpected:")
            print(output.getvalue())
            self.assertTrue(False)

    def test_serialize(self):
        # Issue #1 - serialize goes after the entire graph
        WD = Namespace("http://www.wikidata.org/entity/")
        g = SlurpyGraph(endpoint, agent=UserAgent)
        _ = list(g.predicate_objects(WD.Q29017194))
        g.debug_slurps = True
        # Warning - this will go away forever if the bug isn't fixed
        serialized_graph = g.serialize(format="turtle").decode()
        g2 = Graph()
        g2.parse(data=serialized_graph, format="turtle")
        self.assertEqual(len(list(g)), len(list(g2)))


if __name__ == '__main__':
    unittest.main()
