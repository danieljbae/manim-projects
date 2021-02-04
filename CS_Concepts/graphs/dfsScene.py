from manim import *
from src.graphObj import GraphNode, graphConfigs


# class drawGraphLayout(Scene):
class test(Scene):
    def construct(self):
        """
        Drives Animation Scenes
        """
        ### Graph Layout ###
        titleText = "Depth First Search"
        purpose = "Visit all reachable nodes exactly 1x"

        self.displayTitle(titleText, purpose)
        graph, entireGraph, edgeDict, nodeObjects, edgeObjects = self.displayGraph()

        ### DFS Animations: Traversal Order ###
        nodeValPath, edgePath = dfs(graph, start=0)
        sep, self.sepLen = " -> ", len(" -> ")
        orderTitle = self.displayOrder(nodeValPath, entireGraph, sep)
        self.dfsAnimation(nodeValPath, edgeDict, nodeObjects, orderTitle[1:], edgePath, edgeObjects)

    def dfsAnimation(self, dfs_nodeOrder, edgeDict, nodeObjects, orderTitle, edgePath, edgeObjects):
        """
        Animates DFS selection process (in pre-defined DFS path)
        Backtrack: if out-degree of 0, in-degree

        @ nodeValPath: Values of nodes in dfs order
        @ nodeEdgePath: Nodes and Edges in dfs order
        @ edgeDict: maps edge pairs (u,v) to edge object
        @ nodeObjects: contains node objects
        """
        infoBox = Paragraph("Backtrack:", 'If a node does not change', 'colors (grey), then backtrack').scale(.4)
        infoBox.set_opacity(.7)
        startNodeBox = SurroundingRectangle(nodeObjects[0], color=GREEN, buff=.5*SMALL_BUFF)
        startNodeText = Tex("Start Node").next_to(startNodeBox, UP*.5).scale(.6)
        self.play(
            ShowCreation(infoBox),
            ShowCreation(startNodeBox),
            ShowCreation(startNodeText),
        )
        self.wait(2)

        # DFS with edges of traversal
        nodeIdx = edgeIdx = 0
        nodeTxt_beg = nodeTxt_end = 0
        while edgeIdx < len(edgePath):
            fromNode_val, toNode_val = edgePath[edgeIdx]
            # fromNode_val, toNode_val = nodeEdgePath[edgeIdx]
            nodeTxt_beg, nodeTxt_end = ((self.sepLen+1)*nodeIdx, (self.sepLen+1)*(nodeIdx+1))
            nodeObjects[fromNode_val].set_color(GREEN_A)
            # print(f"Current: edgeIdx {edgeIdx} , edgeVal {nodeEdgePath[edgeIdx]}")
            # print(f"Current: nodeIdx {nodeIdx} , dfs_nodeOrder[nodeIdx] {dfs_nodeOrder[nodeIdx]}")

            self.play(
                ShowCreationThenFadeAround(nodeObjects[toNode_val]),
                WiggleOutThenIn(nodeObjects[toNode_val]),
                # Node to Order text
                TransformFromCopy(nodeObjects[dfs_nodeOrder[nodeIdx]], orderTitle[nodeTxt_beg:nodeTxt_end]),
                runtime=2
            )

            # Reference: https://github.com/3b1b/manim/issues/688
            # Update: this is because I am referencing the edge's original location in memory
            # and not the VGroup
            # Solution: You'll likely have to do some deepcopy of some sort
            # for edges to be freely edited (independent of VGroup)

            # Debug: edges (2,4) amd (4,6)  are not changing colors
            # Expected behaviour: edge object to chnage to green color
            # Because: edgeDict(2,4) contains edge object,
            # and we can clearly see this pair exists and a line is it's value
            # but the line at edgeDict(2,4) doesn't chnage colors

            # Mark traveresed edges and visited nodes (ex. Bread crumbs)
            if (fromNode_val, toNode_val) in edgeDict:
                print("okay thats what i thought")
                print((fromNode_val, toNode_val))
                print(edgeDict)
                print(edgeDict[(fromNode_val, toNode_val)])
                edgeObjects[8].set_color(GREEN)
                edgeObjects[9].set_color(GREEN)
                edgeObjects[10].set_color(GREEN)
                edgeObjects[11].set_color(GREEN)
                edgeObjects[12].set_color(GREEN)
                edgeObjects[13].set_color(GREEN)
                edgeObjects[14].set_color(GREEN)

                # edgeDict[(fromNode_val, toNode_val)].set_color(GREEN)
                # edgeDict[(fromNode_val, toNode_val)].set_color(YELLOW_B)
                nodeObjects[fromNode_val].set_color(GREY)
                edgeIdx += 1
                nodeIdx += 1
                self.wait()

            elif (toNode_val, fromNode_val) in edgeDict:  # Flip Case: swap to and from nodes
                fromNode_val, toNode_val = toNode_val, fromNode_val
                edgeDict[(fromNode_val, toNode_val)].set_color(YELLOW_B)
                nodeObjects[fromNode_val].set_color(GREY)
                edgeIdx += 1
                nodeIdx += 1
                self.wait()
                # If we have already set color to Yellow, this mean we backtracked
            else:
                edgeIdx += 2
                nodeIdx += 1
                break

            # if (fromNode_val, toNode_val) not in edgeDict or (toNode_val, fromNode_val) not in edgeDict:
            #     edgeIdx += 2
            #     nodeIdx += 1
            #     break

            # # Flip edge if edge key is identified
            # if (fromNode_val, toNode_val) in edgeDict:
            #     fromNode_val, toNode_val = toNode_val, fromNode_val

            # edgeDict[(fromNode_val, toNode_val)].set_color(YELLOW_B)
            # nodeObjects[fromNode_val].set_color(GREY)
            # edgeIdx += 2
            # nodeIdx += 1
            # self.wait()

            # Old
            # edgeDict[(fromNode_val, toNode_val)].set_color(YELLOW_B)
            # nodeObjects[fromNode_val].set_color(GREY)
            # edgeIdx += 2
            # nodeIdx += 1
            # self.wait()

        # Final Node in dfs path/tree
        self.play(
            TransformFromCopy(nodeObjects[dfs_nodeOrder[nodeIdx]], orderTitle[-1])
        )
        self.wait()

    def displayTitle(self, title, purpose):
        titleObj = Tex(title)
        purposeObj = Tex(purpose)
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
        nodeVGroup, edgeVGroup = self.groupGraphObjects(graph, edgeDict)
        entireGraph = VGroup(nodeVGroup, edgeVGroup).shift(DOWN*.1)
        self.play(
            ShowCreation(entireGraph),
            run_time=5
        )
        return graph, entireGraph, edgeDict, nodeVGroup, edgeVGroup

    def displayOrder(self, nodeValPath, entireGraph, sep):
        """
        Converts path[0,2,...] to Tex('Order: ','0 -> ','2 -> ',...)
        """
        nodeValPath_str = sep.join(list(map(str, nodeValPath)))
        orderTitle = Tex('Order: ', *nodeValPath_str)
        orderTitle.shift(DOWN * 2, LEFT * 1.5).next_to(entireGraph, DOWN)
        self.play(
            Write(orderTitle[0]),
            run_time=2
        )
        return orderTitle

    def buildGraph(self):
        """
        Create mobjects(node and edge) from adjan 
        """
        config = graphConfigs['config2']
        nodeObjects, edgeObjects = [], {}
        graphVal_toObj = {}  # Maps {key=node val : val=node object}

        # Create node objects
        for nodeVal in config['adjList'].keys():
            # for nodeVal in config['nodeVals']:
            node = GraphNode(nodeVal, position=config['positions'][nodeVal])
            nodeObjects.append(node)
            graphVal_toObj[node.char] = node

        # Create edge objects - 2nd pass to connect edges to nodes
        for nodeFrom in nodeObjects:
            if nodeFrom.char not in config['adjList']:
                continue
            for nodeToVal in config['adjList'][nodeFrom.char]:
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
    nodePath = []
    visited = [False] * len(graph)
    edgeTo = [None] * len(graph)
    stack = [start]
    while stack:
        node = stack.pop()
        if not visited[node]:
            visited[node] = True
            nodePath.append(node)
        for neighbor in graph[node].neighbors:
            neighbor_node = int(neighbor.char)
            if not visited[neighbor_node]:
                edgeTo[neighbor_node] = node
                stack.append(neighbor_node)

    # nodeEdgePath = []
    edgePath = []
    for i in range(len(nodePath) - 1):
        prev, cursor = nodePath[i], nodePath[i + 1]
        # nodeEdgePath.append(prev)
        # nodeEdgePath.append((edgeTo[cursor], cursor))
        edgePath.append((edgeTo[cursor], cursor))

    # nodeEdgePath.append(cursor)
    # print(nodePath)
    return nodePath, edgePath
