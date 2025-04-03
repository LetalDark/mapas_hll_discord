import os
import discord
import time
import datetime
import requests
import logging
import json

from discord import Embed
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, CheckFailure
from discord.utils import get
from datetime import datetime

from dotenv import load_dotenv


logging.basicConfig(level=logging.INFO)

load_dotenv()
# Esta información tiene que escribirse en el .env una vez se escriba
config = {
    'token': os.environ['DISCORD_TOKEN'],
    'url_rcon_login_1': os.environ['URL_RCON_LOGIN_1'],
    'url_rcon_get_status_1': os.environ['URL_RCON_GET_STATUS_1'],
    'url_rcon_get_players_1': os.environ['URL_RCON_GET_PLAYERS_1'],
    'url_rcon_get_map_history_1': os.environ['URL_RCON_GET_MAP_HISTORY_1'],
    'channel_id_1': os.environ['CHANNEL_ID_1'],
    'url_rcon_login_2': os.environ['URL_RCON_LOGIN_2'],
    'url_rcon_get_status_2': os.environ['URL_RCON_GET_STATUS_2'],
    'url_rcon_get_players_2': os.environ['URL_RCON_GET_PLAYERS_2'],
    'url_rcon_get_map_history_2': os.environ['URL_RCON_GET_MAP_HISTORY_2'],
    'channel_id_2': os.environ['CHANNEL_ID_2'],
    'url_rcon_login_3': os.environ['URL_RCON_LOGIN_3'],
    'url_rcon_get_status_3': os.environ['URL_RCON_GET_STATUS_3'],
    'url_rcon_get_players_3': os.environ['URL_RCON_GET_PLAYERS_3'],
    'url_rcon_get_map_history_3': os.environ['URL_RCON_GET_MAP_HISTORY_3'],
    'channel_id_3': os.environ['CHANNEL_ID_3'],
    'url_rcon_login_4': os.environ['URL_RCON_LOGIN_4'],
    'url_rcon_get_status_4': os.environ['URL_RCON_GET_STATUS_4'],
    'url_rcon_get_players_4': os.environ['URL_RCON_GET_PLAYERS_4'],
    'url_rcon_get_map_history_4': os.environ['URL_RCON_GET_MAP_HISTORY_4'],
    'channel_id_4': os.environ['CHANNEL_ID_4'],    
    'url_rcon_login_5': os.environ['URL_RCON_LOGIN_5'],
    'url_rcon_get_status_5': os.environ['URL_RCON_GET_STATUS_5'],
    'url_rcon_get_players_5': os.environ['URL_RCON_GET_PLAYERS_5'],
    'url_rcon_get_map_history_5': os.environ['URL_RCON_GET_MAP_HISTORY_5'],
    'channel_id_5': os.environ['CHANNEL_ID_5'],    
    'url_rcon_login_6': os.environ['URL_RCON_LOGIN_6'],
    'url_rcon_get_status_6': os.environ['URL_RCON_GET_STATUS_6'],
    'url_rcon_get_players_6': os.environ['URL_RCON_GET_PLAYERS_6'],
    'url_rcon_get_map_history_6': os.environ['URL_RCON_GET_MAP_HISTORY_6'],
    'channel_id_6': os.environ['CHANNEL_ID_6'],
    'channel_log': os.environ['CHANNEL_ID_LOG'],
    'channel_admin_commands': os.environ['CHANNEL_ID_ADMIN_COMMANDS'],
    'channel_player_commands': os.environ['CHANNEL_ID_PLAYER_COMMANDS'],
    'user_rcon': os.environ['USER_RCON'],
    'password_rcon': os.environ['PASSWORD_RCON'],
}

