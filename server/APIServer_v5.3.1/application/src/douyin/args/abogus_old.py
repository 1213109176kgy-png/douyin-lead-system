import time
import random
import asyncio
import threading

_fixed_time = None
_random_lock = threading.Lock()


def set_fixed_time(timestamp=None):
    global _fixed_time
    if timestamp is not None:
        _fixed_time = timestamp
    else:
        _fixed_time = None


def get_time():
    global _fixed_time
    if _fixed_time is not None:
        return _fixed_time
    return time.time()


async def encrypt_abogus(user_agent, query, body=''):
    return await _encrypt_abogus_impl(user_agent, query, body)


def encrypt_abogus_sync(user_agent, query, body=''):
    return _encrypt_abogus_core(user_agent, query, body)


async def _encrypt_abogus_impl(user_agent, query, body=''):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(
        None,
        _encrypt_abogus_core,
        user_agent,
        query,
        body
    )


def _encrypt_abogus_core(user_agent, query, body=''):
    with _random_lock:
        # 保存当前随机状态
        random_state = random.getstate()
        table_obj = {
            "s0": "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=",  # 标准
            "s1": "Dkdpgh4ZKsQB80/Mfvw36XI1R25+WUAlEi7NLboqYTOPuzmFjJnryx9HVGcaStCe=",
            "s2": "Dkdpgh4ZKsQB80/Mfvw36XI1R25-WUAlEi7NLboqYTOPuzmFjJnryx9HVGcaStCe=",  # xb
            "s3": "ckdp1h4ZKsUB80/Mfvw36XIgR25+WQAlEi7NLboqYTOPuzmFjJnryx9HVGDaStCe",  # ua
            "s4": "Dkdpgh2ZmsQB80/MfvV36XI1R45-WUAlEixNLwoqYTOPuzKFjJnry79HbGcaStCe"  # ab
        }

        def lm_str_encode(lm_arr, table):
            """完全按照JavaScript版本编码Base64"""
            data_str = ''
            group_num = len(lm_arr) // 3

            for i in range(group_num):
                lm_cha1 = lm_arr[3 * i]
                lm_cha2 = lm_arr[3 * i + 1] if 3 * i + 1 < len(lm_arr) else 0
                lm_cha3 = lm_arr[3 * i + 2] if 3 * i + 2 < len(lm_arr) else 0

                big_num = (lm_cha1 & 255) << 16 | ((lm_cha2 & 255) << 8) | (lm_cha3 & 255)

                chr1 = table[(big_num & 16515072) >> 18]
                chr2 = table[(big_num & 258048) >> 12]
                chr3 = table[(big_num & 4032) >> 6]
                chr4 = table[big_num & 63]

                data_str += f"{chr1}{chr2}{chr3}{chr4}"

            remainder = len(lm_arr) % 3
            if remainder == 1:
                i = group_num
                lm_cha1 = lm_arr[3 * i]
                big_num = (lm_cha1 & 255) << 16
                chr1 = table[(big_num & 16515072) >> 18]
                chr2 = table[(big_num & 258048) >> 12]
                data_str += f"{chr1}{chr2}=="
            elif remainder == 2:
                i = group_num
                lm_cha1 = lm_arr[3 * i]
                lm_cha2 = lm_arr[3 * i + 1]
                big_num = (lm_cha1 & 255) << 16 | ((lm_cha2 & 255) << 8)
                chr1 = table[(big_num & 16515072) >> 18]
                chr2 = table[(big_num & 258048) >> 12]
                chr3 = table[(big_num & 4032) >> 6]
                data_str += f"{chr1}{chr2}{chr3}="

            return data_str

        def parse(lm_str, data_str):
            """对字符串进行变换，与JavaScript版本一致"""
            ret_str = ''
            arr256 = [255 - i for i in range(256)]
            swap_idx = 0
            for s in range(len(arr256)):
                char_code = ord(lm_str[s % len(lm_str)])
                swap_idx = (swap_idx * arr256[s] + swap_idx + char_code) % 256
                arr256[s], arr256[swap_idx] = arr256[swap_idx], arr256[s]
            bak = 0
            for i in range(len(data_str)):
                idx = (i + 1) % 256
                idx2 = (bak + arr256[idx]) % 256
                bak = idx2
                arr256[idx], arr256[idx2] = arr256[idx2], arr256[idx]
                idx3 = (arr256[idx2] + arr256[idx]) % 256
                num = ord(data_str[i]) ^ arr256[idx3]
                ret_str += chr(num)

            return ret_str

        def str_to_int_arr(data_str):
            return [ord(c) for c in data_str]

        class SM3:
            """SM3哈希算法实现，与JavaScript版本保持一致"""

            def __init__(self):
                self.reset()

            def reset(self):
                # 初始向量IV，标准值
                self.reg = [
                    0x7380166f, 0x4914b2b9, 0x172442d7, 0xda8a0600,
                    0xa96f30bc, 0x163138aa, 0xe38dee4d, 0xb0fb0e4e
                ]
                self.block = []
                self.size = 0

            def rotate_left(self, x, n):
                n = n % 32
                return ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF

            def P0(self, x):
                return x ^ self.rotate_left(x, 9) ^ self.rotate_left(x, 17)

            def P1(self, x):
                return x ^ self.rotate_left(x, 15) ^ self.rotate_left(x, 23)

            def FF(self, x, y, z, j):
                if j < 16:
                    return x ^ y ^ z
                else:
                    return (x & y) | (x & z) | (y & z)

            def GG(self, x, y, z, j):
                if j < 16:
                    return x ^ y ^ z
                else:
                    return (x & y) | (~x & z)

            def T(self, j):
                if j < 16:
                    return 0x79CC4519
                else:
                    return 0x7A879D8A

            def update(self, data):
                if isinstance(data, str):
                    data = [ord(c) for c in data]

                self.size += len(data)
                data_idx = 0
                if len(self.block) > 0:
                    while len(self.block) < 64 and data_idx < len(data):
                        self.block.append(data[data_idx])
                        data_idx += 1

                    if len(self.block) == 64:
                        self.compress(self.block)
                        self.block = []
                while data_idx + 64 <= len(data):
                    self.compress(data[data_idx:data_idx + 64])
                    data_idx += 64
                while data_idx < len(data):
                    self.block.append(data[data_idx])
                    data_idx += 1

            def compress(self, block):
                if len(block) != 64:
                    return
                W = [0] * 68
                W1 = [0] * 64
                for i in range(16):
                    W[i] = (block[4 * i] << 24) | (block[4 * i + 1] << 16) | (block[4 * i + 2] << 8) | block[4 * i + 3]
                for j in range(16, 68):
                    W[j] = self.P1(W[j - 16] ^ W[j - 9] ^ self.rotate_left(W[j - 3], 15)) ^ self.rotate_left(W[j - 13],
                                                                                                             7) ^ W[
                               j - 6]
                    W[j] &= 0xFFFFFFFF
                for j in range(64):
                    W1[j] = W[j] ^ W[j + 4]
                A, B, C, D, E, F, G, H = self.reg
                for j in range(64):
                    ss1 = self.rotate_left(
                        (self.rotate_left(A, 12) + E + self.rotate_left(self.T(j), j % 32)) & 0xFFFFFFFF, 7)
                    ss2 = ss1 ^ self.rotate_left(A, 12)
                    tt1 = (self.FF(A, B, C, j) + D + ss2 + W1[j]) & 0xFFFFFFFF
                    tt2 = (self.GG(E, F, G, j) + H + ss1 + W[j]) & 0xFFFFFFFF

                    D = C
                    C = self.rotate_left(B, 9)
                    B = A
                    A = tt1
                    H = G
                    G = self.rotate_left(F, 19)
                    F = E
                    E = self.P0(tt2)
                self.reg[0] ^= A
                self.reg[1] ^= B
                self.reg[2] ^= C
                self.reg[3] ^= D
                self.reg[4] ^= E
                self.reg[5] ^= F
                self.reg[6] ^= G
                self.reg[7] ^= H

            def finalize(self):
                bit_length = self.size * 8

                self.block.append(0x80)

                while (len(self.block) + 8) % 64 != 0:
                    self.block.append(0)

                length_bytes = [(bit_length >> (56 - i * 8)) & 0xFF for i in range(8)]
                self.block.extend(length_bytes)

                for i in range(0, len(self.block), 64):
                    self.compress(self.block[i:i + 64])

                self.block = []

            def digest(self):
                sm3 = SM3()
                sm3.reg = self.reg.copy()
                sm3.block = self.block.copy()
                sm3.size = self.size

                sm3.finalize()

                result = []
                for word in sm3.reg:
                    result.append((word >> 24) & 0xFF)
                    result.append((word >> 16) & 0xFF)
                    result.append((word >> 8) & 0xFF)
                    result.append(word & 0xFF)

                return result

        def sum_encrypt(data):
            hasher = SM3()
            hasher.update(data)
            return hasher.digest()

        def get_abogus_lm_arr4():
            """前缀随机数组，与JavaScript版本一致"""
            random_val1 = int(random.random() * 65535)
            random_val2 = int(random.random() * 40)

            return [
                (random_val1 & 170) | 1,
                (random_val1 & 85) | 2,
                (random_val2 & 170) | 80,
                (random_val2 & 85) | 2
            ]

        def get_tm_arr(tm):
            tm_num = (tm + 3) & 255
            tm_str = f"{tm_num},"
            return [ord(c) for c in tm_str]

        def get_fp_arr():
            """生成浏览器指纹数组，与JavaScript版本保持一致"""
            fp_str = '1440|266|1440|823|1920|1055|1920|1080|MacIntel'
            return [ord(c) for c in fp_str]

        def get_xor_random_arr8():
            """生成8个随机数，与JavaScript版本保持一致"""
            random_val1 = int(random.random() * 65535)
            tmp_val1 = random_val1 & 255
            tmp_val2 = (random_val1 >> 8) & 255

            random_val = int(random.random() * 255)
            random_val2 = int(random.random() * 240)
            is_even = random_val2 + 110
            is_even = is_even if is_even % 2 == 0 else is_even + 1

            return [
                (tmp_val1 & 170) | 1,
                (tmp_val1 & 85) | 0,
                (tmp_val2 & 170) | 0,
                (tmp_val2 & 85) | 0,
                (is_even & 170) | 1,
                (is_even & 85) | 0,
                ((random_val & 77) | 2 | 16 | 32 | 128) & 170 | 16,
                ((random_val & 77) | 16 | 32 | 128) & 85 | 2
            ]

        def get_new_arr50(arr50):
            """重排序数组，与JavaScript版本保持一致"""
            indices = [
                9, 18, 28, 32, 44, 4, 11, 11, 9, 23,
                12, 37, 24, 39, 3, 22, 35, 11, 5, 42,
                1, 27, 33, 11, 30, 14, 6, 7, 2, 43,
                15, 11, 29, 25, 16, 11, 8, 38, 26, 17,
                9, 11, 11, 0, 31, 7, 46, 47, 48, 49
            ]

            ordered_arr50 = [0] * 50
            for i, idx in enumerate(indices):
                if idx < len(arr50):
                    ordered_arr50[i] = arr50[idx]

            return ordered_arr50

        def get_xor_array(arr):
            """计算异或结果，与JavaScript版本保持一致"""
            xor_result = 0
            for i in range(len(arr)):
                xor_result ^= arr[i]
            return [xor_result]

        try:
            salt = 'dhzx'
            current_time = get_time()  # 使用可控的时间函数
            tm2 = int(current_time * 1000) - 1
            tm1_before = int(current_time * 1000)

            query_with_salt = f"{query}{salt}"
            body_with_salt = f"{body}{salt}"

            query_hash1 = sum_encrypt(query_with_salt)
            query_arr32 = sum_encrypt(query_hash1)

            body_hash1 = sum_encrypt(body_with_salt)
            data_arr32 = sum_encrypt(body_hash1)

            ua_init = chr(0) + chr(1) + chr(0)
            user_agent_lm_str = parse(ua_init, user_agent)
            user_agent_bytes = str_to_int_arr(user_agent_lm_str)
            user_agent_encoded = lm_str_encode(user_agent_bytes, table_obj["s3"])
            user_agent_arr32 = sum_encrypt(user_agent_encoded)

            tm1 = int(current_time * 1000)
            fp_arr = get_fp_arr()

            arr50 = [
                41,
                8,
                6,
                ((tm1 - tm1_before) + 3) & 255,

                tm1 & 255,
                (tm1 >> 8) & 255,
                (tm1 >> 16) & 255,
                (tm1 >> 24) & 255,
                int(tm1 / 2 ** 32) & 255,
                int(tm1 / 2 ** 40) & 255,

                1, 0,

                129, 0,

                255, 10, 9, 9,

                0, 0, 0, 0,

                query_arr32[9] if len(query_arr32) > 9 else 0,
                query_arr32[18] if len(query_arr32) > 18 else 0,
                query_arr32[3] if len(query_arr32) > 3 else 0,
                data_arr32[10] if len(data_arr32) > 10 else 0,
                data_arr32[19] if len(data_arr32) > 19 else 0,
                data_arr32[4] if len(data_arr32) > 4 else 0,
                user_agent_arr32[11] if len(user_agent_arr32) > 11 else 0,
                user_agent_arr32[21] if len(user_agent_arr32) > 21 else 0,
                user_agent_arr32[5] if len(user_agent_arr32) > 5 else 0,

                tm2 & 255,
                (tm2 >> 8) & 255,
                (tm2 >> 16) & 255,
                (tm2 >> 24) & 255,
                int(tm2 / 2 ** 32) & 255,
                int(tm2 / 2 ** 40) & 255,

                3,

                27092 & 255,
                (27092 >> 8) & 255,
                (27092 >> 16) & 255,
                (27092 >> 24) & 255,

                549224 & 255,
                (549224 >> 8) & 255,
                (549224 >> 16) & 255,
                (549224 >> 24) & 255,

                46, 0, 3, 0
            ]

            new_arr50 = get_new_arr50(arr50)

            xor_random_arr8 = get_xor_random_arr8()
            arr58 = xor_random_arr8 + arr50
            xor_array = get_xor_array(arr58)

            arr4_merge = new_arr50 + fp_arr + get_tm_arr(tm1) + xor_array

            abogus_lm_arr4 = get_abogus_lm_arr4()
            abogus_lm_str = ''.join(chr(x) for x in abogus_lm_arr4)

            merge_arr = []
            for i in range(len(arr4_merge) // 3):
                idx = 3 * i
                val1 = arr4_merge[idx] if idx < len(arr4_merge) else 0
                val2 = arr4_merge[idx + 1] if idx + 1 < len(arr4_merge) else 0
                val3 = arr4_merge[idx + 2] if idx + 2 < len(arr4_merge) else 0

                random_val = int(random.random() * 1000) & 255

                merge_arr.extend([
                    (random_val & 145) | (val1 & 110),
                    (random_val & 66) | (val2 & 189),
                    (random_val & 44) | (val3 & 211),
                    ((val1 & 145) | (val2 & 66)) | (val3 & 44)
                ])

            big_arr = xor_random_arr8 + merge_arr + xor_array

            big_str = ''.join(chr(x) for x in big_arr)
            abogus_lm_str += parse(chr(211), big_str)

            abogus_lm_arr = str_to_int_arr(abogus_lm_str)
            result = lm_str_encode(abogus_lm_arr, table_obj["s4"])

            return result
        finally:
            random.setstate(random_state)


encrypt_abogus_async = encrypt_abogus
