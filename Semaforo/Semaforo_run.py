import mesa 
import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.pylab as plt
import json
from Semaforo_script import mesa, SemaforoModel


def agent_portrayal(agent):

    if agent.val == 0:
        portrayal = {"Shape": "rect", "Filled": "true", "h": 1.0, "w": 1.0, "Color": "blue", "Layer": 1}
    if agent.val == 1:
        portrayal = {"Shape": "rect", "Filled": "true", "h": 1.0, "w": 1.0, "Color": "green", "Layer": 1}
    if agent.val == 2:
        portrayal = {"Shape": "rect", "Filled": "true", "h": 1.0, "w": 1.0, "Color": "red", "Layer": 1}
    if agent.val == 3:
        portrayal = {"Shape": "rect", "Filled": "true", "h": 1.0, "w": 1.0, "Color": "brown", "Layer": 1}
    if agent.val == 4:
        portrayal = {"Shape": "rect", "Filled": "true", "h": 1.0, "w": 1.0, "Color": "black", "Layer": 1}
    if agent.val == 5:
        portrayal = {"Shape": "rect", "Filled": "true", "h": 1.0, "w": 1.0, "Color": "grey", "Layer": 2}
    if agent.val == 6:
        portrayal = {"Shape": "rect", "Filled": "true", "h": 1.0, "w": 1.0, "Color": "yellow", "Layer": 1}
    return portrayal

def main():

    model = SemaforoModel(24, 24)

    """
    for i in range(100):
        model.step()
        print(model.get_agent_position()) 
    """
    grid = mesa.visualization.CanvasGrid(agent_portrayal, 24, 24)
    
    chart = mesa.visualization.ChartModule(
        [{"Label": "pasos", "Color": "black", }], 
        data_collector_name = "datacollector"
    )
    server = mesa.visualization.ModularServer(
        SemaforoModel, [grid, chart], "Modelo de Ciudad", {"width": 24, "height": 24}
    )

    server.port = 8521  # The default
    server.launch()

main()