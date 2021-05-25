from importlib import reload
# import importlib
# importlib.reload(module)

distance = 300
population = 100000

# lat = 35.956244
# lon = 128.274388
lat = 41.3948975
lon = 2.078556
dist = 1000
import graphs
data = graphs.obtain_worldcitiespop_data()
mod_data = data.dropna(subset=['Population'])
mod_data = data[data.Population >= population]

# /graph ⟨distance⟩ ⟨population⟩
graph = graphs.generate_graph(mod_data, distance, population)

# /nodes
graph.number_of_nodes()
input('Press ENTER if you want to continue ')
# /edges
graph.number_of_edges()
input('Press ENTER if you want to continue ')
# /components
import networkx as nx
nx.number_connected_components(graph)
input('Press ENTER if you want to continue ')


# /plotpop ⟨dist⟩ [⟨lat⟩ ⟨lon⟩]
graphs.plotpop(mod_data, dist, lat, lon)
input('Press ENTER if you want to continue ')

# /plotgraph ⟨dist⟩ [⟨lat⟩ ⟨lon⟩]
graphs.plotgraph(graph, mod_data, dist, lat, lon)
input('Press ENTER if you want to continue ')

# /route ⟨src⟩ ⟨dst⟩
"Nom, codi_país"
srcCity = 'Anshan'
srcCountry = 'cn'
dstCity = 'yantai'
dstCountry = 'cn'
graphs.route(graph, mod_data, 'Lixbun', 'pt', 'culugne', 'de')
graphs.route(graph, mod_data, 'Lisbon', 'pt', 'cologne', 'de')
graphs.route(graph, mod_data, 'Anshan', 'cn', 'yantai', 'cn')
input('Press ENTER if you want to continue ')
