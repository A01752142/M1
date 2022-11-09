from mesa import Agent, Model
from mesa.datacollection import DataCollector
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.batchrunner import BatchRunner

class CeldasSucias(Agent):
    """
    Muestra las celdas sucias
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

        
class LimpiadorAgente(Agent):
    """
    Muestra los limpiadores y sus id
    """
    pasostotales = 0
    
    def __init__(self, unique_id, model): 
        super().__init__(unique_id, model)
    
    def posicion(self): 
        """
        Esta funcion se encarga de mover a los limpiadores a través de las celdas
        """
        # Busca celdas limpias para cambiar de posición a los limpiadores
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False)
    
        new_position = self.random.choice(possible_steps)

        self.model.grid.move_agent(self, new_position)

    def limpiar(self, agent): 
        """
        Limpiar las celdas
        """
        self.model.grid.remove_agent(agent)
        self.model.celdaslimpias += 1

    def step(self): 
        """
        Le da función a los limpiadores (limpiar o moverse)
        """
        # Obtiene todos los objetos de una celda
        gridContent = self.model.grid.get_cell_list_contents([self.pos])
        sucio = False
        suciedadencelda = None
        
        # Verifica si la celda está limpia o sucia
        for element in gridContent:
            if isinstance(element, CeldasSucias):
                sucio = True
                suciedadencelda = element
        # Si no está sucio, el limpiador se mueve
        if not sucio:
            LimpiadorAgente.pasostotales += 1
            self.posicion()
        # Limpiar si está sucio
        else:
            self.limpiar(suciedadencelda)

class LimpiezaModel(Model): 
    def __init__(self, numAgents, m, n, celdassucias, tiempoejecucion):
        # Generar la cuadricula
        self.grid = MultiGrid(m, n, False)
        # Mostrar cantidad de agentes (Limpiadores)
        self.numAgents = numAgents
        # Tiempo maximo de ejecucion
        self.tle = tiempoejecucion
        # Cantidad de pasos usados para la limpieza
        self.stepsTime = 0
        # Cantidad de celdas sucias
        self.estaSucio = int((celdassucias * (n*m)) / 100)
        # Número de celdas que han sido limpiadas
        self.celdaslimpias = 0
        # Schedule
        self.schedule = RandomActivation(self)
        # Estado
        self.running = True
        # Representa si todas las celdas están limpias o no 
        self.cleanLimit = False
        
        # Creación de limpiadores
        for i in range(0,self.numAgents):
            # Generar limpiadores y agregarlos al grid
            a = LimpiadorAgente(i, self)
            self.schedule.add(a)
            # Posición de inicio del agente
            self.grid.place_agent(a, (1, 1))

        
        # Generación de celdas sucias
        estaSucio = set()
        for t in range(self.numAgents+1,self.estaSucio+self.numAgents+1):
            # Generar celdas sucias y agregarlas al grid
            b = CeldasSucias(t,self)
            self.schedule.add(b)
            LimpiadorAgente.pasostotales = 0
            # Le da una posición aleatoria a las celdas sucias
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            
            # Permite que solo haya una sola celda sucia en cada celda
            while (x,y) in estaSucio:
                x = self.random.randrange(self.grid.width)
                y = self.random.randrange(self.grid.height)
            estaSucio.add((x,y))             
            # Colocar agentes
            self.grid.place_agent(b, (x, y))


    def step(self):
        """
        Obtiene cada paso
        """
        # Saber si todas las celdas están limpias
        if(self.celdaslimpias == self.estaSucio):
            self.cleanLimit = True

        # Saber información valiosa
        if(self.cleanLimit or self.tle == self.stepsTime):
                self.running = False

                if(self.cleanLimit):
                    print("\nSe ha completado la limpieza \n")
                else:
                    print("No todas las celdas están limpias, pero el tiempo se agoto")

                print("Tiempo de ejecucion: " + str(self.stepsTime) + ", El porcentaje de limpieza final es: " + str(int((self.celdaslimpias*100)/self.estaSucio))+ "%")
                print("Los limpiadores se movieron: " + str(LimpiadorAgente.pasostotales) + " veces")
        else:
            self.stepsTime += 1
            self.schedule.step()