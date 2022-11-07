#Autoras:
#Sandra Ximena Téllez Olvera A01752142
#Naomi Anciola Calderón A01750363

from Limpieza import *
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

#Definición de agentes
def celdas(agent):
    portrayal = {"Shape": "square",
                 "Filled": "true",
                 "Layer": 0,
                 "Color": "red"
                 }

    if celdas.dirty == 1: #En caso de que las mesas estén sucias
        portrayal["Colour"] = "red"
        portrayal["Layer"] = 0
    else: #Si las mesas están limpias
        portrayal["Color"] = "blue"
        portrayal["Layer"] = 1

    return portrayal

#def limpiador(agent):
 #   portrayal = {"Shape": "circle",
  #               "Filled": "true",
   #              "Layer": 0,
    #             "Color": "green",
     #            "r":0.5
      #           }

#Definición del Grid
ancho = 50
alto = 30
grid = CanvasGrid(celdas, ancho, alto, 750, 750)

#Launch
server = ModularServer(Limpiar,
                       [grid],
                       "Cleaning tables",
                       {"width":ancho, "height":alto})
server.port = 8521 # The default
server.launch()