MAP_NAMES = {
    "Template": "Template",
    "carentan_offensive_ger": "CT O GER",
    "carentan_offensive_us": "CT O US",
    "carentan_warfare": "CT W",
    "carentan_warfare_night": "CT W Night",
    "driel_offensive_ger": "DRL O GER",
    "driel_offensive_us": "DRL O US",
    "driel_warfare": "DRL W",
    "driel_warfare_night": "DRL W Night",
    "DRL_S_1944_Day_P_Skirmish": "DRL S Day",
    "DRL_S_1944_Night_P_Skirmish": "DRL S Night",
    "DRL_S_1944_P_Skirmish": "DRL S",
    "ELA_S_1942_Night_P_Skirmish": "ELA S Night",
    "ELA_S_1942_P_Skirmish": "ELA S",
    "elalamein_offensive_CW": "ELA O BRT",
    "elalamein_offensive_ger": "ELA O GER",
    "elalamein_warfare": "ELA W",
    "elalamein_warfare_night": "ELA W Night",
    "foy_offensive_ger": "Foy O GER",
    "foy_offensive_us": "Foy O US",
    "foy_warfare": "Foy W",
    "foy_warfare_night": "Foy W Night",
    "hill400_offensive_ger": "H400 O GER",
    "hill400_offensive_US": "H400 O US",
    "hill400_warfare": "H400 W",
    "hill400_warfare_night": "H400 W Night",
    "hurtgenforest_offensive_ger": "HUR O GER",
    "hurtgenforest_offensive_US": "HUR O US",
    "hurtgenforest_warfare_V2": "HUR W",
    "hurtgenforest_warfare_V2_night": "HUR W Night",
    "kharkov_offensive_ger": "KHA O GER",
    "kharkov_offensive_rus": "KHA O RUS",
    "kharkov_warfare": "KHA W",
    "kharkov_warfare_night": "KHA W Night",
    "kursk_offensive_ger": "KUR O GER",
    "kursk_offensive_rus": "KUR O RUS",
    "kursk_warfare": "KUR W",
    "kursk_warfare_night": "KUR W Night",
    "mortain_offensiveger_day": "MOR O GER",
    "mortain_offensiveger_overcast": "MOR O GER",
    "mortain_offensiveUS_day": "MOR O US",
    "mortain_offensiveUS_overcast": "MOR O US",
    "mortain_skirmish_day": "MOR S",
    "mortain_skirmish_overcast": "MOR S",
    "mortain_warfare_day": "MOR W",
    "mortain_warfare_overcast": "MOR W",
    "omahabeach_offensive_ger": "OMA O GER",
    "omahabeach_offensive_us": "OMA O US",
    "omahabeach_warfare": "OMA W",
    "omahabeach_warfare_night": "OMA W Night",
    "purpleheartlane_offensive_ger": "PHL O GER",
    "purpleheartlane_offensive_us": "PHL O US",
    "purpleheartlane_warfare": "PHL W",
    "purpleheartlane_warfare_night": "PHL W Night",
    "remagen_offensive_ger": "REM O GER",
    "remagen_offensive_us": "REM O US",
    "remagen_warfare": "REM W",
    "remagen_warfare_night": "REM W Night",
    "SMDM_S_1944_Day_P_Skirmish": "SMDM S",
    "SMDM_S_1944_Night_P_Skirmish": "SMDM S Night",
    "SMDM_S_1944_Rain_P_Skirmish": "SMDM S Rain",
    "stalingrad_offensive_ger": "ST O GER",
    "stalingrad_offensive_rus": "ST O RUS",
    "stalingrad_warfare": "ST W",
    "stalingrad_warfare_night": "ST W Night",
    "stmariedumont_off_ger": "SMDM O GER",
    "stmariedumont_off_us": "SMDM O US",
    "stmariedumont_warfare": "SMDM W",
    "stmariedumont_warfare_night": "SMDM W Night",
    "stmereeglise_offensive_ger": "SME O GER",
    "stmereeglise_offensive_us": "SME O US",
    "stmereeglise_warfare": "SME W",
    "stmereeglise_warfare_night": "SME W Night",
    "utahbeach_offensive_ger": "UTA O GER",
    "utahbeach_offensive_us": "UTA O US",
    "utahbeach_warfare": "UTA W",
    "utahbeach_warfare_night": "UTA W Night",
    "PHL_L_1944_OffensiveGER": "PHL O GER",
    "PHL_L_1944_OffensiveUS": "PHL O US",
    "PHL_L_1944_Warfare": "PHL W",
    "PHL_L_1944_Warfare_Night": "PHL W Night",
    "PHL_S_1944_Rain_P_Skirmish": "PHL S Rain",
    "PHL_S_1944_Morning_P_Skirmish": "PHL S Morn",
    "PHL_S_1944_Night_P_Skirmish": "PHL S Night",
    "HIL_S_1944_Day_P_Skirmish": "HIL S Day",
    "HIL_S_1944_Dusk_P_Skirmish": "HIL S Dusk",
    "elsenbornridge_offensiveUS_day": "ELSE O US Day",
    "elsenbornridge_offensiveUS_morning": "ELSE O US Morn",
    "elsenbornridge_offensiveUS_night": "ELSE O US Night",
    "elsenbornridge_offensiveger_day": "ELSE O GER Day",
    "elsenbornridge_offensiveger_morning": "ELSE O GER Morn",
    "elsenbornridge_offensiveger_night": "ELSE O GER Nigth",
    "elsenbornridge_skirmish_day": "ELSE S Day",
    "elsenbornridge_skirmish_morning": "ELSE S Morn",
    "elsenbornridge_skirmish_night": "ELSE S Nigth",
    "elsenbornridge_warfare_day": "ELSE W Day",
    "elsenbornridge_warfare_morning": "ELSE W Morn",
    "elsenbornridge_warfare_night": "ELSE W Nigth",
    "tobruk_warfare_day": "TBRK W Day",
    "tobruk_offensivebritish_day": "TBRK O B Day",
    "tobruk_offensivebritish_dusk": "TBRK O B Dusk",
    "tobruk_offensivebritish_morning": "TBRK O B Morning",
    "tobruk_offensiveger_day": "TBRK O GER Day",
    "tobruk_offensiveger_dusk": "TBRK O GER Dusk",
    "tobruk_offensiveger_morning": "TBRK O GER Morning",
    "tobruk_skirmish_day": "TBRK S Day",
    "tobruk_skirmish_dusk": "TBRK S Dusk",
    "tobruk_skirmish_morning": "TBRK S Morning",
    "tobruk_warfare_dusk": "TBRK W Dusk",
    "tobruk_warfare_morning": "TBRK W Morning"
}


