import os
from threading import Thread

import discord
import flask
from discord.ext import commands
from opylib.log import log, setup_log
from waitress import serve

from src.bot.custom_bot import Bot
from src.conf import Conf
from src.dictionary.validator import Validator

# TODO: Add game instructions
# TODO: Keep track of score
# TODO: Add Web GUI
# TODO: Add playing via DM instead of in channel


##############################################################################


"""
Global Variables
"""

bot: Bot

##############################################################################
""" 
    HTML Control Section
    Had to put them in the same file to resolve issues with getting 
    access to variable values
    
"""
app = flask.Flask('game-bot')


@app.route('/')
def home():
    return flask.render_template('index.html')


def run():
    serve(app, host="0.0.0.0", port=8080)


def display_start():
    Thread(target=run).start()


##############################################################################


def main():
    global bot
    setup_log(only_std_out=True)
    log('Main Started')

    intents = discord.Intents.default()
    intents.members = True

    bot = Bot(command_prefix=commands.when_mentioned_or(Conf.COMMAND_PREFIX),
              description=Conf.BOT_DESCRIPTION, intents=intents)

    display_start()
    bot.run(os.getenv(Conf.ENV.TOKEN))


if __name__ == '__main__':
    main()
