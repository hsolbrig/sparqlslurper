import io
import unittest
from contextlib import redirect_stdout
from typing import List

from rdflib import Namespace

from sparqlslurper import SlurpyGraph, QueryResultPrinter, QueryResultHook, RDFTriple
from tests import UserAgent

endpoint = 'https://query.wikidata.org/sparql'
WD = Namespace("http://www.wikidata.org/entity/")


class PrintOptionsTestCase(unittest.TestCase):
    @staticmethod
    def setup_test() -> SlurpyGraph:
        g = SlurpyGraph(endpoint, agent=UserAgent)
        g.bind("wd", WD)
        g.bind("wdp", "http://www.wikidata.org/prop/")
        g.bind("wdd", "http://www.wikidata.org/prop/direct/")
        g.bind("sdo", "http://schema.org/")
        g.bind("wds", "http://www.wikidata.org/entity/statement/")
        g.bind("wikiba", "http://wikiba.se/ontology#")
        g.add_result_hook(QueryResultPrinter)
        return g

    @staticmethod
    def do_test(g: SlurpyGraph) -> str:
        output = io.StringIO()
        with redirect_stdout(output):
            _ = list(g.predicate_objects(WD.Q29017194))
        return output.getvalue()

    def valid_print_options_output(self, result: str) -> None:
        if not result.startswith("RESULTS:\n\twd:Q29017194 "):
            print(result)
            self.assertTrue(False, "Unexpected results")

    def test_print_options(self):
        """ Test the basic print_option option """

        # the contents of the graph can change, so just make sure we're printing something
        QueryResultPrinter.include_namespaces = False
        g = self.setup_test()
        self.valid_print_options_output(self.do_test(g))

    def test_print_with_namespace(self):
        """ Test print including namespaces and chain function """
        QueryResultPrinter.include_namespaces = True
        g = self.setup_test()
        result = self.do_test(g)
        if not result.startswith('RESULTS:\n\t@prefix rdfs: ') or '\twd:Q29017194 ' not in result:
            print(result)
            self.assertTrue(False, "Unexpected results")

    def test_hook_chaining(self):
        """ Test the hook chain function """
        nadded = [0]

        class ChainedHook(QueryResultHook):
            def __init__(self, sg: SlurpyGraph):
                super().__init__(sg)

            def add(self, t: RDFTriple) -> None:
                assert isinstance(t, RDFTriple)
                nadded[0] = nadded[0] + 1
                super().add(t)

            def done(self) -> None:
                super().done()
                nadded.append(True)

        QueryResultPrinter.include_namespaces = False
        g = self.setup_test()
        g.add_result_hook(ChainedHook)
        result = self.do_test(g)
        self.valid_print_options_output(result)
        self.assertTrue(nadded[0] > 10)
        self.assertTrue(nadded[1])


if __name__ == '__main__':
    unittest.main()
