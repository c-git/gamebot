from typing import Optional

import discord
from discord.ext import commands
from discord.ext.commands import Context

from src.bot.hangman.game_state import GameState, State
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
            if data.state == State.WAITING_FOR_GUESS:
                msg = data.receive_guess(ctx.author.id, args[0])
            elif data.state == State.WAITING_FOR_WORD:
                msg = data.receive_word(ctx.author.id, args[0])
            else:
                raise Exception('Unexpected State for GameState')
            await ctx.send(embed=msg)
            # TODO: OnSet word send message to channel where game was started
        else:
            await ctx.send(
                f"I'm sorry I didn't recognize those parameters: {args}")

    ##########################################################################
    # NORMAL COMMANDS
    @base.command(**conf.Command.NEW)
    async def new(self, ctx: Context, other_player: discord.User):
        # TODO Consider restricting game to only being started in channel to
        #  have a place to respond to tell the other player they can start to
        #  guess
        data = GameState(ctx.author.id, other_player.id)
        self.data = data
        await self.disp_with_msg(ctx, data, 'New game started')

    ##########################################################################
    # HELPER FUNCTIONS
    @staticmethod
    async def disp_with_msg(ctx: Context, data: GameState, msg: str):
        await ctx.send(embed=data.as_embed(msg))

    async def get_game(self, ctx: Context) -> GameState:
        # TODO Add support for multiple simultaneous games
        result = self.data
        if result is None:
            await ctx.send(
                'NO GAME IN PROGRESS!!! Please start a new game first')
        return result
