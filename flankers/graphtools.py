"""
Tools for SPARQL querying and other Graph utilities.

Try to collect here all the operations that involves Graph()
"""

__author__ = 'niels'

from rdflib import Graph

from datastore.ndbstore import NDBStore
from config.config import _GRAPH_ID


def update(q):
    graph().update(q)


def query(q):
    """
    queries the Graph() instance
    :param q:
    :return:
    """
    response = graph().query(q)
    if response.type == 'CONSTRUCT': #These cannot be JSON-serialized so we extract the data with a SELECT
        g = Graph()
        g += response
        response = g.query("SELECT ?s ?p ?o WHERE {?s ?p ?o}")
    return response.serialize(format='json')


def graph():
    """
    returns the NFBStore
    :return: a Graph() instance
    """
    return Graph(store=NDBStore(identifier=_GRAPH_ID))


def store_triples(triples):
    """
    Caches and store the new triples
    :param triples: triples POSted
    :return: graphs
    """
    cache_graph = Graph()
    cache_graph.parse(data=triples, format="nt")
    app_graph = graph()
    app_graph += cache_graph
    return app_graph, cache_graph