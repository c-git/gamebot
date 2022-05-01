import discord
from discord.ext import commands
from discord.ext.commands import Context

from src.bot.tic_tac_toe.game_state import GameState
from src.conf import Conf

conf = Conf.TicTacToe
"""Map class with setting for this cog to variable"""


class CogTicTacToe(commands.Cog, name='TicTacToe'):
    def __init__(self):
        self.data: GameState = GameState(0, 0)

    ##########################################################################
    # BASE GROUP
    @commands.group(**conf.BASE_GROUP)
    async def base(self, ctx):
        await ctx.send("I'm sorry I didn't recognize that command")

    ##########################################################################
    # NORMAL COMMANDS
    @base.command(**conf.Command.NEW)
    async def new(self, ctx: Context, other_player: discord.User):
        self.data = GameState(ctx.author.id, other_player.id)
