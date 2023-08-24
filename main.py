from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder


class Trash(Agent):
    def __init__(self, model, pos):
        super().__init__(model.next_id(), model)
        self.pos = pos

    def step(self):
        pass


class Robot(Agent):
    def __init__(self, model, pos):
        super().__init__(model.next_id(), model)
        self.pos = pos
        self.count = 1

        self.matrix = [
            [1 if i == 0 or i == 24 or j == 0 or j == 24 else 0 for j in range(25)]
            for i in range(25)
        ]
        self.matrix1 = [[0 for _ in range(51)] for _ in range(51)]



    def findPath(self):
        grid1 = Grid(matrix=self.matrix1)
        start = grid1.node(self.pos[0], self.pos[1])
        end = grid1.node(25, 25)
        finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
        path, runs = finder.find_path(start, end, grid1)
        print(path)
        if self.count < (len(path)):
            self.model.grid.move_agent(self, path[self.count])
            print(path[self.count])
            self.count += 1

    def step(self):
        trash = self.model.schedule.agents[1].pos
        next_moves = self.model.grid.get_neighborhood(self.pos, moore=False)
        while True:
            possible_next_move = self.random.choice(next_moves)
            mat_coords = self.matrix[possible_next_move[1]][possible_next_move[0]]
            if mat_coords != 1:
                next_move = possible_next_move
                break

        if self.pos == trash:
            grid1 = Grid(matrix=self.matrix1)
            print(grid1)
            start = grid1.node(11, 12)
            end = grid1.node(25, 25)
            finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
            path, runs = finder.find_path(start, end, grid1)
            print(path)
            print(self.pos)
            if self.count < (len(path)):
                self.model.grid.move_agent(self, path[self.count])
                self.model.grid.move_agent(self.model.schedule.agents[1], self.pos)
                print(path[self.count])
                self.count += 1
        else:
            self.model.grid.move_agent(self, next_move)
            self.model.grid.move_agent(self.model.schedule.agents[1], self.pos)



class WallBlock(Agent):
    def __init__(self, model, pos):
        super().__init__(model.next_id(), model)
        self.pos = pos

    def step(self):
        pass


class Incinerador(Agent):
    def __init__(self, model, pos):
        super().__init__(model.next_id(), model)
        self.pos = pos

    def step(self):
        pass


class Maze(Model):
    def __init__(self):
        super().__init__()

        self.schedule = RandomActivation(self)
        self.grid = MultiGrid(51, 51, torus=False)

        robot = Robot(self, (12, 12))
        incinerador = Incinerador(self, (25, 25))
        trash = Trash(self, (11, 12))
        wallblock = WallBlock(self, (0, 0))

        self.grid.place_agent(robot, robot.pos)
        self.grid.place_agent(incinerador, incinerador.pos)
        self.grid.place_agent(trash, trash.pos)

        self.schedule.add(robot)
        self.schedule.add(trash)
        self.schedule.add(incinerador)

        matrix = [
            [1 if i == 0 or i == 24 or j == 0 or j == 24 else 0 for j in range(25)]
            for i in range(25)
        ]

        for y in range(len(matrix)):
            for x in range(len(matrix[0])):
                if matrix[y][x] == 1:
                    self.grid.place_agent(wallblock, ((x), (y)))
                    self.grid.place_agent(wallblock, ((x + 26), (y)))
                    self.grid.place_agent(wallblock, ((x), (y + 26)))
                    self.grid.place_agent(wallblock, ((x + 26), (y + 26)))

    def step(self):
        self.schedule.step()


def agent_portrayal(agent):
    if type(agent) == Robot:
        return {"Shape": "robot.png", "Layer": 0}
    elif type(agent) == WallBlock:
        return {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Color": "Blue", "Layer": 0}
    elif type(agent) == Incinerador:
        return {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Color": "Red", "Layer": 0}
    elif type(agent) == Trash:
        return {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Color": "Black", "Layer": 0}


grid = CanvasGrid(agent_portrayal, 51, 51, 700, 700)

server = ModularServer(Maze, [grid], "Robot", {})
server.port = 8522
server.launch()
