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

import os
import sys


if "discord.py" in sys.modules:
    os.system(f"{sys.executable} -m pip uninstall discord.py")

try:
    from discord.ext import commands
    from files.commands import raid, extra
    from requests import get
    from json import loads
    from colorama import Fore, Style
    from datetime import datetime
    from os import system
    from platform import system as os

except Exception:
    print(f"[ERRO] não foi possível importar as bibliotecas necessárias...")
    os.system(f"{sys.executable} -m pip install -r requirements.txt")
    os.system(f"{sys.executable} {sys.argv[0]}")
    exit(0)


DEBUG = True
BANNER = f"""{Fore.RED}
 ██░ ██▓██   ██▓ ██▓███  ▓█████  ██▀███      ███▄    █  █    ██  ██ ▄█▀▓█████  ██▀███  
▓██░ ██▒▒██  ██▒▓██░  ██▒▓█   ▀ ▓██ ▒ ██▒    ██ ▀█   █  ██  ▓██▒ ██▄█▒ ▓█   ▀ ▓██ ▒ ██▒
▒██▀▀██░ ▒██ ██░▓██░ ██▓▒▒███   ▓██ ░▄█ ▒   ▓██  ▀█ ██▒▓██  ▒██░▓███▄░ ▒███   ▓██ ░▄█ ▒
░▓█ ░██  ░ ▐██▓░▒██▄█▓▒ ▒▒▓█  ▄ ▒██▀▀█▄     ▓██▒  ▐▌██▒▓▓█  ░██░▓██ █▄ ▒▓█  ▄ ▒██▀▀█▄  
░▓█▒░██▓ ░ ██▒▓░▒██▒ ░  ░░▒████▒░██▓ ▒██▒   ▒██░   ▓██░▒▒█████▓ ▒██▒ █▄░▒████▒░██▓ ▒██▒
 ▒ ░░▒░▒  ██▒▒▒ ▒▓▒░ ░  ░░░ ▒░ ░░ ▒▓ ░▒▓░   ░ ▒░   ▒ ▒ ░▒▓▒ ▒ ▒ ▒ ▒▒ ▓▒░░ ▒░ ░░ ▒▓ ░▒▓░
 ▒ ░▒░ ░▓██ ░▒░ ░▒ ░      ░ ░  ░  ░▒ ░ ▒░   ░ ░░   ░ ▒░░░▒░ ░ ░ ░ ░▒ ▒░ ░ ░  ░  ░▒ ░ ▒░
 ░  ░░ ░▒ ▒ ░░  ░░          ░     ░░   ░       ░   ░ ░  ░░░ ░ ░ ░ ░░ ░    ░     ░░   ░ 
 ░  ░  ░░ ░                 ░  ░   ░                 ░    ░     ░  ░      ░  ░   ░     
        ░ ░                                                                            {Fore.MAGENTA}By: Snu{Style.RESET_ALL}"""


with open("files/config.json", "r") as file:
    content = loads(file.read())
    TOKEN = content["token"]
    PREFIXO = content["prefixo"] if content["prefixo"] != "" else "hnk!"
    APAGAR_MENSAGENS = content["apagar mensagens"]

    try:
        if TOKEN == "":
            print(f"{Fore.RED}[ERRO] Nenhuma token foi adicionada no arquivo \"config.json\"{Style.RESET_ALL}")
            exit(0)

        elif get("https://discordapp.com/api/v9/users/@me", headers={"Authorization": TOKEN}).status_code != 200:
            print(f"{Fore.RED}[ERRO] token inválida{Style.RESET_ALL}")
            exit(0)

    except Exception:
        print(f"{Fore.RED}[ERRO] Você tem certeza que está conectado a internet?{Style.RESET_ALL}")
        exit(0)

client = commands.Bot(
    command_prefix=PREFIXO,
    help_command=None,
    case_insensitive=True,
    self_bot=True
)
client.add_cog(raid.Raid(client))
client.add_cog(extra.Extra(client))


time = lambda: datetime.now().strftime('%H:%M:%S')
limpar = lambda: system("cls" if os() == "Windows" else "clear")

@client.event
async def on_connect():
    limpar()
    print(f"{BANNER}\n\n")
    
    print(f"Online na conta -> {client.user.name} // prefixo: {PREFIXO}\n")


@client.event
async def on_disconnect():
    print(f"{Fore.RED}Conexão perdida com a conta{Style.RESET_ALL}")


@client.listen()
async def on_command(ctx):
    cmd = ctx.invoked_with.lower()

    if APAGAR_MENSAGENS == True:
        ctx.message.delete()
    
    if ctx.command_failed == False:
        print(f"{Fore.GREEN}Comando {cmd} executado com sucesso - {time()}{Style.RESET_ALL}")


