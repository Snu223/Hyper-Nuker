# By Snu
# The creator is not responsible for misuse

"""
MIT License

Copyright (c) 2022 Snu

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from discord.ext import commands
from discord import Activity, ActivityType
from aiohttp import ClientSession
from json import loads
from colorama import Fore, Style
from datetime import datetime

with open("files/config.json") as file:
    content = loads(file.read())

class Extra(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.time = lambda: datetime.now().strftime('%H:%M:%S')
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 OPR/68.0.3618.191"


    @commands.command(aliases=content["self_purge"][1:])
    async def self_purge(self, ctx, limit:int=100):
        cmd = ctx.invoked_with.lower()
        count = 0

        async for message in ctx.channel.history(limit=None):
            if count > limit:
                break

            if message.author.id == self.client.user.id:
                try:
                    await message.delete()
                    print(f"{Fore.YELLOW}[{cmd.upper()}] Mensagem -> {message.id} deletada - {self.time()}{Style.RESET_ALL}")
                    count += 1

                except:
                    print(f"{Fore.RED}[{cmd.upper()}] Não foi possível apagar a mensagem -> {message.id} - {self.time()}{Style.RESET_ALL}")

        print(f"{Fore.YELLOW}[{cmd.upper()}] {count} Mensagem(ns) apagada(s) com sucesso - {self.time()}{Style.RESET_ALL}")


    @commands.command(aliases=content["remake_channel"][1:])
    @commands.has_permissions(manage_channels=True)
    async def remake_channel(self, ctx):
        cmd = ctx.invoked_with.lower()

        await ctx.channel.delete()
        new_channel = await ctx.channel.clone()
        await new_channel.edit(position=ctx.channel.position, sync_permissions=True)
        print(f"{Fore.YELLOW}[{cmd.upper()}] Canal recriado com sucesso - {self.time()}{Style.RESET_ALL}")


    @commands.command(aliases=content["set_activity"][1:])    
    async def set_activity(self, ctx, type, name, details=None):
        cmd = ctx.invoked_with.lower()
        type = type.lower()

        if type in ["play", "playing", "jogar", "jogando"]:
            activity = Activity(type=ActivityType.playing, name=name, details=details)

        elif type in ["listen", "listening", "escutar", "escutando"]:
            activity = Activity(type=ActivityType.listening, name=name, details=details)

        elif type in ["watch", "watching", "assistir", "assistindo"]:
            activity = Activity(type=ActivityType.watching, name=name, details=details)

        else:
            await ctx.channel.send(content="Erro, atividade escolhida é inválida")
            print(f"{Fore.RED}[{cmd.upper()}] Erro, a atividade escolhida é inválida - {self.time()}{Style.RESET_ALL}")
            return

        try:
            await self.client.change_presence(activity=activity)
            await ctx.channel.send(f"atividade foi mudada com sucesso")
            print(f"{Fore.YELLOW}[{cmd.upper()}] Atividade foi mudada com sucesso - {self.time()}{Style.RESET_ALL}")

        except:
            await ctx.channel.send(f"Erro ao tentar mudar o sua atividade")
            print(f"{Fore.RED}[{cmd.upper()}] Erro ao tentar mudar a atividade - {self.time()}{Style.RESET_ALL}")


    @commands.command(aliases=content["ip"][1:])
    async def ip(self, ctx, ip_code:str):
        cmd = ctx.invoked_with.lower()
        headers = {
            "User-Agent": self.user_agent
        }
        
        async with ClientSession() as session:
            async with session.get(url=f"http://ip-api.com/json/{ip_code}", headers=headers) as r:
                result = await r.text()
                result = loads(result)
                if result["status"] == "success":
                    await ctx.channel.send(content="Ip **VÁLIDO**, informações no terminal")
                    print(f"{Fore.YELLOW}[{cmd.upper()}] Ip -> {ip_code} - {self.time()}")
                    print(f"[{cmd.upper()}] Estado -> {result['regionName']} - {self.time()}")
                    print(f"[{cmd.upper()}] País -> {result['country']} - {self.time()}")
                    print(f"[{cmd.upper()}] Cidade -> {result['city']} - {self.time()}")
                    print(f"[{cmd.upper()}] Latitude -> {result['lat']} - {self.time()}")
                    print(f"[{cmd.upper()}] Longitude -> {result['lon']}[{cmd.upper()}] - {self.time()}")
                    print(f"[{cmd.upper()}] O ip -> \"{ip_code}\" é válido - {self.time()}{Style.RESET_ALL}")
                    
                else:
                    await ctx.channel.send(content="Erro, ip inválido")
                    print(f"{Fore.RED}[{cmd.upper()}] Erro, ip -> \"{ip_code}\" é inválido - {self.time()}{Style.RESET_ALL}")


    @commands.command(aliases=content["token_checker"][1:])
    async def token_checker(self, ctx, token:str):
        cmd = ctx.invoked_with.lower()
        token = token.replace("\"", "")
        headers = {
            "Authorization": token,
            "User-Agent": self.user_agent
        }

        async with ClientSession() as session:
            async with session.get(f"https://discordapp.com/api/v9/users/@me", headers=headers) as r:
                text = await r.text()
                result = loads(text)

                if r.status == 200:
                    await ctx.channel.send(content="Token **VÁLIDO**, informações no terminal")
                    print(f"{Fore.YELLOW}[{cmd.upper()}] Token -> \"{token}\" é valido - {self.time()}")
                    print(f"[{cmd.upper()}] Nome da conta -> {result['username']}#{result['discriminator']} - {self.time()}")
                    print(f"[{cmd.upper()}] Email da conta -> {result['email']} - {self.time()}")
                    print(f"[{cmd.upper()}] Id da conta -> {result['id']} - {self.time()}")
                    print(f"[{cmd.upper()}] Número de celular -> {result['phone'] if result['phone'] != None else 'Não tem'} - {self.time()}")
                    print(f"[{cmd.upper()}] Mfa ativado? -> {'ativado' if result['mfa_enabled'] == True else 'Desativado'} - {self.time()}")
                    print(f"[{cmd.upper()}] Conta verificada? -> {'Sim' if result['verified'] else 'Não'} - {self.time()}")

                else:
                    await ctx.channel.send(content="token **inválido**")
                    print(f"{Fore.RED}[{cmd.upper()}] Token -> \"{token}\" é inválido - {self.time()}{Style.RESET_ALL}")
