from discord import Embed
from discord.ext import commands
from datetime import datetime, timedelta

class AntiRaid(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.join_log = {}  # Dictionary to hold {guild: [join_timestamps]}
        self.raid_detected = False  # To keep track if a raid was detected recently

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild
        if guild.id not in self.join_log:
            self.join_log[guild.id] = []

        self.join_log[guild.id].append(datetime.utcnow())
        await self.handle_raid(member.guild, guild.id)

    async def handle_raid(self, guild, guild_id):
        current_time = datetime.utcnow()
        self.join_log[guild_id] = [t for t in self.join_log[guild_id] if current_time - t <= timedelta(seconds=10)]  #timedelta(seconds=10) = if ur settings is set at 2, it will ban the people that join from the first join and ten seconds later if 2 or more people join

        if len(self.join_log[guild_id]) >= 2: #>= 2: = if 2 or more people join it will trigger the anti raid function, banning them.
            if self.raid_detected:
                return
            
            self.raid_detected = True
            recent_joins = [m for m in guild.members if any(
                m.joined_at.replace(tzinfo=None) >= log_time - timedelta(seconds=10) for log_time in self.join_log[guild_id])] #timedelta(seconds=10) = if ur settings is set at 2, it will ban the people that join from the first join and ten seconds later if 2 or more people join

            banned_users = []
            for member in recent_joins:
                try:
                    banned_users.append(f"{member.mention}")
                    embed = Embed(title="You Have Been Banned",
                                  description=f"You have been banned from {guild.name} because you are suspected of participating in a raid. If you believe this is a mistake, you can contact barkie12 on Discord to appeal.",
                                  color=0xFF0000)
                    await member.send(embed=embed)
                    await member.ban(reason="Automatic ban due to raid detection.")
                except Exception as e:
                    print(f"Failed to ban {member}: {e}")

            self.join_log[guild_id].clear()

            channel = guild.get_channel(CHANNELID)  # Replace with your specific channel ID to receive the message for raid alert.
            if channel:
                embed = Embed(title="⚠ Raid Detected ⚠",
                              description=f"Multiple accounts have joined the server in quick succession. Anti-raid measures have been activated and suspicious accounts have been banned.\n\nUsers:\n{' '.join(banned_users)}",
                              color=0xFF0000)
                await channel.send(embed=embed)
            self.raid_detected = False

async def setup(client):
    await client.add_cog(AntiRaid(client))
    print(f"Cog '{AntiRaid.__name__}' has been loaded.")
