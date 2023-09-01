from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import Slider
from mesa.visualization.UserParam import Checkbox

gridnum = 51


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


class RobotIncinerador(Agent):
    def __init__(self, model, pos, num):
        super().__init__(model.next_id(), model)
        self.pos = pos
        self.counter = 0
        self.movement = 0
        self.hasTrash = 0
        self.save_pos = (0, 0)
        self.trashId = 0
        self.carriesTrash = 1
        self.gridnum = num

    def goToIncinerator(self, save_pos, trashId):
        if self.carriesTrash == 1:
            agents_in_target_square = self.model.grid.get_cell_list_contents([
                                                                             (int((self.gridnum - 1) / 2), int((self.gridnum - 1) / 2))])
            for agent in agents_in_target_square:
                if isinstance(agent, Trash):
                    break
                    pass
            else:
                self.model.grid.move_agent(
                    self, (int((self.gridnum - 1) / 2), int((self.gridnum - 1) / 2)))
                self.model.grid.move_agent(
                    self.model.schedule.agents[trashId], self.pos)
                self.carriesTrash = 0
        else:
            self.model.grid.move_agent(self, save_pos)
            self.hasTrash = 0

    def step(self):
        if self.hasTrash != 1:
            for i in range(len(self.model.schedule.agents)):
                if isinstance(self.model.schedule.agents[i], Trash):
                    trash = self.model.schedule.agents[i].pos
                    if (self.pos == trash) & (self.pos != (int((self.gridnum - 1) / 2), int((self.gridnum - 1) / 2))):
                        self.carriesTrash = 1
                        self.hasTrash = 1
                        self.trashId = i
                        self.save_pos = self.pos
                        break

        if self.hasTrash == 1:
            self.goToIncinerator(self.save_pos, self.trashId)
        else:
            current_x = self.pos[0]
            current_y = self.pos[1]
            if self.movement == 0:
                self.counter += 1
                self.model.grid.move_agent(self, (current_x, current_y + 1))
                if self.counter == 2:
                    self.movement = 1
                    self.counter = 0
            elif self.movement == 1:
                self.counter += 1
                self.model.grid.move_agent(self, (current_x - 1, current_y))
                if self.counter == 2:
                    self.movement = 2
                    self.counter = 0
            elif self.movement == 2:
                self.counter += 1
                self.model.grid.move_agent(self, (current_x, current_y - 1))
                if self.counter == 2:
                    self.movement = 3
                    self.counter = 0
            elif self.movement == 3:
                self.counter += 1
                self.model.grid.move_agent(self, (current_x + 1, current_y))
                if self.counter == 2:
                    self.movement = 0
                    self.counter = 0


