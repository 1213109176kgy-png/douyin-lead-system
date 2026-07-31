
function get_arr(t,a) {
    reg = {
        "chunk": [],
        "reg": [1937774191, 1226093241, 388252375, 3666478592, 2842636476, 372324522, 3817729613, 2969243214],
        "size": 0,
        "write": function (e) {
            var o = typeof e === "string" ? function (e) {
                var n = encodeURIComponent(e).replace(/%([0-9A-F]{2})/g, function (e, t) {
                        return String.fromCharCode("0x" + t);
                    }),
                    o = new Array(n.length);
                return Array.prototype.forEach.call(n, function (e, t) {
                    o[t] = e.charCodeAt(0);
                }), o;
            }(e) : e;
            this.size += o.length;
            var i = 64 - this.chunk.length;
            if (o.length < i) this.chunk = this.chunk.concat(o); else for (this.chunk = this.chunk.concat(o.slice(0, i)); this.chunk.length >= 64;) this._compress(this.chunk), i < o.length ? this.chunk = o.slice(i, Math.min(i + 64, o.length)) : this.chunk = [], i += 64;
        },
        "sum": function (r, n) {
            r && (this.reset(), this.write(r)), this._fill();
            for (var a = 0; a < this.chunk.length; a += 64) this._compress(this.chunk.slice(a, a + 64));
            var c = null;
            if (n == "hex") {
                c = "";
                for (a = 0; a < 8; a++) c += gt(this.reg[a].toString(16), 8, "0");
            } else for (c = new Array(32), a = 0; a < 8; a++) {
                var f = this.reg[a];
                c[4 * a + 3] = (255 & f) >>> 0, f >>>= 8, c[4 * a + 2] = (255 & f) >>> 0, f >>>= 8, c[4 * a + 1] = (255 & f) >>> 0, f >>>= 8, c[4 * a] = (255 & f) >>> 0;
            }
            return this.reset(), c;
        },
        "_compress": function (r) {
            if (r < 64) console.error("compress error: not enough data"); else {
                for (var o = function (e) {
                    for (var t = new Array(132), r = 0; r < 16; r++) t[r] = e[4 * r] << 24, t[r] |= e[4 * r + 1] << 16, t[r] |= e[4 * r + 2] << 8, t[r] |= e[4 * r + 3], t[r] >>>= 0;
                    for (var n = 16; n < 68; n++) {
                        var o = t[n - 16] ^ t[n - 9] ^ Ct(t[n - 3], 15);
                        o = o ^ Ct(o, 15) ^ Ct(o, 23), t[n] = (o ^ Ct(t[n - 13], 7) ^ t[n - 6]) >>> 0;
                    }
                    for (n = 0; n < 64; n++) t[n + 68] = (t[n] ^ t[n + 4]) >>> 0;
                    return t;
                }(r), i = this.reg.slice(0), a = 0; a < 64; a++) {
                    var c = Ct(i[0], 12) + i[4] + Ct(St(a), a),
                        f = ((c = Ct(c = (4294967295 & c) >>> 0, 7)) ^ Ct(i[0], 12)) >>> 0,
                        u = kt(a, i[0], i[1], i[2]);
                    u = (4294967295 & (u = u + i[3] + f + o[a + 68])) >>> 0;
                    var s = xt(a, i[4], i[5], i[6]);
                    s = (4294967295 & (s = s + i[7] + c + o[a])) >>> 0, i[3] = i[2], i[2] = Ct(i[1], 9), i[1] = i[0], i[0] = u, i[7] = i[6], i[6] = Ct(i[5], 19), i[5] = i[4], i[4] = (s ^ Ct(s, 9) ^ Ct(s, 17)) >>> 0;
                }
                for (var l = 0; l < 8; l++) this.reg[l] = (this.reg[l] ^ i[l]) >>> 0;
            }
        },
        "_fill": function () {
            var o = 8 * this.size,
                i = this.chunk.push(128) % 64;
            for (64 - i < 8 && (i -= 64); i < 56; i++) this.chunk.push(0);
            for (var a = 0; a < 4; a++) {
                var c = Math.floor(o / 4294967296);
                this.chunk.push(c >>> 8 * (3 - a) & 255);
            }
            for (a = 0; a < 4; a++) this.chunk.push(o >>> 8 * (3 - a) & 255);
        }
    }

    reg.write(t)
    reg._fill();

    function Ct(e, t) {
        return (e << (t %= 32) | e >>> 32 - t) >>> 0;
    }

    function St(e) {
        return 0 <= e && e < 16 ? 2043430169 : 16 <= e && e < 64 ? 2055708042 : void console.error("invalid j for constant Tj");
    }

    function kt(e, t, r, n) {
        return 0 <= e && e < 16 ? (t ^ r ^ n) >>> 0 : 16 <= e && e < 64 ? (t & r | t & n | r & n) >>> 0 : (console.error("invalid j for bool function FF"), 0);
    }

    function xt(e, t, r, n) {
        return 0 <= e && e < 16 ? (t ^ r ^ n) >>> 0 : 16 <= e && e < 64 ? (t & r | ~t & n) >>> 0 : (console.error("invalid j for bool function GG"), 0);
    }

    for (var i = 0; i < reg["chunk"]["length"]; i += 64) {
        reg["_compress"](reg["chunk"]["slice"](i, i + 64));
    }

    var o = null;
    if (a == "hex") {
        o = "";
        for (i = 0; i < 8; i++)
            o += oe(reg["reg"][i]["toString"](16), 8, "0")
    } else {
        for (o = new Array(32),
                 i = 0; i < 8; i++) {
            var c = reg.reg[i];
            o[4 * i + 3] = (255 & c) >>> 0,
                c >>>= 8,
                o[4 * i + 2] = (255 & c) >>> 0,
                c >>>= 8,
                o[4 * i + 1] = (255 & c) >>> 0,
                c >>>= 8,
                o[4 * i] = (255 & c) >>> 0
        }
    }
    return o;
}