bot = commands.Bot(command_prefix='-',intents = discord.Intents().all())
reactions = ['1️⃣', '2️⃣', '3️⃣', '4️⃣']

def get_status_map_players(url_rcon_login,url_rcon_get_status,user_rcon,password_rcon):
    try:
        with requests.Session() as session:
            post = session.post(url_rcon_login, json={'username': user_rcon, 'password': password_rcon})
            response = session.get(url_rcon_get_status)
            json_data = json.loads(response.text)
            players = json_data['result']['current_players']
            number_players = json_data['result']['current_players']
            current_map = json_data['result']['map']['id']
            current_map = change_name_map(current_map)
            message_log = str(players) + " - " + str(current_map)
            channel_name = str(players) + " - " + str(current_map)
        return (message_log,channel_name,number_players)
    except Exception as e:
        logging.error(f"Error en get_status_map_players: {e}")
        return ("0 - Error", "0 - Error", 0)

def get_players(url_rcon_login,url_rcon_get_players,url_rcon_get_status):
    global json_data_players
    global paginas
    global number_players
    try:
        with requests.Session() as session:
            post = session.post(url_rcon_login, json={'username': config['user_rcon'], 'password': config['password_rcon']})
            response = session.get(url_rcon_get_players)
            json_data_players = json.loads(response.text)
            number_players=int(get_status_map_players(url_rcon_login,url_rcon_get_status,config['user_rcon'],config['password_rcon'])[2])
            paginas=int((number_players-1)/25)+1
            embed=escribir_pagina(1)
        return (embed,paginas)
    except Exception as e:
        logging.error(f"Error en get_players: {e}")
        return ("0 - Error", "0 - Error", 0)

def get_tiempo_mapa(url_rcon_login,url_rcon_get_map_history):
    with requests.Session() as session:
        post = session.post(url_rcon_login, json={'username': config['user_rcon'], 'password': config['password_rcon']})
        response = session.get(url_rcon_get_map_history)
        map_history = response.json()
        tiempo = (map_history['result'][0]['start'])
        start = time.strftime("%d-%m-%Y %H:%M:%S", time.localtime(tiempo))
        now = time.strftime("%d-%m-%Y %H:%M:%S", time.localtime())
        time_left = datetime.strptime(now, '%d-%m-%Y %H:%M:%S') - datetime.strptime(start, '%d-%m-%Y %H:%M:%S')
    return(time_left)

def escribir_pagina(pagina):
    embed = discord.Embed(title=f"Jugadores conectados: {number_players}", color=0x109319)
    if number_players == 0:
        embed.add_field(name="-", value="No hay jugadores en el servidor.", inline=True)
    else:
        start_index = (pagina - 1) * 25
        end_index = min(start_index + 25, number_players)
        for i in range(start_index, end_index):
            tiempo_total = convertSeconds(int(json_data_players['result'][i]['profile']['total_playtime_seconds']))
            embed.add_field(name=f"{i+1} - {json_data_players['result'][i]['name']}", value=tiempo_total, inline=True)

    embed.set_footer(text=f"Tiempo jugado total en los servidores desde Sept. 2020\nEstás en la página: {pagina}")
    return embed

def convertSeconds(seconds):
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    return f"{h}:{m:02}:{s:02}"

def change_name_map(current_map):
    return MAP_NAMES.get(current_map, current_map)

