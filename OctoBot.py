#!/usr/bin/python3
import logging
import sys
import signal
import time
import requests
from Octolib.functions import *
from telegram.ext import *
from itertools import islice

#colors and fronts
"""fonts"""
normal = '\033[0m'
bold = '\033[1m' 
dim = '\033[2m'
italic = '\033[3m' 
under = '\033[4m'
blink = '\033[5m'
reverse = '\033[7m'
conceal = '\033[8m'
nobold = '\033[22m'
noitalic = '\033[23m'
nounder = '\033[24m'
noblink = '\033[35m'
"""Colors(Foreground)"""
gray = '\033[1;30m'
red = '\033[1;31m'
green = '\033[1;32m'
yellow = '\033[1;33m'
blue = '\033[1;34m'
magenta = '\033[1;35m'
cyan = '\033[1;36m'
white = '\033[1;37m'

#trap ctrl-c
def sig_handler(sig, frame):
    print("\n{}[*]{}CTRL-C: Exiting...\n{}".format(red, blue, white))
    sys.exit(1)
    
signal.signal(signal.SIGINT, sig_handler)

try:
    
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    OctoBot_link = 'https://t.me/Pwn2Octobot'
    token = open("Contents/telegram_token.txt").read()
    text = ("{}[!]{}INITIALIZATION OCTOBOT{}\n".format(red, blue, gray))
    for h in text:
        print(h, end='')
        sys.stdout.flush()
        time.sleep(0.05)

    updater = Updater(token=token, use_context=True)
    
    
    def start(update, context):
        login = octo_login('Pwn2Ninja', '19fa05fed01ee89c5f50223ebf425083c42b7489')
        login.auth()
        name_user = update.message.from_user
        update.message.reply_text("Hola {}!😃👍\nEste interesante bot🤖 está creado con el fin de que puedas gestionar GitHub facilmente😉. Usa el comando⌨️ /help para obtener más ayuda💡".format(name_user['first_name']))
    def helper(update, context):
        update.message.reply_text("🔎En este bot tienes disponible los siguientes comandos🔍:\n\n/search_user [usuario]\n/search_repo [repo_path]\n/download [repo]\[archivo]")
    def search_user(update, context):
        user_arg = context.args
        try:
            args = str(user_arg[0])
            user = args
            gh_user = octo_search(args, user)
            res = gh_user.search_user(args)
            with open('Database/JSON/gh_user_data.json', 'r') as gh_user_data:
                js = json.load(gh_user_data)
                owner     = js['login']
                name      = js['name']
                repos     = js['public_repos']
                gists     = js['public_gists']
                company   = js['company']
                blog      = js['blog']
                location  = js['location']
                email     = js['email']
                bio       = js['bio']
                twitter   = js['twitter_username']
                url       = js['html_url']
                followers = js['followers']
                following = js['following']
                
                update.message.reply_text("👤*INFO DE USUARIO: [{}]*\n\n*»Usuario:* {}\n*»Nombre:* {}\n*»Email:* {}\n*»Bio:* {}\n*»Sigue:* {}\n*»Le siguen:* {}\n*»Repos:* {}\n*»Gists:* {}\n*»Empresa:* {}\n*»Blog:* {}\n*»Twitter:* @{}\n*»Localización:* {}\n📎*URL:* {}".format(owner, owner, name, email, bio, following, followers, repos, gists, company, blog, twitter, location, url), parse_mode='Markdown')

        except IndexError:
            update.message.reply_text("❌Faltan argumentos para el comando /search_user❌")
    def search_repo(update, context):
        repo_args = context.args
        try:
            argr = str(repo_args[0])
            repo = argr
            gh_repo = octo_search(argr, repo)
            res = gh_repo.search_repo(argr)
            with open('Database/JSON/gh_repo_data.json', 'r') as gh_repo_data:
                js = json.load(gh_repo_data)
                name = js['name']
                full_name = js['full_name']
                owner = js['owner']['login']
                url = js['html_url']
                description = js['description']
                peso = js['size']
                stars = js['stargazers_count']
                watchers = js['watchers_count']
                language = js['language']
                open_issues = js['open_issues']
                bifurcaciones = js['forks']
                branch = js['default_branch']
                update.message.reply_text("🗂️*INFO DE REPO: [{}]*\n\n*»Nombre:* {}\n*»Ruta Repo:* {}\n*»Propietario:* {}\n*»Descripción:* {}\n*»Lenguage:* {}\n*»Estrellas:* {}\n*»Watchers:* {}\n*»Rama:* {}\n*»Peso:* {}Kb\n*»Open Issues:* {}\n*»Forks:* {}\n📎*URL:* {}".format(full_name, name, full_name, owner, description, language, stars, watchers, branch, peso, open_issues, bifurcaciones, url), parse_mode='Markdown')
                
                
        except IndexError:
            update.message.reply_text("❌Faltan argumentos para el comando /search_repo❌")
    
    def download(update, context):
        download_args = context.args
        try:
            args = str(download_args[0])
            try:
                gh_download = octo_download(args)
                res = gh_download.download_repo()
                chatid = update.message.chat_id
                with open('Database/JSON/gh_repo_data.json', 'r') as gh_repo_data:
                    js = json.load(gh_repo_data)
                    name = js['name']
                    context.bot.sendDocument(chat_id=chatid, document=open(name + '.zip', 'rb'))
                    os.system('rm -rf {}.zip'.format(name))
            except KeyError:
                update.message.reply_text("❌Repositorio no encontrado❌")
        
        except IndexError:
            update.message.reply_text("❌Faltan argumentos para el comando /download")
    
        
    start_handler = CommandHandler('start', start)
    helper_handler = CommandHandler('help', helper)
    search_user_handler = CommandHandler('search_user', search_user)
    search_repo_handler = CommandHandler('search_repo', search_repo)
    download_handler = CommandHandler('download', download)
   
    updater.dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(helper_handler)
    updater.dispatcher.add_handler(search_user_handler)
    updater.dispatcher.add_handler(search_repo_handler)
    updater.dispatcher.add_handler(download_handler)
    
    updater.start_polling()
    
    

except:
    print("{}[!]{}An error has occurred{}".format(red, blue, white))
    sys.exit(1)