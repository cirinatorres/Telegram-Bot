import requests
import pandas as pd
import networkx as nx

from fuzzywuzzy import fuzz
from haversine import haversine
from staticmap import StaticMap, CircleMarker, Line

max_population = 0
world_grid = []


# def compare_corners(region, lat, lon):
#     global regions_and_limits
#     if region not in regions_and_limits:
#             regions_and_limits[region] = []
#             for i in range(4):
#                 regions_and_limits[region].append([lat, lon])
#     else:
#         if lat > regions_and_limits[region][0][0]:
#             # Top
#             regions_and_limits[region][0] = [lat,lon]
#         elif lat < regions_and_limits[region][1][0]:
#             # Bottom
#             regions_and_limits[region][1] = [lat,lon]
#         if lon < regions_and_limits[region][2][1]:
#             # Left
#             regions_and_limits[region][2] = [lat,lon]
#         elif lon > regions_and_limits[region][3][1]:
#             # Right
#             regions_and_limits[region][3] = [lat,lon]


def obtain_worldcitiespop_data():
    url = 'https://github.com/jordi-petit/lp-graphbot-2019/' \
        'blob/master/dades/worldcitiespop.csv.gz?raw=true'
    data = requests.get(url)
    filename = 'worldcitiespop.csv.gz'
    with open(filename, "wb") as file:
        file.write(data.content)
    df_data = pd.read_csv(filename,compression='gzip',low_memory=False,error_bad_lines=False)
    return df_data


def make_world_grid(distance):
    global world_grid
    world_grid = []
    start_lat = -90.0
    start_lon = -180.0
    while (start_lat != 90.0):
        for i in range(int(start_lat*10),900+1):
            d = haversine((start_lat,start_lon),(i/10.0,start_lon),unit='km')
            if d > distance or i == 900:
                if i == 900:
                    start_lat = i/10.0
                else:
                    start_lat = max(i-1, int(start_lat*10))/10.0
                longitudes = []
                while (start_lon != 180.0):
                    for j in range(int(start_lon*10),1800+1):
                        d = haversine((start_lat,start_lon),(start_lat,j/10.0),unit='km')
                        if d > distance or j == 1800:
                            if j == 1800:
                                start_lon = j/10.0
                            else:
                                start_lon = max(j-1, int(start_lon*10))/10.0
                            break
                    longitudes.append([start_lat,start_lon])
                start_lon = -180.0
                world_grid.append(longitudes)
                break


def add_box_to_box_edges(graph, mod_data, coord_city1, c1, row, col, distance):
    for c2 in world_grid[row][col][2:]:
        coord_city2 = (mod_data.iloc[c2]['Latitude'],mod_data.iloc[c2]['Longitude'])
        harvesine_distance = haversine(coord_city1,coord_city2,unit='km')
        if (harvesine_distance <= distance):
            graph.add_edge(c1,c2,weight=harvesine_distance)
    return graph


def add_cross_edges(graph, mod_data, distance):
    global world_grid
    for row in range(len(world_grid[:-1])):
        for col in range(len(world_grid[row][:-1])):
            for i in range(2,len(world_grid[row][col])):
                c1 = world_grid[row][col][i]
                coord_city = (mod_data.iloc[c1]['Latitude'],mod_data.iloc[c1]['Longitude'])
                graph = add_box_to_box_edges(graph, mod_data, coord_city, c1, row, col+1, distance)
                y = 0
                while(coord_city[1] > world_grid[row+1][y][1]):
                    y += 1
                graph = add_box_to_box_edges(graph, mod_data, coord_city, c1, row+1, y, distance)
                if y > 0:
                    graph = add_box_to_box_edges(graph, mod_data, coord_city, c1, row+1, y-1, distance)
                if y < (len(world_grid[row+1])-1):
                    graph = add_box_to_box_edges(graph, mod_data, coord_city, c1, row+1, y+1, distance)
    for row in range(len(world_grid)):
        columns = [0, len(world_grid[row])-1]
        for col in columns:
            for i in range(2,len(world_grid[row][col])):
                c1 = world_grid[row][col][i]
                coord_city = (mod_data.iloc[c1]['Latitude'],mod_data.iloc[c1]['Longitude'])
                graph = add_box_to_box_edges(graph, mod_data, coord_city, c1, row, col, distance)
    return graph    


def add_edges_to_graph(mod_data, graph, distance):
    global world_grid
    for row in world_grid:
        for col in row:
            for i in range(2,len(col)-1):
                c1 = col[i]
                coord_city1 = (mod_data.iloc[c1]['Latitude'],mod_data.iloc[c1]['Longitude'])
                for j in range(i+1,len(col)):
                    c2 = col[j]
                    coord_city2 = (mod_data.iloc[c2]['Latitude'],mod_data.iloc[c2]['Longitude'])
                    harvesine_distance = haversine(coord_city1,coord_city2,unit='km')
                    if (harvesine_distance <= distance):
                        graph.add_edge(c1,c2,weight=harvesine_distance)
    graph = add_cross_edges(graph, mod_data, distance)
    return graph


