import base64

from turing_machine.b64_encode import b64_encode_tm


def encode_base64_url(data: str) -> str:
    data_bytes = data.encode('utf-8')
    bits = ''.join(f'{byte:08b}' for byte in data_bytes)
    b64 = b64_encode_tm.read_input(bits).tape.get_symbols_as_str().replace("_", "")
    b64_url = b64.replace("-", "+").replace(".", "/").replace("=", "")
    return b64_url


def decode_base64_url(encoded_data: str) -> str:
    try:
        encoded_data = _add_padding(encoded_data)
        encoded_bytes = encoded_data.encode('utf-8')
        decoded_bytes = base64.urlsafe_b64decode(encoded_bytes)
        return decoded_bytes.decode('utf-8')
    except Exception as e:
        raise ValueError(f"Invalid base64 URL-encoded data: {e}")


def _add_padding(encoded_data: str) -> str:
    padding = 4 - (len(encoded_data) % 4)
    if padding != 4:
        encoded_data += '=' * padding
    return encoded_data


__all__ = ['encode_base64_url', 'decode_base64_url']
