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
    async def base(self, ctx: Context, *args):
        if len(args) == 1:
            msg = self.data.move(ctx.author, args[0])
            await self.disp_with_msg(ctx, msg)
        else:
            await ctx.send(
                f"I'm sorry I didn't recognize those parameters: {args}")

    ##########################################################################
    # NORMAL COMMANDS
    @base.command(**conf.Command.NEW)
    async def new(self, ctx: Context, other_player: discord.User):
        self.data = GameState(ctx.author.id, other_player.id)
        await self.disp_with_msg(ctx, 'New game started')

    ##########################################################################
    # HELPER FUNCTIONS
    async def disp_with_msg(self, ctx: Context, msg: str):
        await ctx.send(embed=self.data.as_embed())
        await ctx.send(f'{msg}')
