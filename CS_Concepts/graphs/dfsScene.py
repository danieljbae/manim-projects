from manim import *
from src.graphObj import GraphNode, graphConfigs


# TO DO: Animation Video 2
# >> Convert this intro a recursive Tree
# >> Sync with Psuedocode
# >> Add to JS/React Website to view all Projects

# class drawGraphLayout(Scene):
class test(Scene):
    def construct(self):
        """
        Drives Scene Animations
        """
        ### Graph Layout ###
        self.titleText = "Graph Layout"
        self.displayTitle(self.titleText)
        graph, entire_graph, edge_dict, graphNodes, graphEdges = self.displayGraph()

        ### DFS Animations: Traversal Order ###
        nodeValPath, nodeEdgePath = dfs(graph, start=0)
        orderTitle = self.displayOrder(nodeValPath, entire_graph)
        self.dfsAnimation(nodeValPath, nodeEdgePath, edge_dict, graphNodes, orderTitle[1:])

    def dfsAnimation(self, dfs_nodeOrder, nodeEdgePath, edge_dict, graphNodes, orderTitle):
        """
        Animates the DFS selection process (in pre-defined DFS path)
        Backtrack: if out-degree of 0, in-degree

        @ nodeValPath: Values of nodes in dfs order
        @ nodeEdgePath: Nodes and Edges in dfs order
        @ edge_dict: contains edge objects
        @ graphNodes: contains node objects
        """
        infoBox = Paragraph("Backtrack:", 'If a node does not change', 'colors (grey), then backtrack').scale(.4)
        infoBox.set_opacity(.7)
        startNodeBox = SurroundingRectangle(graphNodes[0], color=GREEN, buff=.5*SMALL_BUFF)
        startNodeText = TextMobject("Start Node").next_to(startNodeBox, UP*.5).scale(.6)
        self.play(
            ShowCreation(infoBox),
            ShowCreation(startNodeBox),
            ShowCreation(startNodeText),
        )
        self.wait(2)

        # DFS with edges of traversal
        nodeIdx, edgeIdx = 0, 1
        while edgeIdx < len(nodeEdgePath):
            fromNode_val, toNode_val = nodeEdgePath[edgeIdx]
            graphNodes[fromNode_val].set_color(GREEN_A)
            self.play(
                ShowCreationThenFadeAround(graphNodes[toNode_val]),
                WiggleOutThenIn(graphNodes[toNode_val]),
                TransformFromCopy(graphNodes[dfs_nodeOrder[nodeIdx]], orderTitle[nodeIdx]),
                runtime=2
            )
            # Mark traveresed edges and visited nodes (ex. Bread crumbs)
            edge_dict[(fromNode_val, toNode_val)]
            edge_dict[(fromNode_val, toNode_val)].set_color(YELLOW_B)
            graphNodes[fromNode_val].set_color(GREY)
            nodeIdx += 1
            edgeIdx += 2
            self.wait()

        # Final Node in dfs tree
        self.play(
            TransformFromCopy(graphNodes[dfs_nodeOrder[nodeIdx]], orderTitle[nodeIdx])
        )
        self.wait()
        # Todo: Demonstrate backtracking more clearly, with different color edges
        # and showing which node I am backtracking to (recursive stacks)
        # For example, in my example graph, 2 is not visited until we backtrack from 3

    def displayTitle(self, title):
        title = TextMobject(self.titleText)
        title.scale(1.2).to_edge(UP)
        self.play(
            Write(title),
        )
        self.wait()

    def displayGraph(self):
        """
        Create graph and layout, then animate creation of graph
        """
        graph, edge_dict = self.buildGraph()
        graphNodes, graphEdges = self.groupGraphObjects(graph, edge_dict)
        entire_graph = VGroup(graphNodes, graphEdges)
        self.play(
            ShowCreation(entire_graph),
            run_time=5
        )
        return graph, entire_graph, edge_dict, graphNodes, graphEdges

    def displayOrder(self, nodeValPath, entire_graph):
        nodeValPath_str = " ".join(list(map(str, nodeValPath)))
        orderTitle = TextMobject('Order: ', '0 -> ', '2 -> ', '3 -> ', '1 -> ', '4 -> ', '6 -> ', '5')
        orderTitle.shift(DOWN * 2, LEFT * 1.5).next_to(entire_graph, DOWN)
        self.play(
            Write(orderTitle[0]),
            run_time=2
        )
        return orderTitle

    def buildGraph(self):
        """
        Create mobjects: node and edge 
        """
        config = graphConfigs['simpleConfig']
        graphNodes, graphEdges = [], {}
        # Maps: key = node value, val = node object
        graphVal_toObj = {}

        # Create node objects
        for nodeVal in config['nodeVals']:
            node = GraphNode(nodeVal, position=config['positions'][nodeVal])
            graphNodes.append(node)
            graphVal_toObj[node.char] = node

        # Create/Connect edges based off Node objects
        for nodeFrom in graphNodes:
            if nodeFrom.char in config['edgeDict']:
                for nodeToVal in config['edgeDict'][nodeFrom.char]:
                    nodeTo = graphVal_toObj[nodeToVal]
                    graphEdges[(nodeFrom.char, nodeTo.char)] = nodeFrom.connect(nodeTo)

        return graphNodes, graphEdges

    def groupGraphObjects(self, graph, edge_dict, node_color=BLUE_A, stroke_color=BLUE_C, data_color=WHITE,
                          edge_color=GREY, scale_factor=1.2, show_data=True):
        """
        VGGroup: group manim objects together (ex node: data, circle, color, etc.)
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


def dfs(graph, start):
    """
    Returns a list of vertices and edges in preorder traversal
    """
    nodeValPath = []
    visited = [False] * len(graph)
    edgeTo = [None] * len(graph)
    stack = [start]
    while len(stack) > 0:
        node = stack.pop()
        if not visited[node]:
            visited[node] = True
            nodeValPath.append(node)
        for neighbor in graph[node].neighbors:
            neighbor_node = int(neighbor.char)
            if not visited[neighbor_node]:
                edgeTo[neighbor_node] = node
                stack.append(neighbor_node)

    nodeEdgePath = []
    for i in range(len(nodeValPath) - 1):
        prev, cursor = nodeValPath[i], nodeValPath[i + 1]
        nodeEdgePath.append(prev)
        nodeEdgePath.append((edgeTo[cursor], cursor))

    nodeEdgePath.append(cursor)
    return nodeValPath, nodeEdgePath
