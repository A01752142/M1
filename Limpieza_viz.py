from Limpieza import *
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

#Vosualización de agentes (celdas sucias y limpiador)
def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "r":0.5}

    # Distinción entre agente Aspiradora y Basura
    if isinstance(agent, LimpiadorAgente):
        portrayal["Color"] = "green"
        portrayal["Layer"] = 0.7
    else:
        portrayal["Color"] = "brown"
        portrayal["Layer"] = 0.5
        portrayal["r"] = 0.2
    return portrayal

#Datos iniciales
n = 20 #Ancho
m = 20 #Alto
numAgents = 4 #Agentes (Limpiadores)
celdassucias = 70 #Celdas sucias
tiempoejecucion = 200 #Tiempo máximo de ejecución


#Inicializar el servidor con base a los parametros
grid = CanvasGrid(agent_portrayal, n, m, 750, 750)
server = ModularServer(LimpiezaModel,
                       [grid],
                       "M1 Activity",
                       {"n": n,
                        "m": m,
                        "numAgents": numAgents,
                        "celdassucias": celdassucias,
                        "tiempoejecucion": tiempoejecucion})
server.port = 8521
server.launch()

