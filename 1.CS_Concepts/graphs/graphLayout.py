from manim import *


class GraphNode:
    def __init__(self, data, position=ORIGIN, neighbors=[], scale=1):
        # Data points
        self.char = data
        self.neighbors = []
        self.edges = []
        self.prev = None
        # Formatting
        self.nodeRadius, self.nodeScale = 0.5, 1
        self.edgeSize = 0.4
        self.data = TextMobject(str(data)).scale(self.nodeScale)
        self.data.move_to(position)
        self.center = position
        self.circle = Circle(radius=self.nodeRadius)
        self.circle.move_to(position)
        self.drawn = False
        self.marked = False

    def connect(self, toNode):
        """
        Create mobject: edge, based off @self (fromNode)
        """
        lineCenter = Line(self.center, toNode.center)
        # unitVector: Adjusted sizing and positioning to line's objects (toNode,fromNode)
        unitVector = lineCenter.get_unit_vector()
        start, end = lineCenter.get_start_and_end()
        adjStart, adjEnd = start + unitVector * self.edgeSize,  end - unitVector * self.edgeSize
        line = Line(adjStart, adjEnd)
        # Undirected, update both nodes - update to/from nodes
        self.neighbors.append(toNode)
        self.edges.append(line)
        toNode.neighbors.append(self)
        toNode.edges.append(line)
        return line

    def __repr__(self):
        return 'GraphNode({0})'.format(self.char)

    def __str__(self):
        return 'GraphNode({0})'.format(self.char)


# class drawGraphLayout(Scene):
class test(Scene):
    def construct(self):
        self.titleText = "Graph Layout"
        self.displayTitle(self.titleText)
        self.displayGraph()

    def displayTitle(self, title):
        title = TextMobject(self.titleText)
        title.scale(1.2).move_to(UP*3)
        self.play(
            Write(title),
        )
        self.wait()

    def displayGraph(self):
        """
        Create graph and layout, then animate creation of graph
        """
        graph, edge_dict = self.buildGraph()
        nodes, edges = self.make_graph_mobject(graph, edge_dict)
        entire_graph = VGroup(nodes, edges)
        self.play(
            ShowCreation(entire_graph),
            run_time=3
        )

    def buildGraph(self):
        """
        Create mobjects: node and edge 
        """
        simpleConfig = {
            'nodeVals': ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
            'edgeDict': {
                'A': ['B', 'C'],
                'B': ['C', 'E'],
                'C': ['D'],
                'D': ['B'],
                'E': ['F', 'G'],
                'F': ['G'],
            },
            'positions': {
                'A': LEFT * 4 + UP * 2,
                'B': LEFT * 2 + UP * 2,
                'C': LEFT * 4 + DOWN * 2,
                'D': LEFT * 2 + DOWN * 2,
                'E': RIGHT * 2 + UP * 2,
                'F': RIGHT * 4 + UP * 2,
                'G': RIGHT * 4 + DOWN * 2
            }
        }
        # Maps node Value to node object, to connect edges
        graphVal_toNode = {}
        graphNodes, graphEdges = [], {}

        # Create node objects
        for nodeVal in simpleConfig['nodeVals']:
            node = GraphNode(nodeVal, position=simpleConfig['positions'][nodeVal])
            graphNodes.append(node)
            graphVal_toNode[node.char] = node

        # Create/Connect edges based off Node objects
        for nodeFrom in graphNodes:
            if nodeFrom.char in simpleConfig['edgeDict']:
                for nodeToVal in simpleConfig['edgeDict'][nodeFrom.char]:
                    nodeTo = graphVal_toNode[nodeToVal]
                    graphEdges[(nodeFrom.char, nodeTo)] = nodeFrom.connect(nodeTo)

        return graphNodes, graphEdges

    def make_graph_mobject(self, graph, edge_dict, node_color=BLUE_A, stroke_color=BLUE_C, data_color=WHITE,
                           edge_color=GREY, scale_factor=1.2, show_data=True):
        """
        VGGroup is used to group animation objects (ex node: data, circle, color, etc.)
        """
        nodes = edges = []
        for node in graph:
            node.circle.set_fill(color=node_color, opacity=0.60)
            node.circle.set_stroke(color=stroke_color)
            node.data.set_color(color=data_color)
            if show_data:
                nodes.append(VGroup(node.circle, node.data))
            else:
                nodes.append(node.circle)

        for edge in edge_dict.values():
            edge.set_stroke(width=7*scale_factor)
            edge.set_color(color=edge_color)
            edges.append(edge)
        return VGroup(*nodes), VGroup(*edges)
