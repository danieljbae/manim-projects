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
        """
        Drives Scene Animations
        """
        ### Graph Layout ###
        self.titleText = "Graph Layout"
        self.displayTitle(self.titleText)
        graph, entire_graph, edge_dict = self.displayGraph()

        ### DFS Animations: Traversal Order ###
        dfs_full_order = dfs(graph, start=0)

        wait_times = [0] * len(dfs_full_order)
        wait_time_dict = {}
        for i in range(len(graph)):
            wait_time_dict[i] = 0
        wait_time_dict[0] = 1
        wait_times[0] = 1
        wait_time_dict[1] = 1
        wait_times[1] = 1
        order = TextMobject("O", "r", "d", "e", "r", ":", "0", "2", "3", "1", "4", "6", "5")
        order.shift(DOWN * 0.5)
        order.next_to(entire_graph, DOWN)
        self.play(
            Write(order[:6])
        )
        self.wait(2)

        ### DFS Animations: Decision Options ###
        all_highlights = []
        # print(dfs_full_order[:4], order[7:])
        # print(dfs_full_order)
        # print(order)

        new_highlights = self.show_full_dfs_animation(
            graph, edge_dict, dfs_full_order[:4], order[7:], wait_times, wait_time_dict)
        all_highlights.extend(new_highlights)
        self.wait(10)
        graph[2].surround_circle.set_color(RED)
        self.wait(3)
        self.play(
            CircleIndicate(graph[1].circle, color=BLUE),
            run_time=2
        )
        wait_time_dict[1] = 1
        self.indicate_neighbors(graph, 1, wait_time_dict)
        self.wait(2)

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
        return graph, entire_graph, edge_dict

    def buildGraph(self):
        """
        Create mobjects: node and edge 
        """
        simpleConfig = {
            'nodeVals': [0, 1, 2, 3, 4, 5, 6],
            'edgeDict': {
                0: [1, 2],
                1: [2, 4],
                2: [3],
                3: [1],
                4: [5, 6],
                5: [6],
                6: []
            },
            'positions': {
                0: LEFT * 4 + UP * 2,
                1: LEFT * 2 + UP * 2,
                2: LEFT * 4 + DOWN * 2,
                3: LEFT * 2 + DOWN * 2,
                4: RIGHT * 2 + UP * 2,
                5: RIGHT * 4 + UP * 2,
                6: RIGHT * 4 + DOWN * 2
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
                    graphEdges[(nodeFrom.char, nodeTo.char)] = nodeFrom.connect(nodeTo)

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

    def show_full_dfs_animation(self, graph, edge_dict, full_order, order,
                                wait_times, wait_time_dict, scale_factor=1, run_time=1):
        i = 0
        angle = 180
        surround_circles = [0] * len(graph)
        order_index = 0
        new_highlights = []
        for element in full_order:
            if isinstance(element, int):
                surround_circle = self.highlight_node(graph, element,
                                                      start_angle=angle/360 * TAU, scale_factor=scale_factor, run_time=run_time)
                # print(type(graph[element].data), type(order[order_index]))
                # print(f"element: {element} \t graph[element]: {graph[element].data}")
                # print(f"order_index: {order_index} \t order[order_index]: {order}")
                self.play(
                    TransformFromCopy(graph[element].data, order[order_index])
                )
                order_index += 1
                self.indicate_neighbors(graph, element, wait_time_dict)
                graph[element].surround_circle = surround_circle
                new_highlights.append(surround_circle)
                self.wait(wait_times[element])
            else:
                last_edge = self.sharpie_edge(edge_dict, element[0], element[1],
                                              scale_factor=scale_factor, run_time=run_time)
                angle = self.find_angle_of_intersection(graph, last_edge.get_end(), element[1])
                new_highlights.append(last_edge)

            i += 1

        return new_highlights

    def indicate_neighbors(self, graph, i, wait_time_dict):
        current_node = graph[i]
        neighbors = current_node.neighbors
        self.wait(wait_time_dict[i])
        self.play(
            *[CircleIndicate(neighbor.circle) for neighbor in neighbors],
            run_time=2
        )

    def highlight_node(self, graph, index, color=GREEN_SCREEN,
                       start_angle=TAU/2, scale_factor=1, animate=True, run_time=1):
        node = graph[index]
        # surround_circle = Circle(radius=node.circle.radius * scale_factor, TAU=-TAU, start_angle=start_angle)
        surround_circle = Circle(radius=node.circle.radius * scale_factor)
        surround_circle.move_to(node.circle.get_center())
        # surround_circle.scale(1.15)
        surround_circle.set_stroke(width=8 * scale_factor)
        surround_circle.set_color(color)
        surround_circle.set_fill(opacity=0)
        if animate:
            self.play(
                ShowCreation(surround_circle),
                run_time=run_time
            )
        return surround_circle

    def sharpie_edge(self, edge_dict, u, v, color=GREEN_SCREEN,
                     scale_factor=1, animate=True, run_time=1):
        print(edge_dict)
        switch = False
        if u > v:
            edge = edge_dict[(v, u)]
            switch = True
        else:
            edge = edge_dict[(u, v)]

        if not switch:
            line = Line(edge.get_start(), edge.get_end())
        else:
            line = Line(edge.get_end(), edge.get_start())
        line.set_stroke(width=16 * scale_factor)
        line.set_color(color)
        if animate:
            self.play(
                ShowCreation(line),
                run_time=run_time
            )
        return line

    def find_angle_of_intersection(self, graph, last_point, node_index):
        node = graph[node_index]
        distances = []
        for angle in range(360):
            respective_line = Line(node.circle.get_center(),
                                   node.circle.get_center() + RIGHT * node.circle.radius)
            rotate_angle = angle / 360 * TAU
            respective_line.rotate(rotate_angle, about_point=node.circle.get_center())
            end_point = respective_line.get_end()
            distance = np.linalg.norm(end_point - last_point)
            distances.append(distance)
        return np.argmin(np.array(distances))


def dfs(graph, start):
    """
    Returns a list of vertices and edges in preorder traversal
    """
    dfs_order = []
    marked = [False] * len(graph)
    edge_to = [None] * len(graph)

    stack = [start]
    while len(stack) > 0:
        node = stack.pop()
        if not marked[node]:
            marked[node] = True
            dfs_order.append(node)
        for neighbor in graph[node].neighbors:
            neighbor_node = int(neighbor.char)
            if not marked[neighbor_node]:
                edge_to[neighbor_node] = node
                stack.append(neighbor_node)

    # print(dfs_order)
    dfs_full_order = []
    for i in range(len(dfs_order) - 1):
        prev, curr = dfs_order[i], dfs_order[i + 1]
        dfs_full_order.append(prev)
        dfs_full_order.append((edge_to[curr], curr))

    dfs_full_order.append(curr)
    # print(dfs_full_order)
    return dfs_full_order
