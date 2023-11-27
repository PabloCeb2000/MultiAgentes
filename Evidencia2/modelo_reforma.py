import networkx as nx
import mesa
import random
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from diccionario_grafo import nodos

Grafo = nx.DiGraph()
for nodo, adyacentes in nodos.items():
    Grafo.add_node(nodo)
    for adyacente in adyacentes:
        Grafo.add_edge(nodo, adyacente, costo = 1.0)

def pasos_autos(model):
    pasos = []
    Autos = []

    for agent in model.schedule.agents:
        if isinstance(agent, AgenteAuto):
            Autos.append(agent)

    
    for auto in Autos:
        pasos.append(auto.paso)
    
    return pasos
            
    

class AgenteEdificio(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.val = 0
        
        

class AgenteSemaforoR(mesa.Agent):
    def __init__(self, unique_id, model, orient):
        super().__init__(unique_id, model)
        self.val = 6
        self.cambio = 0
        self.color = "Amarillo"
        self.orientacion = orient


    def deteccion(self):
        x, y = self.pos
        cedas = []

        if self.orientacion == "Norte":
            y1 = y + 1
            y2 = y + 2
            y3 = y + 3
            y4 = y - 1
            y5 = y - 2
            y6 = y - 3
            y7 = y
            y8 = y - 4
            y9 = y - 5
            cedas.append((x, y1))
            cedas.append((x, y2))
            cedas.append((x, y3))
            
            cedas.append((x, y4))
            cedas.append((x, y5))
            cedas.append((x, y6))
            cedas.append((x, y7))
            cedas.append((x, y9))
            
        if self.orientacion == "Este":
            x1 = x + 1
            x2 = x + 2
            x3 = x + 3
            x4 = x - 1
            x5 = x - 2
            x6 = x - 3
            x7 = x
            cedas.append((x1, y))
            cedas.append((x2, y))
            cedas.append((x3, y))
            
            cedas.append((x4, y))
            cedas.append((x5, y))
            cedas.append((x6, y))
            cedas.append((x7, y))
            
        if self.orientacion == "Oeste":
            x1 = x - 1
            x2 = x - 2
            x3 = x - 3
            x4 = x
            x5 = x + 1
            x6 = x + 2
            x7 = x + 3
            cedas.append((x1, y))
            cedas.append((x2, y))
            cedas.append((x3, y))
            
            cedas.append((x4, y))
            cedas.append((x5, y))
            cedas.append((x6, y))
            cedas.append((x7, y))
            
            
        if self.orientacion == "Sur":
            y1 = y - 1
            y2 = y - 2
            y3 = y - 3
            y4 = y
            y5 = y + 1
            y6 = y + 2
            y7 = y + 3
            cedas.append((x, y1))
            cedas.append((x, y2))
            cedas.append((x, y3))
            
            cedas.append((x, y4))
            cedas.append((x, y5))
            cedas.append((x, y6))
            cedas.append((x, y7))
            

        for cell in cedas: 
            cell_content = self.model.grid.get_cell_list_contents([cell])
            for agent in cell_content:
                if isinstance(agent, AgenteAuto):
                    return True    
        return False
            
    def step(self):
        if self.color == "Verde":
            self.val = 1
        if self.color == "Rojo":
            self.val = 2
        if self.color == "Yellow":
            self.val = 6


        
class AgenteGlorieta(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.val = 3

class AgenteMetrobus(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.val = 4

class AgenteAuto(mesa.Agent):
    def __init__(self, unique_id, model, pos_inicial, pos_final, Grafoo):
        super().__init__(unique_id, model)
        self.val = 5
        self.pos_inicial = pos_inicial
        self.pos_final = pos_final
        self.graf = Grafoo
        self.contador = 1
        self.paso = 0
        self.llegado = 0

        self.ruta = nx.shortest_path(self.graf, self.pos_inicial, self.pos_final)


    def move(self, c):
        next_position = self.ruta[c]

        cellmates = self.model.grid.get_cell_list_contents([next_position])

        for agent in cellmates:
            if isinstance(agent, AgenteSemaforoR) and agent.val == 2:
                self.contador -= 1
                return  
            
        for agent in cellmates:
            if isinstance(agent, AgenteAuto):
                self.contador -=1
                return



        self.model.grid.move_agent(self, self.ruta[c])

    def step(self):
        c = self.contador

        if len(self.ruta) > c:
            self.move(c)
            self.paso += 1

        self.contador += 1
        

        if self.pos == self.pos_final:
            self.llegado = 1




class SemaforoModel(mesa.Model):
    def __init__(self, width, height):
        self.schedule = mesa.time.RandomActivation(self)
        self.grid = mesa.space.MultiGrid(width, height, False)
        self.running = True
        self.m = 0
        R = 0
        self.primero = True
        self.esperar = 0

 
        # Abre el archivo y lee las líneas
        with open('mapa.txt', 'r') as file:
            lineas = file.readlines()

    # Elimina los saltos de línea y los caracteres de tabulación (\t), convierte cada línea en una lista de caracteres
        mapa = [list(filter(lambda x: x != '\n' and x != '\t', linea.strip())) for linea in lineas]
        mapa = mapa[::-1]

        n_i = 0
        n_j = 0
        for i in mapa:
            for j in i:

                if j == 'B':
                    r = AgenteEdificio(R, self)
                    self.schedule.add(r)

                    x = n_j 
                    y = n_i
                    self.grid.place_agent(r, (x, y))

                    R += 1

                if j == 'V':
                    r = AgenteEdificio(R, self)
                    self.schedule.add(r)

                    x = n_j 
                    y = n_i

                    self.grid.place_agent(r, (x, y))

                    R += 1
                if j == 'M':
                    r = AgenteMetrobus(R, self)
                    self.schedule.add(r)

                    x = n_j 
                    y = n_i

                    self.grid.place_agent(r, (x, y))

                    R += 1
                if j == 'A':
                    r = AgenteMetrobus(R, self)
                    self.schedule.add(r)

                    x = n_j 
                    y = n_i

                    self.grid.place_agent(r, (x, y))

                    R += 1

                
                n_j += 1

            n_j = 0
            n_i += 1

            

        c = AgenteAuto(j, self, (14, 0), (17, 24), Grafo)
        self.schedule.add(c)
            
        x = 14
        y = 0

        self.grid.place_agent(c, (x, y))

            
    def get_agent_position(self):
        id_pos = []
        for agent in self.schedule.agents:
            if isinstance(agent, AgenteAuto):
                x = {
                    "id": agent.unique_id,
                    "pos": agent.pos
                }
                id_pos.append(x)
                
        return id_pos
    
    def get_agent_position_Sem(self):
        id_pos_sem = []
        for agent in self.schedule.agents:
            if isinstance(agent, AgenteSemaforoR):
                y = {
                    "id": agent.unique_id,
                    "estado": agent.val
                }
                id_pos_sem.append(y)
                
        return id_pos_sem
    
    def Vacios(self):
        for agent in self.schedule.agents:
            if isinstance(agent, AgenteSemaforoR):
                if agent.deteccion() == True:
                    return False
                
        return True
            
    


    def step(self):
        total_llegado = 0
        self.counttt = 0
        if self.esperar == 0: 

            for agent in self.schedule.agents:
                if isinstance(agent, AgenteAuto):
                    if agent.llegado == 1:
                        total_llegado += 1    

          

                if isinstance(agent, (AgenteSemaforoR)):
                    if agent.deteccion() == True and (agent.orientacion == "Norte" or agent.orientacion == "Sur"):
                        self.primero = False
                        for agent in self.schedule.agents:
                            if isinstance(agent, AgenteSemaforoR) and (agent.orientacion == "Norte" or agent.orientacion == "Sur"):
                                agent.color = "Verde"
                            else:
                                agent.color = "Rojo"

                            if isinstance(agent, AgenteSemaforoR) and (agent.orientacion == "Oeste" or agent.orientacion == "Este"):
                                agent.color = "Rojo"
                            else:
                                agent.color = "Verde"
                        self.esperar = 10
                    
                        

                    elif agent.deteccion() == True and (agent.orientacion == "Este" or agent.orientacion == "Oeste"):
                        self.primero = False
                        for agent in self.schedule.agents:
                            if isinstance(agent, AgenteSemaforoR) and (agent.orientacion == "Este" or agent.orientacion == "Oeste"):
                                agent.color = "Verde"
                            else:
                                agent.color = "Rojo"

                            if isinstance(agent, AgenteSemaforoR) and (agent.orientacion == "Norte" or agent.orientacion == "Sur"):
                                agent.color = "Rojo"
                            else:
                                agent.color = "Verde"
                        self.esperar = 10
                                
                    else:
                        if self.Vacios() == True:
                            for agent in self.schedule.agents:
                                if isinstance(agent, AgenteSemaforoR) and self.counttt == 1:
                                    agent.color = "Yellow"


                        self.counttt +=1

        if self.esperar > 0:
            self.esperar -= 1

        

        self.schedule.step()
   
        


        if total_llegado == 4:
            self.running = False
        



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

# Crea una cuadrícula visual para la simulación
grid = CanvasGrid(agent_portrayal, 29, 43)

# Crea una instancia del servidor visual para la simulación
server = mesa.visualization.ModularServer(
    SemaforoModel, [grid], "Modelo de Ciudad", {"width": 29, "height": 43}
)
server.port = 8521  # Asigna el puerto que desees
server.launch()
