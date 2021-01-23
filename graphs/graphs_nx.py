from manim import *
import networkx as nx


class Test(Scene):
    def construct(self):
        G = nx.Graph()

        G.add_node("ROOT")

        for i in range(5):
            G.add_node("Child_%i" % i)
            G.add_node("Grandchild_%i" % i)
            G.add_node("Greatgrandchild_%i" % i)

            G.add_edge("ROOT", "Child_%i" % i)
            G.add_edge("Child_%i" % i, "Grandchild_%i" % i)
            G.add_edge("Grandchild_%i" % i, "Greatgrandchild_%i" % i)

        self.play(ShowCreation(
            Graph(list(G.nodes), list(G.edges), layout="spring")))


# nxgraph = nx.erdos_renyi_graph(14, 0.5)


# class ImportNetworkxGraph(Scene):
#     def construct(self):
#         G = Graph.from_networkx(nxgraph, layout="networkx", layout_scale=3.5)
#         self.play(ShowCreation(G))
#         self.play(*[G[v].animate.move_to(5*RIGHT*np.cos(ind/7 * PI) +
#                                          3*UP*np.sin(ind/7 * PI))
#                     for ind, v in enumerate(G.vertices)])
#         self.play(Uncreate(G))
