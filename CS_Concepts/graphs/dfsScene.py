from manim import *
from src.graphObj import GraphNode, graphConfigs


# class drawGraphLayout(Scene):
class test(Scene):
    def construct(self):
        """
        Drives Scene Animations
        """
        ### Graph Layout ###
        titleText = "Depth First Search"
        purpose = "Visit all reachable nodes exactly 1x"

        self.displayTitle(titleText, purpose)
        graph, entireGraph, edgeDict, nodeObjects, edgeObjects = self.displayGraph()

        ### DFS Animations: Traversal Order ###
        nodeValPath, nodeEdgePath = dfs(graph, start=0)
        orderTitle = self.displayOrder(nodeValPath, entireGraph)
        self.dfsAnimation(nodeValPath, nodeEdgePath, edgeDict, nodeObjects, orderTitle[1:])

    def dfsAnimation(self, dfs_nodeOrder, nodeEdgePath, edgeDict, nodeObjects, orderTitle):
        """
        Animates DFS selection process (in pre-defined DFS path)
        Backtrack: if out-degree of 0

        @ nodeValPath: Values of nodes in dfs order
        @ nodeEdgePath: Nodes and Edges in dfs order
        @ edgeDict: maps edge pairs (u,v) to edge object
        @ nodeObjects: contains node objects
        """
        infoBox = Paragraph("Backtrack:", 'If a node does not change', 'colors (grey), then backtrack').scale(.4)
        infoBox.set_opacity(.7)
        startNodeBox = SurroundingRectangle(nodeObjects[0], color=GREEN, buff=.5*SMALL_BUFF)
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
            nodeObjects[fromNode_val].set_color(GREEN_A)
            self.play(
                ShowCreationThenFadeAround(nodeObjects[toNode_val]),
                WiggleOutThenIn(nodeObjects[toNode_val]),
                TransformFromCopy(nodeObjects[dfs_nodeOrder[nodeIdx]], orderTitle[nodeIdx]),
                runtime=2
            )
            # Mark traveresed edges and visited nodes (ex. Bread crumbs)
            edgeDict[(fromNode_val, toNode_val)]
            edgeDict[(fromNode_val, toNode_val)].set_color(YELLOW_B)
            nodeObjects[fromNode_val].set_color(GREY)
            nodeIdx += 1
            edgeIdx += 2
            self.wait()

        # Final Node in dfs path/tree
        self.play(
            TransformFromCopy(nodeObjects[dfs_nodeOrder[nodeIdx]], orderTitle[nodeIdx])
        )
        self.wait()
        # Todo: Demonstrate backtracking more clearly, with different color edges
        # and showing which node I am backtracking to (recursive stacks)
        # For example, in my example graph, 2 is not visited until we backtrack from 3

    def displayTitle(self, title, purpose):
        titleObj = TextMobject(title)
        purposeObj = TextMobject(purpose)
        titleObj.scale(1.2).to_edge(UP)
        purposeObj.scale(.6).to_edge(UP).shift(DOWN*.7)

        self.play(
            Write(titleObj),
            Write(purposeObj),
        )
        self.wait()

    def displayGraph(self):
        """
        Create graph and layout, then animate creation of graph
        """
        graph, edgeDict = self.buildGraph()
        nodeObjects, edgeObjects = self.groupGraphObjects(graph, edgeDict)
        entireGraph = VGroup(nodeObjects, edgeObjects).shift(DOWN*.1)
        self.play(
            ShowCreation(entireGraph),
            run_time=5
        )
        return graph, entireGraph, edgeDict, nodeObjects, edgeObjects

    def displayOrder(self, nodeValPath, entireGraph):
        nodeValPath_str = " ".join(list(map(str, nodeValPath)))
        orderTitle = TextMobject('Order: ', '0 -> ', '2 -> ', '3 -> ', '1 -> ', '4 -> ', '6 -> ', '5')
        orderTitle.shift(DOWN * 2, LEFT * 1.5).next_to(entireGraph, DOWN)
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
        nodeObjects, edgeObjects = [], {}
        # Maps: key = node value, val = node object
        graphVal_toObj = {}

        # Create node objects
        for nodeVal in config['nodeVals']:
            node = GraphNode(nodeVal, position=config['positions'][nodeVal])
            nodeObjects.append(node)
            graphVal_toObj[node.char] = node

        # Create edge objects
        for nodeFrom in nodeObjects:
            if nodeFrom.char in config['edgeDict']:
                for nodeToVal in config['edgeDict'][nodeFrom.char]:
                    nodeTo = graphVal_toObj[nodeToVal]
                    edgeObjects[(nodeFrom.char, nodeTo.char)] = nodeFrom.connect(nodeTo)

        return nodeObjects, edgeObjects

    def groupGraphObjects(self, graph, edgeDict, node_color=BLUE_A, stroke_color=BLUE_C, data_color=WHITE,
                          edge_color=GREY, scale_factor=1.2, show_data=True):
        """
        VGGroup: groups manim objects together (ex nodes comprised of: circle, data, color, etc.)
        Returns: node and edge containers, with all node objects and all edge objects
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

        for edge in edgeDict.values():
            edge.set_stroke(width=7*scale_factor)
            edge.set_color(color=edge_color)
            edges.append(edge)
        return VGroup(*nodes), VGroup(*edges)


def dfs(graph, start):
    """
    Returns a list of nodes and edges in Pre-Order DFS traversal
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
