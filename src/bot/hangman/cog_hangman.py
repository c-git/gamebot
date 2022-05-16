from typing import Optional

import discord
from discord.ext import commands
from discord.ext.commands import Context

from src.bot.hangman.game_state import GameState
from src.conf import Conf

conf = Conf.Hangman
"""Map class with setting for this cog to variable"""


class CogHangman(commands.Cog, name='Hangman'):
    def __init__(self):
        self.data: Optional[GameState] = None

    ##########################################################################
    # BASE GROUP
    @commands.group(**conf.BASE_GROUP)
    async def base(self, ctx: Context, *args):
        if len(args) == 1:
            data = await self.get_game(ctx)
            if data is None:
                return
            msg = data.user_input(ctx.author.id, args[0])
            await self.disp_with_msg(ctx, data, msg)
        else:
            await ctx.send(
                f"I'm sorry I didn't recognize those parameters: {args}")

    ##########################################################################
    # NORMAL COMMANDS
    @base.command(**conf.Command.NEW)
    async def new(self, ctx: Context, other_player: discord.User):
        data = GameState(ctx.author.id, other_player.id)
        self.data = data
        await self.disp_with_msg(ctx, data, 'New game started')

    ##########################################################################
    # HELPER FUNCTIONS
    @staticmethod
    async def disp_with_msg(ctx: Context, data: GameState, msg: str):
        await ctx.send(embed=data.as_embed())
        await ctx.send(f'{msg}')

    async def get_game(self, ctx: Context) -> GameState:
        # TODO Add support for multiple simultaneous games
        result = self.data
        if result is None:
            await ctx.send(
                'NO GAME IN PROGRESS!!! Please start a new game first')
        return result
