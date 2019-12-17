import datetime
import discord

from discord.ext import commands


def setup(bot):
    bot.remove_command('help')
    bot.add_cog(HelpCog(bot))


class HelpCog(commands.Cog, name="Help"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help', aliases=['man'])
    async def help(self, ctx, *, command: str=''):
        """
        Help me!
        """
        if not command:
            help_embed= discord.Embed(
                title='',
                timestamp=datetime.datetime.utcnow(),
                #description=f'```apache\n{", ".join(c.prefixes)}```',
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

