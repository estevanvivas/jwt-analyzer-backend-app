import unittest
import base64

from turing_machine.b64_encode import b64_encode_tm


class Base64EncodeTest(unittest.TestCase):

    def encode_with_library(self, input_string: str) -> str:
        encoded_bytes = base64.b64encode(input_string.encode('utf-8'))
        return encoded_bytes.decode('utf-8')

    def encode_with_turing_machine(self, input_string: str) -> str:
        data_bytes = input_string.encode('utf-8')
        bits = ''.join(f'{byte:08b}' for byte in data_bytes)

        result = b64_encode_tm.read_input(bits)

        b64_output = result.tape.get_symbols_as_str().replace("_", "")
        return b64_output

    def test_empty_string(self):
        input_string = ""
        library_output = self.encode_with_library(input_string)
        tm_output = self.encode_with_turing_machine(input_string)

        self.assertEqual(tm_output, library_output,
                         f"TM output '{tm_output}' != Library output '{library_output}'")

    def test_single_character(self):
        test_cases = ["a", "b", "A", "Z", "0", "9", "!", "@"]

        for input_string in test_cases:
            with self.subTest(input=input_string):
                library_output = self.encode_with_library(input_string)
                tm_output = self.encode_with_turing_machine(input_string)

                self.assertEqual(tm_output, library_output,
                                 f"Input: '{input_string}' | TM: '{tm_output}' | Library: '{library_output}'")

    def test_two_characters(self):
        """Test con dos caracteres"""
        test_cases = ["ab", "AB", "12", "a1", "!@"]

        for input_string in test_cases:
            with self.subTest(input=input_string):
                library_output = self.encode_with_library(input_string)
                tm_output = self.encode_with_turing_machine(input_string)

                self.assertEqual(tm_output, library_output,
                                 f"Input: '{input_string}' | TM: '{tm_output}' | Library: '{library_output}'")

    def test_three_characters(self):
        test_cases = ["abc", "ABC", "123", "xyz", "foo", "bar"]

        for input_string in test_cases:
            with self.subTest(input=input_string):
                library_output = self.encode_with_library(input_string)
                tm_output = self.encode_with_turing_machine(input_string)

                self.assertEqual(tm_output, library_output,
                                 f"Input: '{input_string}' | TM: '{tm_output}' | Library: '{library_output}'")

    def test_common_words(self):
        test_cases = [
            "hello",
            "world",
            "python",
            "test",
            "data",
            "code",
            "turing",
            "machine"
        ]

        for input_string in test_cases:
            with self.subTest(input=input_string):
                library_output = self.encode_with_library(input_string)
                tm_output = self.encode_with_turing_machine(input_string)

                self.assertEqual(tm_output, library_output,
                                 f"Input: '{input_string}' | TM: '{tm_output}' | Library: '{library_output}'")

    def test_sentences(self):
        test_cases = [
            "Hello World",
            "This is a test",
            "Base64 encoding",
            "Turing Machine Test",
            "1234567890",
        ]

        for input_string in test_cases:
            with self.subTest(input=input_string):
                library_output = self.encode_with_library(input_string)
                tm_output = self.encode_with_turing_machine(input_string)

                self.assertEqual(tm_output, library_output,
                                 f"Input: '{input_string}' | TM: '{tm_output}' | Library: '{library_output}'")

    def test_special_characters(self):
        test_cases = [
            "!@#$%^&*()",
            "test@email.com",
            "path/to/file",
            "key=value",
            "a+b=c",
            "line1\nline2",
            "tab\there",
        ]

        for input_string in test_cases:
            with self.subTest(input=input_string):
                library_output = self.encode_with_library(input_string)
                tm_output = self.encode_with_turing_machine(input_string)

                self.assertEqual(tm_output, library_output,
                                 f"Input: '{input_string}' | TM: '{tm_output}' | Library: '{library_output}'")

    def test_json_strings(self):
        """Test con strings JSON comunes"""
        test_cases = [
            '{"key":"value"}',
            '{"alg":"HS256"}',
            '{"typ":"JWT"}',
            '{"user":"admin"}',
            '{"id":123}',
            '{"name":"test","age":25}',
        ]

        for input_string in test_cases:
            with self.subTest(input=input_string):
                library_output = self.encode_with_library(input_string)
                tm_output = self.encode_with_turing_machine(input_string)

                self.assertEqual(tm_output, library_output,
                                 f"Input: '{input_string}' | TM: '{tm_output}' | Library: '{library_output}'")

    def test_different_lengths(self):
        test_cases = [
            "a",
            "ab",
            "abc",
            "abcd",
            "abcde",
            "abcdef",
            "abcdefg",
            "abcdefgh",
            "abcdefghi",
            "abcdefghij",
            "abcdefghijk",
            "abcdefghijkl",
            "abcdefghijklm",
            "abcdefghijklmn",
            "abcdefghijklmno",
            "abcdefghijklmnop",
            "abcdefghijklmnopq",
            "abcdefghijklmnopqr",
            "abcdefghijklmnopqrs",
            "abcdefghijklmnopqrst",
        ]

        for input_string in test_cases:
            with self.subTest(length=len(input_string), input=input_string):
                library_output = self.encode_with_library(input_string)
                tm_output = self.encode_with_turing_machine(input_string)

                self.assertEqual(tm_output, library_output,
                                 f"Length: {len(input_string)} | Input: '{input_string}' | TM: '{tm_output}' | Library: '{library_output}'")

    def test_numeric_strings(self):
        """Test con strings numéricos"""
        test_cases = [
            "0",
            "1",
            "12",
            "123",
            "1234",
            "12345",
            "123456",
            "1234567890",
            "9876543210",
        ]

        for input_string in test_cases:
            with self.subTest(input=input_string):
                library_output = self.encode_with_library(input_string)
                tm_output = self.encode_with_turing_machine(input_string)

                self.assertEqual(tm_output, library_output,
                                 f"Input: '{input_string}' | TM: '{tm_output}' | Library: '{library_output}'")

    def test_repeated_characters(self):
        test_cases = [
            "a" * 5,
            "b" * 10,
            "xyz" * 3,
            "123" * 5,
            "ab" * 10,
        ]

        for input_string in test_cases:
            with self.subTest(input=input_string[:20] + "..."):
                library_output = self.encode_with_library(input_string)
                tm_output = self.encode_with_turing_machine(input_string)

                self.assertEqual(tm_output, library_output,
                                 f"Input length: {len(input_string)} | TM: '{tm_output}' | Library: '{library_output}'")

    def test_padding_cases(self):
        test_cases = [
            ("a", "YQ=="),
            ("M", "TQ=="),
            ("Man", "TWFu"),
            ("Ma", "TWE="),
            ("ab", "YWI="),
            ("hello", "aGVsbG8="),
        ]

        for input_string, expected_output in test_cases:
            with self.subTest(input=input_string):
                library_output = self.encode_with_library(input_string)
                tm_output = self.encode_with_turing_machine(input_string)

                self.assertEqual(library_output, expected_output,
                                 f"Library output doesn't match expected for '{input_string}'")

                self.assertEqual(tm_output, library_output,
                                 f"Input: '{input_string}' | TM: '{tm_output}' | Library: '{library_output}'")

    def test_long_strings(self):
        test_cases = [
            "The quick brown fox jumps over the lazy dog",
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit",
            "a" * 100,
            "1234567890" * 10,
        ]

        for input_string in test_cases:
            with self.subTest(length=len(input_string)):
                library_output = self.encode_with_library(input_string)
                tm_output = self.encode_with_turing_machine(input_string)

                self.assertEqual(tm_output, library_output,
                                 f"Input length: {len(input_string)} | TM length: {len(tm_output)} | Library length: {len(library_output)}")


if __name__ == '__main__':
    unittest.main()
