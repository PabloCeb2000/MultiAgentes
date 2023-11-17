import mesa 
import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.pylab as plt
import json
from Evidencia1_script import mesa, CalleModel

def batch():
    paramas = {"width": 24, "height": 24}
    results = mesa.batch_run(
        CalleModel,
        parameters=paramas,
        iterations=10,
        max_steps=100,
        number_processes=1,
        data_collection_period=1,
        display_progress=True,
    )

    results_df = pd.DataFrame(results)
    #results_df.to_excel("output_E6.xlsx") 

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
        portrayal = {"Shape": "rect", "Filled": "true", "h": 1.0, "w": 1.0, "Color": "yellow", "Layer": 1}
    if agent.val == 5:
        portrayal = {"Shape": "rect", "Filled": "true", "h": 1.0, "w": 1.0, "Color": "grey", "Layer": 2}
    return portrayal

def main():

    model = CalleModel(24, 24)
    batch()

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
        CalleModel, [grid, chart], "Modelo de Ciudad", {"width": 24, "height": 24}
    )

    server.port = 8521  # The default
    server.launch()

    
    

main()