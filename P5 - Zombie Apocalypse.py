"""
Student portion of Zombie Apocalypse mini-project
"""

import poc_grid
import poc_queue
import poc_zombie_gui


EMPTY = 0
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = "obstacle"
HUMAN = "human"
ZOMBIE = "zombie"


class Zombie(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list=None, \
                 zombie_list=None, human_list=None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)
        else:
            self._human_list = []

    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        poc_grid.Grid.clear(self)
        self._zombie_list = []
        self._human_list = []

    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row, col))

    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)

    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        return (zombie for zombie in self._zombie_list)

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row, col))

    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)

    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        return (human for human in self._human_list)

    def compute_distance_field(self, entity_type):
        """
        Function computes a 2D distance field
        Distance at member of entity_queue is zero
        Shortest paths avoid obstacles and use distance_type distances
        """

        visited = poc_grid.Grid(self.get_grid_height(), self.get_grid_width())
        for row in range(self.get_grid_height()):
            for col in range(self.get_grid_width()):
                if not self.is_empty(row, col):
                    visited.set_full(row, col)
        distance_field = [[self.get_grid_height() * self.get_grid_width() \
            for dummy_col in range(self.get_grid_width())] \
            for dummy_row in range(self.get_grid_height())]
        entity_cells = self._zombie_list \
            if entity_type is ZOMBIE \
            else self._human_list
        boundary = poc_queue.Queue()
        for entity_cell in entity_cells:
            visited.set_full(entity_cell[0], entity_cell[1])
            distance_field[entity_cell[0]][entity_cell[1]] = 0
            boundary.enqueue(entity_cell)

        while len(boundary) > 0:
            current = boundary.dequeue()
            neighbors = self.four_neighbors(current[0], current[1])
            distance = distance_field[current[0]][current[1]] + 1
            for neighbor in neighbors:
                if visited.is_empty(neighbor[0], neighbor[1]):
                    if distance < distance_field[neighbor[0]][neighbor[1]]:
                        distance_field[neighbor[0]][neighbor[1]] = distance
                    visited.set_full(neighbor[0], neighbor[1])
                    boundary.enqueue(neighbor)

        return distance_field

    def move_humans(self, zombie_distance):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        for index, human_cell in enumerate(self._human_list):
            safest_cell = human_cell
            safest_distance = zombie_distance[human_cell[0]][human_cell[1]]
            neighbors = self.eight_neighbors(human_cell[0], human_cell[1])
            for neighbor_cell in neighbors:
                if not self.is_empty(neighbor_cell[0], neighbor_cell[1]):
                    continue
                distance = zombie_distance[neighbor_cell[0]][neighbor_cell[1]]
                if distance > safest_distance:
                    safest_cell = neighbor_cell
                    safest_distance = distance
            self._human_list[index] = safest_cell

    def move_zombies(self, human_distance):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        for index, zombie_cell in enumerate(self._zombie_list):
            nearest_cell = zombie_cell
            nearest_distance = human_distance[zombie_cell[0]][zombie_cell[1]]
            neighbors = self.four_neighbors(zombie_cell[0], zombie_cell[1])
            for neighbor_cell in neighbors:
                if not self.is_empty(neighbor_cell[0], neighbor_cell[1]):
                    continue
                distance = human_distance[neighbor_cell[0]][neighbor_cell[1]]
                if distance < nearest_distance:
                    nearest_cell = neighbor_cell
                    nearest_distance = distance
            self._zombie_list[index] = nearest_cell



# poc_zombie_gui.run_gui(Zombie(30, 40))