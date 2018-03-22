from typing import Dict, NamedTuple, Union, List, Tuple, Optional

import time
from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Graph, URIRef, Literal, BNode

QueryTriple = Tuple[Optional[URIRef], Optional[URIRef], Optional[Union[Literal, URIRef]]]


NodeType = Union[URIRef, Literal, BNode]


class RDFTriple(NamedTuple):
    s: Union[URIRef, BNode]
    p: URIRef
    o: Union[Literal, URIRef, BNode]


class SlurpyGraph(Graph):
    """ A Graph that acts as a "cache" for a SPARQL endpoint """
    def __init__(self, endpoint: str, *args, **kwargs) -> None:
        """ Create a graph

        :param endpoint: URL of SPARQL endpoint
        """
        self.sparql = SPARQLWrapper(endpoint)
        self.sparql.setReturnFormat(JSON)
        self.resolved_nodes: List[QueryTriple] = [(None, None, None)]
        self.debug_slurps = False
        super().__init__(*args, **kwargs)

    @staticmethod
    def _map_type(node: Dict) -> NodeType:
        if node['type'] not in ('uri', 'literal'):
            raise ValueError("SlurpyGraph cannot process BNodes")
        return URIRef(node['value']) if node['type'] == 'uri' else Literal(node['value'], datatype=node.get('datatype'))

    def already_resolved(self, pattern: QueryTriple) -> bool:
        """ Determine whether pattern has already been loaded into the cache.

        The "wild card" - `(None, None, None)` - always counts as resolved.

        :param pattern: pattern to check
        :return: True it is a subset of elements already loaded
        """
        if pattern == (None, None, None):
            return True
        for resolved_node in self.resolved_nodes:
            if resolved_node != (None, None, None) and \
                    (pattern[0] == resolved_node[0] or resolved_node[0] is None) and \
                    (pattern[1] == resolved_node[1] or resolved_node[1] is None) and\
                    (pattern[2] == resolved_node[2] or resolved_node[2] is None):
                return True
        return False

    def triples(self, pattern: QueryTriple):
        """ Return the triples that match pattern

        :param pattern: `(s, p, o)` tuple, with `None` as wild cards
        :return: Generator for resulting triples
        """
        if not self.already_resolved(pattern):
            subj = f"<{pattern[0]}>" if pattern[0] is not None else '?s'
            pred = f"<{pattern[1]}>" if pattern[1] is not None else '?p'
            obj = f"<{pattern[2]}>" if isinstance(pattern[2], URIRef) else \
                str(pattern[2]) if pattern[2] is not None else '?o'
            query = f"SELECT ?s ?p ?o {{{subj} {pred} {obj}}}"
            if self.debug_slurps:
                start = time.time()
                print(f"SLURPER: ({subj} {pred} {obj})", end="")
            self.sparql.setQuery(query)
            resp = self.sparql.query().convert()
            if self.debug_slurps:
                print(f" ({round(time.time() - start, 2)} secs) - {len(resp['results']['bindings'])} triples")
            for row in resp['results']['bindings']:
                self.add(RDFTriple(pattern[0] if pattern[0] is not None else self._map_type(row['s']),
                                   pattern[1] if pattern[1] is not None else self._map_type(row['p']),
                                   pattern[2] if pattern[2] is not None else self._map_type(row['o'])))
            self.resolved_nodes.append(pattern)
        return super().triples(pattern)
