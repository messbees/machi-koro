#!/usr/bin/env python

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import argparse
import logging
from log import init_console_logging
import os
import json
from game import Game
from room import Room
from deck import Deck
from player import Player
import creature, ability
#from exceptions import EvolutionServerException

LOGGER = logging.getLogger(__name__)

class Server:
    f = open('settings.json')
    settings = json.loads(f.read())
    nick = settings["nick"]
    version = settings["version"]


    def __init__(self):
        # why can't i leave it empty?
        LOGGER.info("Server initiated.")

    def load_game(self, id):
        if (os.path.isfile("games/{}.json".format(id))):
            f = open('games/{}.json'.format(id))
            j = json.loads(f.read())
            game = Game('load', json=j)
            return game
        else:
            return False

    def new_game(self, game, players, deck):
        g = Game('init', name=game, players=players, deck=deck.cards)
        return g

    def new_room(self, game, admin):
        LOGGER.info("Player '{}' is trying to create room '{}'.".format(admin, game))
        if (os.path.isfile("rooms/{}.json".format(game))):
            LOGGER.warn('Room with the same name already exists.')
            return False
        else:
            room = Room(game, admin)
            LOGGER.info('Room is initialized.')
            return True

    def join_room(self, game, new_player):
        LOGGER.info("Player '{}' is trying to join room '{}'.".format(new_player, game))
        if (os.path.isfile("rooms/{}.json".format(game))):
            f = open('rooms/{}.json'.format(game))
            room = json.loads(f.read())
            if (room["status"] == 'playing'):
                LOGGER.warn("This game is already playing.")
                return 'PLAYING'
            name = room["name"]
            players = []
            for player in room["players"]:
                players.append(player)
            admin = room["admin"]
            updated = Room(name, admin)
            for player in players:
                if not (updated.connect(player)):
                    LOGGER.warn("Player with nick '{}' is already in this room.".format(player))
                    return 'WRONG_USER'
            if not (updated.connect(new_player)):
                LOGGER.warn("Player with nick '{}' is already in this room.".format(new_player))
                return 'WRONG_USER'
            updated.save()
            LOGGER.info("Joined successfully.")
            return 'JOINED'
        else:
            LOGGER.warn('There is no such room.')
            return 'WRONG_ROOM'

    def begin_game(self, game, admin):
        LOGGER.info("Player '{}' is trying to begin the game in room '{}'.".format(admin, game))
        if not (os.path.isfile("rooms/{}.json".format(game))):
            LOGGER.warn("There is no such game.")
            return 'WRONG_ROOM'
        f = open('rooms/{}.json'.format(game))
        room = json.loads(f.read())
        if (room["status"] == 'playing'):
            LOGGER.warn("This room was closed.")
            return 'PLAYING'
        if not (room["admin"] == admin):
            LOGGER.warn("{} is not a creator of this room.".format("admin"))
            return 'NOT_ADMIN'
        deck = Deck()
        players = []
        for player in room["players"]:
            players.append(Player('init', name=player, deck=deck))
        LOGGER.info('Creating game...')
        g = game_server.new_game(game, players, deck)
        if not (os.path.isfile("games/{}.json".format(g.id))):
            g.save()
            room["status"] = "playing"
            room["id"] = g.id
            with open('rooms/{}.json'.format(room["name"]), 'w') as outfile:
                json.dump(room, outfile)
            LOGGER.info("Game {} begins!".format(g.id))
            return 'BEGIN'
        else:
            LOGGER.warn('Game with same id already exists.')
            return 'WRONG_ID'

    def do_evolution(self, game, player, creature, card):
        LOGGER.info("Player '{}' in game '{}' is trying to play card {} on creature {}.".format(player, game, card, creature))
        if (game["stage"] == "evolution"):
            for p in game["players"]:
                if (p["name"] == player):
                    if not (game["turn"] == player):
                        LOGGER.warn("It is not {}'s turn!".format(player))
                        return 'NOT_YOUR_TURN'

                    #if (creature == 999):
            return 'WRONG_USER'
        else:
            return 'WRONG_STAGE'

