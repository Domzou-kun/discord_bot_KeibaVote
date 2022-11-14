from discord.ext import commands
import discord

class Omake_Help_Cmd_Cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def omake_help(self, ctx):
        embed = discord.Embed(title="おまけモード", description="投票botのおまけモードです", color=0xeee657)
        
        # botのタイトル表記
        embed.set_author(name='絶対競馬予想する君', icon_url=self.bot.user.avatar.url)


        # コマンドの説明
        embed.add_field(name="$umadle", value="競馬ガチ勢向けの競馬版wordleが遊べます", inline=False)
        embed.add_field(name="$umaquiz", value="競馬ガチ勢向けの一発勝負クイズが遊べます", inline=False)
        embed.add_field(name="$omake_help", value="おまけモードのヘルプ", inline=False)

        # 開発者
        embed.set_footer(text="made by Domzou")

        await ctx.channel.send(embed=embed)



def setup(bot):
    bot.add_cog(Omake_Help_Cmd_Cog(bot))