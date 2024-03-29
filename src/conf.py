class DBKeys:  # Database key values
    TIC_TAC_TOE = 'tictactoe'


class Conf:
    BOT_DESCRIPTION = "GameBot"
    VERSION = '0.0.2'
    COMMAND_PREFIX = '.'
    EMBED_COLOR = 0x373977

    class ENV:  # Environment variable names
        TOKEN = 'TOKEN'

    class TopLevel:
        class Command:
            PING = {
                'name': 'ping',
                'help': 'Tests if the bot is alive. If alive bot responds '
                        'pong'}

    class TicTacToe:
        BASE_GROUP = {'name': 't',
                      'help': 'Grouping for Tic Tac Toe Commands',
                      'invoke_without_command': True}

        class Command:
            NEW = {
                'name': 'new',
                'help': 'Starts a new game'}
            RESET = {
                'name': 'r',
                'help': 'reset/clear the board'}
