const crypto = require('crypto'); //引入crypto加密模块
// const crypto = require('crypto-js'); //引入crypto加密模块
function MD5 (text) {
    return crypto.createHash('md5').update(text).digest('hex');
}
var window = {};
var navigator = {}
var location = {
    "ancestorOrigins": {},
    "href": "https://h5api.m.taobao.com/h5/mtop.relationrecommend.wirelessrecommend.recommend/2.0/",
    "origin": "https://www.taobao.com",
    "protocol": "https:",
    "host": "www.taobao.com",
    "hostname": "www.taobao.com",
    "port": "",
    "pathname": "/explore/641ae24e0000000013036dd2",
    "search": "",
    "hash": ""
}
var document = {location:location}

function(e, n) {
    function r() {
        var e = {}
          , t = new v((function(t, n) {
            e.resolve = t,
            e.reject = n
        }
        ));
        return e.promise = t,
        e
    }
    function o(e, t) {
        for (var n in t)
            void 0 === e[n] && (e[n] = t[n]);
        return e
    }
    function i(e) {
        var t;
        (document.getElementsByTagName("head")[0] || document.getElementsByTagName("body")[0] || document.firstElementChild || document).appendChild(e)
    }
    function a(e) {
        var t = [];
        for (var n in e)
            e[n] && t.push(n + "=" + encodeURIComponent(e[n]));
        return t.join("&")
    }
    function s(e) {
        try {
            return ".com" !== e.substring(e.lastIndexOf(".")) ? (e.split(".") || []).length <= 3 ? e : e.split(".").slice(1).join(".") : e.substring(e.lastIndexOf(".", e.lastIndexOf(".") - 1) + 1)
        } catch (t) {
            return e.substring(e.lastIndexOf(".", e.lastIndexOf(".") - 1) + 1)
        }
    }
    function u(e) {
        function t(e, t) {
            return e << t | e >>> 32 - t
        }
        function n(e, t) {
            var n, r, o, i, a;
            return o = 2147483648 & e,
            i = 2147483648 & t,
            a = (1073741823 & e) + (1073741823 & t),
            (n = 1073741824 & e) & (r = 1073741824 & t) ? 2147483648 ^ a ^ o ^ i : n | r ? 1073741824 & a ? 3221225472 ^ a ^ o ^ i : 1073741824 ^ a ^ o ^ i : a ^ o ^ i
        }
        function r(e, t, n) {
            return e & t | ~e & n
        }
        function o(e, t, n) {
            return e & n | t & ~n
        }
        function i(e, t, n) {
            return e ^ t ^ n
        }
        function a(e, t, n) {
            return t ^ (e | ~n)
        }
        function s(e, o, i, a, s, u, l) {
            return e = n(e, n(n(r(o, i, a), s), l)),
            n(t(e, u), o)
        }
        function u(e, r, i, a, s, u, l) {
            return e = n(e, n(n(o(r, i, a), s), l)),
            n(t(e, u), r)
        }
        function l(e, r, o, a, s, u, l) {
            return e = n(e, n(n(i(r, o, a), s), l)),
            n(t(e, u), r)
        }
        function c(e, r, o, i, s, u, l) {
            return e = n(e, n(n(a(r, o, i), s), l)),
            n(t(e, u), r)
        }
        function f(e) {
            for (var t, n = e.length, r = n + 8, o, i = 16 * ((r - r % 64) / 64 + 1), a = new Array(i - 1), s = 0, u = 0; n > u; )
                s = u % 4 * 8,
                a[t = (u - u % 4) / 4] = a[t] | e.charCodeAt(u) << s,
                u++;
            return s = u % 4 * 8,
            a[t = (u - u % 4) / 4] = a[t] | 128 << s,
            a[i - 2] = n << 3,
            a[i - 1] = n >>> 29,
            a
        }
        function d(e) {
            var t, n, r = "", o = "";
            for (n = 0; 3 >= n; n++)
                r += (o = "0" + (t = e >>> 8 * n & 255).toString(16)).substr(o.length - 2, 2);
            return r
        }
        function p(e) {
            e = e.replace(/\r\n/g, "\n");
            for (var t = "", n = 0; n < e.length; n++) {
                var r = e.charCodeAt(n);
                128 > r ? t += String.fromCharCode(r) : r > 127 && 2048 > r ? (t += String.fromCharCode(r >> 6 | 192),
                t += String.fromCharCode(63 & r | 128)) : (t += String.fromCharCode(r >> 12 | 224),
                t += String.fromCharCode(r >> 6 & 63 | 128),
                t += String.fromCharCode(63 & r | 128))
            }
            return t
        }
        var h, m, y, v, g, A, b, _, w, M = [], S = 7, x = 12, k = 17, L = 22, E = 5, C = 9, T = 14, O = 20, Y = 4, D = 11, j = 16, P = 23, I = 6, B = 10, N = 15, R = 21, F;
        for (M = f(e = p(e)),
        A = 1732584193,
        b = 4023233417,
        _ = 2562383102,
        w = 271733878,
        h = 0; h < M.length; h += 16)
            m = A,
            y = b,
            v = _,
            g = w,
            A = s(A, b, _, w, M[h + 0], 7, 3614090360),
            w = s(w, A, b, _, M[h + 1], x, 3905402710),
            _ = s(_, w, A, b, M[h + 2], k, 606105819),
            b = s(b, _, w, A, M[h + 3], L, 3250441966),
            A = s(A, b, _, w, M[h + 4], 7, 4118548399),
            w = s(w, A, b, _, M[h + 5], x, 1200080426),
            _ = s(_, w, A, b, M[h + 6], k, 2821735955),
            b = s(b, _, w, A, M[h + 7], L, 4249261313),
            A = s(A, b, _, w, M[h + 8], 7, 1770035416),
            w = s(w, A, b, _, M[h + 9], x, 2336552879),
            _ = s(_, w, A, b, M[h + 10], k, 4294925233),
            b = s(b, _, w, A, M[h + 11], L, 2304563134),
            A = s(A, b, _, w, M[h + 12], 7, 1804603682),
            w = s(w, A, b, _, M[h + 13], x, 4254626195),
            _ = s(_, w, A, b, M[h + 14], k, 2792965006),
            A = u(A, b = s(b, _, w, A, M[h + 15], L, 1236535329), _, w, M[h + 1], 5, 4129170786),
            w = u(w, A, b, _, M[h + 6], 9, 3225465664),
            _ = u(_, w, A, b, M[h + 11], T, 643717713),
            b = u(b, _, w, A, M[h + 0], O, 3921069994),
            A = u(A, b, _, w, M[h + 5], 5, 3593408605),
            w = u(w, A, b, _, M[h + 10], 9, 38016083),
            _ = u(_, w, A, b, M[h + 15], T, 3634488961),
            b = u(b, _, w, A, M[h + 4], O, 3889429448),
            A = u(A, b, _, w, M[h + 9], 5, 568446438),
            w = u(w, A, b, _, M[h + 14], 9, 3275163606),
            _ = u(_, w, A, b, M[h + 3], T, 4107603335),
            b = u(b, _, w, A, M[h + 8], O, 1163531501),
            A = u(A, b, _, w, M[h + 13], 5, 2850285829),
            w = u(w, A, b, _, M[h + 2], 9, 4243563512),
            _ = u(_, w, A, b, M[h + 7], T, 1735328473),
            A = l(A, b = u(b, _, w, A, M[h + 12], O, 2368359562), _, w, M[h + 5], 4, 4294588738),
            w = l(w, A, b, _, M[h + 8], D, 2272392833),
            _ = l(_, w, A, b, M[h + 11], j, 1839030562),
            b = l(b, _, w, A, M[h + 14], P, 4259657740),
            A = l(A, b, _, w, M[h + 1], 4, 2763975236),
            w = l(w, A, b, _, M[h + 4], D, 1272893353),
            _ = l(_, w, A, b, M[h + 7], j, 4139469664),
            b = l(b, _, w, A, M[h + 10], P, 3200236656),
            A = l(A, b, _, w, M[h + 13], 4, 681279174),
            w = l(w, A, b, _, M[h + 0], D, 3936430074),
            _ = l(_, w, A, b, M[h + 3], j, 3572445317),
            b = l(b, _, w, A, M[h + 6], P, 76029189),
            A = l(A, b, _, w, M[h + 9], 4, 3654602809),
            w = l(w, A, b, _, M[h + 12], D, 3873151461),
            _ = l(_, w, A, b, M[h + 15], j, 530742520),
            A = c(A, b = l(b, _, w, A, M[h + 2], P, 3299628645), _, w, M[h + 0], 6, 4096336452),
            w = c(w, A, b, _, M[h + 7], B, 1126891415),
            _ = c(_, w, A, b, M[h + 14], N, 2878612391),
            b = c(b, _, w, A, M[h + 5], R, 4237533241),
            A = c(A, b, _, w, M[h + 12], 6, 1700485571),
            w = c(w, A, b, _, M[h + 3], B, 2399980690),
            _ = c(_, w, A, b, M[h + 10], N, 4293915773),
            b = c(b, _, w, A, M[h + 1], R, 2240044497),
            A = c(A, b, _, w, M[h + 8], 6, 1873313359),
            w = c(w, A, b, _, M[h + 15], B, 4264355552),
            _ = c(_, w, A, b, M[h + 6], N, 2734768916),
            b = c(b, _, w, A, M[h + 13], R, 1309151649),
            A = c(A, b, _, w, M[h + 4], 6, 4149444226),
            w = c(w, A, b, _, M[h + 11], B, 3174756917),
            _ = c(_, w, A, b, M[h + 2], N, 718787259),
            b = c(b, _, w, A, M[h + 9], R, 3951481745),
            A = n(A, m),
            b = n(b, y),
            _ = n(_, v),
            w = n(w, g);
        return (d(A) + d(b) + d(_) + d(w)).toLowerCase()
    }
    function l(e) {
        return "[object Object]" == {}.toString.call(e)
    }
    function c(e, t, n) {
        var r = n || {};
        document.cookie = e.replace(/[^+#$&^`|]/g, encodeURIComponent).replace("(", "%28").replace(")", "%29") + "=" + t.replace(/[^+#$&/:<-\[\]-}]/g, encodeURIComponent) + (r.domain ? ";domain=" + r.domain : "") + (r.path ? ";path=" + r.path : "") + (r.secure ? ";secure" : "") + (r.httponly ? ";HttpOnly" : "") + (r.sameSite ? ";Samesite=" + r.sameSite : "")
    }
    function f(e) {
        var t = new RegExp("(?:^|;\\s*)" + e + "\\=([^;]+)(?:;\\s*|$)").exec(document.cookie);
        return t ? t[1] : void 0
    }
    function d(e, t, n) {
        var r = new Date;
        r.setTime(r.getTime() - 864e5);
        var o = "/";
        document.cookie = e + "=;path=" + "/;domain=." + t + ";expires=" + r.toGMTString(),
        document.cookie = e + "=;path=" + "/;domain=." + n + "." + t + ";expires=" + r.toGMTString()
    }
    function p(e, t) {
        for (var n = e.split("."), r = t.split("."), o = 3, i = 0; 3 > i; i++) {
            var a = Number(n[i])
              , s = Number(r[i]);
            if (a > s)
                return 1;
            if (s > a)
                return -1;
            if (!isNaN(a) && isNaN(s))
                return 1;
            if (isNaN(a) && !isNaN(s))
                return -1
        }
        return 0
    }
    function h() {
        var t = e.location.hostname;
        if (!t) {
            var n = e.parent.location.hostname;
            n && ~n.indexOf("zebra.alibaba-inc.com") && (t = n)
        }
        var r, o = new RegExp("([^.]*?)\\.?((?:" + ["taobao.net", "taobao.com", "tmall.com", "tmall.hk", "alibaba-inc.com"].join(")|(?:").replace(/\./g, "\\.") + "))","i"), i = t.match(o) || [], a = i[2] || "taobao.com", s = i[1] || "m";
        "taobao.net" !== a || "x" !== s && "waptest" !== s && "daily" !== s ? "taobao.net" === a && "demo" === s ? s = "demo" : "alibaba-inc.com" === a && "zebra" === s ? s = "zebra" : "waptest" !== s && "wapa" !== s && "m" !== s && (s = "m") : s = "waptest";
        var u = "h5api";
        "taobao.net" === a && "waptest" === s && (u = "acs"),
        A.mainDomain = a,
        A.subDomain = s,
        A.prefix = u
    }
    function m() {
        var t = e.navigator.userAgent
          , n = t.match(/WindVane[\/\s]([\d\.\_]+)/);
        n && (A.WindVaneVersion = n[1]);
        var r = t.match(/AliApp\(([^\/]+)\/([\d\.\_]+)\)/i);
        r && (A.AliAppName = r[1],
        A.AliAppVersion = r[2]);
        var o = t.match(/AMapClient\/([\d\.\_]+)/i);
        o && (A.AliAppName = "AMAP",
        A.AliAppVersion = o[1])
    }
    function y(e) {
        this.id = "" + (new Date).getTime() + ++x,
        this.params = o(e || {}, {
            v: "*",
            data: {},
            type: "get",
            dataType: "jsonp"
        }),
        this.params.type = this.params.type.toLowerCase(),
        "object" == t(this.params.data) && (this.params.data = JSON.stringify(this.params.data)),
        this.middlewares = b.slice(0)
    }
    var v = e.Promise
      , g = (v || {
        resolve: function e() {}
    }).resolve();
    String.prototype.trim || (String.prototype.trim = function() {
        return this.replace(/^[\s\uFEFF\xA0]+|[\s\uFEFF\xA0]+$/g, "")
    }
    );
    var A = {
        useJsonpResultType: !1,
        safariGoLogin: !0,
        useAlipayJSBridge: !1
    }
      , b = []
      , _ = {
        ERROR: -1,
        SUCCESS: 0,
        TOKEN_EXPIRED: 1,
        SESSION_EXPIRED: 2
    };
    h(),
    m();
    var w = /[Android|Adr]/.test(e.navigator.userAgent), M, S = "AP" === A.AliAppName && p(A.AliAppVersion, "10.1.2") >= 0 || "KB" === A.AliAppName && p(A.AliAppVersion, "7.1.62") >= 0 || w && "AMAP" === A.AliAppName && p(A.AliAppVersion, "1.0.1") >= 0, x = 0, k = "2.6.2";
    y.prototype.use = function(e) {
        if (!e)
            throw new Error("middleware is undefined");
        return this.middlewares.push(e),
        this
    }
    ,
    y.prototype.__processRequestMethod = function(e) {
        var t = this.params
          , n = this.options;
        "get" === t.type && "jsonp" === t.dataType ? n.getJSONP = !0 : "get" === t.type && "originaljsonp" === t.dataType ? n.getOriginalJSONP = !0 : "get" === t.type && "json" === t.dataType ? n.getJSON = !0 : "post" === t.type && (n.postJSON = !0),
        e()
    }
    ,
    y.prototype.__processRequestType = function(t) {
        var r = this
          , o = this.params
          , i = this.options;
        if (!0 === A.H5Request && (i.H5Request = !0),
        !0 === A.WindVaneRequest && (i.WindVaneRequest = !0),
        !1 === i.H5Request && !0 === i.WindVaneRequest) {
            if (!S && (!n.windvane || parseFloat(i.WindVaneVersion) < 5.4))
                throw new Error("WINDVANE_NOT_FOUND::\u7f3a\u5c11WindVane\u73af\u5883");
            if (S && !e.AlipayJSBridge)
                throw new Error("ALIPAY_NOT_READY::\u652f\u4ed8\u5b9d\u901a\u9053\u672a\u51c6\u5907\u597d\uff0c\u652f\u4ed8\u5b9d\u8bf7\u89c1 https://lark.alipay.com/mtbsdkdocs/mtopjssdkdocs/pucq6z")
        } else if (!0 === i.H5Request)
            i.WindVaneRequest = !1;
        else if (void 0 === i.WindVaneRequest && void 0 === i.H5Request) {
            if (n.windvane && parseFloat(i.WindVaneVersion) >= 5.4 ? i.WindVaneRequest = !0 : i.H5Request = !0,
            S) {
                if (i.WindVaneRequest = i.H5Request = void 0,
                e.AlipayJSBridge)
                    if (l(o.data))
                        i.WindVaneRequest = !0;
                    else
                        try {
                            l(JSON.parse(o.data)) ? i.WindVaneRequest = !0 : i.H5Request = !0
                        } catch (e) {
                            i.H5Request = !0
                        }
                else
                    i.H5Request = !0;
                "AMAP" !== A.AliAppName || o.useNebulaJSbridgeWithAMAP || (i.WindVaneRequest = i.H5Request = void 0,
                i.H5Request = !0)
            }
            window.self !== window.top && (i.H5Request = !0)
        }
        var a = e.navigator.userAgent.toLowerCase();
        return a.indexOf("youku") > -1 && i.mainDomain.indexOf("youku.com") < 0 && (i.WindVaneRequest = !1,
        i.H5Request = !0),
        i.mainDomain.indexOf("youku.com") > -1 && a.indexOf("youku") < 0 && (i.WindVaneRequest = !1,
        i.H5Request = !0),
        t ? t().then((function() {
            var e = i.retJson.ret;
            if (e instanceof Array && (e = e.join(",")),
            !0 === i.WindVaneRequest && S && i.retJson.error || !e || e.indexOf("PARAM_PARSE_ERROR") > -1 || e.indexOf("HY_FAILED") > -1 || e.indexOf("HY_NO_HANDLER") > -1 || e.indexOf("HY_CLOSED") > -1 || e.indexOf("HY_EXCEPTION") > -1 || e.indexOf("HY_NO_PERMISSION") > -1) {
                if (!S || !isNaN(i.retJson.error) || -1 !== i.retJson.error.indexOf("FAIL_SYS_ACCESS_DENIED"))
                    return S && l(o.data) && (o.data = JSON.stringify(o.data)),
                    A.H5Request = !0,
                    r.__sequence([r.__processRequestType, r.__processToken, r.__processRequestUrl, r.middlewares, r.__processRequest]);
                void 0 === i.retJson.api && void 0 === i.retJson.v && (i.retJson.api = o.api,
                i.retJson.v = o.v,
                i.retJson.ret = [i.retJson.error + "::" + i.retJson.errorMessage],
                i.retJson.data = {})
            }
        }
        )) : void 0
    }
    ;
    var L = "_m_h5_c"
      , E = "_m_h5_tk"
      , C = "_m_h5_tk_enc";
    y.prototype.__getTokenFromAlipay = function() {
        var t = r()
          , n = this.options
          , o = (e.navigator.userAgent,
        !!location.protocol.match(/^https?\:$/));
        return !0 === n.useAlipayJSBridge && !o && S && e.AlipayJSBridge && e.AlipayJSBridge.call ? e.AlipayJSBridge.call("getMtopToken", (function(e) {
            e && e.token && (n.token = e.token),
            t.resolve()
        }
        ), (function() {
            t.resolve()
        }
        )) : t.resolve(),
        t.promise
    }
    ,
    y.prototype.__getTokenFromCookie = function() {
        var e = this.options;
        return e.CDR && f(L) ? e.token = f(L).split(";")[0] : e.token = e.token || f(E),
        e.token && (e.token = e.token.split("_")[0]),
        v.resolve()
    }
    ,
    y.prototype.__waitWKWebViewCookie = function(t) {
        var n = this.options;
        n.waitWKWebViewCookieFn && n.H5Request && e.webkit && e.webkit.messageHandlers ? n.waitWKWebViewCookieFn(t) : t()
    }
    ,
    y.prototype.__processToken = function(e) {
        var t = this
          , n = this.options;
        return this.params,
        n.token && delete n.token,
        !0 !== n.WindVaneRequest ? g.then((function() {
            return t.__getTokenFromAlipay()
        }
        )).then((function() {
            return t.__getTokenFromCookie()
        }
        )).then(e).then((function() {
            var e = n.retJson
              , r = e.ret;
            if (r instanceof Array && (r = r.join(",")),
            r.indexOf("TOKEN_EMPTY") > -1 || (!0 === n.CDR || !0 === n.syncCookieMode) && r.indexOf("ILLEGAL_ACCESS") > -1 || r.indexOf("TOKEN_EXOIRED") > -1) {
                if (n.maxRetryTimes = n.maxRetryTimes || 5,
                n.failTimes = n.failTimes || 0,
                n.H5Request && ++n.failTimes < n.maxRetryTimes) {
                    var o = [t.__waitWKWebViewCookie, t.__processToken, t.__processRequestUrl, t.middlewares, t.__processRequest];
                    if (!0 === n.syncCookieMode && t.constructor.__cookieProcessorId !== t.id)
                        if (t.constructor.__cookieProcessor) {
                            var i = function e(n) {
                                var r = function e() {
                                    t.constructor.__cookieProcessor = null,
                                    t.constructor.__cookieProcessorId = null,
                                    n()
                                };
                                t.constructor.__cookieProcessor ? t.constructor.__cookieProcessor.then(r).catch(r) : n()
                            };
                            o = [i, t.__waitWKWebViewCookie, t.__processToken, t.__processRequestUrl, t.middlewares, t.__processRequest]
                        } else
                            t.constructor.__cookieProcessor = t.__requestProcessor,
                            t.constructor.__cookieProcessorId = t.id;
                    return t.__sequence(o)
                }
                n.maxRetryTimes > 0 && (d(L, n.pageDomain, "*"),
                d(E, n.mainDomain, n.subDomain),
                d(C, n.mainDomain, n.subDomain)),
                e.retType = _.TOKEN_EXPIRED
            }
        }
        )) : void e()
    }
    ,
    y.prototype.__processRequestUrl = function(t) {
        var n = this.params
          , r = this.options;
        if (r.hostSetting && r.hostSetting[e.location.hostname]) {
            var o = r.hostSetting[e.location.hostname];
            o.prefix && (r.prefix = o.prefix),
            o.subDomain && (r.subDomain = o.subDomain),
            o.mainDomain && (r.mainDomain = o.mainDomain)
        }
        if (!0 === r.H5Request) {
            var i = "//" + (r.prefix ? r.prefix + "." : "") + (r.subDomain ? r.subDomain + "." : "") + r.mainDomain + "/h5/" + n.api.toLowerCase() + "/" + n.v.toLowerCase() + "/"
              , a = n.appKey || ("waptest" === r.subDomain ? "4272" : "12574478")
              , s = (new Date).getTime()
              , l = u(r.token + "&" + s + "&" + a + "&" + n.data)
              , c = {
                jsv: k,
                appKey: a,
                t: s,
                sign: l
            }
              , f = {
                data: n.data,
                ua: n.ua
            };
            Object.keys(n).forEach((function(e) {
                void 0 === c[e] && void 0 === f[e] && "headers" !== e && "ext_headers" !== e && "ext_querys" !== e && (c[e] = n[e])
            }
            )),
            n.ext_querys && Object.keys(n.ext_querys).forEach((function(e) {
                c[e] = n.ext_querys[e]
            }
            )),
            r.getJSONP ? c.type = "jsonp" : r.getOriginalJSONP ? c.type = "originaljsonp" : (r.getJSON || r.postJSON) && (c.type = "originaljson"),
            void 0 !== n.valueType && ("original" === n.valueType ? r.getJSONP || r.getOriginalJSONP ? c.type = "originaljsonp" : (r.getJSON || r.postJSON) && (c.type = "originaljson") : "string" === n.valueType && (r.getJSONP || r.getOriginalJSONP ? c.type = "jsonp" : (r.getJSON || r.postJSON) && (c.type = "json"))),
            !0 === r.useJsonpResultType && "originaljson" === c.type && delete c.type,
            r.dangerouslySetProtocol && (i = r.dangerouslySetProtocol + ":" + i),
            r.querystring = c,
            r.postdata = f,
            r.path = i
        }
        t()
    }
    ,
    y.prototype.__processUnitPrefix = function(e) {
        e()
    }
    ;
    var T = 0;
    y.prototype.__requestJSONP = function(e) {
        function t(e) {
            if (c && clearTimeout(c),
            f.parentNode && f.parentNode.removeChild(f),
            "TIMEOUT" === e)
                window[l] = function() {
                    window[l] = void 0;
                    try {
                        delete window[l]
                    } catch (e) {}
                }
                ;
            else {
                window[l] = void 0;
                try {
                    delete window[l]
                } catch (e) {}
            }
        }
        var n = r()
          , o = this.params
          , s = this.options
          , u = o.timeout || 2e4
          , l = "mtopjsonp" + (o.jsonpIncPrefix || "") + ++T
          , c = setTimeout((function() {
            e(s.timeoutErrMsg || "TIMEOUT::\u63a5\u53e3\u8d85\u65f6"),
            t("TIMEOUT")
        }
        ), u);
        s.querystring.callback = l;
        var f = document.createElement("script");
        return f.src = s.path + "?" + a(s.querystring) + "&" + a(s.postdata),
        f.async = !0,
        f.onerror = function() {
            t("ABORT"),
            e(s.abortErrMsg || "ABORT::\u63a5\u53e3\u5f02\u5e38\u9000\u51fa")
        }
        ,
        window[l] = function() {
            s.results = Array.prototype.slice.call(arguments),
            t(),
            n.resolve()
        }
        ,
        i(f),
        n.promise
    }
    ,
    y.prototype.__requestJSON = function(t) {
        function n(e) {
            c && clearTimeout(c),
            "TIMEOUT" === e && u.abort()
        }
        var o = r()
          , i = this.params
          , s = this.options
          , u = new e.XMLHttpRequest
          , l = i.timeout || 2e4
          , c = setTimeout((function() {
            t(s.timeoutErrMsg || "TIMEOUT::\u63a5\u53e3\u8d85\u65f6"),
            n("TIMEOUT")
        }
        ), l);
        s.CDR && f(L) && (s.querystring.c = decodeURIComponent(f(L))),
        u.onreadystatechange = function() {
            if (4 == u.readyState) {
                var e, r, i = u.status;
                if (i >= 200 && 300 > i || 304 == i) {
                    n(),
                    e = u.responseText,
                    r = u.getAllResponseHeaders() || "";
                    try {
                        (e = /^\s*$/.test(e) ? {} : JSON.parse(e)).responseHeaders = r,
                        s.results = [e],
                        o.resolve()
                    } catch (e) {
                        t("PARSE_JSON_ERROR::\u89e3\u6790JSON\u5931\u8d25")
                    }
                } else
                    n("ABORT"),
                    t(s.abortErrMsg || "ABORT::\u63a5\u53e3\u5f02\u5e38\u9000\u51fa")
            }
        }
        ;
        var d, p, h = s.path + "?" + a(s.querystring);
        s.getJSON ? (d = "GET",
        h += "&" + a(s.postdata)) : s.postJSON && (d = "POST",
        p = a(s.postdata)),
        u.open(d, h, !0),
        u.withCredentials = !0,
        u.setRequestHeader("Accept", "application/json"),
        u.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        var m = i.ext_headers || i.headers;
        if (m)
            for (var y in m)
                u.setRequestHeader(y, m[y]);
        return u.send(p),
        o.promise
    }
    ,
    y.prototype.__requestWindVane = function(e) {
        function t(e) {
            a.results = [e],
            o.resolve()
        }
        var o = r()
          , i = this.params
          , a = this.options
          , s = i.data
          , u = i.api
          , l = i.v
          , c = a.postJSON ? 1 : 0
          , f = a.getJSON || a.postJSON || a.getOriginalJSONP ? "originaljson" : "";
        void 0 !== i.valueType && ("original" === i.valueType ? f = "originaljson" : "string" === i.valueType && (f = "")),
        !0 === a.useJsonpResultType && (f = "");
        var d, p, h = "https" === location.protocol ? 1 : 0, m = i.isSec || 0, y = i.sessionOption || "AutoLoginOnly", v = i.ecode || 0, g = i.ext_headers || {}, A = i.ext_querys || {};
        d = 2 * (p = void 0 !== i.timer ? parseInt(i.timer) : void 0 !== i.timeout ? parseInt(i.timeout) : 2e4),
        !0 === i.needLogin && void 0 === i.sessionOption && (y = "AutoLoginAndManualLogin"),
        void 0 !== i.secType && void 0 === i.isSec && (m = i.secType);
        var b = {
            api: u,
            v: l,
            post: String(c),
            type: f,
            isHttps: String(h),
            ecode: String(v),
            isSec: String(m),
            param: JSON.parse(s),
            timer: p,
            needLogin: !!i.needLogin,
            sessionOption: y,
            ext_headers: g,
            ext_querys: A
        };
        i.ttid && !0 === a.dangerouslySetWVTtid && (b.ttid = i.ttid),
        Object.assign && i.dangerouslySetWindvaneParams && Object.assign(b, i.dangerouslySetWindvaneParams);
        var _ = "MtopWVPlugin";
        return "string" == typeof i.customWindVaneClassName && (_ = i.customWindVaneClassName),
        n.windvane.call(_, "send", b, t, t, d),
        o.promise
    }
    ,
    y.prototype.__requestAlipay = function(t) {
        function n(e) {
            a.results = [e],
            o.resolve()
        }
        var o = r()
          , i = this.params
          , a = this.options
          , s = {
            apiName: i.api,
            apiVersion: i.v,
            needEcodeSign: "1" === String(i.ecode),
            headers: i.ext_headers || {},
            usePost: !!a.postJSON
        };
        l(i.data) || (i.data = JSON.parse(i.data)),
        s.data = i.data,
        i.ttid && !0 === a.dangerouslySetWVTtid && (s.ttid = i.ttid),
        (a.getJSON || a.postJSON || a.getOriginalJSONP) && (s.type = "originaljson"),
        void 0 !== i.valueType && ("original" === i.valueType ? s.type = "originaljson" : "string" === i.valueType && delete s.type),
        !0 === a.useJsonpResultType && delete s.type,
        Object.assign && i.dangerouslySetAlipayParams && Object.assign(s, i.dangerouslySetAlipayParams);
        var u = "mtop";
        return "string" == typeof i.customAlipayJSBridgeApi && (u = i.customAlipayJSBridgeApi),
        e.AlipayJSBridge.call(u, s, n),
        o.promise
    }
    ,
    y.prototype.__processRequest = function(e, t) {
        var n = this;
        return g.then((function() {
            var e = n.options;
            if (e.H5Request && (e.getJSONP || e.getOriginalJSONP))
                return n.__requestJSONP(t);
            if (e.H5Request && (e.getJSON || e.postJSON))
                return n.__requestJSON(t);
            if (e.WindVaneRequest)
                return S ? n.__requestAlipay(t) : n.__requestWindVane(t);
            throw new Error("UNEXCEPT_REQUEST::\u9519\u8bef\u7684\u8bf7\u6c42\u7c7b\u578b")
        }
        )).then(e).then((function() {
            var e = n.options
              , t = (n.params,
            e.results[0])
              , r = t && t.ret || [];
            t.ret = r,
            r instanceof Array && (r = r.join(","));
            var o = t.c;
            e.CDR && o && c(L, o, {
                domain: e.pageDomain,
                path: "/",
                secure: e.secure,
                sameSite: e.sameSite
            }),
            r.indexOf("SUCCESS") > -1 ? t.retType = _.SUCCESS : t.retType = _.ERROR,
            e.retJson = t
        }
        ))
    }
    ,
    y.prototype.__sequence = function(e) {
        function t(e) {
            if (e instanceof Array)
                e.forEach(t);
            else {
                var a, s = r(), u = r();
                o.push((function() {
                    return s = r(),
                    (a = e.call(n, (function(e) {
                        return s.resolve(e),
                        u.promise
                    }
                    ), (function(e) {
                        return s.reject(e),
                        u.promise
                    }
                    ))) && (a = a.catch((function(e) {
                        s.reject(e)
                    }
                    ))),
                    s.promise
                }
                )),
                i.push((function(e) {
                    return u.resolve(e),
                    a
                }
                ))
            }
        }
        var n = this
          , o = []
          , i = [];
        e.forEach(t);
        for (var a, s = g; a = o.shift(); )
            s = s.then(a);
        for (; a = i.pop(); )
            s = s.then(a);
        return s
    }
    ;
    var O = function e(t) {
        t()
    }
      , Y = function e(t) {
        t()
    };
    y.prototype.request = function(t) {
        var r = this;
        if (this.options = o(t || {}, A),
        !v) {
            var i = "\u5f53\u524d\u6d4f\u89c8\u5668\u4e0d\u652f\u6301Promise\uff0c\u8bf7\u5728windows\u5bf9\u8c61\u4e0a\u6302\u8f7dPromise\u5bf9\u8c61";
            throw n.mtop = {
                ERROR: i
            },
            new Error(i)
        }
        var a = v.resolve([O, Y]).then((function(e) {
            var t = e[0]
              , n = e[1];
            return r.__sequence([t, r.__processRequestMethod, r.__processRequestType, r.__processToken, r.__processRequestUrl, r.middlewares, r.__processRequest, n])
        }
        )).then((function() {
            var e = r.options.retJson;
            return e.retType !== _.SUCCESS ? v.reject(e) : r.options.successCallback ? void r.options.successCallback(e) : v.resolve(e)
        }
        )).catch((function(e) {
            var t;
            return e instanceof Error ? (console.error(e.stack),
            t = {
                ret: [e.message],
                stack: [e.stack],
                retJson: _.ERROR
            }) : t = "string" == typeof e ? {
                ret: [e],
                retJson: _.ERROR
            } : void 0 !== e ? e : r.options.retJson,
            n.mtop.errorListener && n.mtop.errorListener({
                api: r.params.api,
                data: r.params.data,
                v: r.params.v,
                retJson: t
            }),
            r.options.failureCallback ? void r.options.failureCallback(t) : v.reject(t)
        }
        ));
        return this.__processRequestType(),
        r.options.H5Request && (r.constructor.__firstProcessor || (r.constructor.__firstProcessor = a),
        O = function e(t) {
            r.constructor.__firstProcessor.then(t).catch(t)
        }
        ),
        ("get" === this.params.type && "json" === this.params.dataType || "post" === this.params.type) && (t.pageDomain = t.pageDomain || s(e.location.hostname),
        t.mainDomain !== t.pageDomain && (t.maxRetryTimes = 4,
        t.CDR = !0)),
        this.__requestProcessor = a,
        a
    }
    ,
    n.mtop = function(e) {
        return new y(e)
    }
    ,
    n.mtop.request = function(e, t, n) {
        var r = {
            H5Request: e.H5Request,
            WindVaneRequest: e.WindVaneRequest,
            LoginRequest: e.LoginRequest,
            AntiCreep: e.AntiCreep,
            AntiFlood: e.AntiFlood,
            successCallback: t,
            failureCallback: n || t
        };
        return new y(e).request(r)
    }
    ,
    n.mtop.H5Request = function(e, t, n) {
        var r = {
            H5Request: !0,
            successCallback: t,
            failureCallback: n || t
        };
        return new y(e).request(r)
    }
    ,
    n.mtop.middlewares = b,
    n.mtop.config = A,
    n.mtop.RESPONSE_TYPE = _,
    n.mtop.CLASS = y
}