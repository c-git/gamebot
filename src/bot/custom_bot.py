import logging

from discord import Embed
from discord.ext import commands
from opylib.log import log

from src.bot.tic_tac_toe.cog_tic_tac_toe import CogTicTacToe
from src.conf import Conf

conf = Conf.TopLevel
"""Map class with setting for this cog to variable"""


class Bot(commands.Bot):
    def __init__(self, **args):
        super().__init__(**args)

        self.tic_tac_toe = CogTicTacToe()
        self.add_cog(self.tic_tac_toe)

        @self.command()
        async def test(ctx):
            result = '```\n'
            result += """
┌────────────────────────────┐
│                            │
│     ┌──────┐  ┌──────┐     │
│     │      │  │      │     │
│     │      │  │      │     │
│     └──────┘  └──────┘     │
│                            │
│                            │
│          ┌──────┐          │
│          │      │          │
│          └──────┘          │
│                            │
│                            │
│                            │
│                            │
│                            │
└────────────────────────────┘
"""
            result += '```'
            await ctx.send(
                embed=Embed(color=Conf.EMBED_COLOR, description=result))

        @self.command(help="Echos back the message in an embed")
        async def echo(ctx, *, msg: str):
            await ctx.send(embed=Embed(color=Conf.EMBED_COLOR, description=msg))

        # TOP Level Commands (No Category)
        @self.command(**conf.Command.PING)
        async def ping(ctx):
            """
            Responds with pong if bot can talk here
            :param ctx: The Context
            """
            await ctx.send('pong')

        @self.event
        async def on_command_error(ctx, error):
            if isinstance(error, commands.errors.CommandNotFound):
                log(error, logging.DEBUG)
                await ctx.send('Command Not Found (Maybe you have a typo)')
            elif isinstance(error, commands.errors.UserInputError):
                log(error, logging.INFO)
                await ctx.send(error)
            elif isinstance(error, commands.errors.MissingAnyRole):
                log(error, logging.INFO)
                await ctx.send('Restricted Command')
            elif isinstance(error, commands.errors.CheckFailure):
                log(error,
                    logging.DEBUG)  # Mostly expected to be because of wrong
                # channel
            else:
                # Command failed for an unexpected reason. Usually this
                # shouldn't happen
                log(error, logging.WARNING)
                await ctx.send('Command Failed!!!')

        @self.event
        async def on_ready():
            log(f'Successfully logged in as {self.user}')
