const CryptoJS = require('crypto-js');
var wp;
window = global;

var _ts = Date.now(),
    _fp = '1733260139752348',
    _appId = '586ae',
    _token = "tk03wb3c91c5518nXSL2egI9QuTKOLXLWBjx5lwKOpslUAXudyJSt0AmNRFyy4si5VCp4NpZB8wclFWOpK07zoso0J6C",
    _version = '3.1',
    _unknown = '24c9ee85e67cf80746dd82817ecbeafc7a829b35c7f446a4c7d476cc9faa1d8834a93323ad7bce9bef1bba682b93d2e355076cc27b11bb228be53f32ed20565266eae147141141e0d154463e1733333213609f805a4de2ddf29a06541f6bb9892b80989b96d4724a0aaba834467cab40debef3f59396c2874c1a5d3ee361ffc6'

var _td = ts2format(_ts)

!function (o) {
    "use strict";
    var e, n, t, a = {};

    function r(e) {
        var n = a[e];
        if (void 0 !== n)
            return n.exports;
        var t = a[e] = {
            id: e,
            loaded: !1,
            exports: {}
        };
        // console.log(e)
        return o[e].call(t.exports, t, t.exports, r),
            t.loaded = !0,
            t.exports
    }

    r.m = o,
        e = [],
        r.O = function (n, t, o, a) {
            if (!t) {
                var c = 1 / 0;
                for (u = 0; u < e.length; u++) {
                    t = e[u][0],
                        o = e[u][1],
                        a = e[u][2];
                    for (var i = !0, f = 0; f < t.length; f++)
                        (!1 & a || c >= a) && Object.keys(r.O).every((function (e) {
                                return r.O[e](t[f])
                            }
                        )) ? t.splice(f--, 1) : (i = !1,
                        a < c && (c = a));
                    if (i) {
                        e.splice(u--, 1);
                        var d = o();
                        void 0 !== d && (n = d)
                    }
                }
                return n
            }
            a = a || 0;
            for (var u = e.length; u > 0 && e[u - 1][2] > a; u--)
                e[u] = e[u - 1];
            e[u] = [t, o, a]
        }
        ,
        r.n = function (e) {
            var n = e && e.__esModule ? function () {
                    return e.default
                }
                : function () {
                    return e
                }
            ;
            return r.d(n, {
                a: n
            }),
                n
        }
        ,
        r.d = function (e, n) {
            for (var t in n)
                r.o(n, t) && !r.o(e, t) && Object.defineProperty(e, t, {
                    enumerable: !0,
                    get: n[t]
                })
        }
        ,
        r.f = {},
        r.e = function (e) {
            return Promise.all(Object.keys(r.f).reduce((function (n, t) {
                    return r.f[t](e, n),
                        n
                }
            ), []))
        }
        ,
        r.u = function (e) {
            return {
                34: "biservicefee",
                81: "promotion",
                378: "user",
                410: "marketActivities",
                621: "entire",
                685: "lineReport",
                869: "createShop",
                917: "agreement",
                929: "common-731babaf",
                973: "common-43dd7041",
                1131: "appMng",
                1276: "shopActPromotion",
                1288: "myApi",
                1621: "investmentEffect",
                1666: "planDetails",
                1806: "officalPromotion",
                1884: "taskDetail",
                1913: "jdauthentication",
                1970: "newWithdraw",
                1992: "cashDetail",
                2337: "withdraw",
                2412: "socialMediaMng",
                2479: "marketingCalendar",
                2481: "realTimeScreen",
                2527: "withdrawRecord",
                2690: "couponList",
                2795: "cashGiftCreate",
                2832: "taskSquare",
                2951: "RewardActivity",
                2970: "articlePromotion",
                2992: "myTask",
                3012: "subCommission",
                3386: "cashGiftDeposit",
                3513: "trafficMediaMng",
                3583: "webExtension",
                3712: "openplatform-9a53bcac",
                3756: "shopPromotion",
                3761: "openplatform-9a6b8f1e",
                3765: "skuAnalyse",
                3779: "active",
                3888: "external",
                3940: "cashCoupon",
                4163: "InterfaceManagement",
                4256: "channel",
                4565: "common-d91a9049",
                4738: "cpcMedia",
                4843: "openplatform-d91a9049",
                4962: "common-8912b8e4",
                5001: "groupList",
                5075: "planList",
                5142: "reverseInvestment",
                5177: "home",
                5313: "myStarEnlist2",
                5413: "recommendMng",
                5512: "accounting",
                5549: "jingPlanMng",
                5724: "common-69b0bd4f",
                5769: "appMedia",
                5847: "socialMediaExtension",
                5863: "projectDetail",
                6026: "InvestmentData",
                6103: "common-b4fa4e1a",
                6419: "batchMng",
                6596: "404",
                6653: "DataPromotion",
                6659: "common-4720890c",
                6682: "appExtension",
                6810: "common-c7713fe4",
                7012: "shopPromotionDetail",
                7066: "secretOrder",
                7253: "shopAnalyse",
                7468: "openOrder",
                7815: "chatExtension",
                7899: "custompromotion",
                7991: "webMng",
                8022: "cashGiftDepositResult",
                8273: "actAnalyse",
                8277: "cashGift",
                8300: "msg",
                8429: "helpcenter",
                8442: "moreProductList",
                8608: "channelPromotion",
                8722: "common-fb051ecb",
                8924: "initRevGroup",
                8983: "report",
                8989: "common-a07e9f05",
                9206: "trafficMediaExtension",
                9223: "initiate",
                9557: "couponPromotion",
                9621: "myInvoice",
                9664: "taskEffectData",
                9704: "batchDetail",
                9734: "myShop",
                9830: "darenBank",
                9847: "userTask",
                9851: "common-c0d952d5",
                9920: "operate",
                9940: "promotionSite",
                9974: "myStarEnlist"
            }[e] + "." + {
                34: "884dabbf",
                81: "516fbf65",
                378: "4fa7f455",
                410: "f3b3ce65",
                621: "779cbc2d",
                685: "635b41c3",
                869: "6e91e04e",
                917: "8931b075",
                929: "3c7249c4",
                973: "dd604fd9",
                1131: "5c758086",
                1276: "4afef4b0",
                1288: "efd9ca56",
                1621: "dd68ef97",
                1666: "15ddc024",
                1806: "2ce9aabc",
                1884: "26a69c37",
                1913: "7cf33bc8",
                1970: "2f4e7bbb",
                1992: "ede710f5",
                2337: "ed174f32",
                2412: "35ff0de8",
                2479: "a21c8c42",
                2481: "6fed6857",
                2527: "6a37ef3c",
                2690: "64ddf7cc",
                2795: "a674eb69",
                2832: "feecd3be",
                2951: "93b3e34d",
                2970: "0384070e",
                2992: "be5042ce",
                3012: "2347219c",
                3386: "1a1f7d84",
                3513: "c04a31fc",
                3583: "f5d3ef48",
                3712: "e2f73577",
                3756: "7a6444be",
                3761: "53e3439b",
                3765: "a4ec0efd",
                3779: "38223816",
                3888: "fce9007a",
                3940: "6e0a2517",
                4163: "f5764a34",
                4256: "d71746f3",
                4565: "38532a63",
                4738: "d5a92ea5",
                4843: "ac578919",
                4962: "46dd7b93",
                5001: "6ffabe1f",
                5075: "bf8fe0b0",
                5142: "f02f701e",
                5177: "95d0d33a",
                5313: "81217ce7",
                5413: "c7fd2e9a",
                5512: "9f7c1dc7",
                5549: "b90e6eb0",
                5724: "fae8a443",
                5769: "3026d89e",
                5847: "88f445a5",
                5863: "26a850a1",
                6026: "d554b6c8",
                6103: "9a594517",
                6419: "8a5d5b4f",
                6596: "43477835",
                6653: "e904d280",
                6659: "c79c71eb",
                6682: "9a980d14",
                6810: "767f177d",
                7012: "310763bf",
                7066: "0930edea",
                7253: "093b1d51",
                7468: "abc74f1b",
                7815: "7176c4b5",
                7899: "e3745e3e",
                7991: "bf2e88d9",
                8022: "0b3b8d2b",
                8273: "7597ef4f",
                8277: "4abc271d",
                8300: "386bd6f1",
                8429: "0a43b716",
                8442: "866be077",
                8608: "ce7516bf",
                8722: "d3db8be6",
                8924: "e678bf90",
                8983: "0eb1ef70",
                8989: "ba78e6ab",
                9206: "178b940f",
                9223: "bfda0e2b",
                9557: "a25c4ce7",
                9621: "56164042",
                9664: "fa4795b0",
                9704: "5721dc0a",
                9734: "74dcc744",
                9830: "de870bad",
                9847: "2b8f9834",
                9851: "cf04e91b",
                9920: "f2cde753",
                9940: "eb35820c",
                9974: "a83b6246"
            }[e] + ".js"
        }
        ,
        r.g = function () {
            if ("object" == typeof globalThis)
                return globalThis;
            try {
                return this || new Function("return this")()
            } catch (e) {
                if ("object" == typeof window)
                    return window
            }
        }(),
        r.o = function (e, n) {
            return Object.prototype.hasOwnProperty.call(e, n)
        }
        ,
        n = {},
        t = "JDUnion:",
        r.l = function (e, o, a, c) {
            if (n[e])
                n[e].push(o);
            else {
                var i, f;
                if (void 0 !== a)
                    for (var d = document.getElementsByTagName("script"), u = 0; u < d.length; u++) {
                        var b = d[u];
                        if (b.getAttribute("src") == e || b.getAttribute("data-webpack") == t + a) {
                            i = b;
                            break
                        }
                    }
                i || (f = !0,
                    (i = document.createElement("script")).charset = "utf-8",
                    i.timeout = 120,
                r.nc && i.setAttribute("nonce", r.nc),
                    i.setAttribute("data-webpack", t + a),
                    i.src = e),
                    n[e] = [o];
                var s = function (t, o) {
                    i.onerror = i.onload = null,
                        clearTimeout(l);
                    var a = n[e];
                    if (delete n[e],
                    i.parentNode && i.parentNode.removeChild(i),
                    a && a.forEach((function (e) {
                            return e(o)
                        }
                    )),
                        t)
                        return t(o)
                }
                    , l = setTimeout(s.bind(null, void 0, {
                    type: "timeout",
                    target: i
                }), 12e4);
                i.onerror = s.bind(null, i.onerror),
                    i.onload = s.bind(null, i.onload),
                f && document.head.appendChild(i)
            }
        }
        ,
        r.r = function (e) {
            "undefined" != typeof Symbol && Symbol.toStringTag && Object.defineProperty(e, Symbol.toStringTag, {
                value: "Module"
            }),
                Object.defineProperty(e, "__esModule", {
                    value: !0
                })
        }
        ,
        r.nmd = function (e) {
            return e.paths = [],
            e.children || (e.children = []),
                e
        }
        ,
        r.p = "//storage.360buyimg.com/pubfree-bucket/unionpc/b7e5298d5/",
        function () {
            var e = {
                6700: 0
            };
            r.f.j = function (n, t) {
                var o = r.o(e, n) ? e[n] : void 0;
                if (0 !== o)
                    if (o)
                        t.push(o[2]);
                    else if (6700 != n) {
                        var a = new Promise((function (t, a) {
                                o = e[n] = [t, a]
                            }
                        ));
                        t.push(o[2] = a);
                        var c = r.p + r.u(n)
                            , i = new Error;
                        r.l(c, (function (t) {
                                if (r.o(e, n) && (0 !== (o = e[n]) && (e[n] = void 0),
                                    o)) {
                                    var a = t && ("load" === t.type ? "missing" : t.type)
                                        , c = t && t.target && t.target.src;
                                    i.message = "Loading chunk " + n + " failed.\n(" + a + ": " + c + ")",
                                        i.name = "ChunkLoadError",
                                        i.type = a,
                                        i.request = c,
                                        o[1](i)
                                }
                            }
                        ), "chunk-" + n, n)
                    } else
                        e[n] = 0
            }
                ,
                r.O.j = function (n) {
                    return 0 === e[n]
                }
            ;
            var n = function (n, t) {
                var o, a, c = t[0], i = t[1], f = t[2], d = 0;
                if (c.some((function (n) {
                        return 0 !== e[n]
                    }
                ))) {
                    for (o in i)
                        r.o(i, o) && (r.m[o] = i[o]);
                    if (f)
                        var u = f(r)
                }
                for (n && n(t); d < c.length; d++)
                    a = c[d],
                    r.o(e, a) && e[a] && e[a][0](),
                        e[a] = 0;
                return r.O(u)
            }
                , t = window.webpackChunkJDUnion = window.webpackChunkJDUnion || [];
            t.forEach(n.bind(null, 0)),
                t.push = n.bind(null, t.push.bind(t))
        }(),
        r.nc = void 0
    wp = r
}({
    78249: function (t, n, e) {
        var i;
        t.exports = (i = i || function (t, n) {
            var i;
            if ("undefined" != typeof window && window.crypto && (i = window.crypto),
            "undefined" != typeof self && self.crypto && (i = self.crypto),
            "undefined" != typeof globalThis && globalThis.crypto && (i = globalThis.crypto),
            !i && "undefined" != typeof window && window.msCrypto && (i = window.msCrypto),
            !i && void 0 !== e.g && e.g.crypto && (i = e.g.crypto),
                !i)
                try {
                    i = e(42480)
                } catch (t) {
                }
            var r = function () {
                if (i) {
                    if ("function" == typeof i.getRandomValues)
                        try {
                            return i.getRandomValues(new Uint32Array(1))[0]
                        } catch (t) {
                        }
                    if ("function" == typeof i.randomBytes)
                        try {
                            return i.randomBytes(4).readInt32LE()
                        } catch (t) {
                        }
                }
                throw new Error("Native crypto module could not be used to get secure random number.")
            }
                , s = Object.create || function () {
                function t() {
                }

                return function (n) {
                    var e;
                    return t.prototype = n,
                        e = new t,
                        t.prototype = null,
                        e
                }
            }()
                , o = {}
                , u = o.lib = {}
                , f = u.Base = {
                extend: function (t) {
                    var n = s(this);
                    return t && n.mixIn(t),
                    n.hasOwnProperty("init") && this.init !== n.init || (n.init = function () {
                            n.$super.init.apply(this, arguments)
                        }
                    ),
                        n.init.prototype = n,
                        n.$super = this,
                        n
                },
                create: function () {
                    var t = this.extend();
                    return t.init.apply(t, arguments),
                        t
                },
                init: function () {
                },
                mixIn: function (t) {
                    for (var n in t)
                        t.hasOwnProperty(n) && (this[n] = t[n]);
                    t.hasOwnProperty("toString") && (this.toString = t.toString)
                },
                clone: function () {
                    return this.init.prototype.extend(this)
                }
            }
                , h = u.WordArray = f.extend({
                init: function (t, n) {
                    t = this.words = t || [],
                        this.sigBytes = null != n ? n : 4 * t.length
                },
                toString: function (t) {
                    return (t || l).stringify(this)
                },
                concat: function (t) {
                    var n = this.words
                        , e = t.words
                        , i = this.sigBytes
                        , r = t.sigBytes;
                    if (this.clamp(),
                    i % 4)
                        for (var s = 0; s < r; s++) {
                            var o = e[s >>> 2] >>> 24 - s % 4 * 8 & 255;
                            n[i + s >>> 2] |= o << 24 - (i + s) % 4 * 8
                        }
                    else
                        for (var u = 0; u < r; u += 4)
                            n[i + u >>> 2] = e[u >>> 2];
                    return this.sigBytes += r,
                        this
                },
                clamp: function () {
                    var n = this.words
                        , e = this.sigBytes;
                    n[e >>> 2] &= 4294967295 << 32 - e % 4 * 8,
                        n.length = t.ceil(e / 4)
                },
                clone: function () {
                    var t = f.clone.call(this);
                    return t.words = this.words.slice(0),
                        t
                },
                random: function (t) {
                    for (var n = [], e = 0; e < t; e += 4)
                        n.push(r());
                    return new h.init(n, t)
                }
            })
                , c = o.enc = {}
                , l = c.Hex = {
                stringify: function (t) {
                    for (var n = t.words, e = t.sigBytes, i = [], r = 0; r < e; r++) {
                        var s = n[r >>> 2] >>> 24 - r % 4 * 8 & 255;
                        i.push((s >>> 4).toString(16)),
                            i.push((15 & s).toString(16))
                    }
                    return i.join("")
                },
                parse: function (t) {
                    for (var n = t.length, e = [], i = 0; i < n; i += 2)
                        e[i >>> 3] |= parseInt(t.substr(i, 2), 16) << 24 - i % 8 * 4;
                    return new h.init(e, n / 2)
                }
            }
                , a = c.Latin1 = {
                stringify: function (t) {
                    for (var n = t.words, e = t.sigBytes, i = [], r = 0; r < e; r++) {
                        var s = n[r >>> 2] >>> 24 - r % 4 * 8 & 255;
                        i.push(String.fromCharCode(s))
                    }
                    return i.join("")
                },
                parse: function (t) {
                    for (var n = t.length, e = [], i = 0; i < n; i++)
                        e[i >>> 2] |= (255 & t.charCodeAt(i)) << 24 - i % 4 * 8;
                    return new h.init(e, n)
                }
            }
                , d = c.Utf8 = {
                stringify: function (t) {
                    try {
                        return decodeURIComponent(escape(a.stringify(t)))
                    } catch (t) {
                        throw new Error("Malformed UTF-8 data")
                    }
                },
                parse: function (t) {
                    return a.parse(unescape(encodeURIComponent(t)))
                }
            }
                , p = u.BufferedBlockAlgorithm = f.extend({
                reset: function () {
                    this._data = new h.init,
                        this._nDataBytes = 0
                },
                _append: function (t) {
                    "string" == typeof t && (t = d.parse(t)),
                        this._data.concat(t),
                        this._nDataBytes += t.sigBytes
                },
                _process: function (n) {
                    var e, i = this._data, r = i.words, s = i.sigBytes, o = this.blockSize, u = s / (4 * o),
                        f = (u = n ? t.ceil(u) : t.max((0 | u) - this._minBufferSize, 0)) * o, c = t.min(4 * f, s);
                    if (f) {
                        for (var l = 0; l < f; l += o)
                            this._doProcessBlock(r, l);
                        e = r.splice(0, f),
                            i.sigBytes -= c
                    }
                    return new h.init(e, c)
                },
                clone: function () {
                    var t = f.clone.call(this);
                    return t._data = this._data.clone(),
                        t
                },
                _minBufferSize: 0
            })
                , g = (u.Hasher = p.extend({
                cfg: f.extend(),
                init: function (t) {
                    this.cfg = this.cfg.extend(t),
                        this.reset()
                },
                reset: function () {
                    p.reset.call(this),
                        this._doReset()
                },
                update: function (t) {
                    return this._append(t),
                        this._process(),
                        this
                },
                finalize: function (t) {
                    return t && this._append(t),
                        this._doFinalize()
                },
                blockSize: 16,
                _createHelper: function (t) {
                    return function (n, e) {
                        return new t.init(e).finalize(n)
                    }
                },
                _createHmacHelper: function (t) {
                    return function (n, e) {
                        return new g.HMAC.init(t, e).finalize(n)
                    }
                }
            }),
                o.algo = {});
            return o
        }(Math),
            i)
    },
    52153: function (t, n, e) {
        var i;
        t.exports = (i = e(78249),
            function (t) {
                var n = i
                    , e = n.lib
                    , r = e.WordArray
                    , s = e.Hasher
                    , o = n.algo
                    , u = []
                    , f = [];
                !function () {
                    function n(n) {
                        for (var e = t.sqrt(n), i = 2; i <= e; i++)
                            if (!(n % i))
                                return !1;
                        return !0
                    }

                    function e(t) {
                        return 4294967296 * (t - (0 | t)) | 0
                    }

                    for (var i = 2, r = 0; r < 64;)
                        n(i) && (r < 8 && (u[r] = e(t.pow(i, .5))),
                            f[r] = e(t.pow(i, 1 / 3)),
                            r++),
                            i++
                }();
                var h = []
                    , c = o.SHA256 = s.extend({
                    _doReset: function () {
                        this._hash = new r.init(u.slice(0))
                    },
                    _doProcessBlock: function (t, n) {
                        for (var e = this._hash.words, i = e[0], r = e[1], s = e[2], o = e[3], u = e[4], c = e[5], l = e[6], a = e[7], d = 0; d < 64; d++) {
                            if (d < 16)
                                h[d] = 0 | t[n + d];
                            else {
                                var p = h[d - 15]
                                    , g = (p << 25 | p >>> 7) ^ (p << 14 | p >>> 18) ^ p >>> 3
                                    , m = h[d - 2]
                                    , y = (m << 15 | m >>> 17) ^ (m << 13 | m >>> 19) ^ m >>> 10;
                                h[d] = g + h[d - 7] + y + h[d - 16]
                            }
                            var v = i & r ^ i & s ^ r & s
                                , w = (i << 30 | i >>> 2) ^ (i << 19 | i >>> 13) ^ (i << 10 | i >>> 22)
                                ,
                                $ = a + ((u << 26 | u >>> 6) ^ (u << 21 | u >>> 11) ^ (u << 7 | u >>> 25)) + (u & c ^ ~u & l) + f[d] + h[d];
                            a = l,
                                l = c,
                                c = u,
                                u = o + $ | 0,
                                o = s,
                                s = r,
                                r = i,
                                i = $ + (w + v) | 0
                        }
                        e[0] = e[0] + i | 0,
                            e[1] = e[1] + r | 0,
                            e[2] = e[2] + s | 0,
                            e[3] = e[3] + o | 0,
                            e[4] = e[4] + u | 0,
                            e[5] = e[5] + c | 0,
                            e[6] = e[6] + l | 0,
                            e[7] = e[7] + a | 0
                    },
                    _doFinalize: function () {
                        var n = this._data
                            , e = n.words
                            , i = 8 * this._nDataBytes
                            , r = 8 * n.sigBytes;
                        return e[r >>> 5] |= 128 << 24 - r % 32,
                            e[14 + (r + 64 >>> 9 << 4)] = t.floor(i / 4294967296),
                            e[15 + (r + 64 >>> 9 << 4)] = i,
                            n.sigBytes = 4 * e.length,
                            this._process(),
                            this._hash
                    },
                    clone: function () {
                        var t = s.clone.call(this);
                        return t._hash = this._hash.clone(),
                            t
                    }
                });
                n.SHA256 = s._createHelper(c),
                    n.HmacSHA256 = s._createHmacHelper(c)
            }(Math),
            i.SHA256)
    },
});

