#!/usr/bin/env python3

import requests
import argparse
import sys
import os
import urllib3
import re
import psutil
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
                res = "%s\n%s"

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
    ua = UserAgent()

    parser = argparse.ArgumentParser(description='RuTracker: Native Linux Games parser')
    parser.add_argument('--game', '-g', help='A game as search query')
    parser.add_argument('--details', '-d', help='Shows more deatiled information during searching', action="store_true", default=False)
    parser.add_argument('--stop', '-s', help='Stop after a first found game', action="store_true", default=False)
    parser.add_argument('--icache', '-i', help='Ignores already saved cache', action="store_true", default=False)
    parser.add_argument('--eword', '-e', help='Checks every single word in the game name', action="store_true", default=False)

    args = parser.parse_args()
    THREADS_COUNT = psutil.cpu_count(logical=True)

    if not args.game:
        print("Usage: " + sys.argv[0] + " --game \"Hacknet\"")
        exit(-1)

    if args.details:
        print(f"THREADS: {THREADS_COUNT}")

    try:
        pages = int((bs(get_content("https://rutracker.org/forum/viewforum.php?f=1992"), "html.parser").find("div", id="page_content").find("td", id="main_content").find("div", id="main_content_wrap").find("td", class_="w100 vBottom pad_2").find("div").find("b").find_all("a"))[-2].text)
    except:
        pages = 47

    threads = []
    step = pages // THREADS_COUNT
    start = 0
    for i in range(THREADS_COUNT):
        tmp = (start, start+step, args)
        if i != THREADS_COUNT - 1:
            threads.append(Thread(target=process, args=tmp))
        start += step

    tmp = (tmp[0], tmp[1]+(pages-step*THREADS_COUNT), args)
    threads.append(Thread(target=process, args=tmp))

    for th in threads:
        th.start()

    for th in threads:
        th.join()

    print()
    print(Back.GREEN + "Program finished!" + Style.RESET_ALL)

