from discord.ext import commands
import discord

class Comment_Help_Cmd_Cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def comment_help(self, ctx):

        # 注意事項の説明embed
        comment_help_embed = discord.Embed(title="コメント投票方法", color=0x00ff00, description="コメントを投票する際は「$comment_voted レースID コメント文」のような\n形式で送信してください。\n以下の画像は投稿例です")   #テスト版
        comment_help_file = discord.File(r"example_img\ok2.png", filename=r"comment_example.png")
        comment_help_embed.set_image(url=r"attachment://comment_example.png")
        await ctx.author.send(file=comment_help_file, embed=comment_help_embed)

def setup(bot):
    bot.add_cog(Comment_Help_Cmd_Cog(bot))