@client.listen()
async def on_command_error(ctx, error):
    if DEBUG == True:
        print(error)
        
    cmd = ctx.invoked_with.lower()

    if isinstance(error, commands.CommandNotFound):
        print(f"{Fore.RED}Erro ao tentar executar um comando desconhecido - {time()}{Style.RESET_ALL}")
        await ctx.channel.send(content=f"O comando digitado não existe. Use o comando {PREFIXO}help")

    elif isinstance(error, commands.BadArgument):
        print(f"{Fore.RED}Erro ao executar o comando {cmd}, os argumentos passados foram inválidos - {time()}{Style.RESET_ALL}")
        await ctx.channel.send(content=f"Erro. Para ver como usar o comando **{cmd.upper()}** "
                                f"use o comando \"{PREFIXO}help {cmd}\"")

    elif isinstance(error, commands.MissingRequiredArgument):
        print(f"{Fore.RED}Erro ao executar o comando {cmd}, faltaram argumentos necessários para ser executado - {time()}{Style.RESET_ALL}")
        await ctx.channel.send(content=f"Erro. Falta de argumentos, Para ver como usar o **{cmd.upper()}** "
                                f"use o comando \"{PREFIXO}help {cmd}\"")

    elif isinstance(error, commands.MissingPermissions):
        print(f"{Fore.RED}Erro ao executar o comando {cmd}, o usuário não tem permissões suficientes - {time()}{Style.RESET_ALL}")
        await ctx.channel.send(content=f"Erro. Você não tem permissão suficientes para executar este comando")

    else:
        print(f"{Fore.RED}Erro ao executar o comando {cmd}, motivo desconhecido - {time()}{Style.RESET_ALL}")


@client.command()
async def status(ctx):
    await ctx.channel.send(content=f"HyperNuker Online", delete_after=5)


