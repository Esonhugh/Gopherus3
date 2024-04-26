import base 

import logging as log
log.basicConfig(level=log.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

def test_base():
    b = base.GENERATOR()
    b.set_port(12345)
    b.set_payload("ls -al").replace("l", "k").replace("s", "a")
    b.debug_dump()
    print(b.generate())


if __name__ == "__main__":
    test_base()