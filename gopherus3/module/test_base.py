import argparse
import contextlib
import io
import tempfile
import unittest
from urllib.parse import unquote_to_bytes

from gopherus3 import gopherus
from gopherus3.piper import Default, EndWith00, LineN, LineRN
from . import base
from .Redis import resp_bulk, resp_command
from .encoding import percent_encode_bytes, quote_payload


def generate_payload(argv):
    parser = gopherus.build_parser()
    args, _ = parser.parse_known_args(argv)
    with contextlib.redirect_stdout(io.StringIO()):
        generator = gopherus.class_map[args.exploit](parser, {
            "host": args.host,
            "port": args.port,
            "argv": argv,
        })
        return gopherus.piper_map[args.post]().pipe(generator.generate())


class GeneratorTest(unittest.TestCase):
    def test_generate_replaced_payload(self):
        generator = base.GENERATOR(argparse.ArgumentParser(add_help=False))
        generator.set_port(12345)
        generator.set_payload("ls -al").replace("l", "k").replace("s", "a")

        self.assertEqual(generator.generate(), "gopher://127.1:12345/_ka+-ak")

    def test_default_port_is_applied_per_subclass(self):
        class CustomGenerator(base.GENERATOR):
            default_port = 9999

        generator = CustomGenerator(options={"port": 0})

        self.assertEqual(generator.port, 9999)

    def test_hex_encoding_zero_pads_bytes(self):
        self.assertEqual(percent_encode_bytes("\x00\x0f\xff", encoding="latin-1"), "%00%0f%ff")
        self.assertEqual(percent_encode_bytes("\x00\x0f\xff", uppercase=True, encoding="latin-1"), "%00%0F%FF")

    def test_quote_payload_preserves_gopher_safe_characters(self):
        self.assertEqual(quote_payload("/tmp/a b:100%"), "/tmp/a%20b:100%25")


class PostProcessorTest(unittest.TestCase):
    def test_line_rn_is_idempotent_for_existing_crlf(self):
        payload = "a%0D%0Ab%0ac%0A"

        self.assertEqual(LineRN().pipe(payload), "a%0D%0Ab%0D%0Ac%0D%0A")
        self.assertNotIn("%0D%0D%0A", LineRN().pipe(payload))

    def test_line_n_collapses_crlf_only(self):
        self.assertEqual(LineN().pipe("a%0D%0Ab%0d%0ac"), "a%0Ab%0Ac")

    def test_default_and_end_with_00(self):
        self.assertEqual(Default().pipe("abc"), "abc")
        self.assertEqual(EndWith00().pipe("abc"), "abc%00")


class RedisRespTest(unittest.TestCase):
    def test_resp_bulk_uses_byte_length(self):
        self.assertEqual(resp_bulk("é"), b"$2\r\n\xc3\xa9\r\n")

    def test_resp_command_builds_array(self):
        self.assertEqual(resp_command("set", "k", "v"), b"*3\r\n$3\r\nset\r\n$1\r\nk\r\n$1\r\nv\r\n")

    def test_redis_cli_payload_decodes_to_resp_crlf(self):
        payload = generate_payload([
            "--exploit", "redis",
            "--content", "hello",
            "--dir", "/tmp",
            "--filename", "shell.php",
            "--silent",
        ]).split("/_", 1)[1]
        decoded = unquote_to_bytes(payload)

        self.assertIn(b"*1\r\n$8\r\nflushall\r\n", decoded)
        self.assertNotIn(b"\r\r\n", decoded)

    def test_redis_payload_preserves_literal_percent_sequences(self):
        payload = generate_payload([
            "--exploit", "redis",
            "--content", "hello%0A",
            "--dir", "/tmp",
            "--filename", "shell.php",
            "--silent",
        ])
        decoded = unquote_to_bytes(payload.split("/_", 1)[1])

        self.assertIn(b"\n\nhello%0A\n\n", decoded)
        self.assertNotIn(b"hello\n", decoded)

    def test_redis_line_rn_postprocessor_does_not_double_cr(self):
        payload = generate_payload([
            "--exploit", "redis",
            "--content", "hello",
            "--dir", "/tmp",
            "--filename", "shell.php",
            "--silent",
            "--post", "line-rn",
        ])

        self.assertIn("%0D%0A", payload)
        self.assertNotIn("%0D%0D%0A", payload)


