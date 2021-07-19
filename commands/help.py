import discord
import asyncio
import datetime
from db_actions import Database
from discord.ext import commands
from discord_slash import cog_ext, SlashContext

class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @cog_ext.cog_slash(name="help", description="Show all the commands and their syntax")
    async def _help(self, ctx: SlashContext):
        await self.help(ctx)

    @commands.command()
    async def help(self, ctx, command_name = None):
        prefix = Database.find_prefix(ctx.guild.id)[0]

        def gen_embed(category, fields):
            global embed

            if category == 0:
                title = "Help Menu"
                description = "Use reactions to get more info about a category"
                field_vaulues = "🤖 General Commands__Other - not so useful commands__✍️ Sending Messages__Main feature of the bot__📕 Reporting Users__How to report and block user"
            elif category == 1:
                title = "🤖 General Commands"
                description = "General commands desc\narguments in () are required, and <> are optional"
                field_vaulues = f"Latency__`{prefix}ping`__Prefix__`{prefix}prefix (new_prefix)`__Ignore__`{prefix}ignore (action) <user>`__Privacy Policy__`{prefix}privacy`__Contributing__`{prefix}contribute`"
            elif category == 2:
                title = "✍️ Sending messages"
                description = "How to send a new message to user\narguments in () are required, and <> are optional"
                field_vaulues = f"Send__`{prefix}send (Usernam#tag) (message)`\n*must be executed in bot's private messages*"
            elif category == 3:
                title = "📕 Reporting Users"
                description = "How to report a user\narguments in () are required, and <> are optional"
                field_vaulues = f"Submit a report__`{prefix}report (message_id) <reason>`"

            values_list = field_vaulues.split("__")
            values_loop = 0

            bot_name = self.client.user.name
            bot_pfp = self.client.user.avatar_url

            embed=discord.Embed(title=title, description=description, color=0x169cdf)
            embed.timestamp = datetime.datetime.now()
            embed.set_footer(text=bot_name, icon_url=bot_pfp)


            while fields > 0:
                embed.add_field(name=values_list[values_loop], value=values_list[values_loop+1], inline=False)
                values_loop += 2
                fields -= 1

            if help_msg == None:
                return ctx.send(embed=embed)
            else:
                return help_msg.edit(embed=embed)

        if command_name == None:

            help_msg = None
            author = ctx.author
            robot_emoji = "🤖"
            hand_emoji = "✍️"
            book_emoji = "📕"
            home_emoji = "🏠"

            help_msg = await gen_embed(0, 3)

            await help_msg.add_reaction(robot_emoji)
            await help_msg.add_reaction(hand_emoji)
            await help_msg.add_reaction(book_emoji)
            await help_msg.add_reaction(home_emoji)

            def check(reaction, user):
                return user == ctx.author

            while True:
                try:
                    reaction, user = await self.client.wait_for('reaction_add', timeout=25.0, check=check)
                except asyncio.TimeoutError:
                    break
                else:
                    await help_msg.remove_reaction(reaction.emoji, author)

                    if str(reaction.emoji) == robot_emoji:
                        await gen_embed(1, 5)
                    elif str(reaction.emoji) == hand_emoji:
                        await gen_embed(2, 1)
                    elif str(reaction.emoji) == book_emoji:
                        await gen_embed(3, 1)
                    elif str(reaction.emoji) == home_emoji:
                        await gen_embed(0, 3)

        else:
            def find_command():
                command = discord.utils.find(lambda c: c.name == command_name, self.client.commands)
                if command == None:
                    return None
                else:
                    return command
            
            command = find_command()

            if command == None:
                await ctx.send(f"Command `{command_name}` does not exist")
            else:
                await ctx.send(f"Syntax for `{command_name}` is\n`{prefix}{command_name} {command.signature}`")
        
                

def setup(client):
    client.add_cog(Help(client))