@bot.event
async def on_ready():
    date = datetime.now()
    if config['channel_id_1'] and config['channel_id_2'] and config['channel_id_3'] and config['channel_id_4']:
        get_data.start()
        await bot.get_channel(int(config['channel_log'])).send(str(date) + " - Bot activado correctamente.")

@bot.event
async def on_disconnect():
    date = datetime.now()
    await bot.get_channel(int(config['channel_log'])).send(str(date) + " - Señal de desconexión recibida. Desconectando...")

@bot.event
async def on_resumed():
    date = datetime.now()
    await bot.get_channel(int(config['channel_log'])).send(str(date) + " - Reconectado.")

@bot.event
async def on_command_error(ctx, error):
    pass

@bot.event
async def on_reaction_add(reaction, user):
    if user == bot.user:
        return

    if reaction.emoji == "1️⃣" and reaction.message.id == message_id:
        embed=escribir_pagina(1)
        message = reaction.message
        await message.remove_reaction(reaction, user)
        await message.edit(embed=embed)
    if reaction.emoji == "2️⃣" and reaction.message.id == message_id:
        embed=escribir_pagina(2)
        message = reaction.message
        await message.remove_reaction(reaction, user)
        await message.edit(embed=embed)
    if reaction.emoji == "3️⃣" and reaction.message.id == message_id:
        embed=escribir_pagina(3)
        message = reaction.message
        await message.remove_reaction(reaction, user)
        await message.edit(embed=embed)
    if reaction.emoji == "4️⃣" and reaction.message.id == message_id:
        embed=escribir_pagina(4)
        message = reaction.message
        await message.remove_reaction(reaction, user)
        await message.edit(embed=embed)

async def handle_server_command(ctx, server_number: int, action: str):
    if ctx.channel.id not in [int(config['channel_admin_commands']), int(config['channel_player_commands'])]:
        return

    login_url = config[f'url_rcon_login_{server_number}']
    status_url = config[f'url_rcon_get_status_{server_number}']
    players_url = config[f'url_rcon_get_players_{server_number}']
    map_hist_url = config[f'url_rcon_get_map_history_{server_number}']

    if action == "players":
        players = get_players(login_url, players_url, status_url)
        message = await ctx.channel.send(embed=players[0])
        if players[1] > 1:
            for i in range(players[1]):
                await message.add_reaction(reactions[i])
        global message_id
        message_id = message.id

    elif action == "tiempo":
        tiempo_mapa = get_tiempo_mapa(login_url, map_hist_url)
        await ctx.send(f"``Tiempo de la partida actual: {tiempo_mapa}``")
    else:
        await ctx.send("❌ Comando inválido. Usa `players` o `tiempo`.")

@bot.command()
async def server1(ctx, arg1):
    await handle_server_command(ctx, 1, arg1)

@bot.command()
async def server2(ctx, arg1):
    await handle_server_command(ctx, 2, arg1)

@bot.command()
async def server3(ctx, arg1):
    await handle_server_command(ctx, 3, arg1)

@bot.command()
async def server4(ctx, arg1):
    await handle_server_command(ctx, 4, arg1)

@bot.command()
async def server5(ctx, arg1):
    await handle_server_command(ctx, 5, arg1)
   
@bot.command()
async def server6(ctx, arg1):
    await handle_server_command(ctx, 6, arg1) 

@has_permissions(administrator=True)
async def start_bot(ctx):
    try:
        date = datetime.datetime.now()
        get_data.start()
        await bot.get_channel(int(config['channel_log'])).send(str(date) + " - Inicializado correctamente.")
    except Exception as ex:
        await bot.get_channel(int(config['channel_log'])).send(str(date) + " - ¡Ocurrió un error durante el arranque del bot!" + str(ex))

@tasks.loop(minutes=10.0)
async def get_data():
    for i in range(1, 7):
        try:
            login_url = config[f'url_rcon_login_{i}']
            status_url = config[f'url_rcon_get_status_{i}']
            channel_id = config[f'channel_id_{i}']

            status = get_status_map_players(login_url, status_url, config['user_rcon'], config['password_rcon'])
            await bot.get_channel(int(config['channel_log'])).send(f"Actualizando: 📱 #{i} - {status[0]}")
            await bot.get_channel(int(channel_id)).edit(name=f'📱 #{i} - {status[1]}')
        except Exception as ex:
            await bot.get_channel(int(config['channel_log'])).send(f"¡Error actualizando server{i}! {str(ex)}")
try:
    bot.run(config['token'], reconnect=True)

except Exception as ex:
    print(f'Error! {ex}')
