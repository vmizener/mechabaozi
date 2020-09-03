import datetime
import discord

from lib.globals import COMMAND_PREFIX
from lib.command import command
from lib.base_cog import BaseCog


def setup(bot):
    bot.remove_command('help')
    bot.add_cog(GeneralCog(bot))


class GeneralCog(BaseCog, name="General"):
    """ Contains general, commonly used commands """

    @command()
    async def help(self, ctx, *, keyword=None):
        """
        Get helpful information on bot cogs and commands.

        Will display help with the following priorities:
            If `keyword` is empty, all non-hidden commands will be listed, organized by cog.
            If `keyword` matches a known cog, information about that cog will be displayed, along with its commands.
            If `keyword` matches a known, non-hidden command, that command's usage will be displayed.

        :kwarg keyword str:     The cog or command name to get help on.  If empty, lists all commands organized by cog.
        """
        help_embed = discord.Embed(
            timestamp=datetime.datetime.utcnow(),
            color=discord.Color.dark_blue(),
        )
        help_embed.set_footer(text='help')
        if not keyword:
            # List all known commands, organized by cog
            help_embed.title='All Commands List'
            help_embed.description = \
                f'Yo, I\'ve listed all my commands below, organized by cog.\n' \
                f'E.g. `{COMMAND_PREFIX}hi` to say hi (or something)\n' \
                f'Use `{COMMAND_PREFIX}help <cog|command>` for more info'
            cog_to_cmd_map = {}
            for cmd in self.bot.commands:
                cog_name = cmd.cog.qualified_name
                if cog_name not in cog_to_cmd_map:
                    cog_to_cmd_map[cog_name] = []
                cog_to_cmd_map[cog_name].append(cmd)
            for cog_name, cmd_list in sorted(cog_to_cmd_map.items()):
                cog_cmd_fmt_list = []
                visible_commands = [cmd for cmd in cmd_list if not cmd.hidden]
                if len(visible_commands) == 0:
                    continue
                for cmd in sorted(visible_commands, key=lambda cmd: str(cmd)):
                    cog_cmd_fmt_list.append(f'  • `{COMMAND_PREFIX}{cmd.name}` - {cmd.short_doc}')
                help_embed.add_field(
                    name=cog_name,
                    value='\n'.join(cog_cmd_fmt_list),
                    inline=False,
                )
        elif command := self.bot.get_command(keyword):
            # Display info on a specific command
            title_str = command.name
            if parent_name := command.full_parent_name:
                title_str = f'{parent_name} {title_str}'
            help_embed.title = f'`{COMMAND_PREFIX}{title_str}{" "+command.signature if command.signature else ""}`'
            help_embed.set_footer(text=f'help {title_str}')
            help_embed.description = command.help
            if hasattr(command, 'commands') and command.commands:
                if len(visible_subcommands := [c for c in command.commands if not c.hidden]) > 0:
                    help_embed.add_field(
                        name='Subcommands',
                        value='\n'.join([
                            f'  • `{COMMAND_PREFIX}{c.full_parent_name} {c.name}` - {c.short_doc}'
                            for c in visible_subcommands
                        ]),
                    )
            if command.aliases:
                help_embed.add_field(
                    name='Aliases',
                    value=' | '.join([f'`{alias}`' for alias in command.aliases]),
                )
        elif cog := self.bot.get_cog(keyword):
            # Display info on a specific cog
            help_embed.title = cog.qualified_name
            help_embed.set_footer(text=f'help {cog.qualified_name}')
            help_embed.description = cog.description
            cog_cmd_fmt_list = []
            for cmd in cog.get_commands():
                if not cmd.hidden:
                    cog_cmd_fmt_list.append(f'  • `{COMMAND_PREFIX}{cmd.name}` - {cmd.short_doc}')
            if len(cog_cmd_fmt_list) > 0:
                help_embed.add_field(
                    name='Commands',
                    value='\n'.join(cog_cmd_fmt_list),
                    inline=False,
                )
        else:
            # Report unknown input
            help_embed.title = 'Unknown Command or Cog Name'
            help_embed.description = \
                f'Yo, I dunno what `{keyword}` is.  Use `!help` for available options.\n(I\'m case-sensitive btw)'
        await ctx.send(embed=help_embed)
