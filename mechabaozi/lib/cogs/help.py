import datetime
import discord

from discord.ext import commands

from lib.globals import COMMAND_PREFIX


def setup(bot):
    bot.remove_command('help')
    bot.add_cog(HelpCog(bot))


class HelpCog(commands.Cog, name="Help"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help', aliases=['man'])
    async def help(self, ctx, *, keyword: str=''):
        """
        Get helpful information on bot cogs and commands.

        Will display help with the following priorities:
            If `keyword` is empty, all non-hidden commands will be listed, organized by cog.
            If `keyword` matches a known cog, information about that cog will be displayed, along with its commands.
            If `keyword` matches a known, non-hidden command, that command's usage will be displayed.

        :kwarg keyword str:     The cog or command name to get help on.  If empty, lists all commands organized by cog.
        """
        # List all known commands, organized by cog
        if not command:
            help_embed= discord.Embed(
                title='',
                timestamp=datetime.datetime.utcnow(),
                description=f'```apache\n{COMMAND_PREFIX}```',
                color=discord.Color.from_rgb(48, 105, 152),
            )
            help_embed.set_footer(text='All Commands')
            cog_to_cmd_map = {}
            for cmd in self.bot.commands:
                cog_name = cmd.cog.qualified_name
                if cog_name not in cog_to_cmd_map:
                    cog_to_cmd_map[cog_name] = []
                cog_to_cmd_map[cog_name].append(cmd)
            for cog_name, cmd_list in sorted(cog_to_cmd_map.items()):
                cog_cmd_fmt_list = []
                for cmd in sorted(cmd_list, key=lambda cmd: str(cmd)):
                    cmd_names = ' | '.join([str(cmd)] + cmd.aliases)
                    cog_cmd_fmt_list.append(f'  • {cmd_names}')
                help_embed.add_field(
                    name=cog_name,
                    value='\n'.join(cog_cmd_fmt_list),
                    inline=False,
                )
            await ctx.send(embed=help_embed)
            return

        # TODO: rest of this

