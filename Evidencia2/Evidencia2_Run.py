import mesa 
import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.pylab as plt
import json
from Evidencia2_Script import mesa, ReformaModel

def batch():
    paramas = {"width": 29, "height": 43}
    results = mesa.batch_run(
        ReformaModel,
        parameters=paramas,
        iterations=50,
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
    promedio_1 = []
    suma_promedio = 0

    for i in range(50):
        condition = results_df['iteration'] == i
        df_s = results_df[condition]

        plt.plot(df_s['Step'], df_s['Agentes precentes'])

        df_s_nd = df_s.drop_duplicates('iteration', keep='last')
        val_paso_total = df_s_nd['Step']

        val_lista = val_paso_total.values
        suma_promedio += val_lista

    total_promedio = suma_promedio/50
    total_promedio_int = float(total_promedio)
    print(total_promedio_int)
    
    
    
    plt.xlabel('Pasos Totales')
    plt.ylabel('Total de autos simultaneos')
    plt.title('Distribución de autos a lo largo del dia (sin semaforo)')

    plt.grid(True)
    plt.show()  

    ptomedios_totales = [158.36, 133.56]
    marcas = ['Con semaforo', 'Sin semaforo']

    # Plotting the bar plot
    plt.bar(marcas, ptomedios_totales, color=['blue', 'orange'])

    # Adding labels and title
    plt.xlabel('Marcas')
    plt.ylabel('Promedio Total de pasos')
    plt.title('Promedios de pasos con Semaforo vs sin Semafor')

    # Display the plot
    plt.ylim(0, 200)
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
    if agent.val == 3.1:
        portrayal = {"Shape": "rect", "Filled": "true", "h": 1.0, "w": 1.0, "Color": "green", "Layer": 1}
    if agent.val == 3.2:
        portrayal = {"Shape": "rect", "Filled": "true", "h": 1.0, "w": 1.0, "Color": "black", "Layer": 1}
    if agent.val == 4:
        portrayal = {"Shape": "rect", "Filled": "true", "h": 1.0, "w": 1.0, "Color": "red", "Layer": 1}
    if agent.val == 5:
        portrayal = {"Shape": "rect", "Filled": "true", "h": 1.0, "w": 1.0, "Color": "grey", "Layer": 2}
    if agent.val == 6:
        portrayal = {"Shape": "rect", "Filled": "true", "h": 1.0, "w": 1.0, "Color": "yellow", "Layer": 1}
    if agent.val == 7:
        portrayal = {"Shape": "rect", "Filled": "true", "h": 1.0, "w": 1.0, "Color": "brown", "Layer": 1}
    if agent.val == 8:
        portrayal = {"Shape": "rect", "Filled": "true", "h": 1.0, "w": 1.0, "Color": "purple", "Layer": 1}
    return portrayal

def main():
    batch()
    # Crea una cuadrícula visual para la simulación
    grid = mesa.visualization.CanvasGrid(agent_portrayal, 29, 43)

    # Crea una instancia del servidor visual para la simulación
    chart = mesa.visualization.ChartModule(
        [{"Label": "pasos", "Color": "black", }], 
        data_collector_name = "datacollector"
    )
    server = mesa.visualization.ModularServer(
        ReformaModel, [grid, chart], "Modelo de Ciudad", {"width": 29, "height": 43}
    )
    server.port = 8521  # Asigna el puerto que desees
    server.launch()

main()