function getABogus(url,data,userAgent){
   // 生成乱码字符串
    var params = url.slice(url.indexOf("?") + 1) + "dhzx";
	data += "dhzx";
    var garbledString = getGarbledString(params,data,userAgent);
    var short_str = "Dkdpgh2ZmsQB80/MfvV36XI1R45-WUAlEixNLwoqYTOPuzKFjJnry79HbGcaStCe"
    var ABogus = "";
    // 依次生成七组字符串
    let j = 0
    for (var i = 0; i <= garbledString.length;i += 3) {
        if ((i + 3) <= garbledString.length) {
            var charCodeAtNum0 = garbledString.charCodeAt(i);
            var charCodeAtNum1 = garbledString.charCodeAt(i + 1);
            var charCodeAtNum2 = garbledString.charCodeAt(i + 2);
            var baseNum = charCodeAtNum2 | charCodeAtNum1 << 8 | charCodeAtNum0 << 16;

            var str1 = short_str[(baseNum & 16515072) >> 18];
            var str2 = short_str[(baseNum & 258048) >> 12];
            var str3 = short_str[(baseNum & 4032) >> 6];
            var str4 = short_str[baseNum & 63];
            ABogus += str1 + str2 + str3 + str4;
        }
        if (i + 3 > garbledString.length){
            let u = garbledString.length - j
            if (u === 2){
                var charCodeAtNum0 = garbledString.charCodeAt(j);
                var charCodeAtNum1 = garbledString.charCodeAt(j + 1);
                var baseNum = charCodeAtNum1 << 8 | charCodeAtNum0 << 16;
                var str1 = short_str[(baseNum & 16515072) >> 18];
                var str2 = short_str[(baseNum & 258048) >> 12];
                var str3 = short_str[(baseNum & 4032) >> 6];
                ABogus += str1 + str2 + str3 + '=';
            }
            if (u === 1){
                var charCodeAtNum0 = garbledString.charCodeAt(j);
                var baseNum = 0 | charCodeAtNum0 << 16;
                var str1 = short_str[(baseNum & 16515072) >> 18];
                var str2 = short_str[(baseNum & 258048) >> 12];
                ABogus += str1 + str2 + '=' + '=';
            }

        }
        j +=3
    }
    return ABogus;
}