function ts2format(ts) {
    const date = new Date(ts);
    const y = date.getFullYear(),
        m = String(date.getMonth() + 1).padStart(2, '0'),
        d = String(date.getDate()).padStart(2, '0'),
        h = String(date.getHours()).padStart(2, '0'),
        mi = String(date.getMinutes()).padStart(2, '0'),
        s = String(date.getSeconds()).padStart(2, '0'),
        ms = String(date.getMilliseconds()).padStart(3, '0')
    return `${y}${m}${d}${h}${mi}${s}${ms}`;
}

function body(obj) {
    const F = wp(52153),
        K = wp.n(F),
        args_str = JSON.stringify(obj)
    return K()(args_str).toString()
}

function secret_str() {
    var rd = '4LP439v0MSSD';
    var str = "".concat(_token).concat(_fp).concat(_td).concat(_appId).concat(rd);
    return CryptoJS.SHA256(str).toString(CryptoJS.enc.Hex);
}

function encrypt_data(r, i) {
    function convertToQueryString(data) {
        return data.map(item => `${item.key}:${item.value}`).join('&');
    }

    const c = convertToQueryString(i)
    return CryptoJS.HmacSHA256(c, r).toString(CryptoJS.enc.Hex)
}

function h5st(p) {
    const b = body(p)
    const jsonArray = [
        {
            "key": "appid",
            "value": "unionpc"
        },
        {
            "key": "body",
            "value": b
        },
        {
            "key": "functionId",
            "value": "unionSearch"
        }
    ]
    const secret = secret_str()
    const _encrypt = encrypt_data(secret, jsonArray)

    const dt = "".concat(_td),
        fp = "".concat(_fp),
        appId = "".concat(_appId),
        tk = "".concat(_token),
        encrypt = "".concat(_encrypt),
        version = "".concat(_version),
        ts = "".concat(_ts),
        unknown = "".concat(_unknown)
    return [dt, fp, appId, tk, encrypt, version, ts, unknown].join(";")
}


e = {
    "funName": "search",
    "version": "v3",
    "source": 20310,
    "param": {
        "pageNo": 2,
        "pageSize": 60,
        "searchUUID": "e7fb274ce31247e689982c7375d29f5e",
        "bonusIds": null,
        "category1": null,
        "category2": null,
        "category3": null,
        "deliveryType": null,
        "wlRate": null,
        "maxWlRate": null,
        "fromPrice": null,
        "toPrice": null,
        "hasCoupon": null,
        "isHot": null,
        "isNeedPreSale": null,
        "isPinGou": null,
        "isZY": null,
        "isCare": null,
        "lock": null,
        "orientationFlag": null,
        "sort": null,
        "sortName": null,
        "keyWord": "",
        "searchType": "st3",
        "keywordType": "kt0"
    },
    "clientPageId": "jingfen_pc"
}
hs = h5st(e)
console.log("h5st:", hs);