game_server = Server()

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.data_string = self.rfile.read(int(self.headers['Content-Length']))
        data = json.loads(self.data_string)
        print("")
        LOGGER.info("---------------------------------------------------")
        if not (data["version"] == Server.version):
            self.send_response(405)
            self.end_headers()
            return
        action = data["action"]

        # calls after trying to fetch room state
        if (action == "ROOM_UPDATE"):
            game = data["room_update"]["game"]
            player = data["room_update"]["player"]
            LOGGER.info("Player '{}' is trying to update state of the room '{}'.".format(player, game))
            if not (os.path.isfile("rooms/{}.json".format(game))):
                LOGGER.warn("There is no such room.")
                self.send_response(404)
                self.end_headers()
                return
            else:
                f = open('rooms/{}.json'.format(game))
                room = json.loads(f.read())
                for p in room["players"]:
                    if (p == player):
                        self.send_response(200)
                        self.send_header("Content-type", "application/json")
                        self.end_headers()
                        self.wfile.write(json.dumps(room))
                        return
                self.send_response(403)
                self.end_headers()
                return

        # calls after trying to fetch game state
        if (action == "GAME_UPDATE"):
            id = data["update"]["game"]
            player = data["update"]["player"]
            LOGGER.info("Player '{}' is trying to update state of the game '{}'.".format(player, id))
            game = game_server.load_game(id)
            if not (game):
                LOGGER.warn("There is no such game.")
                self.send_response(404)
                self.end_headers()
                return
            #LOGGER.debug("Checking if player is in this game...")
            for p in game.players:
                if (player == p.name):
                    #LOGGER.debug("Player name matches, player is in this game!")
                    if (os.path.isfile("rooms/{}.json".format(game.name))):
                        LOGGER.info("Room of this game still exists.")
                        f = open('rooms/{}.json'.format(game.name))
                        room = json.loads(f.read())
                        #LOGGER.debug("Checking if this player is still in the room...")
                        for p in room["players"]:
                            if (p == player):
                                room["players"].remove(player)
                                #LOGGER.debug("Player has connected for the first time. Deleting player from room file...")
                                with open('rooms/{}.json'.format(room["name"]), 'w') as outfile:
                                    json.dump(room, outfile)
                        if (room["players"] == []):
                            LOGGER.info("All players have connected to the game. Deleting room...")
                            os.remove('rooms/{}.json'.format(room["name"]))
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(game.json()))
                    return
            LOGGER.warn("Player is not in this game.")
            self.send_response(403)
            self.end_headers()

    def do_POST(self):
        self.data_string = self.rfile.read(int(self.headers['Content-Length']))
        data = json.loads(self.data_string)
        print("")
        LOGGER.info("---------------------------------------------------")

        if not (data["version"] == Server.version):
            self.send_response(405)
            self.end_headers()
            return
        action = data["action"]

        # calls after creating new room
        if (action == "ROOM_NEW"):
            game = data["room_new"]["game"]
            player = data["room_new"]["player"]
            if (game_server.new_room(game, player)):
                self.send_response(200)
                self.end_headers()
            else:
                self.send_response(409)
                self.end_headers()

        # calls after creating new room, when connecting to existing room, or while updating current room
        if (action == "ROOM_CONNECT"):
            game = data["room_connect"]["game"]
            player = data["room_connect"]["player"]
            status = game_server.join_room(game, player)
            if (status == 'WRONG_USER'):
                self.send_response(409)
                self.end_headers()
            elif(status == 'WRONG_ROOM'):
                self.send_response(404)
                self.end_headers()
            elif(status == 'JOINED'):
                self.send_response(200)
                self.end_headers()
            elif(status == 'PLAYING'):
                self.send_response(403)
                self.end_headers()

        # calls after beginning the game in room by room admin
        if (action == "ROOM_START"):
            game = data["room_start"]["game"]
            admin = data["room_start"]["player"]
            status = game_server.begin_game(game, admin)
            if (status == 'WRONG_ROOM'):
                self.send_response(404)
                self.end_headers()
            elif (status == 'NOT_ADMIN'):
                self.send_response(403)
                self.end_headers()
            elif (status == 'PLAYING'):
                self.send_response(423)
                self.end_headers()
            elif (status == 'WRONG_ID'):
                self.send_response(500)
                self.end_headers()
            elif (status == 'BEGIN'):
                self.send_response(200)
                self.end_headers()


        if (action == "EVOLUTION"):
            game = data["evolution"]["game_id"]
            player = data["evolution"]["player"]
            creature = data["evolution"]["creature"]
            card = data["evolution"]["card"]
            g = game_server.load_game(game)
            if (g == None):
                self.send_response(404)
                self.end_headers()
                return
            status = game_server.do_evolution(g, player, creature, card)

            if (status == 'WRONG_USER'):
                self.send_response(403)
                self.end_headers()
                return
            for p in game.players:
                if (p.name == player):
                    player = p
            if (game_server.do_evolution(game, player, creature, card)):
                self.send_response(200)
                self.end_headers()
                return
            self.send_response(403)
            self.end_headers()

        if (action == "TEST"):
            f = open('rooms/null.json')
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(f.read())

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='HTTP Server')
    parser.add_argument('port', type=int, help='Listening port for HTTP Server')
    parser.add_argument('ip', help='HTTP Server IP')
    parser.add_argument('-v', '--verbose', action='count', default=0, help='Increase output sent to stderr')
    args = parser.parse_args()

    init_console_logging(args.verbose)
    LOGGER.info('Listening on {}:{}'.format(args.ip, args.port))
    HTTPserver = HTTPServer((args.ip, args.port), RequestHandler)
    HTTPserver.serve_forever()