function _0x46fa4c(a, c) {
    let e, b = [], d = 0, f = "";
    for (let a = 0; a < 256; a++) {
        b[a] = a;
    }
    for (let c = 0; c < 256; c++) {
        d = (d + b[c] + a.charCodeAt(c % a.length)) % 256,
            e = b[c],
            b[c] = b[d],
            b[d] = e;
    }
    let t = 0;
    d = 0;
    for (let a = 0; a < c.length; a++) {
        t = (t + 1) % 256,
            d = (d + b[t]) % 256,
            e = b[t],
            b[t] = b[d],
            b[d] = e,
            f += String.fromCharCode(c.charCodeAt(a) ^ b[(b[t] + b[d]) % 256]);
    }
    return f;
}

function getGarbledString(params,data,userAgent) {
    let timestamp1 = Date.now(),timestamp2 = timestamp1 - Math.floor(Math.random() * 10);
    let arr_29 = get_arr29(timestamp1,timestamp2,params,data,userAgent)
    // let a = get_fromCharCodeStr1();
    let a = topHeaderRandomGarbledCharacters();
    let b = abGarbledCharacters(String.fromCharCode.apply(null,arr_29))
    return a+b;
}

function abGarbledCharacters(userAgent) {
    let arr_256 = ab_arr_256();
    let n4 = 0;
    let ans = "";
    for (let i = 0; i < userAgent.length; i++) {
        let n2 = (i + 1) % 256;
        let n3 = n4 + arr_256[n2]
        n4 = n3 % 256
        let old_arr_n2 = arr_256[n2]
        arr_256[n2] = arr_256[n4]
        arr_256[n4] = old_arr_n2
        let n5 = userAgent.charCodeAt(i);
        let n6 = arr_256[n2] + old_arr_n2;
        let n7 = n6 % 256
        let n8 = n5 ^ arr_256[n7]
        ans += String.fromCharCode(n8)
    }
    return ans;
}

function ab_arr_256() {
    let nums = [255,254,253,252,251,250,249,248,247,246,245,244,243,242,241,240,239,238,237,236,235,234,233,232,231,230,229,228,227,226,225,224,223,222,221,220,219,218,217,216,215,214,213,212,211,210,209,208,207,206,205,204,203,202,201,200,199,198,197,196,195,194,193,192,191,190,189,188,187,186,185,184,183,182,181,180,179,178,177,176,175,174,173,172,171,170,169,168,167,166,165,164,163,162,161,160,159,158,157,156,155,154,153,152,151,150,149,148,147,146,145,144,143,142,141,140,139,138,137,136,135,134,133,132,131,130,129,128,127,126,125,124,123,122,121,120,119,118,117,116,115,114,113,112,111,110,109,108,107,106,105,104,103,102,101,100,99,98,97,96,95,94,93,92,91,90,89,88,87,86,85,84,83,82,81,80,79,78,77,76,75,74,73,72,71,70,69,68,67,66,65,64,63,62,61,60,59,58,57,56,55,54,53,52,51,50,49,48,47,46,45,44,43,42,41,40,39,38,37,36,35,34,33,32,31,30,29,28,27,26,25,24,23,22,21,20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0]
    let previousValue = 0;
    let lm = String.fromCharCode(211);
    for (let i = 0; i < nums.length; i++) {
        let num1 = previousValue * nums[i];
        previousValue = (num1+previousValue+lm.charCodeAt(0)) % 256
        let tmp = nums[i];
        nums[i] = nums[previousValue]
        nums[previousValue] = tmp
    }
    return nums;
}

