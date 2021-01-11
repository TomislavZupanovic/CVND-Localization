

class Localizer(object):
    def __init__(self, grid, prob_hit):
        self.grid = grid
        self.height = len(grid)
        self.width = len(grid[0])
        self.prob_hit = prob_hit
        self.prob_miss = 1.0

    def initialize_dist(self):
        """ Initialize uniform distribution based on grid size """
        distribution = []
        for i in range(self.height):
            row = [1.0 / (self.height * self.width) for _ in range(self.width)]
            distribution.append(row)
        return distribution

    def sense(self, distribution, color):
        """ Senses environment and updates position distribution """
        new_distribution = []
        for i in range(self.height):
            row = [distribution[i][j] * self.prob_hit if color == self.grid[i][j]
                   else distribution[i][j] * self.prob_miss for j in range(self.width)]
            new_distribution.append(row)
        # Normalize
        grid_sum = sum(map(sum, new_distribution))
        for i in range(self.height):
            for j in range(self.width):
                new_distribution[i][j] = new_distribution[i][j] / grid_sum
        return new_distribution
