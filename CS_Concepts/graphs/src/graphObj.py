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
        self.data = Tex(str(data)).scale(self.nodeScale)
        self.data.move_to(position)
        self.center = position
        self.circle = Circle(radius=self.nodeRadius)
        self.circle.move_to(position)
        self.drawn = False
        self.visited = False

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


graphConfigs = {
    'config1': {
        'adjList': {
            0: [1, 2],
            1: [4],
            2: [3],
            3: [],
            4: [5, 6],
            5: [],
            6: [5]
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
    },
    'config2': {
        'adjList': {
            0: [1, 2],
            1: [2, 4],
            2: [3, 4],
            3: [4],
            4: [3, 2, 5, 6],
            5: [4, 6],
            6: [4, 5]
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

        # Add more configs here (ex different positions, # of nodes)

    }
}


if __name__ == "__main__":
    GraphNode()
