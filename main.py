from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder


class WallBlock(Agent):
    def __init__(self, model, pos):
        super().__init__(model.next_id(), model)
        self.pos = pos

    def step(self):
        pass


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
        self.save_pos = (0, 0)
        self.carriesTrash = 1
        self.hasTrash = 0
        self.trashId = 0
        if self.pos == (1,1):
            self.matrix = [
                [1 if i == 0 or i == 24 or j == 0 or j == 24 else 0 for j in range(25)]
                for i in range(25)
            ]
        elif self.pos == (27,27):
            self.matrix = [
                [1 if i == 0 or i == 24 or j == 0 or j == 24 else 0 for j in range(26, 51)]
                for (i) in range(26, 51)
            ]
        self.matrix1 = [[0 for _ in range(51)] for _ in range(51)]

    #         estado incinerador = self.model.schedule.agents[5].estado
    # si estado incinerador es prendido:
    # pass
    # else:
    #       mover a incinerador

    def goToIncinerator(self, current_x, current_y, save_pos, trashId):

        xDistancePos = save_pos[0] - current_x
        yDistancePos = save_pos[1] - current_y

        xDistanceIncinerator = 25 - current_x
        yDistanceIncinerator = 25 - current_y

        if (xDistanceIncinerator >= 2) & (self.carriesTrash == 1) & (xDistanceIncinerator > 0):
            current_x += 1
            self.model.grid.move_agent(self, (current_x, current_y))
            self.model.grid.move_agent(self.model.schedule.agents[trashId], self.pos)

        elif (yDistanceIncinerator >= 2) & (self.carriesTrash == 1) & (yDistanceIncinerator > 0):
            current_y += 1
            self.model.grid.move_agent(self, (current_x, current_y))
            self.model.grid.move_agent(self.model.schedule.agents[trashId], self.pos)

        elif (abs(xDistanceIncinerator) >= 2) & (self.carriesTrash == 1) & (xDistanceIncinerator < 0):
            current_x -= 1
            self.model.grid.move_agent(self, (current_x, current_y))
            self.model.grid.move_agent(self.model.schedule.agents[trashId], self.pos)

        elif (abs(yDistanceIncinerator) >= 2) & (self.carriesTrash == 1) & (yDistanceIncinerator < 0):
            current_y -= 1
            self.model.grid.move_agent(self, (current_x, current_y))
            self.model.grid.move_agent(self.model.schedule.agents[trashId], self.pos)

        else:
            self.carriesTrash = 0
            if (xDistancePos <= -1) & (current_x != save_pos[0]):
                current_x -= 1
                self.model.grid.move_agent(self, (current_x, current_y))

            elif (yDistancePos <= -1) & (current_y != save_pos[1]):
                current_y -= 1
                self.model.grid.move_agent(self, (current_x, current_y))

            elif (xDistancePos >= 1) & (current_x != save_pos[0]):
                current_x += 1
                self.model.grid.move_agent(self, (current_x, current_y))

            elif (yDistancePos >= 1) & (current_y != save_pos[1]):
                current_y += 1
                self.model.grid.move_agent(self, (current_x, current_y))

            else:
                self.hasTrash = 0

    def step(self):
        current_x = self.pos[0]
        current_y = self.pos[1]

        if self.hasTrash != 1:
            for i in range(len(self.model.schedule.agents)):
                if isinstance(self.model.schedule.agents[i], Trash):
                    trash = self.model.schedule.agents[i].pos
                    if self.pos == trash:
                        self.carriesTrash = 1
                        self.hasTrash = 1
                        self.trashId = i
                        self.save_pos = self.pos
                        break

        if self.hasTrash == 1:
            self.goToIncinerator(current_x, current_y, self.save_pos, self.trashId)
        else:
            possible_next_move = (current_x + 1, current_y)
            mat_coords = self.matrix[possible_next_move[0]][possible_next_move[1]]
            if mat_coords != 1:
                next_move = possible_next_move
                self.matrix[possible_next_move[0]][possible_next_move[1]] = 1
                self.model.grid.move_agent(self, next_move)
            else:
                possible_next_move = (current_x, current_y + 1)
                mat_coords = self.matrix[possible_next_move[0]][possible_next_move[1]]
                if mat_coords != 1:
                    next_move = possible_next_move
                    self.matrix[possible_next_move[0]][possible_next_move[1]] = 1
                    self.model.grid.move_agent(self, next_move)
                else:
                    possible_next_move = (current_x - 1, current_y)
                    mat_coords = self.matrix[possible_next_move[0]][possible_next_move[1]]
                    if mat_coords != 1:
                        next_move = possible_next_move
                        self.matrix[possible_next_move[0]][possible_next_move[1]] = 1
                        self.model.grid.move_agent(self, next_move)
                    else:
                        possible_next_move = (current_x, (current_y - 1))
                        mat_coords = self.matrix[possible_next_move[0]][possible_next_move[1]]
                        if mat_coords != 1:
                            next_move = possible_next_move
                            self.matrix[possible_next_move[0]][possible_next_move[1]] = 1
                            self.model.grid.move_agent(self, next_move)

    # if self.pos == trash:
    # self.model.grid.move_agent(self.model.schedule.agents[1], self.pos)


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

        robot = Robot(self, (1, 1))
      #  robot1 = Robot(self, (27, 27))

        incinerador = Incinerador(self, (25, 25))
        trash = Trash(self, (10, 1))
        trash1 = Trash(self, (11, 1))
        trash2 = Trash(self, (11, 15))
        wallblock = WallBlock(self, (0, 0))

        self.grid.place_agent(robot, robot.pos)
    #    self.grid.place_agent(robot1, robot1.pos)

        self.grid.place_agent(incinerador, incinerador.pos)
        self.grid.place_agent(trash, trash.pos)
        self.grid.place_agent(trash2, trash2.pos)
        self.grid.place_agent(trash1, trash1.pos)

        self.schedule.add(robot)
      #  self.schedule.add(robot1)

        self.schedule.add(trash)
        self.schedule.add(trash1)
        self.schedule.add(trash2)
        self.schedule.add(incinerador)

        matrix = [
            [1 if i == 0 or i == 24 or j == 0 or j == 24 else 0 for j in range(25)]
            for i in range(25)
        ]

        for y in range(len(matrix)):
            for x in range(len(matrix[0])):
                if matrix[y][x] == 1:
                    self.grid.place_agent(wallblock, (x, y))
                    self.grid.place_agent(wallblock, ((x + 26), y))
                    self.grid.place_agent(wallblock, (x, (y + 26)))
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