class Robot(Agent):
    def __init__(self, model, pos, num):
        super().__init__(model.next_id(), model)
        self.pos = pos
        self.count = 1
        self.save_pos = (0, 0)
        self.carriesTrash = 1
        self.hasTrash = 0
        self.trashId = 0
        self.gridnum = num

        if self.pos == (0, 0):
            self.matrix = [[0 for _ in range(self.gridnum + 1)]
                           for _ in range(self.gridnum + 1)]
            for row in self.matrix:
                row[int((self.gridnum - 1) / 2)] = 1

            # Creating the horizontal line
            self.matrix[int((self.gridnum - 1) / 2)] = [1] * self.gridnum

            self.matrix[int((self.gridnum - 1) / 2) -
                        1][int((self.gridnum - 1) / 2) - 1] = 1
            self.matrix[int((self.gridnum - 1) / 2) +
                        1][int((self.gridnum - 1) / 2) - 1] = 1
            self.matrix[int((self.gridnum - 1) / 2) -
                        1][int((self.gridnum - 1) / 2) + 1] = 1
            self.matrix[int((self.gridnum - 1) / 2) +
                        1][int((self.gridnum - 1) / 2) + 1] = 1
            self.matrix[0][0] = 1
            self.matrix[(self.gridnum - 1)][self.gridnum - 1] = 1
            self.matrix[0][(self.gridnum - 1)] = 1
            self.matrix[(self.gridnum - 1)][0] = 1
        elif self.pos == (self.gridnum - 1, 0):
            self.matrix = [[0 for _ in range(self.gridnum+1)]
                           for _ in range(self.gridnum+1)]
            for row in self.matrix:
                row[int((self.gridnum - 1) / 2)] = 1

            # Creating the horizontal line
            self.matrix[int((self.gridnum - 1) / 2)] = [1] * self.gridnum

            self.matrix[int((self.gridnum - 1) / 2) -
                        1][int((self.gridnum - 1) / 2) - 1] = 1
            self.matrix[int((self.gridnum - 1) / 2) +
                        1][int((self.gridnum - 1) / 2) - 1] = 1
            self.matrix[int((self.gridnum - 1) / 2) -
                        1][int((self.gridnum - 1) / 2) + 1] = 1
            self.matrix[int((self.gridnum - 1) / 2) +
                        1][int((self.gridnum - 1) / 2) + 1] = 1
            self.matrix[int((self.gridnum - 1) / 2)
                        ][int((self.gridnum - 1) / 2) - 1] = 1
            self.matrix[0][0] = 1
            self.matrix[(self.gridnum - 1)][(self.gridnum - 1)] = 1
            self.matrix[0][(self.gridnum - 1)] = 1
            self.matrix[(self.gridnum - 1)][0] = 1
        elif self.pos == ((self.gridnum - 1), (self.gridnum - 1)):
            self.matrix = [[0 for _ in range(self.gridnum+1)]
                           for _ in range(self.gridnum+1)]
            for row in self.matrix:
                row[int((self.gridnum - 1) / 2) - 1] = 1

            # Creating the horizontal line
            self.matrix[int((self.gridnum - 1) / 2) - 1] = [1] * self.gridnum

            self.matrix[int((self.gridnum - 1) / 2) -
                        1][int((self.gridnum - 1) / 2) - 1] = 1
            self.matrix[int((self.gridnum - 1) / 2) +
                        1][int((self.gridnum - 1) / 2) - 1] = 1
            self.matrix[int((self.gridnum - 1) / 2) -
                        1][int((self.gridnum - 1) / 2) + 1] = 1
            self.matrix[int((self.gridnum - 1) / 2) +
                        1][int((self.gridnum - 1) / 2) + 1] = 1
            self.matrix[0][0] = 1
            self.matrix[(self.gridnum - 1)][(self.gridnum - 1)] = 1
            self.matrix[0][(self.gridnum - 1)] = 1
            self.matrix[(self.gridnum - 1)][0] = 1
        elif self.pos == (0, (self.gridnum - 1)):
            self.matrix = [[0 for _ in range(self.gridnum+1)]
                           for _ in range(self.gridnum+1)]
            for row in self.matrix:
                row[int((self.gridnum - 1) / 2) - 1] = 1

            # Creating the horizontal line
            self.matrix[int((self.gridnum - 1) / 2)] = [1] * self.gridnum

            self.matrix[int((self.gridnum - 1) / 2) -
                        1][int((self.gridnum - 1) / 2) - 1] = 1
            self.matrix[int((self.gridnum - 1) / 2) +
                        1][int((self.gridnum - 1) / 2) - 1] = 1
            self.matrix[int((self.gridnum - 1) / 2) -
                        1][int((self.gridnum - 1) / 2) + 1] = 1
            self.matrix[int((self.gridnum - 1) / 2) +
                        1][int((self.gridnum - 1) / 2) + 1] = 1
            self.matrix[0][0] = 1
            self.matrix[(self.gridnum - 1)][(self.gridnum - 1)] = 1
            self.matrix[0][(self.gridnum - 1)] = 1
            self.matrix[(self.gridnum - 1)][0] = 1

    #         estado incinerador = self.model.schedule.agents[5].estado
    # si estado incinerador es prendido:
    # pass
    # else:
    #       mover a incinerador

    def goToIncinerator(self, current_x, current_y, save_pos, trashId, num):

        xDistancePos = save_pos[0] - current_x
        yDistancePos = save_pos[1] - current_y

        xDistanceIncinerator = int((num - 1) / 2) - current_x
        yDistanceIncinerator = int((num - 1) / 2) - current_y

        if (xDistanceIncinerator >= 2) & (self.carriesTrash == 1) & (xDistanceIncinerator > 0):
            current_x += 1
            if (not self.model.grid.is_cell_empty((current_x, current_y))) & (abs(yDistanceIncinerator) < 2) & (
                    abs(xDistanceIncinerator) < 2):
                pass
            else:
                self.model.grid.move_agent(self, (current_x, current_y))
                self.model.grid.move_agent(
                    self.model.schedule.agents[trashId], self.pos)

        elif (yDistanceIncinerator >= 2) & (self.carriesTrash == 1) & (yDistanceIncinerator > 0):
            current_y += 1
            if (not self.model.grid.is_cell_empty((current_x, current_y))) & (abs(yDistanceIncinerator) < 2) & (
                    abs(xDistanceIncinerator) < 2):
                pass
            else:
                self.model.grid.move_agent(self, (current_x, current_y))
                self.model.grid.move_agent(
                    self.model.schedule.agents[trashId], self.pos)

        elif (abs(xDistanceIncinerator) >= 2) & (self.carriesTrash == 1) & (xDistanceIncinerator < 0):
            current_x -= 1
            if (not self.model.grid.is_cell_empty((current_x, current_y))) & (abs(yDistanceIncinerator) < 2) & (
                    abs(xDistanceIncinerator) < 2):
                pass
            else:
                self.model.grid.move_agent(self, (current_x, current_y))
                self.model.grid.move_agent(
                    self.model.schedule.agents[trashId], self.pos)

        elif (abs(yDistanceIncinerator) >= 2) & (self.carriesTrash == 1) & (yDistanceIncinerator < 0):
            current_y -= 1
            if (not self.model.grid.is_cell_empty((current_x, current_y))) & (abs(yDistanceIncinerator) < 2) & (
                    abs(xDistanceIncinerator) < 2):
                pass
            else:
                self.model.grid.move_agent(self, (current_x, current_y))
                self.model.grid.move_agent(
                    self.model.schedule.agents[trashId], self.pos)

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
        current_x, current_y = self.pos

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
            self.goToIncinerator(current_x, current_y,
                                 self.save_pos, self.trashId, self.gridnum)
        else:
            possible_moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            for dx, dy in possible_moves:
                possible_next_move = (current_x + dx, current_y + dy)
                mat_coords = self.matrix[possible_next_move[0]
                                         ][possible_next_move[1]]
                if mat_coords != 1 and not self.model.grid.out_of_bounds(possible_next_move):
                    next_move = possible_next_move
                    self.matrix[next_move[0]][next_move[1]] = 1
                    self.model.grid.place_agent(
                        WallBlock(self.model, self.pos), self.pos)
                    self.model.grid.move_agent(self, next_move)
                    break