function get_arr29(dateTime1,dateTime2,params,data,userAgent) {
    let parArr = get_arr(get_arr(params))
    let dataArr = get_arr(get_arr(data))
    let ua_salt;
    switch (userAgent.indexOf('Win')) {
        case -1:
            ua_salt = 0;
            break;
        default:
            ua_salt = 0;
    }
    var browser_arr = get_arr(encryptionUa(uaGarbledCharacters(userAgent,ua_salt)));
    let arr = []
    let arr2 = []
    let num = get_arr2(userAgent)
    let dateTime3 = (parseFloat(Date.now()) - 1721836800000) / 1000 / 60 / 60 / 24 / 14 >> 0
    let arr0 = randomGarbledCharactersArrayList();
    arr[0] = 41;
    arr[1] = dateTime3;
    arr[2] = 5
    arr[3] = (parseFloat(dateTime1) - parseFloat(dateTime2)) + 3 & 255;
    arr[4] = dateTime1 >> 0 & 255;
    arr[5] = dateTime1 >> 8 & 255;
    arr[6] = dateTime1 >> 16 & 255;
    arr[7] = dateTime1 >> 24 & 255;
    arr[8] = dateTime1/256/256/256/256 & 255;
    arr[9] = dateTime1/256/256/256/256/256 & 255;
    arr[10] = 1 % 256 & 255;
    arr[11] = 1 / 256 & 255;
    arr[12] = 1 & 255;
    arr[13] = 1 >> 8 & 255;
    // arr[14] = 602 % 401 % 256 & 255;
    arr[14] = 1;
    arr[15] = 0 % 101 % 256 & 255;
    arr[16] = 0 % 201 % 256 & 255;
    arr[17] = 0 % 101 % 256 & 255;
    arr[18] = ua_salt & 255;
    arr[19] = ua_salt >> 8 & 255;
    arr[20] = ua_salt >> 16 & 255;
    arr[21] = ua_salt >> 24 & 255;
    arr[22] = parArr[9];
    arr[23] = parArr[18];
    arr[24] = 3;
    arr[25] = parArr[3];;
    arr[26] = dataArr[10];
    arr[27] = dataArr[19];
    arr[28] = 4;
    arr[29] = dataArr[4];
    arr[30] = browser_arr[11];
    arr[31] = browser_arr[21];
    arr[32] = 5;
    arr[33] = browser_arr[5];
    arr[34] = dateTime2 >> 0 & 255;
    arr[35] = dateTime2 >> 8 & 255;
    arr[36] = dateTime2 >> 16 & 255;
    arr[37] = dateTime2 >> 24 & 255;
    arr[38] = dateTime2/256/256/256/256 & 255;
    arr[39] = dateTime2/256/256/256/256/256 & 255;
    arr[40] = 3;
    let arr32 = 6241;
    arr[41] = arr32 >> 0 & 255;
    arr[42] = arr32 >> 8 & 255;
    arr[43] = arr32 >> 16 & 255;
    arr[44] = arr32 >> 24 & 255;
    let arr36 = 6383;
    arr[45] = arr36 & 255;
    arr[46] = arr36 >> 8 & 255;
    arr[47] = arr36 >> 16 & 255;
    arr[48] = arr36 >> 24 & 255;
    let last_num_one= getLast_3Num(dateTime1)
    arr[49] = num.length
    arr[50] = num.length & 255
    arr[51] = num.length >> 8 & 255
    arr[52] = last_num_one.length
    arr[53] = last_num_one.length & 255
    arr[54] = last_num_one.length >> 8 & 255
    let last_num = getLastNum2(arr0,arr)

    arr2[0] = arr[9]
    arr2[1] = arr[18]
    arr2[2] = arr[30]
    arr2[3] = arr[35]
    arr2[4] = arr[47]
    arr2[5] = arr[4]
    arr2[6] = arr[44]
    arr2[7] = arr[19]
    arr2[8] = arr[10]
    arr2[9] = arr[23]
    arr2[10] = arr[12]
    arr2[11] = arr[40];
    arr2[12] = arr[25];
    arr2[13] = arr[42];
    arr2[14] = arr[3];
    arr2[15] = arr[22];
    arr2[16] = arr[38];
    arr2[17] = arr[21];
    arr2[18] = arr[5];
    arr2[19] = arr[45];
    arr2[20] = arr[1];
    arr2[21] = arr[29];
    arr2[22] = arr[6];
    arr2[23] = arr[43];
    arr2[24] = arr[33];
    arr2[25] = arr[14];
    arr2[26] = arr[36];
    arr2[27] = arr[37];
    arr2[28] = arr[2];
    arr2[29] = arr[46];
    arr2[30] = arr[15];
    arr2[31] = arr[48];
    arr2[32] = arr[31];
    arr2[33] = arr[26];
    arr2[34] = arr[16];
    arr2[35] = arr[13];
    arr2[36] = arr[8];
    arr2[37] = arr[41];
    arr2[38] = arr[27];
    arr2[39] = arr[17];
    arr2[40] = arr[39]
    arr2[41] = arr[20]
    arr2[42] = arr[11]
    arr2[43] = arr[0]
    arr2[44] = arr[34]
    arr2[45] = arr[7]
    arr2[46] = arr[50]
    arr2[47] = arr[51]
    arr2[48] = arr[53]
    arr2[49] = arr[54]

    let newArr = [...arr2,...num]
    let newArr2 = [...newArr,...last_num_one]
    newArr2.push(last_num)
    return getNumList(arr0,newArr2);
}

