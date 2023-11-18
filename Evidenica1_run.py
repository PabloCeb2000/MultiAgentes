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
        iterations=70,
        max_steps=500,
        number_processes=1,
        data_collection_period=1,
        display_progress=True,
    )

    results_df = pd.DataFrame(results)

    results_df = results_df.drop('width', axis=1)
    results_df = results_df.drop('height', axis=1)
    results_df = results_df.drop('RunId', axis=1)

    print(results_df)

    pasos_auto = results_df['Autos'].apply(lambda x: pd.Series(x)).add_prefix('Auto_')

    result_df_2 = pd.concat([results_df, pasos_auto], axis=1)

    result_df_2 = result_df_2.drop('Autos', axis=1)

    print(result_df_2)

    result_df_2_np = result_df_2.drop_duplicates('iteration', keep='last')
    print(result_df_2_np)

    columas_promedio = ['Auto_0', 'Auto_1', 'Auto_2', 'Auto_3']
    total = ['Step']
    promedio_pasos_coche = result_df_2_np[columas_promedio].mean()
    promedio_total = result_df_2_np[total].mean()

    ax = promedio_pasos_coche.plot(kind='bar', rot=0, ylabel='Pasos Totales', xlabel='Autos', title='Promedio de Pasos por Agente', ylim=(0, 100), color = "red")
    ax.set_xticklabels(promedio_pasos_coche.index, rotation=0)
    for i, v in enumerate(promedio_pasos_coche):
        ax.text(i, v + 0.5, str(round(v, 2)), ha='center', va='bottom')
    plt.show()

    ax = promedio_total.plot(kind='bar', rot=0, ylabel='Pasos Totales', xlabel='Autos', title='Promedio de Pasos Totales', ylim=(0, 100), color = "blue")
    ax.set_xticklabels(promedio_total.index, rotation=0)
    for i, v in enumerate(promedio_total):
        ax.text(i, v + 0.5, str(round(v, 2)), ha='center', va='bottom')

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