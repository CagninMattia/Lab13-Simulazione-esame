import copy
from geopy import distance

from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        # Creo grafo
        self.grafo = nx.Graph()
        # Creo dizionario per nodi
        self.diz_vertici = {}
        self.costo_max = None
        self.percorso_migliore = []
    def get_anni(self):
        return DAO.get_anni()

    def get_forme(self):
        return DAO.get_forme()

    def crea_grafo(self, anno, forma):
        self.grafo.clear()
        # Cancello diz o liste se le ho inizializzate se uno schiacca due volte pulsante non ci sono problemi
        self.diz_vertici.clear()
        nodi = DAO.get_vertici()
        for n in nodi:
            self.diz_vertici[n.id] = n
            self.grafo.add_node(n)
        archi = DAO.get_archi(anno, forma)
        for a in archi:
            self.grafo.add_edge(self.diz_vertici[a[0]], self.diz_vertici[a[1]], weight=a[2])

    # Ritorno lunghezza nodi e archi
    def num_nodi(self):
        return len(self.grafo.nodes)

    def num_archi(self):
        return len(self.grafo.edges)

    def get_peso_nodi(self):
        diz = {}
        for v in self.diz_vertici.values():
            somma = 0
            for vicino in self.grafo.neighbors(v):
                somma += self.grafo[v][vicino]["weight"]
            diz[v] = somma
        return diz

    def get_ciclo_max(self):
        self.costo_max = -100000000
        self.percorso_migliore.clear()
        nodi = self.grafo.nodes
        for n in nodi:
            self.ricorsione([n])
        return self.costo_max, self.percorso_migliore

    def ricorsione(self, lista_nodi_tutti):
        if self.costo_tot(lista_nodi_tutti) > self.costo_max:
            self.costo_max = copy.deepcopy(self.costo_tot(lista_nodi_tutti))
            self.percorso_migliore = copy.deepcopy(lista_nodi_tutti)

        if len(lista_nodi_tutti) > 1:
            for nodo in self.grafo.neighbors(lista_nodi_tutti[-1]):
                if (nodo not in lista_nodi_tutti and self.grafo[lista_nodi_tutti[-1]][nodo]["weight"] >
                        self.grafo[lista_nodi_tutti[-2]][lista_nodi_tutti[-1]]["weight"]):
                    lista_nodi_tutti.append(nodo)
                    self.ricorsione(lista_nodi_tutti)
                    lista_nodi_tutti.pop()
        else:
            for nodo in self.grafo.neighbors(lista_nodi_tutti[-1]):
                lista_nodi_tutti.append(nodo)
                self.ricorsione(lista_nodi_tutti)
                lista_nodi_tutti.pop()



    # Lo uso nella ricorsione per calcolarmi il costo del ciclo
    def costo_tot(self, lista_nodi_tutti):
        d = 0
        for num in range(0, len(lista_nodi_tutti)-1):
            lat1 = lista_nodi_tutti[num].Lat
            lng1 = lista_nodi_tutti[num].Lng
            lat2 = lista_nodi_tutti[num+1].Lat
            lng2 = lista_nodi_tutti[num+1].Lng
            d += distance.geodesic((lat1, lng1), (lat2, lng2)).km
        return d

    def get_archi(self, lista):
        listabella = []
        for i in range(len(lista)-1):
            listabella.append((lista[i], lista[i+1],self.grafo[lista[i]][lista[i+1]]['weight'], self.get_distanza(lista[i], lista[i+1])))
        return listabella

    def get_distanza(self, a1, a2):
        lat1 = a1.Lat
        lon1 = a1.Lng
        lat2 = a2.Lat
        lon2 = a2.Lng
        d = distance.geodesic((lat1, lon1), (lat2, lon2)).km
        return d