function getLast_3Num(dateTime1){
    let intStr = parseFloat(dateTime1)
    intStr += 3
    let timestamp1 = (intStr& 255) + ","
    let num = []
    for (let i = 0; i < timestamp1.length; i++) {
        num.push(timestamp1.charCodeAt(i))
    }
    return num;
}

function get_arr2(userAgent){
    let data = '';
    switch (userAgent.indexOf('Win')) {
        case -1:
            // data = '2056|390|2056|1202|0|44|0|0|2056|1203|2056|1329|2056|2815|30|30|MacIntel';
            data = '2056|1080|2056|1201|2056|1201|2056|1329|MacIntel';
            break;
        default:
            data = '2056|1080|2056|1201|2056|1201|2056|1329|Win32';
    }
    // let data = '2056|1087|2056|1208|0|44|0|0|2056|1209|2056|1329|2056|1087|30|30|MacIntel'
    let sum = []
    for (let i = 0; i < data.length; i++) {
        sum.push(data.charCodeAt(i))
    }
    return sum
}
function getLastNum2(arr1,arr){
    const xorResult = arr1[0]^arr1[1]^arr1[2]^arr1[3]^arr1[4]^arr1[5]^arr1[6]^arr1[7]^arr[0] ^arr[1]^arr[2] ^arr[3]^arr[4]^arr[5]^arr[6]^arr[7]^arr[8]^arr[9]^arr[10]^arr[11]^arr[12]^arr[13]^arr[14]^arr[15]^arr[16]^arr[17]^arr[18]^arr[19]^arr[20]^arr[21]^arr[22]^arr[23]^arr[25]^arr[26]^arr[27]^arr[29]^arr[30]^arr[31]^arr[33]^arr[34]^arr[35]^arr[36]^arr[37]^arr[38]^arr[39]^arr[40]^arr[41]^arr[42]^arr[43]^arr[44]^arr[45]^arr[46]^arr[47]^arr[48]^arr[50]^arr[51]^arr[53]^arr[54]
    return xorResult
}

