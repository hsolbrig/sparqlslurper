import unittest

from rdflib import Namespace, Literal

from sparqlslurper import SlurpyGraph


class AlreadyResolvedTestCase(unittest.TestCase):
    def test_already_resolved(self):
        g = SlurpyGraph("endpoint")
        EX = Namespace("http://example.org/")
        g.resolved_nodes.append((EX.s1, EX.p1, EX.o1))
        g.resolved_nodes.append((EX.s1, EX.p1, Literal("Steam")))
        g.resolved_nodes.append((EX.s1, EX.p1, Literal(117)))
        g.resolved_nodes.append((EX.s2, EX.p2, None))
        g.resolved_nodes.append((EX.s3, None, EX.o3))
        g.resolved_nodes.append((EX.s3, None, Literal("Gas")))
        g.resolved_nodes.append((EX.s3, None, Literal(-42)))
        g.resolved_nodes.append((EX.s4, None, None))
        g.resolved_nodes.append((None, EX.p5, EX.o5))
        g.resolved_nodes.append((None, EX.p5, Literal("Coal")))
        g.resolved_nodes.append((None, EX.p5, Literal(11.2)))
        g.resolved_nodes.append((None, EX.p6, None))
        g.resolved_nodes.append((None, None, EX.o7))
        g.resolved_nodes.append((None, None, Literal("Wood")))
        g.resolved_nodes.append((None, None, Literal(3.14159)))
        self.assertTrue(g.already_resolved((None, None, None)))

        self.assertTrue(g.already_resolved((EX.s1, EX.p1, EX.o1)))
        self.assertFalse(g.already_resolved((EX.s1, EX.p1, EX.o2)))
        self.assertTrue(g.already_resolved((EX.s1, EX.p1, Literal("Steam"))))
        self.assertFalse(g.already_resolved((EX.s1, EX.p1, Literal("Gas"))))
        self.assertTrue(g.already_resolved((EX.s1, EX.p1, Literal(117))))
        self.assertFalse(g.already_resolved((EX.s1, EX.p1, Literal(118))))
        self.assertFalse(g.already_resolved((EX.s1, None, Literal(117))))
        self.assertFalse(g.already_resolved((None, EX.p1, Literal(117))))

        self.assertTrue(g.already_resolved((EX.s2, EX.p2, Literal(143))))
        self.assertFalse(g.already_resolved((EX.s2, None, Literal(143))))
        self.assertTrue(g.already_resolved((EX.s4, EX.p4, None)))
        self.assertTrue(g.already_resolved((EX.s4, None, Literal(12))))
        self.assertTrue(g.already_resolved((EX.s4, None, None)))

        self.assertTrue(g.already_resolved((EX.s5, EX.p5, EX.o5)))
        self.assertFalse(g.already_resolved((EX.s5, EX.p5, EX.o5n)))

        self.assertTrue(g.already_resolved((EX.s7, None, EX.o7)))
        self.assertTrue(g.already_resolved((None, EX.p7, EX.o7)))
        self.assertFalse(g.already_resolved((EX.s7, None, None)))


if __name__ == '__main__':
    unittest.main()
