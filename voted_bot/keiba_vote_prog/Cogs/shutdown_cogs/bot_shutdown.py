from tabnanny import check
from discord.ext import commands
import discord
import time
import os

class Shutdown_Cmd_Cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def Bye_bot(self, ctx: commands.context):
        
        print('Bot Shutdown......')
        print(f'We have shutdown in as {self.bot.user}\n')

        # mode flag file remove
        check_dir_path = r'user_record\mode_flag'
        check_files_dir = os.listdir(check_dir_path)
        check_file_name = [ f for f in check_files_dir if os.path.isfile(os.path.join(check_dir_path, f)) ]
        
        removed_file_sum = 0
        if len(check_file_name) != 0:
            check_files = [ os.path.join(check_dir_path, f) for f in check_file_name ]
        
            print('Remove Files')
            max_check_file_len = max([ len(x)+10 for x in check_files ])
            print('-'*max_check_file_len)

            for remove_file in check_files:
                os.remove(remove_file)
                print(f'REMOVE : {remove_file}')
                removed_file_sum += 1
            
            print('-'*max_check_file_len)
            print(f'REMOVE FILES : {removed_file_sum} files...')
            print('-'*max_check_file_len)


        time.sleep(3)

        await self.bot.close()


def setup(bot):
    bot.add_cog(Shutdown_Cmd_Cog(bot))