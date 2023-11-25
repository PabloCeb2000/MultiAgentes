import mesa 
import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.pylab as plt
import json
from Semaforo_script_I import mesa, SemaforoModel
from Semaforo_script_N import mesa, SemaforoModelN

def batch():
    paramas = {"width": 24, "height": 24}
    results = mesa.batch_run(
        SemaforoModel,
        parameters=paramas,
        iterations=100,
        max_steps=100,
        number_processes=1,
        data_collection_period=1,
        display_progress=True,
    )

    results2 = mesa.batch_run(
        SemaforoModelN,
        parameters=paramas,
        iterations=100,
        max_steps=100,
        number_processes=1,
        data_collection_period=1,
        display_progress=True,
    )


    results_df = pd.DataFrame(results)
    results2_df = pd.DataFrame(results2)

    results_df = results_df.drop('width', axis=1)
    results_df = results_df.drop('height', axis=1)
    results_df = results_df.drop('RunId', axis=1)
    results_df = results_df.drop('Autos', axis=1)

    results2_df = results2_df.drop('width', axis=1)
    results2_df = results2_df.drop('height', axis=1)
    results2_df = results2_df.drop('RunId', axis=1)
    results2_df = results2_df.drop('Autos', axis=1)

    print(results_df)
    print(results2_df)

    result_df_2_np = results_df.drop_duplicates('iteration', keep='last')
    result2_df_2_np = results2_df.drop_duplicates('iteration', keep='last')

    print(result_df_2_np)
    print(result2_df_2_np)


    total = ['Step']
    promedio_total = result_df_2_np[total].mean()
    promedio_total2 = result2_df_2_np[total].mean()

    promedio_total_n = float(promedio_total)
    promedio_total2_n = float(promedio_total2)

    print(promedio_total_n)
    print(promedio_total2_n)

    fig, ax = plt.subplots()

    columas_promedio = [promedio_total_n, promedio_total2_n]
    nombres = ['Semaforo Inteligente', 'Semaforo Normal']


    ax.bar(nombres, columas_promedio)
    ax.set_ylabel('Pasos Totales')
    ax.set_title('Promedio de pasos con distintos tipos de semaforos')
    
    
    plt.show()


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
        SemaforoModel, [grid, chart], "Modelo de Ciudad", {"width": 24, "height": 24}
    )

    server.port = 8521  # The default
    server.launch()


main()
