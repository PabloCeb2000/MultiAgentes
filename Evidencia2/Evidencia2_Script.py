import mesa 
import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.pylab as plt
import random
import networkx as nx
from diccionario_grafo import diccionario_glorieta, diccionario_abajo_derecha, diccionario_arriba_derecha, diccionario_metrobus_derecha

Grafo = nx.DiGraph()

# Añadir nodos y sus nodos adyacentes desde diccionario
for nodo, adyacentes in diccionario_glorieta.items():
    Grafo.add_node(nodo)
    for adyacente in adyacentes:
        Grafo.add_edge(nodo, adyacente, costo = 1.0)

for nodo, adyacentes in diccionario_abajo_derecha.items():
    Grafo.add_node(nodo)
    for adyacente in adyacentes:
        Grafo.add_edge(nodo, adyacente, costo = 1.0)

for nodo, adyacentes in diccionario_arriba_derecha.items():
    Grafo.add_node(nodo)
    for adyacente in adyacentes:
        Grafo.add_edge(nodo, adyacente, costo = 1.0)

for nodo, adyacentes in diccionario_metrobus_derecha.items():
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

class AgenteCamellon(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.val = 3.1

class AgenteAngel(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.val = 3.2

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
        self.completaste = False

        self.ruta = nx.shortest_path(self.graf, self.pos_inicial, self.pos_final)


    def move(self, c, cambiarC):
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

        x, y = self.pos 
        celda_metrobus = self.model.grid.get_cell_list_contents([(x+1, y)])

        siEsCarril = False

        for agent in celda_metrobus:
            if isinstance(agent, AgenteMetrobus):
                siEsCarril = True


        if cambiarC < 0.2 and siEsCarril == True:
            self.model.grid.move_agent(self, ([self.pos[0] + 1, self.pos[1]]))
            pos_tuple = tuple(self.pos)
            self.pos_inicial = pos_tuple
            self.pos_final = (17, 42)
            self.ruta = nx.shortest_path(self.graf, self.pos_inicial, self.pos_final)
            print(self.ruta)
            siEsCarril = False
            self.contador = 0

        else:
            self.model.grid.move_agent(self, self.ruta[c])



    def step(self):
        c = self.contador

        if len(self.ruta) > c:
            mover = random.random()
            self.move(c, mover)
            self.paso += 1

        self.contador += 1
        


class AgenteMetrobusB(mesa.Agent):
    def __init__(self, unique_id, model, pos_inicial, pos_final, Grafoo):
        super().__init__(unique_id, model)
        self.val = 7
        self.pos_inicial = pos_inicial
        self.pos_final = pos_final
        self.graf = Grafoo
        self.contador = 1
        self.paso = 0
        self.llegado = 0
        self.completaste = False
        self.movement = 0

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

        if len(self.ruta) > c :
            self.move(c)
            self.paso += 1

        self.contador += 1
        

        if self.pos == self.pos_final:
            self.llegado = 1
            self.completaste = True
            self.contador = 1

        self.movement += 1


        
        


class ReformaModel(mesa.Model):
    def __init__(self, width, height):
        self.schedule = mesa.time.RandomActivation(self)
        self.grid = mesa.space.MultiGrid(width, height, False)
        self.running = True
        self.m = 0
        R = 0
        self.primero = True
        self.esperar = 0

        mapa_Reforma = [['#', '#', '#', '#', ' ', ' ', '#', '#', '#', 'M', ' ', ' ', ' ', 'C', ' ', ' ', ' ', 'M', '#', '#', '#', ' ', ' ', '#', '#', ' ', '#', '#', '#'],
                        ['#', '#', '#', '#', ' ', ' ', '#', '#', '#', 'M', ' ', ' ', ' ', 'C', ' ', ' ', ' ', 'M', '#', '#', '#', ' ', ' ', '#', '#', ' ', '#', '#', '#'],
                        ['#', '#', '#', '#', ' ', ' ', '#', '#', '#', 'M', ' ', ' ', ' ', 'C', ' ', ' ', ' ', 'M', '#', '#', '#', ' ', ' ', '#', '#', ' ', '#', '#', '#'],
                        ['#', '#', '#', '#', ' ', ' ', '#', '#', '#', 'M', ' ', ' ', ' ', 'C', ' ', ' ', ' ', 'M', '#', '#', '#', ' ', ' ', '#', '#', ' ', '#', '#', '#'],
                        ['#', '#', '#', '#', ' ', ' ', '#', '#', '#', 'M', ' ', ' ', ' ', 'C', ' ', ' ', ' ', 'M', '#', '#', '#', ' ', ' ', '#', '#', ' ', '#', '#', '#'],
                        ['#', '#', '#', '#', ' ', ' ', '#', '#', '#', 'M', ' ', ' ', ' ', 'C', ' ', ' ', ' ', 'M', '#', '#', '#', ' ', ' ', '#', '#', ' ', '#', '#', '#'],
                        ['#', '#', '#', '#', ' ', ' ', '#', '#', '#', 'M', ' ', ' ', ' ', 'C', ' ', ' ', ' ', 'M', '#', '#', '#', ' ', ' ', '#', '#', ' ', '#', '#', '#'],
                        [' ', ' ', ' ', ' ', ' ', ' ', '#', '#', '#', 'M', ' ', ' ', ' ', 'C', ' ', ' ', ' ', 'M', '#', '#', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', '#', '#', '#', 'M', ' ', ' ', ' ', 'C', ' ', ' ', ' ', 'M', '#', '#', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        ['#', '#', ' ', '#', ' ', ' ', '#', '#', '#', 'M', ' ', ' ', ' ', 'C', ' ', ' ', ' ', 'M', '#', '#', '#', ' ', ' ', '#', '#', '#', ' ', '#', '#'],
                        ['#', '#', ' ', '#', ' ', ' ', '#', '#', '#', 'M', ' ', ' ', ' ', 'C', ' ', ' ', ' ', 'M', '#', '#', '#', ' ', ' ', '#', '#', '#', ' ', '#', '#'],
                        ['#', '#', ' ', '#', ' ', ' ', '#', '#', '#', 'M', ' ', ' ', ' ', 'C', ' ', ' ', ' ', 'M', '#', '#', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        ['#', '#', ' ', '#', ' ', ' ', '#', '#', '#', 'M', ' ', ' ', ' ', 'C', ' ', ' ', ' ', 'M', '#', '#', '#', ' ', ' ', '#', '#', '#', '#', '#', '#'],
                        ['#', '#', ' ', '#', ' ', ' ', '#', '#', '#', 'M', ' ', ' ', ' ', 'C', ' ', ' ', ' ', 'M', '#', '#', '#', ' ', ' ', '#', '#', ' ', '#', '#', '#'],
                        ['#', '#', ' ', '#', ' ', ' ', '#', '#', '#', 'M', ' ', ' ', ' ', 'C', ' ', ' ', ' ', 'M', '#', '#', '#', ' ', ' ', '#', '#', ' ', '#', '#', '#'],
                        ['#', '#', ' ', '#', ' ', ' ', '#', '#', '#', 'M', ' ', ' ', ' ', 'C', ' ', ' ', ' ', 'M', '#', '#', '#', ' ', ' ', '#', '#', ' ', '#', '#', '#'],
                        [' ', ' ', ' ', ' ', ' ', ' ', '#', '#', '#', 'M', ' ', ' ', ' ', 'C', ' ', ' ', ' ', 'M', '#', '#', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', '#', '#', '#', 'M', ' ', ' ', ' ', 'C', ' ', ' ', ' ', 'M', '#', '#', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        ['#', ' ', '#', '#', ' ', ' ', '#', '#', '#', 'M', ' ', ' ', ' ', 'C', ' ', ' ', ' ', 'M', '#', '#', '#', ' ', ' ', '#', '#', '#', '#', '#', '#'],
                        ['#', ' ', '#', '#', ' ', ' ', '#', '#', '#', 'M', ' ', ' ', ' ', 'C', ' ', ' ', ' ', 'M', '#', '#', '#', ' ', ' ', '#', '#', '#', '#', '#', '#'],
                        ['#', ' ', '#', '#', ' ', ' ', '#', '#', '#', 'M', ' ', ' ', ' ', 'C', ' ', ' ', ' ', 'M', '#', '#', '#', ' ', ' ', '#', '#', '#', '#', '#', '#'],
                        ['#', ' ', '#', '#', ' ', ' ', '#', '#', '#', 'M', ' ', ' ', ' ', 'C', ' ', ' ', ' ', 'M', '#', '#', '#', ' ', ' ', '#', '#', '#', '#', '#', '#'],
                        ['#', ' ', '#', '#', ' ', ' ', '#', '#', '#', 'M', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'M', '#', '#', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        ['#', ' ', '#', '#', ' ', ' ', '#', '#', 'M', 'M', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'M', 'M', '#', '#', ' ', ' ', '#', '#', '#', '#', '#', '#'],
                        ['#', ' ', '#', '#', ' ', ' ', ' ', ' ', 'M', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'M', ' ', ' ', ' ', ' ', '#', '#', '#', '#', '#', '#'],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'M', ' ', ' ', 'A', 'A', 'A', 'A', 'A', ' ', ' ', 'M', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'M', ' ', ' ', 'A', 'A', 'A', 'A', 'A', ' ', ' ', 'M', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        ['C', 'C', 'C', 'C', ' ', ' ', ' ', ' ', 'M', ' ', ' ', 'A', 'A', 'X', 'A', 'A', ' ', ' ', 'M', ' ', ' ', ' ', ' ', 'C', 'C', 'C', 'C', 'C', 'C'],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'M', ' ', ' ', 'A', 'A', 'A', 'A', 'A', ' ', ' ', 'M', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'M', ' ', ' ', 'A', 'A', 'A', 'A', 'A', ' ', ' ', 'M', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        ['#', '#', '#', '#', ' ', ' ', '#', '#', 'M', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'M', '#', '#', ' ', ' ', '#', '#', ' ', '#', '#', '#'],
                        ['#', '#', '#', '#', ' ', ' ', '#', '#', 'M', 'M', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'M', 'M', '#', '#', ' ', ' ', '#', '#', ' ', '#', '#', '#'],
                        ['#', '#', '#', '#', ' ', ' ', '#', '#', '#', 'M', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'M', '#', '#', '#', ' ', ' ', '#', '#', ' ', '#', '#', '#'],
                        [' ', ' ', ' ', ' ', ' ', ' ', '#', '#', '#', 'M', ' ', ' ', ' ', 'C', ' ', ' ', ' ', 'M', '#', '#', '#', ' ', ' ', ' ', ' ', ' ', '#', '#', '#'],
                        ['#', '#', '#', '#', ' ', ' ', '#', '#', '#', 'M', ' ', ' ', ' ', 'C', ' ', ' ', ' ', 'M', '#', '#', '#', ' ', ' ', '#', '#', '#', '#', '#', '#'],
                        ['#', '#', '#', '#', ' ', ' ', '#', '#', '#', 'M', ' ', ' ', ' ', 'C', ' ', ' ', ' ', 'M', '#', '#', '#', ' ', ' ', '#', '#', '#', '#', '#', '#'],
                        ['#', '#', '#', '#', ' ', ' ', '#', '#', '#', 'M', ' ', ' ', ' ', 'C', ' ', ' ', ' ', 'M', '#', '#', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        ['#', '#', '#', '#', ' ', ' ', '#', '#', '#', 'M', ' ', ' ', ' ', 'C', ' ', ' ', ' ', 'M', '#', '#', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', '#', '#', '#', 'M', ' ', ' ', ' ', 'C', ' ', ' ', ' ', 'M', '#', '#', '#', ' ', ' ', '#', '#', '#', ' ', '#', '#'],
                        [' ', ' ', ' ', ' ', ' ', ' ', '#', '#', '#', 'M', ' ', ' ', ' ', 'C', ' ', ' ', ' ', 'M', '#', '#', '#', ' ', ' ', '#', '#', '#', ' ', '#', '#'],
                        ['#', ' ', '#', '#', ' ', ' ', '#', '#', '#', 'M', ' ', ' ', ' ', 'C', ' ', ' ', ' ', 'M', '#', '#', '#', ' ', ' ', '#', '#', '#', ' ', '#', '#'],
                        ['#', ' ', '#', '#', ' ', ' ', '#', '#', '#', 'M', ' ', ' ', ' ', 'C', ' ', ' ', ' ', 'M', '#', '#', '#', ' ', ' ', '#', '#', '#', ' ', '#', '#'],
                        ['#', ' ', '#', '#', ' ', ' ', '#', '#', '#', 'M', ' ', ' ', ' ', 'C', ' ', ' ', ' ', 'M', '#', '#', '#', ' ', ' ', '#', '#', '#', ' ', '#', '#']]

        n_i = 0
        n_j = 0
        for i in mapa_Reforma:
            for j in i:

                if j == '#':
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

                if j == 'C':
                    r = AgenteCamellon(R, self)
                    self.schedule.add(r)

                    x = n_j 
                    y = n_i

                    self.grid.place_agent(r, (x, y))

                    R += 1

                if j == 'A':
                    r = AgenteGlorieta(R, self)
                    self.schedule.add(r)

                    x = n_j 
                    y = n_i

                    self.grid.place_agent(r, (x, y))

                    R += 1

                if j == 'X':
                    r = AgenteAngel(R, self)
                    self.schedule.add(r)

                    x = n_j 
                    y = n_i

                    self.grid.place_agent(r, (x, y))

                    R += 1
 
                n_j += 1

            n_j = 0
            n_i += 1

        posiciones_pasadas = []
        
        for i in range(1):        
            p_inicial = (16, 0)
            p_final = (16, 42)
            j = R + 1 + i
            #print(random.choice(diccionario_abajo_derecha))
            """
            while p_inicial in posiciones_pasadas:
                p_inicial = random.choice(p_iniciales)"""

            
            c = AgenteAuto(j, self, p_inicial, p_final, Grafo)
            self.schedule.add(c)
                
            x = p_inicial[0]
            y = p_inicial[1]

            self.grid.place_agent(c, (x, y))
            R += 1

            #posiciones_pasadas.append(p_inicial)
        
        for i in range(0): 
            j = R + 1 + i

            p_inicial = (17, 8)
            p_final = (17, 42)

            c = AgenteMetrobusB(j, self, p_inicial, p_final, Grafo)
            self.schedule.add(c)
                

            x = p_inicial[0]
            y = p_inicial[1]
            

            self.grid.place_agent(c, (x, y))
            R += 1

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
                """
                if isinstance(agent, AgenteAuto):
                    if agent.llegado == 1:
                        total_llegado += 1

                    if agent.completaste == True:
                        agent.pos_inicial == agent.pos_final
                        agent.pos_final == agent.pos_inicial
                        agent.ruta = nx.shortest_path(Grafo, agent.pos_inicial, agent.pos_final)
                        agent.completaste = False

                if isinstance(agent, AgenteMetrobusB):
                    if agent.llegado == 1:
                        total_llegado += 1

                    if agent.completaste == True:
                        agent.pos_inicial == agent.pos_final
                        agent.pos_final == agent.pos_inicial
                        agent.ruta = nx.shortest_path(Grafo, agent.pos_inicial, agent.pos_final)
                        agent.completaste = False
"""

          

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
