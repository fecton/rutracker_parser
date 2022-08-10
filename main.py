#!/usr/bin/env python3

import requests
import argparse
import sys
import os
import urllib3
import re
from threading import Thread
from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent
from colorama import Fore, Back, Style

urllib3.disable_warnings()

def process_name(name: str) -> str:
    new_name = re.sub(r'\\x..', '', name)
    return new_name

def get_content(url: str) -> str:
    headers = {
        'User-Agent': ua.random
    }
    return requests.get(url, headers=headers, verify=False).content

def process(start: int, end: int, args: argparse.Namespace) -> None:
    URL = "https://rutracker.org/forum/viewforum.php?f=1992&start="
    VIEW_URL = "https://rutracker.org/forum/"
    KEYWORD = args.game

    ua = UserAgent()
    if not os.path.exists("cache"):
        os.mkdir("cache")

    for i in range(start,end):
        if args.details:
            print(Back.BLUE + "[INFO]" + Style.RESET_ALL + " " + f"Parsing page {i+1}...")
        current_url = URL + str(i*50)

        try:
            with open(f"cache/{i}.html", "r") as file:
                content = file.read()
            if args.icache:
                raise FileNotFoundError
        except FileNotFoundError:
            content = get_content(current_url)
            with open(f"cache/{i}.html", "w") as file:
                file.write(str(content))

        soup = bs(content, 'html.parser')
        container = soup.find("div", id="page_content")

        if container is not None:
            container = container.find("table", class_="vf-table vf-tor forumline forum")
            games_on_page = container.find_all("tr", class_="hl-tr")
            for game in games_on_page:
                block = game.find("td", class_="vf-col-t-title tt")
                info = block.div.a
                game_name = process_name(info.text)

                link = VIEW_URL + info["href"]

                full_keyword = KEYWORD.lower() in game_name.lower()
                res = "`%s`\n%s"

                if full_keyword: # suits
                    pos = game_name.lower().find(KEYWORD.lower())
                    key = game_name[pos:pos+len(KEYWORD)]
                    print(res % (game_name.replace(key, Back.CYAN + key + Style.RESET_ALL), link), end='\n'*2)
                    if args.stop:
                        exit(0)
                else:
                    if args.eword:
                        marked_game_name = game_name
                        words = KEYWORD.split(" ")
                        is_game = False

                        if len(words) > 1:
                            i = 0
                            for keyword in words:
                                if keyword.lower() in [i.lower() for i in marked_game_name.split(" ")]:
                                    is_game = True
                                    pos = marked_game_name.lower().find(keyword.lower())
                                    key = marked_game_name[pos:pos+len(keyword)]
                                    marked_game_name = marked_game_name.replace(key, Back.MAGENTA + key + Style.RESET_ALL)

                            if is_game:
                                print(res % (marked_game_name, link), end='\n'*2)
                                if args.stop:
                                    exit(0)
        else:
            if args.details:
                print(Back.RED + "[ERROR]" + Style.RESET_ALL + " Container object is None, iteration skipped...")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='RuTracker: Native Linux Games parser')
    parser.add_argument('--game', '-g', help='A game as search query')
    parser.add_argument('--details', '-d', help='Shows more deatiled information during searching', action="store_true", default=False)
    parser.add_argument('--stop', '-s', help='Stop after a first found game', action="store_true", default=False)
    parser.add_argument('--icache', '-i', help='Ignores already saved cache', action="store_true", default=False)
    parser.add_argument('--eword', '-e', help='Checks every single word in the game name', action="store_true", default=False)

    args = parser.parse_args()

    if not args.game:
        print("Usage: " + sys.argv[0] + " --game \"Hacknet\"")
        exit(-1)


    th1 = Thread(target=process, args=(0,12,args))
    th2 = Thread(target=process, args=(12,23,args))
    th3 = Thread(target=process, args=(23,34,args))
    th4 = Thread(target=process, args=(34,47,args))

    th1.start()
    th2.start()
    th3.start()
    th4.start()

    th1.join()
    th2.join()
    th3.join()
    th4.join()

    print(Back.GREEN + "Finished!" + Style.RESET_ALL)



