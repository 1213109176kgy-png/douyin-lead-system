import hashlib
import time
import asyncio
from functools import partial


class XBogus:
    def __init__(self) -> None:
        self.Array = [
            None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
            None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
            None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
            0, 1, 2, 3, 4, 5, 6, 7, 8, 9, None, None, None, None, None, None, None, None, None, None, None,
            None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
            None, None, None, None, None, None, None, None, None, None, None, None, 10, 11, 12, 13, 14, 15
        ]
        self.character = "Dkdpgh4ZKsQB80/Mfvw36XI1R25-WUAlEi7NLboqYTOPuzmFjJnryx9HVGcaStCe="

    def md5_str_to_array(self, md5_str):
        if isinstance(md5_str, str) and len(md5_str) > 32:
            return [ord(char) for char in md5_str]

        array = []
        idx = 0
        while idx < len(md5_str):
            array.append((self.Array[ord(md5_str[idx])] << 4) | self.Array[ord(md5_str[idx + 1])])
            idx += 2
        return array

    async def md5(self, input_data):

        def _compute_md5(data):
            if isinstance(data, str):
                array = self.md5_str_to_array(data)
            elif isinstance(data, list):
                array = data
            else:
                raise ValueError("Invalid input type. Expected str or list.")

            md5_hash = hashlib.md5()
            md5_hash.update(bytes(array))
            return md5_hash.hexdigest()

        return await asyncio.get_event_loop().run_in_executor(None, _compute_md5, input_data)

    async def md5_encrypt(self, url_path):
        first_md5 = await self.md5(url_path)
        first_array = self.md5_str_to_array(first_md5)
        second_md5 = await self.md5(first_array)
        return self.md5_str_to_array(second_md5)

    def encoding_conversion(self, a, b, c, e, d, t, f, r, n, o, i, _, x, u, s, l, v, h, p):
        y = [a]
        y.append(int(i))
        y.extend([b, _, c, x, e, u, d, s, t, l, f, v, r, h, n, p, o])
        return bytes(y).decode('ISO-8859-1')

    def encoding_conversion2(self, a, b, c):
        return chr(a) + chr(b) + c

    async def rc4_encrypt(self, key, data):

        def _compute_rc4(k, d):
            S = list(range(256))
            j = 0
            encrypted_data = bytearray()

            # 初始化 S 盒
            for i in range(256):
                j = (j + S[i] + k[i % len(k)]) % 256
                S[i], S[j] = S[j], S[i]

            # 生成密文
            i = j = 0
            for byte in d:
                i = (i + 1) % 256
                j = (j + S[i]) % 256
                S[i], S[j] = S[j], S[i]
                encrypted_byte = byte ^ S[(S[i] + S[j]) % 256]
                encrypted_data.append(encrypted_byte)

            return encrypted_data

        return await asyncio.get_event_loop().run_in_executor(
            None, partial(_compute_rc4, key, data))

    def calculation(self, a1, a2, a3):
        x1 = (a1 & 255) << 16
        x2 = (a2 & 255) << 8
        x3 = x1 | x2 | a3
        return (self.character[(x3 & 16515072) >> 18] +
                self.character[(x3 & 258048) >> 12] +
                self.character[(x3 & 4032) >> 6] +
                self.character[x3 & 63])

    async def getXBogus(self, url_path):
        array1_task = asyncio.create_task(
            self.md5("d88201c9344707acde7261b158656c0e"))
        array2_task = asyncio.create_task(
            self.md5("d41d8cd98f00b204e9800998ecf8427e"))

        array1 = self.md5_str_to_array(await array1_task)
        temp_array = self.md5_str_to_array(await array2_task)
        array2 = self.md5_str_to_array(await self.md5(temp_array))

        url_path_array = await self.md5_encrypt(url_path)

        timer = int(time.time())
        ct = 536919696
        array3 = []
        array4 = []
        xb_ = ""

        new_array = [
            64, 0.00390625, 1, 8,
            url_path_array[14], url_path_array[15], array2[14], array2[15], array1[14], array1[15],
            timer >> 24 & 255, timer >> 16 & 255, timer >> 8 & 255, timer & 255,
            ct >> 24 & 255, ct >> 16 & 255, ct >> 8 & 255, ct & 255
        ]

        xor_result = new_array[0]
        for i in range(1, len(new_array)):
            b = new_array[i]
            if isinstance(b, float):
                b = int(b)
            xor_result ^= b

        new_array.append(xor_result)

        idx = 0
        while idx < len(new_array):
            array3.append(new_array[idx])
            try:
                array4.append(new_array[idx + 1])
            except IndexError:
                pass
            idx += 2

        merge_array = array3 + array4

        garbled_code = self.encoding_conversion2(
            2, 255, (await self.rc4_encrypt(
                "ÿ".encode('ISO-8859-1'),
                self.encoding_conversion(*merge_array).encode('ISO-8859-1')
            )).decode('ISO-8859-1'))

        idx = 0
        while idx < len(garbled_code):
            xb_ += self.calculation(ord(garbled_code[idx]),
                                    ord(garbled_code[idx + 1]),
                                    ord(garbled_code[idx + 2]))
            idx += 3

        self.params = f'{url_path}&X-Bogus={xb_}'
        return self.params