class Incinerador(Agent):
    def __init__(self, model, pos, num):
        super().__init__(model.next_id(), model)
        self.pos = pos
        self.type = 0
        self.gridnum = num

    def step(self):
        self.type = 0
        print(self.gridnum)
        agents_in_target_square = self.model.grid.get_cell_list_contents([
                                                                         (int((self.gridnum) / 2), int((self.gridnum) / 2))])
        for agent in agents_in_target_square:
            if isinstance(agent, Robot):
                break
                pass
            elif isinstance(agent, Trash):
                self.type = 1
                self.model.grid.remove_agent(agent)


class Maze(Model):
    def __init__(self, density=.10, stepslimit=10000, islegal=True):
        super().__init__()

        if(islegal):
            self.gridnum = 21
        else:
            self.gridnum = 51

        self.schedule = RandomActivation(self)
        self.grid = MultiGrid(self.gridnum, self.gridnum, torus=False)

        robot = Robot(self, (0, 0), self.gridnum)
        robot1 = Robot(self, (self.gridnum - 1, 0), self.gridnum)
        robot2 = Robot(self, (0, self.gridnum - 1), self.gridnum)
        robot3 = Robot(
            self, (self.gridnum - 1, self.gridnum - 1), self.gridnum)
        robot4 = RobotIncinerador(
            self, (int((self.gridnum - 1) / 2) + 1, int((self.gridnum - 1) / 2) - 1), self.gridnum)

        incinerador = Incinerador(
            self, (int((self.gridnum - 1) / 2), int((self.gridnum - 1) / 2)), self.gridnum)
        trash = Trash(self, (int((self.gridnum - 1) / 2), 1))
        trash1 = Trash(self, (15, 15))
        trash2 = Trash(self, (int((self.gridnum - 1) / 2), 12))
        trash3 = Trash(self, (int((self.gridnum - 1) / 2) + 1, 1))
        trash4 = Trash(self, (16, 15))
        trash5 = Trash(self, (int((self.gridnum - 1) / 2) + 1, 12))
        wallblock = WallBlock(self, (0, 0))

        self.grid.place_agent(robot, robot.pos)
        self.grid.place_agent(robot1, robot1.pos)
        self.grid.place_agent(robot2, robot2.pos)
        self.grid.place_agent(robot3, robot3.pos)
        self.grid.place_agent(robot4, robot4.pos)

        self.grid.place_agent(incinerador, incinerador.pos)
        self.grid.place_agent(trash, trash.pos)
        self.grid.place_agent(trash2, trash2.pos)
        self.grid.place_agent(trash1, trash1.pos)

        self.grid.place_agent(trash3, trash3.pos)
        self.grid.place_agent(trash4, trash4.pos)
        self.grid.place_agent(trash5, trash5.pos)

        self.schedule.add(robot)
        self.schedule.add(robot1)
        self.schedule.add(robot2)
        self.schedule.add(robot3)
        self.schedule.add(robot4)

        self.schedule.add(trash)
        self.schedule.add(trash1)
        self.schedule.add(trash2)

        self.schedule.add(trash3)
        self.schedule.add(trash4)
        self.schedule.add(trash5)
        self.schedule.add(incinerador)

        self.stepslimit = stepslimit

        for _, (x, y) in self.grid.coord_iter():
            if (self.random.random() * 2) < density:
                trash = Trash(self, (x, y))
                self.grid.place_agent(trash, (x, y))
                self.schedule.add(trash)

    def step(self):
        if(self.schedule.time + 1 > self.stepslimit):
            self.running = False
        self.schedule.step()


def agent_portrayal(agent):
    if type(agent) == Robot:
        return {"Shape": "robot.png", "Layer": 0}
    elif type(agent) == WallBlock:
        return {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Color": "Blue", "Layer": 0}
    elif type(agent) == Trash:
        return {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Color": "Black", "Layer": 0}
    elif type(agent) == RobotIncinerador:
        return {"Shape": "robot.png", "Layer": 0}
    elif (type(agent) == Incinerador) & (agent.type == 1):
        return {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Color": "Orange", "Layer": 1}
    elif type(agent) == Incinerador:
        return {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Color": "Red", "Layer": 0}


grid = CanvasGrid(agent_portrayal, 51, 51, 700, 700)

server = ModularServer(Maze, [grid], "Robot", {
                       "density": Slider("Tree density", 0.45, 0.01, 1.0, 0.01), "stepslimit": Slider("Steps Limiter", 10000, 1, 20000, 10), "islegal": Checkbox("Enable 21 x 21", True)})
server.port = 8522
server.launch()
