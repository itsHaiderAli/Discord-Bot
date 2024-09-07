import discord
from discord.ext import commands, tasks
from discord.utils import get
from db.database import Database
import asyncio

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Database()

    async def has_role(self, ctx, role_id):
        role = get(ctx.guild.roles, id=role_id)
        return role in ctx.author.roles

    @commands.command()
    async def warn(self, ctx, member: discord.Member, *, reason=None):
        if await self.has_role(ctx, int(self.bot.config['STAFF_ROLE_ID'])):
            self.db.add_warning(member.id, reason)
            await member.send(f'You have been warned for: {reason}')
            await ctx.send(f'{member.mention} has been warned for: {reason}')
            mod_log_channel = self.bot.get_channel(int(self.bot.config['MOD_LOG_CHANNEL_ID']))
            await mod_log_channel.send(f'{ctx.author.mention} warned {member.mention} for: {reason}')
        else:
            await ctx.send("You do not have permission to use this command.")

    @commands.command()
    async def mute(self, ctx, member: discord.Member, duration: str, *, reason=None):
        if await self.has_role(ctx, int(self.bot.config['STAFF_ROLE_ID'])):
            muted_role = get(ctx.guild.roles, id=int(self.bot.config['MUTED_ROLE_ID']))
            await member.add_roles(muted_role)
            self.db.add_mute(member.id, duration, reason)
            await member.send(f'You have been muted for {duration} for: {reason}')
            await ctx.send(f'{member.mention} has been muted for {duration} for: {reason}')
            mod_log_channel = self.bot.get_channel(int(self.bot.config['MOD_LOG_CHANNEL_ID']))
            await mod_log_channel.send(f'{ctx.author.mention} muted {member.mention} for {duration} for: {reason}')

            # Convert duration to seconds and unmute after the time expires
            time_multiplier = {'m': 60, 'h': 3600, 'd': 86400}
            duration_seconds = int(duration[:-1]) * time_multiplier[duration[-1]]

            await asyncio.sleep(duration_seconds)
            await member.remove_roles(muted_role)
            await member.send(f'You have been unmuted.')
            await mod_log_channel.send(f'{member.mention} has been unmuted.')

    @commands.command()
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        if await self.has_role(ctx, int(self.bot.config['STAFF_ROLE_ID'])):
            await member.ban(reason=reason)
            self.db.add_ban(member.id, reason)
            await member.send(f'You have been banned for: {reason}')
            await ctx.send(f'{member.mention} has been banned for: {reason}')
            mod_log_channel = self.bot.get_channel(int(self.bot.config['MOD_LOG_CHANNEL_ID']))
            await mod_log_channel.send(f'{ctx.author.mention} banned {member.mention} for: {reason}')

    @commands.command()
    async def warnings(self, ctx, member: discord.Member):
        if await self.has_role(ctx, int(self.bot.config['STAFF_ROLE_ID'])):
            warnings = self.db.get_warnings(member.id)
            if warnings:
                warnings_list = '\n'.join([f'{w[1]}: {w[0]}' for w in warnings])
                await ctx.send(f'{member.mention} has {len(warnings)} warning(s):\n{warnings_list}')
            else:
                await ctx.send(f'{member.mention} has no warnings.')
        else:
            await ctx.send("You do not have permission to use this command.")

def setup(bot):
    bot.add_cog(Moderation(bot))
