import argparse
import unittest

from . import base


class GeneratorTest(unittest.TestCase):
    def test_generate_replaced_payload(self):
        generator = base.GENERATOR(argparse.ArgumentParser(add_help=False))
        generator.set_port(12345)
        generator.set_payload("ls -al").replace("l", "k").replace("s", "a")

        self.assertEqual(generator.generate(), "gopher://127.1:12345/_ka+-ak")


if __name__ == "__main__":
    unittest.main()