class PayloadStabilityTest(unittest.TestCase):
    def test_cli_silent_aliases_are_equivalent(self):
        base_args = [
            "--exploit", "redis",
            "--content", "hello",
            "--dir", "/tmp",
            "--filename", "shell.php",
        ]

        self.assertEqual(
            generate_payload(base_args + ["--silent"]),
            generate_payload(base_args + ["--slient"]),
        )

    def test_plaintext_default_encodes_spaces_as_percent_20(self):
        with tempfile.NamedTemporaryFile("w", delete=True) as f:
            f.write("GET / HTTP/1.1\nHost: example.com%0A")
            f.flush()
            payload = generate_payload([
                "--exploit", "plaintext",
                "--filename", f.name,
                "--mode", "QUOTE_PLUS",
                "--silent",
            ])

        self.assertIn("GET%20/%20HTTP/1.1", payload)
        self.assertIn("example.com%250A", payload)
        self.assertNotIn("GET+", payload)

    def test_smtp_preserves_percent_sequences_as_literal_text(self):
        payload = generate_payload([
            "--exploit", "smtp",
            "--mailfrom", "a%@example.com",
            "--mailto", "b@example.com",
            "--subject", "hi%0Athere",
            "--msg", "%0Abody",
            "--silent",
        ])
        decoded = unquote_to_bytes(payload.split("/_", 1)[1])

        self.assertIn(b"MAIL FROM:a%@example.com\n", decoded)
        self.assertIn(b"Subject:hi%0Athere\n", decoded)
        self.assertIn(b"Message:%0Abody\n", decoded)

    def test_php_memcached_uses_byte_length_for_non_ascii_code(self):
        payload = generate_payload([
            "--exploit", "phpmemcache",
            "--code", "é",
            "--silent",
        ])
        decoded = unquote_to_bytes(payload.split("/_", 1)[1])

        self.assertIn(b"set SpyD3r 4 0 2\r\n\xc3\xa9\r\n", decoded)

    def test_all_generators_are_deterministic_and_url_like(self):
        cases = [
            ["--exploit", "dmpmemcache", "--code", "stats items", "--silent"],
            ["--exploit", "fastcgi", "--targetfile", "/usr/share/php/PEAR.php", "--command", "id", "--silent"],
            ["--exploit", "mysql", "--user", "root", "--query", "select 1", "--silent"],
            ["--exploit", "phpmemcache", "--code", "O:5:\"Hello\":0:{}", "--silent"],
            ["--exploit", "postgresql", "--user", "postgres", "--db", "postgres", "--query", "select 1", "--silent"],
            ["--exploit", "pymemcache", "--command", "id", "--silent"],
            ["--exploit", "rbmemcache", "--command", "id", "--silent"],
            ["--exploit", "redis", "--content", "hello", "--dir", "/tmp", "--filename", "shell.php", "--silent"],
            ["--exploit", "smtp", "--mailfrom", "a@example.com", "--mailto", "b@example.com", "--subject", "hi", "--msg", "body", "--silent"],
            ["--exploit", "zabbix", "--command", "id", "--silent"],
        ]

        for argv in cases:
            with self.subTest(exploit=argv[1]):
                first = generate_payload(argv)
                second = generate_payload(argv)
                self.assertEqual(first, second)
                self.assertRegex(first, r"^gopher://127\.0\.0\.1:\d+/_")
                self.assertNotIn(" ", first)


if __name__ == "__main__":
    unittest.main()