@client.command(aliases=content["help"][1:])
async def help(ctx, *, cmd=""):
    cmd = cmd.lower()
    command = ctx.invoked_with.lower()

    if cmd in content["spam"]:
        apelidos = [apelido for apelido in content["spam"] if apelido != cmd]

        msg = "" \
        f"Comado: **{cmd}**\n" \
        f"Apelido(s): {apelidos}\n" \
        f"O que faz: repete o envio da mensagem escolhida pelo usuário\n" \
        f"Como usar: {PREFIXO}{cmd} \"quantas vezes repetir o envio da mensagem\" \"mensagem\"\n" \
        f"Exemplo: {PREFIXO}{cmd} 100 Hyper Nuker"

        await ctx.send(content=msg)

    elif cmd in content["purge"]:
        apelidos = [apelido for apelido in content["purge"] if apelido != cmd]

        msg = "" \
        f"Comando: **{cmd}**\n" \
        f"Apelido(s): {apelidos}\n" \
        f"O que faz: apaga a quantidade de mensagens escolhida pelo usuário\n" \
        f"Como usar: {PREFIXO}{cmd} \"quantas mensagens deseja apagar\"\n" \
        f"Exemplo: {PREFIXO}{cmd} 100\n" \
        f"**OBS**: se você não especificar quantas mensagens deseja apagar, 100 mensagens vão ser apagadas por padrão"

        await ctx.send(content=msg)

    elif cmd in content["create_channels"]:
        apelidos = [apelido for apelido in content["create_channels"] if apelido != cmd]

        msg = "" \
        f"Comando: **{cmd}**\n" \
        f"Apelido(s): {apelidos}\n" \
        f"O que faz: cria a quantidade de canais escolhida pelo usuário\n" \
        f"Como usar: {PREFIXO}{cmd} \"quantos canais você deseja criar\"\n" \
        f"Exemplo: {PREFIXO}{cmd} 100\n" \
        f"**OBS**: se você não especificar quantos canais deseja criar, 100 canais vão ser criados por padrão"

        await ctx.send(content=msg)

    elif cmd in content["create_roles"]:
        apelidos = [apelido for apelido in content["create_roles"] if apelido != cmd]

        msg = "" \
        f"Comando: **{cmd}**\n" \
        f"Apelido(s): {apelidos}\n" \
        f"O que faz: cria a quantidade de cargos escolhida pelo usuário\n" \
        f"Como usar: {PREFIXO}{cmd} \"quantos cargos você deseja criar\"\n" \
        f"Exemplo: {PREFIXO}{cmd} 50\n" \
        f"**OBS**: se você não especificar quantos cargos deseja criar, 50 cargos vão ser criados por padrão"

        await ctx.send(content=msg)

    elif cmd in content["delete_channels"]:
        apelidos = [apelido for apelido in content["delete_channels"] if apelido != cmd]

        msg = "" \
        f"Comando: **{cmd}**\n" \
        f"Apelido(s): {apelidos}\n" \
        f"O que faz: exclui todos os canais do servidor\n" \
        f"Como usar: {PREFIXO}{cmd}\n" \
        f"Exemplo: {PREFIXO}{cmd}"

        await ctx.send(content=msg)

    elif cmd in content["delete_roles"]:
        apelidos = [apelido for apelido in content["delete_roles"] if apelido != cmd]

        msg = "" \
        f"Comando: **{cmd}**\n" \
        f"Apelido(s): {apelidos}\n" \
        f"O que faz: exclui todos os cargos do servidor\n" \
        f"Como usar: {PREFIXO}{cmd}\n" \
        f"Exemplo: {PREFIXO}{cmd}\n"

        await ctx.send(content=msg)

    elif cmd in content["ban_all"]:
        apelidos = [apelido for apelido in content["ban_all"] if apelido != cmd]

        msg = "" \
        f"Comando: **{cmd}**\n" \
        f"Apelido(s): {apelidos}\n" \
        f"O que faz: bane todos os membros do servidor\n" \
        f"Como usar: {PREFIXO}{cmd}\n" \
        f"Exemplo: {PREFIXO}{cmd}"

        await ctx.send(content=msg)

    elif cmd in content["nuke"]:
        apelidos = [apelido for apelido in content["nuke"] if apelido != cmd]

        msg = "" \
        f"Comando: **{cmd}**\n" \
        f"Apelido(s): {apelidos}\n" \
        f"O que faz: junção de todos os principais comandos de raid\n" \
        f"Como usar: {PREFIXO}{cmd}\n" \
        f"Exemplo: {PREFIXO}{cmd}"

        await ctx.send(content=msg)

    elif cmd in content["self_purge"]:
        apelidos = [apelido for apelido in content["self_purge"] if apelido != cmd]

        msg = "" \
        f"Comando: **{cmd}**\n" \
        f"Apelido(s): {apelidos}\n" \
        f"O que faz: apaga a quantidade de mensagens escolhida pelo usuário (apenas as mensagens do usuário)\n" \
        f"Como usar: {PREFIXO}{cmd} \"quantas mensagens deseja apagar\"\n" \
        f"Exemplo: {PREFIXO}{cmd} 100\n" \
        f"**OBS**: se você não especificar quantas mensagens deseja apagar, 100 mensagens vão ser apagadas por padrão"

        await ctx.send(content=msg)

    elif cmd in content["remake_channel"]:
        apelidos = [apelido for apelido in content["remake_channel"] if apelido != cmd]

        msg = "" \
        f"Comando: **{cmd}**\n" \
        f"Apelido(s): {apelidos}\n" \
        f"O que faz: apaga e recria o canal com as mesmas permissões e posição\n" \
        f"Como usar: {PREFIXO}{cmd}\n" \
        f"Exemplo: {PREFIXO}{cmd}"

        await ctx.send(content=msg)

    elif cmd in content["set_activity"]:
        apelidos = [apelido for apelido in content["set_activity"] if apelido != cmd]

        msg = "" \
        f"Comando: **{cmd}**\n" \
        f"Apelido(s): {apelidos}\n" \
        f"O que faz: muda a sua atividade atual no discord\n" \
        f"tipos de modo: [\"watch\", \"play\", \"listen\"]\n" \
        f"Como Usar: {PREFIXO}{cmd} \"modo\" \"ação\" \"descrição\"\n" \
        f"Exemplo: {PREFIXO}{cmd} watch \"Hyper Nuker\" \"O melhor\""

        await ctx.send(content=msg)

    
    elif cmd in content["ip"]:
        apelidos = [apelido for apelido in content["ip"] if apelido != cmd]

        msg = "" \
        f"Comando: **{cmd}**\n" \
        f"Apelido(s): {apelidos}\n" \
        f"O que faz: busca informações sobre um ip\n"\
        f"Como usar: {PREFIXO}{cmd} \"código do ip\"\n" \
        f"Exemplo: {PREFIXO}{cmd} 127.0.0.1"

        await ctx.send(content=msg)

    elif cmd in content["token_checker"]:
        apelidos = [apelido for apelido in content["token_checker"] if apelido != cmd]

        msg = "" \
        f"Comando: **{cmd}**\n" \
        f"Apelido(s): {apelidos}\n" \
        f"O que faz: verifica se uma token é válida e trás informações sobre ela\n" \
        f"Como usar: {PREFIXO}{cmd} \"código do token\"\n" \
        f"Exemplo: {PREFIXO}{cmd} Nzc1MDkzNjQ2Mzc4NTMyODk3.X6hUNQ.SvAzsSOiTAJgyRgtp5T7TKs69nM"

        await ctx.send(content=msg)

    else:
        image = "https://ibb.co/0yR98hF""
        msg = f"\n**OBS**: use {PREFIXO}{command} \"comando\" para ver mais informações sobre algum comando"
        await ctx.send(content=image) 
        await ctx.send(content=msg)


client.run(TOKEN)
