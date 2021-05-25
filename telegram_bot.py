import telegram
import graphs
import networkx as nx

from telegram.ext import Updater
from telegram.ext import CommandHandler


data = mod_data = graph = 0

started = False
user_location = False

lat = lon = 0

my_help_message = """
Hi! I see that you have asked for help. Here are all the commands
that you can execute:

*/start
Initializes the bot

* /author
To know my creator.

* /graph ⟨distance⟩ ⟨population⟩
To create a new graph with a maximum distance=⟨distance⟩ between
each pair of connected cities and a minimum of population=⟨population⟩
Example:
    /graph 300 100000

*/nodes
To know the number of cities in the graph

*/edges
To know the number of edges connecting the graph

*/components
To know the number of connected components in the graph

*/plotpop ⟨dist⟩ [⟨lat⟩ ⟨lon⟩]
Shows a map with all the cities in the graphs at distance<=dist from ⟨lat⟩ ⟨lon⟩.
Example:
    /plotpop 1000 41.39 2.07

*/plotgraph ⟨dist⟩ [⟨lat⟩ ⟨lon⟩]
Shows a map with all the cities in the graphs at distance<=dist from ⟨lat⟩ ⟨lon⟩ and all the edges connecting the cities.
Example:
    /plotgraph 1000 41.39 2.07

*/route ⟨src⟩ ⟨dst⟩
Shows a map with all the edges that make the shortest past between the two cities.
Example:
    /route Lixbun, pt - culugne, de
    Where Lixbun is Lisbon, Portugal and culugne is Cologne, Deutschland
    That's right, I can sense which city you meant. But... only if you put the country code correctly
"""

author_message = "Daniel Torres"


def start(bot, update):
    global started
    started = True
    global data, mod_data, graph
    data = graphs.obtain_worldcitiespop_data()
    mod_data = data.dropna(subset=['Population'])
    population = 100000
    distance = 300
    mod_data = data[data.Population >= population]
    graph = graphs.generate_graph(mod_data, distance, population)
    bot.send_message(chat_id=update.message.chat_id, text="Hi")

def my_help(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=my_help_message)


def author(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=author_message)


def graph(bot, update):
    global started
    if started:
        message = update.message.text.split()
        if len(message) != 3:
            wrong_parameter = "You must have written something wrong. Try sending the whole command again"
            bot.send_message(chat_id=update.message.chat_id, text=wrong_parameter)
        else:
            global data, mod_data, graph
            distance = int(message[1])
            population = int(message[2])
            mod_data = data[data.Population >= population]
            graph = graphs.generate_graph(mod_data, distance, population)
            bot.send_message(chat_id=update.message.chat_id, text="Graph created")
    else:
        bot.send_message(chat_id=update.message.chat_id, text="You need to /start first...")


def nodes(bot, update):
    global started
    if started:
        global graph
        num_nodes = graph.number_of_nodes()
        bot.send_message(chat_id=update.message.chat_id, text=str(num_nodes))
    else:
        bot.send_message(chat_id=update.message.chat_id, text="You need to /start first...")


def edges(bot, update):
    global started
    if started:
        global graph
        num_edges = graph.number_of_edges()
        bot.send_message(chat_id=update.message.chat_id, text=str(num_edges))
    else:
        bot.send_message(chat_id=update.message.chat_id, text="You need to /start first...")
        

def components(bot, update):
    global started
    if started:
        global graph
        num_com = nx.number_connected_components(graph)
        bot.send_message(chat_id=update.message.chat_id, text=str(num_com))
    else:
        bot.send_message(chat_id=update.message.chat_id, text="You need to /start first...")


def plotpop(bot, update):
    global started
    if started:
        global mod_data
        message = update.message.text.split()
        if len(message) != 4:
            wrong_parameter = "You must have written something wrong. Try sending the whole command again"
            bot.send_message(chat_id=update.message.chat_id, text=wrong_parameter)
        else:
            dist = int(message[1])
            lat = float(message[2])
            lon = float(message[3])
            bot.send_message(chat_id=update.message.chat_id, text="Creating the map")
            message = graphs.plotpop(mod_data, dist, lat, lon)
            if message == "":
                bot.send_photo(chat_id=update.message.chat_id, photo=open('plotpop_map.png', 'rb'))
            else:
                bot.send_message(chat_id=update.message.chat_id, text="There was an error, please try again")
    else:
        bot.send_message(chat_id=update.message.chat_id, text="You need to /start first...")


def plotgraph(bot, update):
    global started
    if started:
        global graph, mod_data
        message = update.message.text.split()
        if len(message) != 4:
            wrong_parameter = "You must have written something wrong. Try sending the whole command again"
            bot.send_message(chat_id=update.message.chat_id, text=wrong_parameter)
        else:
            dist = int(message[1])
            lat = float(message[2])
            lon = float(message[3])
            bot.send_message(chat_id=update.message.chat_id, text="Creating the map")
            message = graphs.plotgraph(graph, mod_data, dist, lat, lon)
            if message == "":
                bot.send_photo(chat_id=update.message.chat_id, photo=open('plotgraph_map.png', 'rb'))
            else:
                bot.send_message(chat_id=update.message.chat_id, text="There was an error, please try again")
    else:
        bot.send_message(chat_id=update.message.chat_id, text="You need to /start first...")


def route(bot, update):
    global started
    if started:
        global graph, mod_data
        message = update.message.text
        srcCity = ""
        for word in message.split(',')[0].split()[1:]:
            srcCity += word + ' '
        srcCity = srcCity[:-1]
        srcCountry = message.split(',')[1].split('-')[0][1:-1]
        dstCity = ""
        for word in message.split(',')[1].split('-')[1].split():
            dstCity += word + ' '
        dstCity = dstCity[:-1]
        dstCountry = str(message.split(',')[2])[1:]
        bot.send_message(chat_id=update.message.chat_id, text="Creating the map")
        messages = graphs.route(graph, mod_data, srcCity, srcCountry, dstCity, dstCountry)
        all_good = True
        for m in messages:
            bot.send_message(chat_id=update.message.chat_id, text=m)
            if m == 'Source could not be found' or m == 'Destination could not be found' or m == 'There is no path available between this two cities':
                all_good = False
        if all_good:
            bot.send_photo(chat_id=update.message.chat_id, photo=open('route_map.png', 'rb'))
    else:
        bot.send_message(chat_id=update.message.chat_id, text="You need to /start first...")


def where(bot, update, user_data):
    global lat, lon, user_location
    user_location = True
    lat, lon = update.message.location.latitude, update.message.location.longitude


TOKEN = '855910097:AAH3P3y8U23l2xPvljSKdfczKOliIfr7Q2M'

updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('help', my_help))
dispatcher.add_handler(CommandHandler('author', author))
dispatcher.add_handler(CommandHandler('graph', graph))
dispatcher.add_handler(CommandHandler('nodes', nodes))
dispatcher.add_handler(CommandHandler('edges', edges))
dispatcher.add_handler(CommandHandler('components', components))
dispatcher.add_handler(CommandHandler('plotpop', plotpop))
dispatcher.add_handler(CommandHandler('plotgraph', plotgraph))
dispatcher.add_handler(CommandHandler('route', route))
dispatcher.add_handler(CommandHandler('where', where))

updater.start_polling()
