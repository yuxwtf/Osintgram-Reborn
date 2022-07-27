# imports

import sys
from cv2 import floodFill
from instagrapi import Client
from instagrapi.types import StoryMention, StoryMedia, StoryLink, StoryHashtag
from matplotlib.style import use
from prettytable import PrettyTable
from pystyle import Center, Box
from colorama import init, Fore
from geopy.geocoders import Nominatim
import json
import os
import requests
import ssl
import time
ssl._create_default_https_context = ssl._create_unverified_context

# inits

init()
count = 0
table = PrettyTable()
target = None
config = json.load(open('./config/config.json'))
isprivate = False
api = Client()
api.login(config['username'], config['password'])
# Main

osintgram = r"""

________    _________.___ ____________________________________    _____      _____   
\_____  \  /   _____/|   |\      \__    ___/  _____/\______   \  /  _  \    /     \  
 /   |   \ \_____  \ |   |/   |   \|    | /   \  ___ |       _/ /  /_\  \  /  \ /  \ 
/    |    \/        \|   /    |    \    | \    \_\  \|    |   \/    |    \/    Y    \
\_______  /_______  /|___\____|__  /____|  \______  /|____|_  /\____|__  /\____|__  /
        \/        \/             \/               \/        \/         \/         \/ 
"""

def cool_input(arg):
    return input("\n"*1 + f'{" "*6} {arg} ')

def cool_print(arg):
    print("\n"*1 + f'{" "*6} {arg}')


def get_user_id(target):
    return api.user_id_from_username(target)

def get_user_info(target):
    return api.user_info_by_username(target)

def cmd_addrs(target):
    count = 0
    usrid = get_user_id(target)
    t = PrettyTable()
    sys.stdout.write(Fore.YELLOW + f"\n"*1 + " "*6 + f"\rCatched {count} address !")
    sys.stdout.flush()
    t.field_names = ["ID", "ZIP", "Address", "City"]
    for post in api.user_medias(usrid):
        if 'location' in api.media_info(post.pk):
            count = count + 1
            sys.stdout.write(Fore.YELLOW + " "*6 + f"Catched {count} address !\n")
            sys.stdout.flush()
            t.add_row([post.pk, post.location.zip, post.location.address, post.location.city])
    print('\n'*3)
    print(Center.XCenter(Fore.YELLOW + str(t)))
    print('\n'*2)

def cmd_tagged(target):
    t = PrettyTable()
    count = 0
    t.field_names = ["ID", "User"]
    usrid = get_user_id(target)
    sys.stdout.write(Fore.YELLOW + f"\n"*1 + " "*6 + f"\rCatched {count} tagged users !")
    sys.stdout.flush()
    for post in api.user_medias(usrid):
        usertags = post.usertags
        for usertag in usertags:
            count = count + 1
            sys.stdout.write(Fore.YELLOW + " "*6 + f"Catched {count} tagged users !\n")
            sys.stdout.flush()
            t.add_row([post.pk, "@"+usertag.user.username])
    print('\n'*3)
    print(Center.XCenter(Fore.YELLOW + str(t)))
    print('\n'*2)



def cmd_fwersemail(target):
    count = 0
    usrid = get_user_id(target)
    t = PrettyTable()
    t.field_names = ["ID", "Username", "Email"]
    followers = api.user_followers(usrid)
    sys.stdout.write(Fore.YELLOW + f"\n"*1 + " "*6 + f"\rCatched {count} emails !")
    sys.stdout.flush()
    for follower in followers.keys():
        try:
            usrinfo = api.user_info(follower)
            if '@' in usrinfo.public_email:
                count = count + 1
                sys.stdout.write(Fore.YELLOW + " "*6 + f"Catched {count} emails !\n")
                sys.stdout.flush()
                t.add_row([usrinfo.pk, usrinfo.username, usrinfo.public_email])
            else:
                pass
        except:
            pass
    print('\n'*3)
    print(Center.XCenter(Fore.YELLOW + str(t)))
    print('\n'*2)


def cmd_fwingsemail(target):
    count = 0
    usrid = get_user_id(target)
    t = PrettyTable()
    t.field_names = ["ID", "Username", "Email"]
    following = api.user_following(usrid)
    sys.stdout.write(Fore.YELLOW + f"\n"*1 + " "*6 + f"\rCatched {count} emails !")
    sys.stdout.flush()
    for follow in following.keys():
        try:
            usrinfo = api.user_info(follow)
            if '@' in usrinfo.public_email:
                count = count + 1
                sys.stdout.write(Fore.YELLOW + " "*6 + f"Catched {count} emails !\n")
                sys.stdout.flush()
                t.add_row([usrinfo.pk, usrinfo.username, usrinfo.public_email])
            else:
                pass
        except:
            pass
    print('\n'*3)
    print(Center.XCenter(Fore.YELLOW + str(t)))
    print('\n'*2)

def cmd_fwingsnumber(target):
    count = 0
    usrid = get_user_id(target)
    t = PrettyTable()
    t.field_names = ["ID", "Username", "Number"]
    following = api.user_following(usrid)
    sys.stdout.write(f"\rCatched {count} numbers !")
    sys.stdout.flush()
    for follow in following.keys():
        try:
            usrinfo = api.user_info(follow)
            if usrinfo.public_phone_number or usrinfo.contact_phone_number != None:
                count = count + 1
                sys.stdout.write(Fore.YELLOW + " "*6 + f"Catched {count} numbers !\n")
                sys.stdout.flush()
                t.add_row([usrinfo.pk, usrinfo.username, usrinfo.public_email, usrinfo.contact_phone_number])
            else:
                pass
        except:
            pass
    print('\n'*3)
    print(Center.XCenter(Fore.YELLOW + str(t)))
    print('\n'*2)


