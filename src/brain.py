import numpy as np
from hyperparameters import mutation_rate, brain_size

# accelerate with 1 in given direction

class Brain:
    """
    This is the brain of each ball.

    The chromosome is defined as directions.
    The chromosome is a vector with given size.
    Each item in the chromosome is in the range [0, 2pi]
    """

    def __init__(self):
        self.size = brain_size
        self.step = 0
        self.directions = np.zeros(self.size, dtype=float)

    def randomize(self):
        self.directions = 2 * np.pi * np.random.rand(self.size)
        return self.directions

    def mutate(self):
        dirs = []
        for i in range(self.size):
            rand = np.random.rand()
            if rand <= mutation_rate:
                dirs.append(2*np.pi*np.random.rand())
            else:
                dirs.append(self.directions[i])
        self.directions = dirs
