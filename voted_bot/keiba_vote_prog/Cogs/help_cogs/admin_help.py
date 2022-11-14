from discord.ext import commands
import discord

class Admin_Help_Cmd_Cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def admin_help(self, ctx):

        embed = discord.Embed(title="投票botの使い方", description="投票botのコマンドです\n基本は「$vote_start」で投票を開始してください", color=0xeee657)
        
        # botのタイトル表記
        embed.set_author(name='絶対競馬予想する君', icon_url=self.bot.user.avatar.url)


        # コマンドの説明
        embed.add_field(name="$registed_races", value="登録されているレースを表示します", inline=False)
        embed.add_field(name="$vote_start xxxxxxx", value="投票を開始します。DM充てに投票項目が生成されます(xxxxxxはレースID)", inline=False)
        embed.add_field(name="$comment_voted xxxxxxx", value="コメントの投票を行います(xxxxxxはレースID)", inline=False)
        embed.add_field(name="$race_close_timer", value="レースの投票締切の自動タイマーの起動（必須）", inline=False)
        embed.add_field(name="$Bye_bot", value="botを終了します(特定ユーザーのみ実行可能)", inline=False)

        # 画像の描画
        file = discord.File(r"paper_logos\logo.jpg", filename=r"keiba_logo.png")
        embed.set_image(url=r"attachment://keiba_logo.png")

        # 開発者
        embed.set_footer(text="made by Domzou")

        await ctx.channel.send(file=file, embed=embed)


def setup(bot):
    bot.add_cog(Admin_Help_Cmd_Cog(bot))