def cmd_fwersnumber(target):
    count = 0
    usrid = get_user_id(target)
    t = PrettyTable()
    t.field_names = ["ID", "Username", "Number"]
    followers = api.user_followers(usrid)
    sys.stdout.write(Fore.YELLOW + f"\n"*1 + " "*6 + f"\rCatched {count} numbers !")
    sys.stdout.flush()
    for follower in followers.keys():
        try:
            usrinfo = api.user_info(follower)
            if usrinfo.public_phone_number or usrinfo.contact_phone_number != None:
                count = count + 1
                sys.stdout.write(Fore.YELLOW + " "*6 + f"Catched {count} numbers !\n")
                sys.stdout.flush()
                t.add_row([usrinfo.pk, usrinfo.username, usrinfo.public_email, usrinfo.contact_phone_number])
            else:
                pass
        except:
            pass
    print('\n'*3)
    print(Center.XCenter(Fore.YELLOW + str(t)))
    print('\n'*2)



def cmd_info(target):
    data = get_user_info(target).dict()
    print('\n'*5)
    print(Center.XCenter(Fore.YELLOW + '\n[Main]' + Fore.WHITE))
    print(Center.XCenter(Fore.WHITE + f' Follower : {data["follower_count"]}'))
    print(Center.XCenter(Fore.WHITE + f' Following : {data["following_count"]}'))
    print(Center.XCenter(Fore.WHITE + f' Username : {data["username"]}'))
    print(Center.XCenter(Fore.WHITE + f' ID : {data["pk"]}'))
    print(Center.XCenter(Fore.WHITE + f' Full Name : {data["full_name"]}'))
    print(Center.XCenter(Fore.WHITE + f' Bio : {data["biography"]}'))
    print(Center.XCenter(Fore.YELLOW + '\n[Others]' + Fore.WHITE))
    print(Center.XCenter(Fore.WHITE + f' Email : {data["public_email"]}'))
    print(Center.XCenter(Fore.WHITE + f' Phone Number : {data["contact_phone_number"]}'))
    print(Center.XCenter(Fore.YELLOW + '\n[Location]' + Fore.WHITE))
    print(Center.XCenter(Fore.WHITE + f' Latitude : {data["latitude"]}'))
    print(Center.XCenter(Fore.WHITE + f' City Name : {data["city_name"]}'))
    print(Center.XCenter(Fore.WHITE + f' City ID : {data["city_id"]}'))
    print(Center.XCenter(Fore.WHITE + f' ZIP : {data["zip"]}'))
    print(Center.XCenter(Fore.WHITE + f' Address Street : {data["address_street"]}'))
    print(Center.XCenter(Fore.YELLOW + '\n[Details]' + Fore.WHITE))
    print(Center.XCenter(Fore.WHITE + f' Private : {data["is_private"]}'))
    print(Center.XCenter(Fore.WHITE + f' Verified : {data["is_verified"]}'))
    print(Center.XCenter(Fore.WHITE + f' Business : {data["is_business"]}'))
    print('\n'*2)

    

def main():
    os.system('cls')
    print(Center.XCenter(Fore.YELLOW + osintgram))
    print(Center.XCenter(Box.Lines("REBORN BY YUX")))
    print('\n'*3)
    target = cool_input(Fore.YELLOW + 'Target ? :' + Fore.WHITE)
    cool_print(Fore.GREEN + f'[+] Logged as {Fore.YELLOW + str(api.username) + Fore.GREEN} [{Fore.YELLOW + str(api.user_id) + Fore.GREEN}] | Target: {Fore.YELLOW + target + Fore.GREEN} [{Fore.YELLOW + get_user_id(target) + Fore.GREEN}]')
    while True:
        command = cool_input(Fore.YELLOW + 'Run a command:'+ Fore.WHITE)
        
        if command == "info":
            cmd_info(target)
        elif command == "addrs":
            cmd_addrs(target)
        elif command == "fwersemail":
            cmd_fwersemail(target)
        elif command == "fwingsemail":
            cmd_fwingsemail(target)
        elif command == "tagged":
            cmd_tagged(target)
        elif command == "exit":
            exit()
        elif command == "target":
            target = command[2]
        elif command == "fwersnumber":
            cmd_fwersnumber(target)
        elif command == "fwingsnumber":
            cmd_fwingsnumber(target)
        elif command == "selftarget":
            target = api.username
            cool_print(Fore.GREEN + f'Target is now {api.username}')
        elif command == "follow":
            try:
                api.user_follow(get_user_id(target))
                cool_print(Fore.GREEN + f'Followed target!')
            except:
                cool_print(Fore.RED + f'Failed to follow target !')
        elif command == "unfollow":
            try:
                api.user_unfollow(get_user_id(target))
                cool_print(Fore.GREEN + f'Unfollowed target!')
            except:
                cool_print(Fore.RED + f'Failed to unfollow target !')
        else:
            print('[!] Invalid command.')

main()
