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
    
    def siguientecelda(self):
        """
        Función que envía al limpiador a una celda cercana de forma aleatoria
        """
        
        # Busca celdas limpias para mover al limpiador
        ubirandom = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False)
        
        # Escoge una celda limpia aleatoria
        nuevaubi = self.random.choice(ubirandom)
        
        # Se mueve al limpiador a la celda seleccionada
        self.model.grid.siguientecelda_agent(self, nuevaubi)

    def limpiar(self, agent): 
        """
        Se encarga de limpiar la celda sucia
        """
        self.model.grid.remove_agent(agent)
        self.model.celdaslimpias += 1

    def movimiento(self):
        """
        Define el movimiento de los limpiadores, ya sea para limpiar o moverse
        """
        gridContent = self.model.grid.get_cell_list_contents([self.pos])
        sucio = False
        elementoSucio = None
        
        # Busca celdas sucias
        for element in gridContent:
            if isinstance(element, CeldasSucias):
                sucio = True
                elementoSucio = element
        # Si no se encuentra basura mover al agente
        if not sucio:
            LimpiadorAgente.pasostotales += 1
            self.siguientecelda()
        # Si se encuentra basura, eliminarla
        else:
            self.limpiar(elementoSucio)

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
        self.dirtyCells = int((celdassucias * (n*m)) / 100)
        # Número de celdas que han sido limpiadas
        self.celdasLimpias = 0
        # Schedule
        self.schedule = RandomActivation(self)
        # Estado de la simulación
        self.running = True
        # Bool que representa si ya se terminó de limpiar toda la basura
        self.cleanLimit = False
        
        # Creación de agentes aspiradoras
        for i in range(0,self.numAgents):
            # Crear agente y agregarlo al schedule
            a = LimpiadorAgente(i, self)
            self.schedule.add(a)
            
            # Colocar al agente en la posición (1,1)
            self.grid.place_agent(a, (1, 1))

        
        # Creación de celdas sucias por medio de un set
        dirtyCells = set()
        for t in range(self.numAgents+1,self.dirtyCells+self.numAgents+1):
            # Crear agente basura y agregarlo al schedule
            b = CeldasSucias(t,self)
            self.schedule.add(b)
            LimpiadorAgente.pasostotales = 0
            # Establecer coordenadas aleatorias para la basura
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            
            # Evitar poner doble basura en una misma celda
            while (x,y) in dirtyCells:
                x = self.random.randrange(self.grid.width)
                y = self.random.randrange(self.grid.height)
            dirtyCells.add((x,y))
                        
            # Colocar el agente en su posición
            self.grid.place_agent(b, (x, y))


    def step(self): #Cambiar nombre de función
        """
        Representación de cada paso de la simulación
        """
        # Determinar si ya se limpiaron todas las celdas
        if(self.celdasLimpias == self.dirtyCells):
            self.cleanLimit = True

        # Imprimir la información solicitada sobre la corrida del modelo
        if(self.cleanLimit or self.tle == self.stepsTime):
                self.running = False

                if(self.cleanLimit):
                    print("\nTodas las celdas están limpias \n")
                else:
                    print("Se ha agotado el tiempo límite")

                print("Tiempo transcurrido: " + str(self.stepsTime) + " steps, Porcentaje de celdas limpiadas: " + str(int((self.cleanCells*100)/self.dirtyCells))+ "%")
                print("Número de movimientos: " + str(LimpiadorAgente.pasostotales))
        # Hacer que todos los agentes den un paso (determinado en sus respectivos modelos)
        else:
            self.stepsTime += 1
            self.schedule.step()