function getNumList(arr0,arrAr){
    let numList = []
    // 传入 102 位数组
    for (let i = 0; i < arrAr.length; i+=3) {
        if (i + 2 >= arrAr.length) {
            if (i + 1 >= arrAr.length){
                let num1 = arrAr[i]
                numList.push(num1)
            } else {
                let num1 = arrAr[i]
                let num2 = arrAr[i+1]
                numList.push(num1)
                numList.push(num2)
            }
        } else {
            let random = Math.random() * 1000 & 255
            let num1 =  (random & 145) | (arrAr[i] & 110)
            let num2 =  (random & 66) | (arrAr[i+1] & 189)
            let num3 = (random & 44) | (arrAr[i+2] & 211)
            let num4 = ((arrAr[i]  & 145) | (arrAr[i+1] & 66)) | (arrAr[i+2] & 44)
            numList.push(num1)
            numList.push(num2)
            numList.push(num3)
            numList.push(num4)
        }

    }
    return  [...arr0,...numList];
}

function topHeaderRandomGarbledCharacters() {
    let arr = []
    let random = Math.random() * 65535
    // let num1 = random & 255
    let num1 = random & 255
    let num2 = Math.random() * 40 >> 0
    arr.push((num1 & 170) | (3 & 85))
    arr.push((num1 & 85) | (3 & 170))
    arr.push((num2 & 170) | (82 & 85))
    arr.push((num2 & 85) | (82 & 170))
    return String.fromCharCode.apply(null,arr);
}

function randomGarbledCharactersArrayList() {
     function randomGarbledCharactersArray1() {
        let arr = []
        random = Math.random() * 65535
        num1 = random & 255
        num2 = random >> 8 & 255
        arr.push((num1 & 170) | (1 & 85))
        arr.push((num1 & 85) | (1 & 170))
        arr.push((num2 & 170) | (0 & 85))
        arr.push((num2 & 85) | (0 & 170))
        return arr;
    }

    function randomGarbledCharactersArray2() {
        let arr = []
        let num1 = Math.random() * 240 >> 0
        let num2 = (Math.random() * 255 >> 0) & 77 | 2 | 16 | 32 | 128
        arr.push((num1 & 170) | (1 & 85))
        arr.push((num1 & 85) | (1 & 170))
        arr.push((num2 & 170) | (0 & 85))
        arr.push((num2 & 85) | (0 & 170))
        return arr;
    }
    return [...randomGarbledCharactersArray1(),...randomGarbledCharactersArray2()]
}

function encryptionUa(ss) {
    let str = "ckdp1h4ZKsUB80/Mfvw36XIgR25+WQAlEi7NLboqYTOPuzmFjJnryx9HVGDaStCe";
    let uaEncryption = "";
    let j = 0
    for (let i = 0; i < ss.length; i+=3) {
        if (i + 3 <= ss.length) {
            let number = (((ss.charCodeAt(i) & 255) << 16) | ((ss.charCodeAt(i+1) & 255) << 8)) | ((ss.charCodeAt(i+2) & 255) << 0);
            uaEncryption += str.charAt((number & 16515072) >> 18);
            uaEncryption += str.charAt((number & 258048) >> 12);
            uaEncryption += str.charAt((number & 4032) >> 6);
            uaEncryption += str.charAt((number & 63) >> 0);
        }
        if (i + 3 > ss.length){
            let u = ss.length - j
            if (u === 2){
                var charCodeAtNum0 = ss.charCodeAt(j);
                var charCodeAtNum1 = ss.charCodeAt(j + 1);
                var baseNum = charCodeAtNum1 << 8 | charCodeAtNum0 << 16;
                var str1 = str[(baseNum & 16515072) >> 18];
                var str2 = str[(baseNum & 258048) >> 12];
                var str3 = str[(baseNum & 4032) >> 6];
                uaEncryption += str1 + str2 + str3 + '=';
            }
            if (u === 1){
                var charCodeAtNum0 = ss.charCodeAt(j);
                var baseNum = 0 | charCodeAtNum0 << 16;
                var str1 = str[(baseNum & 16515072) >> 18];
                var str2 = str[(baseNum & 258048) >> 12];
                uaEncryption += str1 + str2 + '=' + '=';
            }

        }
        j +=3
    }
    return uaEncryption
}

