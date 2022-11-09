import mesa

class Suciedad(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)


class LimpiadorAgent(mesa.Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)



    def step(self):
        
        x, y = self.pos
        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        if isinstance(this_cell, suciedad):
            suciedad = this_cell
        if len(suciedad) > 0:
            self.model.grid.remove_agent(suciedad)
            self.model.schedule.remove(suciedad)


        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False)

        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)


class Modelo(mesa.Model):

    def __init__(self, N, porcentaje, tiempo_maximo):
        for i in range(N):
            self.grid.place_agent(LimpiadorAgent, (1, 1))


        self.grid = mesa.space.MultiGrid(width, height, True)
        self.num_agents = N
        celdassucias = (width * height) * porcentaje/100
        # inicializa celdas sucias
        for i in range(celdassucias):
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(Suciedad, (x, y))

        self.schedule = mesa.time.RandomActivation(self)


        # Create agents
        for i in range(self.num_agents):
            a = LimpiadorAgent(i, self)
            self.schedule.add(a)
            self.grid.place_agent(agente, (1, 1))

    def step(self):
        if tiempo < tiempo_maximo:
            self.schedule.step()