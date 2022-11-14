from discord.ext import commands
import discord

class Help_Cmd_Cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(title="投票botの使い方", description="投票botのコマンドです\n投票したいレースの番号を「$vote_start レースID」のように送信すると\nDMにて投票が開始されます", color=0xeee657)
        
        # botのタイトル表記
        embed.set_author(name='絶対競馬予想する君', icon_url=self.bot.user.avatar.url)


        # コマンドの説明
        embed.add_field(name="$vote_start xxxxxx", value="投票を開始します。DMに投票項目が生成されます(xxxxxxはレースID)", inline=False)
        embed.add_field(name="$help", value="botの使い方（本メッセージ）", inline=False)

        # 画像の描画
        file = discord.File(r"paper_logos\logo.jpg", filename=r"keiba_logo.png")
        embed.set_image(url=r"attachment://keiba_logo.png")

        # 開発者
        embed.set_footer(text="made by Domzou")

        await ctx.channel.send(file=file, embed=embed)



def setup(bot):
    bot.add_cog(Help_Cmd_Cog(bot))