function uaGarbledCharacters(userAgent,ua_salt) {
    let arr_256 = ua_arr_256(userAgent,ua_salt);
    let n4 = 0;
    let ans = "";
    for (let i = 0; i < userAgent.length; i++) {
        let n2 = (i + 1) % 256;
        let n3 = n4 + arr_256[n2]
        n4 = n3 % 256
        let old_arr_n2 = arr_256[n2]
        arr_256[n2] = arr_256[n4]
        arr_256[n4] = old_arr_n2
        let n5 = userAgent.charCodeAt(i);
        let n6 = arr_256[n2] + old_arr_n2;
        let n7 = n6 % 256
        let n8 = n5 ^ arr_256[n7]
        ans += String.fromCharCode(n8)
    }
    return ans;
}


function ua_arr_256(userAgent,ua_salt) {
    let nums = [255,254,253,252,251,250,249,248,247,246,245,244,243,242,241,240,239,238,237,236,235,234,233,232,231,230,229,228,227,226,225,224,223,222,221,220,219,218,217,216,215,214,213,212,211,210,209,208,207,206,205,204,203,202,201,200,199,198,197,196,195,194,193,192,191,190,189,188,187,186,185,184,183,182,181,180,179,178,177,176,175,174,173,172,171,170,169,168,167,166,165,164,163,162,161,160,159,158,157,156,155,154,153,152,151,150,149,148,147,146,145,144,143,142,141,140,139,138,137,136,135,134,133,132,131,130,129,128,127,126,125,124,123,122,121,120,119,118,117,116,115,114,113,112,111,110,109,108,107,106,105,104,103,102,101,100,99,98,97,96,95,94,93,92,91,90,89,88,87,86,85,84,83,82,81,80,79,78,77,76,75,74,73,72,71,70,69,68,67,66,65,64,63,62,61,60,59,58,57,56,55,54,53,52,51,50,49,48,47,46,45,44,43,42,41,40,39,38,37,36,35,34,33,32,31,30,29,28,27,26,25,24,23,22,21,20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0]
    let previousValue = 0;
    let lm = String.fromCharCode(0.00390625,1,ua_salt);
    for (let i = 0; i < nums.length; i++) {
        let num1 = previousValue * nums[i];
        previousValue = (num1+previousValue+lm.charCodeAt(i % 3)) % 256
        let tmp = nums[i];
        nums[i] = nums[previousValue]
        nums[previousValue] = tmp
    }
    return nums;
}

// url = "is_h5=1&origin_type=638301&pc_client_type=1&pc_libra_divert=Mac&update_version_code=170400&version_code=&version_name=&cookie_enabled=true&screen_width=2056&screen_height=1329&browser_language=zh-CN&browser_platform=MacIntel&browser_name=Edge&browser_version=129.0.0.0&browser_online=true&engine_name=Blink&engine_version=129.0.0.0&os_name=Mac+OS&os_version=10.15.7&cpu_core_num=10&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=50&webid=7405403544101193253&msToken=rEpEllX6eVlseu50ClnxP9NbX-q7bb6sYNheTM1Dgyd4Xk5xsIIoJjNxl_d9BWHSlfeeHI2Rpxrrb2qv4hAU3ShEWnoek6d-ySl9SbIk8DQ4awPOGfdbeqFC9YEVlxykbeo9pGrJ0vkMshUQszxoITJeO1lpv8CzFYpfIa5-Aqh5tzL9p8cuY5DM"
// data = 'bff_type=2&is_h5=1&origin_type=638301&promotion_id=3704239957154652788'
// userAgent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
// console.log(getABogus(url, data, userAgent))

if (require.main === module) {
    try {
        // 从命令行参数中解析输入
        const userAgent = process.argv[3];
        const url = process.argv[4];
        const data = process.argv[5] || ''; // 默认值为空字符串
        const result = getABogus(userAgent, url, data);
        console.log(result); // 输出
    } catch (error) {
        console.error("Error parsing arguments:", error.message);
        process.exit(1);
    }
}
