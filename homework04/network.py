import time
import json
from typing import List, Tuple
from api import get_friends
from igraph import Graph, plot

import config
import numpy as np


def get_network(users_ids: List, as_edgelist: bool = True) -> List[Tuple[int, int]]:
    """ Create user friends network in form of matrix or graph

    :param users_ids: list with ID's of user's friends
    :param as_edgelist: result in form of graph edges if True, and in matrix if False
    :return: user's friends network in form of matrix or in edges list (as_edgeList option)
    """
    graph_edges = []
    matrix = [[0 for _ in range(len(users_ids))] for _ in range(len(users_ids))]

    for l1_friend in range(len(users_ids)):
        try:
            friend_ids = json.loads(get_friends(users_ids[l1_friend], '').text)['response']['items']
        except Exception:
            resp_json = json.loads(get_friends(users_ids[l1_friend], '').text)
            if resp_json['error']['error_code'] == 18:
                print(f"The user with id: {users_ids[l1_friend]} has been deleted or banned :(")
            continue
        for l2_friend in range(l1_friend + 1, len(users_ids)):
            if users_ids[l2_friend] in friend_ids:
                if as_edgelist:
                    graph_edges.append((l1_friend, l2_friend))
                else:
                    matrix[l1_friend][l2_friend] = 1
                    matrix[l2_friend][l1_friend] = 1
        time.sleep(0.2) # to prevent vk api requests limit

        progress = ((l1_friend + 1) * 100) // len(users_ids)
        if progress > ((l1_friend) * 100) // len(users_ids):
            print(str(progress) + "% completed...")

    if as_edgelist:
        return graph_edges
    else:
        return matrix


def plot_graph(graph: object) -> object:
    """ Draw the graph

    :param graph: graph edges list
    :return: nothing
    """
    friends = json.loads(get_friends(int(config.VK_CONFIG['my_id']), 'bdate').text)['response']['items']
    vertexes = [friend['last_name'] for friend in friends]  # graph vertexes
    edges = graph  # graph edges

    # Create graph
    g = Graph(vertex_attrs={"label": vertexes, "shape": "circle", "size": 10}, edges=edges, directed=False)

    # Graph appearance
    n = len(vertexes)
    visual_style = {
        "vertex_size": 10,
        "vertex_color": "blue",
        "edge_color": "gray",
        "bbox": (1500, 1000),
        "layout": g.layout_fruchterman_reingold(
            maxiter=1000,
            area=n ** 3,
            repulserad=n ** 3)
    }

    # Delete loops and repeating edges
    g.simplify(multiple=True, loops=True)

    # Separate vertices in groups by interconnection
    g.community_multilevel()

    # Draw graph
    plot(g, **visual_style)


if __name__ == '__main__':
    user_id = int(config.VK_CONFIG.get('my_id'))
    response = json.loads(get_friends(user_id, '').text)['response']['items']
    graph = get_network(response, as_edgelist=True)
    plot_graph(graph)