def generate_graph(mod_data, distance, population):
    make_world_grid(distance)
    global world_grid
    global max_population
    max_population = mod_data['Population'].max()

    graph = nx.Graph()
    for i in range(len(mod_data)):
        graph.add_node(i)
        coord_city = (mod_data.iloc[i]['Latitude'],mod_data.iloc[i]['Longitude'])
        x = y = 0
        while(coord_city[0] > world_grid[x][0][0]):
            x += 1
        while(coord_city[1] > world_grid[x][y][1]):
            y += 1
        world_grid[x][y].append(i)
    graph = add_edges_to_graph(mod_data, graph, distance)
    return graph


# def generate_graph(data, distance, population):
#     global max_population
#     max_population = df_data['Population'].max()

#     graph = nx.Graph()
#     for i in range(len(data)-1):
#         coord_city1 = (data.iloc[i]['Latitude'],data.iloc[i]['Longitude'])
#         for j in range(i+1,len(data)):
#             coord_city2 = (data.iloc[j]['Latitude'],data.iloc[j]['Longitude'])
#             harvesine_distance = haversine(coord_city1,coord_city2,unit='km')
#             if (harvesine_distance <= distance):
#                 graph.add_edge(i,j,weight=harvesine_distance)
#             else:
#                 if not graph.has_node(i):
#                     graph.add_node(i)
#                 if not graph.has_node(j):
#                     graph.add_node(j)
#     return graph


def plot_map(data, dist, lat, lon, varyNodeSize):
    plot_map = StaticMap(1500, 1500)
    nodes_in_map = []
    for i in range(len(data)):
        coord_city = (data.iloc[i]['Latitude'],data.iloc[i]['Longitude'])
        if haversine((lat,lon),coord_city) <= dist:
            if i not in nodes_in_map:
                nodes_in_map.append(i)
            if varyNodeSize:
                global max_population
                nodeSize = int(600*(data.iloc[i]['Population']/max_population))
            else:
                nodeSize = 7
            marker = CircleMarker((data.iloc[i]['Longitude'], data.iloc[i]['Latitude']), 'red', nodeSize)
            plot_map.add_marker(marker)
            # print(' Country=', data.iloc[i]['Country'],' City=',data.iloc[i]['City'],' AccentCity=',data.iloc[i]['AccentCity'])
    return nodes_in_map, plot_map


def plotpop(data, dist, lat, lon):
    _, plot = plot_map(data, dist, lat, lon, True)
    message = ""
    try:
        plotpop_map = plot.render()
        plotpop_map.save('plotpop_map.png')
        return message
    except RuntimeError as e:
        return e


def add_edges_to_map(graph, data, plot, nodes_in_map):
    for line in nx.generate_adjlist(graph):
        index = int(line.split()[0])
        if index in nodes_in_map:
            nodes_in_map.remove(index)
            coord_city1 = (data.iloc[index]['Longitude'],data.iloc[index]['Latitude'])
            for i in line.split():
                i = int(i)
                if i != index:
                    coord_city2 = (data.iloc[i]['Longitude'],data.iloc[i]['Latitude'])
                    plot.add_line(Line((coord_city1, coord_city2), 'blue', 3))
    return plot


def plotgraph(graph, data, dist, lat, lon):
    nodes_in_map, plot = plot_map(data, dist, lat, lon, False)
    plot = add_edges_to_map(graph, data, plot, nodes_in_map)
    message = ""
    try:
        plotgraph_map = plot.render()
        plotgraph_map.save('plotgraph_map.png')
        return message
    except RuntimeError as e:
        return e



def src_dst_map(mod_data, path):
    plot_map = StaticMap(1500, 1500)
    marker = CircleMarker((mod_data.iloc[path[0]]['Longitude'], mod_data.iloc[path[0]]['Latitude']), 'red', 7)
    plot_map.add_marker(marker)
    for i in range(1,len(path)):
        marker = CircleMarker((mod_data.iloc[path[i]]['Longitude'], mod_data.iloc[path[i]]['Latitude']), 'red', 7)
        plot_map.add_marker(marker)
        coord_city1 = (mod_data.iloc[path[i-1]]['Longitude'],mod_data.iloc[path[i-1]]['Latitude'])
        coord_city2 = (mod_data.iloc[path[i]]['Longitude'],mod_data.iloc[path[i]]['Latitude'])
        plot_map.add_line(Line((coord_city1, coord_city2), 'blue', 3))
    return plot_map


