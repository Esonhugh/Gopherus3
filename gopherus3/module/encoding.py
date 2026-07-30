import binascii
import urllib.parse


def to_bytes(value, encoding="utf-8"):
    if isinstance(value, bytes):
        return value
    return str(value).encode(encoding)


def quote_payload(value, safe="/:", encoding="utf-8"):
    return urllib.parse.quote_from_bytes(to_bytes(value, encoding), safe=safe)


def quote_plus_payload(value, safe="", encoding="utf-8"):
    return urllib.parse.quote_plus(to_bytes(value, encoding), safe=safe)


def percent_encode_bytes(value, uppercase=False, encoding="utf-8"):
    template = "%{byte:02X}" if uppercase else "%{byte:02x}"
    return "".join(template.format(byte=byte) for byte in to_bytes(value, encoding))


def hexlify_text(value, encoding="latin-1"):
    return binascii.hexlify(to_bytes(value, encoding)).decode("ascii")


def percent_encode_hex(hex_string):
    pairs = [hex_string[i:i + 2] for i in range(0, len(hex_string), 2)]
    return "%" + "%".join(pairs)
