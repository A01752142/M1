#Autoras:
#Sandra Ximena Téllez Olvera A01752142
#Naomi Anciola Calderón A01750363

from mesa import Agent,Model #Cada modelo puede contener múltiples agentes y todos ellos son instancias de la clase `Agent`.
from mesa.space import SingleGrid #Para que haya un solo agente por celda
from mesa.time import SimultaneousActivation #Para que los agentes se activen al mismo tiempo
import numpy as np

class EstadoMesas(Agent):
    #Representa a un agente en una celda, si la mesa esta limpia o sucia
    def __init__(self, unique_id, model):
        #Elije un valor aleatorio 1 o 0, para asignar un estado
        super().__init__(unique_id, model)
        self.live = np.random.choice([0,1])
        self.next_state = None

    def step(self):
        live_neighbours = 0   
        neighbours = self.model.grid.get_neighbors(
            self.pos,
            moore=True,
            include_center=False)

        for neighbor in neighbours:
            live_neighbours = live_neighbours + neighbor.live

        self.next_state = self.live
        if self.next_state == 1:
            if live_neighbours < 2 or live_neighbours > 3:
                self.next_state = 0
        else:
            if live_neighbours == 3:
                self.next_state = 1

    def advance(self):
        self.live = self.next_state


class GameLifeModel(Model):
    '''
    Define el modelo del juego de la vida.
    '''
    def __init__(self, width, height):
        self.num_agents = width * height
        self.grid = SingleGrid(width, height, True)
        self.schedule = SimultaneousActivation(self)
        self.running = True #Para la visualizacion usando navegador
        
        for (content, x, y) in self.grid.coord_iter():
            a = GameLifeAgent((x, y), self)
            self.grid.place_agent(a, (x, y))
            self.schedule.add(a)
        
    
    def step(self):
        self.schedule.step()
