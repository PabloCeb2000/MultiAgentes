import mesa 
import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.pylab as plt
import random
import networkx as nx
from diccionario_grafo import diccionario_reforma, diccionario_reforma_spawneables

Grafo = nx.DiGraph()
contador_agentes = 0
total_agentes = 0

# Añadir nodos y sus nodos adyacentes desde diccionario
for nodo, adyacentes in diccionario_reforma.items():
    Grafo.add_node(nodo)
    for adyacente in adyacentes:
        Grafo.add_edge(nodo, adyacente, costo = 1.0)

pos_finales = [(2, 42), (1, 37),
               (2, 32), (0, 20),
               (3, 12), (1, 6),
               (25, 41), (27, 35),
               (27, 18), 
               (26, 13), (28, 12),
               (24, 1)]


def pasos_autos(model):
    pasos = []
    Autos = []

    for agent in model.schedule.agents:
        if isinstance(agent, AgenteAuto):
            Autos.append(agent)

    
    for auto in Autos:
        pasos.append(auto.paso)
    
    return pasos
            
def agentes_precentes(model):
    return model.total_agentes_precentes

    

class AgenteEdificio(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.val = 0
        
        

class AgenteSemaforoB(mesa.Agent):
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

class AgenteSemaforoR(mesa.Agent):
    def __init__(self, unique_id, model, vall):
        super().__init__(unique_id, model)
        self.val = 6
        self.cambio = 0

        if vall == 1:
            self.val = 1
        if vall == 2:
            self.val = 2


            
    def step(self):
        if self.cambio % 6 == 0:
            if (self.val == 1):
                self.val = 2
            elif (self.val == 2):
                self.val = 1

        self.cambio += 1

        
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

class AgenteEstacionamiento(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.val = 8

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
        """
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
            self.contador = 0"""

        
        self.model.grid.move_agent(self, self.ruta[c])



    def step(self):
        c = self.contador

        if len(self.ruta) > c:
            mover = random.random()
            self.move(c, mover)
            self.paso += 1

        if self.pos == self.pos_final:
            self.llegado = 1

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
        self.R = 0
        self.primero = True
        self.esperar = 0
        self.total_agentes = 0
        self.total_agentes_precentes = 0
        self.conteo_final = False

        mapa_Reforma = [['#', '#', '#', '#', ' ', ' ', '#', '#', '#', 'M', ' ', ' ', ' ', 'C', ' ', ' ', ' ', 'M', '#', '#', '#', ' ', ' ', '#', '#', ' ', '#', '#', '#'],
                        ['#', '#', '#', '#', ' ', ' ', '#', '#', '#', 'M', ' ', ' ', ' ', 'C', ' ', ' ', ' ', 'M', '#', '#', '#', ' ', ' ', '#', 'P', ' ', '#', '#', '#'],
                        ['#', '#', '#', '#', ' ', ' ', '#', '#', '#', 'M', ' ', ' ', ' ', 'C', ' ', ' ', ' ', 'M', '#', '#', '#', ' ', ' ', '#', '#', ' ', '#', '#', '#'],
                        ['#', '#', '#', '#', ' ', ' ', '#', '#', '#', 'M', ' ', ' ', ' ', 'C', ' ', ' ', ' ', 'M', '#', '#', '#', ' ', ' ', '#', '#', ' ', '#', '#', '#'],
                        ['#', '#', '#', '#', ' ', ' ', '#', '#', '#', 'M', ' ', ' ', ' ', 'C', ' ', ' ', ' ', 'M', '#', '#', '#', ' ', ' ', '#', '#', ' ', '#', '#', '#'],
                        ['#', '#', '#', '#', ' ', ' ', '#', '#', '#', 'M', ' ', ' ', ' ', 'C', ' ', ' ', ' ', 'M', '#', '#', '#', ' ', ' ', '#', '#', ' ', '#', '#', '#'],
                        ['#', 'P', '#', '#', ' ', ' ', '#', '#', '#', 'M', ' ', ' ', ' ', 'C', ' ', ' ', ' ', 'M', '#', '#', '#', ' ', ' ', '#', '#', ' ', '#', '#', '#'],
                        [' ', ' ', ' ', ' ', ' ', ' ', '#', '#', '#', 'M', ' ', ' ', ' ', 'C', ' ', ' ', ' ', 'M', '#', '#', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', '#', '#', '#', 'M', ' ', ' ', ' ', 'C', ' ', ' ', ' ', 'M', '#', '#', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        ['#', '#', ' ', '#', ' ', ' ', '#', '#', '#', 'M', ' ', ' ', ' ', 'C', ' ', ' ', ' ', 'M', '#', '#', '#', ' ', ' ', '#', '#', '#', ' ', '#', '#'],
                        ['#', '#', ' ', '#', ' ', ' ', '#', '#', '#', 'M', ' ', ' ', ' ', 'C', ' ', ' ', ' ', 'M', '#', '#', '#', ' ', ' ', '#', '#', '#', ' ', '#', '#'],
                        ['#', '#', ' ', '#', ' ', ' ', '#', '#', '#', 'M', ' ', ' ', ' ', 'C', ' ', ' ', ' ', 'M', '#', '#', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        ['#', '#', ' ', 'P', ' ', ' ', '#', '#', '#', 'M', ' ', ' ', ' ', 'C', ' ', ' ', ' ', 'M', '#', '#', '#', ' ', ' ', '#', '#', '#', '#', '#', 'P'],
                        ['#', '#', ' ', '#', ' ', ' ', '#', '#', '#', 'M', ' ', ' ', ' ', 'C', ' ', ' ', ' ', 'M', '#', '#', '#', ' ', ' ', '#', '#', ' ', 'P', '#', '#'],
                        ['#', '#', ' ', '#', ' ', ' ', '#', '#', '#', 'M', ' ', ' ', ' ', 'C', ' ', ' ', ' ', 'M', '#', '#', '#', ' ', ' ', '#', '#', ' ', '#', '#', '#'],
                        ['#', '#', ' ', '#', ' ', ' ', '#', '#', '#', 'M', ' ', ' ', ' ', 'C', ' ', ' ', ' ', 'M', '#', '#', '#', ' ', ' ', '#', '#', ' ', '#', '#', '#'],
                        [' ', ' ', ' ', ' ', ' ', ' ', '#', '#', '#', 'M', ' ', ' ', ' ', 'C', ' ', ' ', ' ', 'M', '#', '#', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', '#', '#', '#', 'M', ' ', ' ', ' ', 'C', ' ', ' ', ' ', 'M', '#', '#', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        ['#', ' ', '#', '#', ' ', ' ', '#', '#', '#', 'M', ' ', ' ', ' ', 'C', ' ', ' ', ' ', 'M', '#', '#', '#', ' ', ' ', '#', '#', '#', '#', 'P', '#'],
                        ['#', ' ', '#', '#', ' ', ' ', '#', '#', '#', 'M', ' ', ' ', ' ', 'C', ' ', ' ', ' ', 'M', '#', '#', '#', ' ', ' ', '#', '#', '#', '#', '#', '#'],
                        ['P', ' ', '#', '#', ' ', ' ', '#', '#', '#', 'M', ' ', ' ', ' ', 'C', ' ', ' ', ' ', 'M', '#', '#', '#', ' ', ' ', '#', '#', '#', '#', '#', '#'],
                        ['#', ' ', '#', '#', ' ', ' ', '#', '#', '#', 'M', ' ', ' ', ' ', 'C', '/', '/', '/', 'M', '#', '#', '#', ' ', ' ', '#', '#', '#', '#', '#', '#'],
                        ['#', ' ', '#', '#', '/', '/', '#', '#', '#', 'M', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'M', '#', '#', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        ['#', ' ', '#', '#', ' ', ' ', '#', '#', 'M', 'M', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'M', 'M', '#', '#', '/', '/', '#', '#', '#', '#', '#', '#'],
                        ['#', ' ', '#', '#', ' ', ' ', ' ', ' ', 'M', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'M', ' ', ' ', ' ', ' ', '#', '#', '#', '#', '#', '#'],
                        [' ', ' ', ' ', '-', ' ', ' ', ' ', ' ', 'M', ' ', ' ', 'A', 'A', 'A', 'A', 'A', ' ', ' ', 'M', ' ', ' ', ' ', ' ', '-', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', '-', ' ', ' ', ' ', ' ', 'M', ' ', ' ', 'A', 'A', 'A', 'A', 'A', ' ', ' ', 'M', ' ', ' ', ' ', ' ', '-', ' ', ' ', ' ', ' ', ' '],
                        ['C', 'C', 'C', 'C', ' ', ' ', ' ', ' ', 'M', ' ', ' ', 'A', 'A', 'X', 'A', 'A', ' ', ' ', 'M', ' ', ' ', ' ', ' ', 'C', 'C', 'C', 'C', 'C', 'C'],
                        [' ', ' ', ' ', '-', ' ', ' ', ' ', ' ', 'M', ' ', ' ', 'A', 'A', 'A', 'A', 'A', ' ', ' ', 'M', ' ', ' ', ' ', ' ', '-', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', '-', ' ', ' ', ' ', ' ', 'M', ' ', ' ', 'A', 'A', 'A', 'A', 'A', ' ', ' ', 'M', ' ', ' ', ' ', ' ', '-', ' ', ' ', ' ', ' ', ' '],
                        ['#', '#', '#', '#', ' ', ' ', '#', '#', 'M', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'M', '#', '#', ' ', ' ', '#', '#', ' ', '#', '#', '#'],
                        ['#', '#', '#', '#', ' ', ' ', '#', '#', 'M', 'M', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'M', 'M', '#', '#', ' ', ' ', '#', '#', ' ', '#', '#', '#'],
                        ['#', '#', 'P', '#', ' ', ' ', '#', '#', '#', 'M', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'M', '#', '#', '#', ' ', ' ', '#', '#', ' ', 'P', '#', '#'],
                        [' ', ' ', ' ', ' ', ' ', ' ', '#', '#', '#', 'M', '/', '/', '/', 'C', ' ', ' ', ' ', 'M', '#', '#', '#', ' ', ' ', ' ', ' ', ' ', '#', '#', '#'],
                        ['#', '#', '#', '#', ' ', ' ', '#', '#', '#', 'M', ' ', ' ', ' ', 'C', ' ', ' ', ' ', 'M', '#', '#', '#', ' ', ' ', '#', '#', '#', '#', '#', '#'],
                        ['#', '#', '#', '#', ' ', ' ', '#', '#', '#', 'M', ' ', ' ', ' ', 'C', ' ', ' ', ' ', 'M', '#', '#', '#', ' ', ' ', '#', '#', '#', '#', 'P', '#'],
                        ['#', '#', '#', '#', ' ', ' ', '#', '#', '#', 'M', ' ', ' ', ' ', 'C', ' ', ' ', ' ', 'M', '#', '#', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        ['#', 'P', '#', '#', ' ', ' ', '#', '#', '#', 'M', ' ', ' ', ' ', 'C', ' ', ' ', ' ', 'M', '#', '#', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', '#', '#', '#', 'M', ' ', ' ', ' ', 'C', ' ', ' ', ' ', 'M', '#', '#', '#', ' ', ' ', '#', '#', '#', ' ', '#', '#'],
                        [' ', ' ', ' ', ' ', ' ', ' ', '#', '#', '#', 'M', ' ', ' ', ' ', 'C', ' ', ' ', ' ', 'M', '#', '#', '#', ' ', ' ', '#', '#', '#', ' ', '#', '#'],
                        ['#', ' ', '#', '#', ' ', ' ', '#', '#', '#', 'M', ' ', ' ', ' ', 'C', ' ', ' ', ' ', 'M', '#', '#', '#', ' ', ' ', '#', '#', '#', ' ', '#', '#'],
                        ['#', ' ', '#', '#', ' ', ' ', '#', '#', '#', 'M', ' ', ' ', ' ', 'C', ' ', ' ', ' ', 'M', '#', '#', '#', ' ', ' ', '#', '#', 'P', ' ', '#', '#'],
                        ['#', ' ', 'P', '#', ' ', ' ', '#', '#', '#', 'M', ' ', ' ', ' ', 'C', ' ', ' ', ' ', 'M', '#', '#', '#', ' ', ' ', '#', '#', '#', ' ', '#', '#']]

        n_i = 0
        n_j = 0
        for i in mapa_Reforma:
            for j in i:

                if j == '#':
                    r = AgenteEdificio(self.R, self)
                    self.schedule.add(r)

                    x = n_j 
                    y = n_i
                    self.grid.place_agent(r, (x, y))

                    self.R += 1

                if j == 'M':
                    r = AgenteMetrobus(self.R, self)
                    self.schedule.add(r)

                    x = n_j 
                    y = n_i

                    self.grid.place_agent(r, (x, y))

                    self.R += 1

                if j == 'C':
                    r = AgenteCamellon(self.R, self)
                    self.schedule.add(r)

                    x = n_j 
                    y = n_i

                    self.grid.place_agent(r, (x, y))

                    self.R += 1

                if j == 'A':
                    r = AgenteGlorieta(self.R, self)
                    self.schedule.add(r)

                    x = n_j 
                    y = n_i

                    self.grid.place_agent(r, (x, y))

                    self.R += 1

                if j == 'X':
                    r = AgenteAngel(self.R, self)
                    self.schedule.add(r)

                    x = n_j 
                    y = n_i

                    self.grid.place_agent(r, (x, y))

                    self.R += 1

                if j == 'N':
                    r = AgenteSemaforoB(self.R, self, "Norte")
                    self.schedule.add(r)

                    x = n_j 
                    y = n_i

                    self.grid.place_agent(r, (x, y))

                    self.R += 1

                if j == 'S':
                    r = AgenteSemaforoB(self.R, self, "Sur")
                    self.schedule.add(r)

                    x = n_j 
                    y = n_i

                    self.grid.place_agent(r, (x, y))

                    self.R += 1

                if j == 'O':
                    r = AgenteSemaforoB(self.R, self, "Oeste")
                    self.schedule.add(r)

                    x = n_j 
                    y = n_i

                    self.grid.place_agent(r, (x, y))

                    self.R += 1

                if j == '/':
                    col = 1
                    r = AgenteSemaforoR(self.R, self, col)
                    self.schedule.add(r)

                    x = n_j 
                    y = n_i

                    self.grid.place_agent(r, (x, y))

                    self.R += 1

                if j == '-':
                    col = 2
                    r = AgenteSemaforoR(self.R, self, col)
                    self.schedule.add(r)

                    x = n_j 
                    y = n_i

                    self.grid.place_agent(r, (x, y))

                    self.R += 1
 
                if j == 'P':
                    r = AgenteEstacionamiento(self.R, self)
                    self.schedule.add(r)

                    x = n_j 
                    y = n_i

                    self.grid.place_agent(r, (x, y))

                    self.R += 1
                n_j += 1

            n_j = 0
            n_i += 1

        #contador_agentes = R
        
        for i in range(0):      
            eleccion_1 = random.randint(0, 613)  

            p_inicial = list(diccionario_reforma.keys())[eleccion_1]
            p_final = random.choice(pos_finales)

            j = self.R + 1 + i
            """            
            while p_inicial in posiciones_pasadas:
                p_inicial = list(diccionario_reforma.keys())[random.randint(0, 684)]"""

            
            c = AgenteAuto(j, self, p_inicial, p_final, Grafo)
            self.schedule.add(c)
                
            x = p_inicial[0]
            y = p_inicial[1]
            print(x, y)

            self.grid.place_agent(c, (x, y))
            self.R += 1

        self.datacollector = mesa.DataCollector( 
            model_reporters={"Agentes precentes": agentes_precentes},
        )

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

        if self.total_agentes < 50:
            eleccion_1 = random.randint(0, 553)  

            p_inicial = list(diccionario_reforma_spawneables.keys())[eleccion_1]
            p_final = random.choice(pos_finales)

            j = self.R + 1 
    
            c = AgenteAuto(j, self, p_inicial, p_final, Grafo)
            self.schedule.add(c)
                    
            x = p_inicial[0]
            y = p_inicial[1]
            #print(x, y)

            self.grid.place_agent(c, (x, y))
            self.R += 1
            
            #posiciones_pasadas.append(p_inicial)
            self.total_agentes += 1
            self.total_agentes_precentes += 1

        for agent in self.schedule.agents:
                    if isinstance(agent, AgenteAuto):
                        if agent.llegado == 1:
                            total_llegado += 1
                            self.schedule.remove(agent)
                            self.grid.remove_agent(agent)
                            self.total_agentes_precentes -= 1
        

        """
        if self.esperar == 0: 



            for agent in self.schedule.agents:
                
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
                        self.esperar = 5
                        
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
                        self.esperar = 5
                        
                                
                    else:
                        if self.Vacios() == True:
                            for agent in self.schedule.agents:
                                if isinstance(agent, AgenteSemaforoR) and self.counttt == 1:
                                    agent.color = "Yellow"


                        self.counttt +=1
                    

        if self.esperar > 0:
            self.esperar -= 1


"""
        
        self.schedule.step()
        self.datacollector.collect(self)

        if self.total_agentes_precentes == 0:
            self.conteo_final = True
        
        if self.conteo_final == True:
            self.running = False
