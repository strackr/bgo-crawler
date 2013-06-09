#!/usr/bin/env python2

from argparse import ArgumentParser
from bgo.parser import LogParser

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-u", "--user", dest="user", help="username")
    parser.add_argument("-p", "--password", dest="password", help="password")
    parser.add_argument("-g", "--game", dest="game", help="game id")
    
    # Process arguments
    args = parser.parse_args()

    crawler = LogParser(args.user, args.password, args.game)
    entries = crawler.extract_logs()
    for entry in entries:
        print(entry)
