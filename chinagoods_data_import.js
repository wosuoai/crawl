// ==UserScript==
// @name         Chinagoods 导入数据
// @namespace    chinagoods
// @version      0.2
// @description  采集数据
// @author       You
// @include      *://detail.1688.com/*
// @include      *://detail.tmall.com/*
// @include      *://item.taobao.com/*
// @include      *://*.chinagoods.com/*
// @require      https://ql.chinagoods.com/youhou/chinagoods-imprt.js
// @icon         https://chinagoods.com//favicon.ico
// @grant GM_setValue
// @grant GM_getValue
// @grant GM_deleteValue
// @grant unsafeWindow
// @grant GM_xmlhttpRequest
// @grant GM_openInTab
// @grant GM_addStyle
// ==/UserScript==

var script = document.createElement('script')
script.setAttribute('type', 'text/javascript')
script.setAttribute('src', 'https://ql.chinagoods.com/youhou/chinagoods.js?t=' + new Date().getTime().toString().substr(0, 8))
document.getElementsByTagName('head')[0].appendChild(script)

var _this = unsafeWindow
var t = setInterval(function() {
  if (_this.bootstrap && (window.$ || window.jQuery || _this.$ || _this.jQuery)) {
    window.$ = (window.$ || window.jQuery || _this.$ || _this.jQuery)
    if (!_this.$) _this.$ = _this.jQuery = window.$
    _this.bootstrap({
      GM_xmlhttpRequest,
      GM_setValue,
      GM_getValue,
      GM_openInTab,
      Swal,
      GM_addStyle
    })
    clearInterval(t)
  }
}, 300)
