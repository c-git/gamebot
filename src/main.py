# TODO: Add game instructions
# TODO: Keep track of score
# TODO: Add Web GUI
# TODO: Add playing via DM instead of in channel
import os

from discord.ext import commands
from opylib.log import log, setup_log

from src.bot.custom_bot import Bot
from src.conf import Conf

##############################################################################
"""
Global Variables
"""

bot: Bot


##############################################################################


def main():
    global bot
    setup_log(only_std_out=True)
    log('Main Started')

    bot = Bot(command_prefix=commands.when_mentioned_or(Conf.COMMAND_PREFIX),
              description=Conf.BOT_DESCRIPTION)

    bot.run(os.getenv(Conf.ENV.TOKEN))


if __name__ == '__main__':
    main()