def route(graph, mod_data, srcCity, srcCountry, dstCity, dstCountry):
    # Doesn't work. For some reason srcRow isn't the index on mod_data.
    #               mod_data.loc[...] returns the index on the original csv prior all and filtering.
    #               http://i.imgur.com/bsAGvYr.gif
    # # srcRow = mod_data.loc[((mod_data['City'] == srcCity) | (mod_data['AccentCity'] == srcCity)) & (mod_data['Country'] == srcCountry)]
    # # if not srcRow.empty:
    # #     srcIndex = srcRow.index[0]
    # # dstRow = mod_data.loc[((mod_data['City'] == dstCity) | (mod_data['AccentCity'] == dstCity)) & (mod_data['Country'] == dstCountry)]
    # # if not dstRow.empty:
    # #     dstIndex = dstRow.index[0]
    # if nx.has_path(graph, srcIndex, dstIndex):
    messages = []
    srcIndex = dstIndex = -1
    srcFound = dstFound = False
    srcPercentage = dstPercentage = 0
    for i in range(len(mod_data)):
        if srcFound and dstFound:
            break
        if (mod_data.iloc[i]['City'] == srcCity or mod_data.iloc[i]['AccentCity'] == srcCity) and mod_data.iloc[i]['Country'] == srcCountry:
            srcIndex = i
            srcFound = True
        elif (mod_data.iloc[i]['City'] == dstCity or mod_data.iloc[i]['AccentCity'] == dstCity) and mod_data.iloc[i]['Country'] == dstCountry:
            dstIndex = i
            dstFound = True
        else:
            if not srcFound and mod_data.iloc[i]['Country'] == srcCountry:
                percentage = max(fuzz.ratio(mod_data.iloc[i]['City'], srcCity), fuzz.ratio(mod_data.iloc[i]['AccentCity'], srcCity))
                if percentage > srcPercentage:
                    srcIndex = i
                    srcPercentage = percentage
            if not dstFound and mod_data.iloc[i]['Country'] == dstCountry:
                percentage = max(fuzz.ratio(mod_data.iloc[i]['City'], dstCity), fuzz.ratio(mod_data.iloc[i]['AccentCity'], dstCity))
                if percentage > dstPercentage:
                    dstIndex = i
                    dstPercentage = percentage
    if srcIndex == dstIndex:
        messages.append('Source and Destination are the same place')
    cut_percentage = 60
    if (srcFound or srcPercentage > cut_percentage) and (dstFound or dstPercentage > cut_percentage):
        if not srcFound:
            m = 'Source was estimated. Routing from ' + str(mod_data.iloc[srcIndex]['AccentCity']) + ', ' + str(mod_data.iloc[srcIndex]['Country'])
            messages.append(m)
        if not dstFound:
            m = 'Destination was estimated. Routing to ' + str(mod_data.iloc[dstIndex]['AccentCity']) + ', ' + str(mod_data.iloc[dstIndex]['Country'])
            messages.append(m)
        if nx.has_path(graph, srcIndex, dstIndex):
            path = nx.shortest_path(graph,source=srcIndex,target=dstIndex,weight='weight')
            route = src_dst_map(mod_data, path)
            try:
                route_map = route.render()
                route_map.save('route_map.png')
                return messages
            except RuntimeError as e:
                return e
        else:
            messages.append('There is no path available between this two cities')
    else:
        if not srcFound or not srcPercentage > cut_percentage:
            messages.append('Source could not be found')
        if not dstFound or not dstPercentage > cut_percentage:
            messages.append('Destination could not be found')
    return messages


# def find_nearest_city(data, graph, lat, lon):
#     coord_city1 = (lat,lon)
#     min_distance = 1000000
#     index = 0
#     for i in list(graph.nodes()):
#         coord_city2 = (data.iloc[i]['Latitude'],data.iloc[i]['Longitude'])
#         harvesine_distance = haversine(coord_city1,coord_city2,unit='km')
#         if harvesine_distance < min_distance:
#             min_distance = harvesine_distance
#             index = i
#     return index


# def bfs_up_to_distance(data, graph, dist, lat, lon, index):
#     plot_map = StaticMap(1500, 1500)
#     coord_city1 = (lat,lon)
#     coord_city2 = (data.iloc[index]['Latitude'],data.iloc[index]['Longitude'])
#     if haversine(coord_city1,coord_city2,unit='km') <= dist:
#         visited = [False] * len(data)
#         queue = [index]
#         visited[index] = True
#         while len(queue):
#             i = queue.pop(0)
#             coord_city2 = (data.iloc[i]['Latitude'],data.iloc[i]['Longitude'])
#             marker = CircleMarker(coord_city2, 'red', 20)
#             plot_map.add_marker(marker)
#             for (j, adj) in graph.edges([i]):
#                 if not visited[adj]:
#                     visited[adj] = True
#                     coord_city2 = (data.iloc[adj]['Latitude'],data.iloc[adj]['Longitude'])
#                     print(coord_city2)
#                     if haversine(coord_city1,coord_city2,unit='km') <= dist:
#                         # print('adj = ', adj)
#                         queue.append(adj)
#     return plot_map


# Country,City,AccentCity,Region,Population,Latitude,Longitude
# ad,andorra la vella,Andorra la Vella,7,20430.0,42.5,1.5166667

