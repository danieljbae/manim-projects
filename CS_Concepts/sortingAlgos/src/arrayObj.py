from manim import *


class ArrayMobj:
    def __init__(self, values):
        self.values = values
        self

        pass


arrayConfigs = {
    'simpleConfig': {
        'values': [6, 2, 5, 1, 3],
        # 'positions': {
        #     0: LEFT * 4 + UP * 2,
        #     1: LEFT * 2 + UP * 2,
        #     2: LEFT * 4 + DOWN * 2,
        #     3: LEFT * 2 + DOWN * 2,
        #     4: RIGHT * 2 + UP * 2,
        #     5: RIGHT * 4 + UP * 2,
        #     6: RIGHT * 4 + DOWN * 2
        # }
    },
    # Add more configs here (ex different positions, # of nodes)

}

if __name__ == "__main__":
    ArrayMobj()
