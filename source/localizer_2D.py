

class Localizer(object):
    def __init__(self, grid, prob_hit, blur_factor):
        self.height = len(grid)
        self.width = len(grid[0])
        self.prob_hit = prob_hit
        self.prob_miss = 1.0
        self.blur_factor = blur_factor

    @staticmethod
    def normalize(grid):
        """ Normalizes the given probabilities grid """
        grid_sum = sum(map(sum, grid))
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                grid[i][j] = grid[i][j] / grid_sum
        return grid

    def initialize_dist(self):
        """ Initialize uniform distribution based on grid size """
        distribution = []
        for i in range(self.height):
            row = [1.0 / (self.height * self.width) for _ in range(self.width)]
            distribution.append(row)
        return distribution

    def sense(self, distribution, color):
        """ Senses environment and updates position distribution based on sensed color """
        new_distribution = []
        for i in range(self.height):
            row = [distribution[i][j] * self.prob_hit if color == self.grid[i][j]
                   else distribution[i][j] * self.prob_miss for j in range(self.width)]
            new_distribution.append(row)
        return self.normalize(new_distribution)

    def move(self, dy, dx, distribution):
        """ Performs the move based on dx and dy, blurs the resulting distribution """
        new_distribution = [[0.0 for _ in range(self.width)] for _ in range(self.height)]
        for i, row in enumerate(distribution):
            for j, column in enumerate(row):
                new_i = int((i + dy) % self.height)
                new_j = int((j + dx) % self.width)
                new_distribution[new_i][new_j] = column
        return self.blur(new_distribution)

    def blur(self, grid):
        """ Performs probability blurring of adjacent cells around center using 3x3 window,
            if blur factor is 0 nothing changes """
        center = 1.0 - self.blur_factor
        corner = self.blur_factor / 12.0
        adjacent = self.blur_factor / 6.0
        window = [[corner, adjacent, corner],
                  [adjacent, center, adjacent],
                  [corner, adjacent, corner]]
        new_grid = [[0.0 for _ in range(self.width)] for _ in range(self.height)]
        for i in range(self.height):
            for j in range(self.width):
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        window_factor = window[dx+1][dy+1]
                        new_i = int((i + dy) % self.height)
                        new_j = int((j + dx) % self.width)
                        new_grid[new_i][new_j] += window_factor * grid[i][j]
        return self.normalize(new_grid)

