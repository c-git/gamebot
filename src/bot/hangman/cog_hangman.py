from typing import Dict, List

import discord
from discord import Embed
from discord.ext import commands
from discord.ext.commands import Context

from src.bot.hangman.game_model import GameModel, State
from src.conf import Conf

conf = Conf.Hangman
"""Map class with setting for this cog to variable"""


class CogHangman(commands.Cog, name='Hangman'):
    def __init__(self):
        # Both dicts need to be kept synced.

        # K: channel_id V: Game
        self.data: Dict[int, GameModel] = {}

        # K: player_id V: [Games] (in order pending started)
        self.pending_setting_word: Dict[int, List[GameModel]] = {}

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
                if data.state == State.WAITING_FOR_WORD:
                    # Game ended and new game started reg new word
                    self.reg_awaiting_word(data)
                    await self.dm_setter(ctx, data)
                await ctx.send(embed=msg)
            elif data.state == State.WAITING_FOR_WORD:
                msg = data.receive_word(ctx.author.id, args[0])
                if data.state == State.WAITING_FOR_GUESS:
                    # Succeeded notify other player to start guessing
                    await ctx.send(
                        f'Word has been set for game in <#{data.channel}>')
                    await self.notify_game_start(ctx, data, msg)
                    # Remove from waiting for guess
                    self.unreg_awaiting_word(data)
                else:
                    # Still waiting send message generated back to user
                    await ctx.send(embed=msg)
            else:
                raise Exception('Unexpected State for GameState')
        else:
            await ctx.send(
                f"I'm sorry I didn't recognize those parameters: {args}")

    ##########################################################################
    # NORMAL COMMANDS
    @base.command(**conf.Command.NEW)
    async def new(self, ctx: Context, other_player: discord.User):
        if self.is_dm(ctx):
            await ctx.send(
                'Error: Games can only be started in server channels')
            return
        old_game = await self.get_game(ctx, False)
        if old_game is not None:
            self.unreg_awaiting_word(old_game)
        new_game = GameModel(ctx.author.id, other_player.id, ctx.channel.id)
        self.data[ctx.channel.id] = new_game
        self.reg_awaiting_word(new_game)
        await self.dm_setter(ctx, new_game)
        await self.disp_with_msg(ctx, new_game, 'New game started')

    @base.command(**conf.Command.DISP)
    async def disp(self, ctx: Context):
        result = f'There are {len(self.data)} game(s) in progress\n'
        awaiting = []
        for player in self.pending_setting_word:
            for _ in range(len(self.pending_setting_word[player])):
                awaiting.append(player)
        for channel, game in self.data.items():
            if game.state == State.WAITING_FOR_WORD:
                assert game.player_setter in awaiting
                awaiting.remove(game.player_setter)
            result += f'Game in <#{channel}> status: {game.status_disp}\n'
        await ctx.send(result)
        assert len(awaiting) == 0, \
            f'Expected all awaiting games to be accounted for but got ' \
            f'{len(awaiting)} left over after printing others {awaiting}'

    ##########################################################################
    # HELPER FUNCTIONS
    @staticmethod
    def is_dm(ctx: Context) -> bool:
        return isinstance(ctx.message.channel, discord.DMChannel)

    @staticmethod
    async def disp_with_msg(ctx: Context, data: GameModel, msg: str):
        await ctx.send(embed=data.as_embed(msg))

    def reg_awaiting_word(self, game: GameModel):
        """
        Registers this game for awaiting a word
        :param game: the game to unregister
        """
        assert game.state.WAITING_FOR_GUESS == State.WAITING_FOR_GUESS
        setter = game.player_setter
        pending = self.pending_setting_word.get(setter)
        if pending is None:
            pending = []
            self.pending_setting_word[setter] = pending
        pending.append(game)

    def unreg_awaiting_word(self, game: GameModel):
        """
        Unregisters this game from awaiting a word if it's registered.
        :param game: the game to unregister
        """
        setter = game.player_setter
        pending = self.pending_setting_word.get(setter)
        if pending is not None and game in pending:
            pending.remove(game)
            if len(pending) < 1:
                self.pending_setting_word.pop(setter)

    async def get_game(self, ctx: Context,
                       should_send_msg_if_not_found=True) -> GameModel:
        if self.is_dm(ctx):
            # Lookup setting a word
            pending = self.pending_setting_word.get(ctx.author.id)
            if pending is not None:
                result = pending[0]  # Get first game pending a word being set
            else:
                result = None
        else:
            result = self.data.get(ctx.channel.id)
        if result is None and should_send_msg_if_not_found:
            await ctx.send(
                'NO GAME IN PROGRESS!!! Please start a new game first')
        return result

    @staticmethod
    async def dm_setter(ctx: Context, game: GameModel):
        user = ctx.bot.get_user(game.player_setter)
        await user.send(
            f'Please supply the word to be guessed here for the game in '
            f'<#{game.channel}>. \n Please use "{ctx.prefix}'
            f'{"".join(ctx.invoked_parents)}" then a space and the word you '
            f'want to set')

    @staticmethod
    async def notify_game_start(ctx: Context, game: GameModel, msg: Embed):
        channel = ctx.bot.get_channel(game.channel)
        await channel.send(embed=msg)
