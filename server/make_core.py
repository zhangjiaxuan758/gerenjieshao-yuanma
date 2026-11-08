# -*- coding: utf-8 -*-
"""从服务端 .env.profile.json 生成 core.min.js（敏感数据编码 + 联系方式注入 + 常规反扒）。
真实数据文件 .env.profile.json 只在服务器上，.gitignore 已排除，绝不提交到仓库。"""
import json, base64, pathlib
HERE = pathlib.Path(__file__).parent
env = HERE / '.env.profile.json'
if not env.exists():
    raise SystemExit('缺少 .env.profile.json：请把 .env.example.json 复制为 .env.profile.json 并填入真实数据')
P = json.loads(env.read_text(encoding='utf-8'))
K = 0x5A
raw = json.dumps(P, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
DATA = base64.b64encode(bytes(b ^ K for b in raw)).decode('ascii')

TPL = r"""(function(){var _0x4b5a="__DATA__",_0xK=90;
function _d(s){var b=atob(s),o="";for(var i=0;i<b.length;i++){o+=String.fromCharCode(b.charCodeAt(i)^_0xK);}return o;}
var _P;try{_P=JSON.parse(_d(_0x4b5a));}catch(e){_P={links:{},apps:{}};}window.__P=_P;
function _inj(){var a=document.querySelectorAll("[data-c]");for(var i=0;i<a.length;i++){var el=a[i],k=el.getAttribute("data-c"),u=_P.links&&_P.links[k];if(!u)continue;el.setAttribute("href",u);if(el.getAttribute("data-app")==="1"&&_P.apps&&_P.apps[k]){el.setAttribute("onclick","return openAppLink(this, window.__P.apps[\""+k+"\"])");}}}
if(document.readyState==="loading"){document.addEventListener("DOMContentLoaded",_inj);}else{_inj();}
(function(){var B=["contextmenu","selectstart","copy","cut","dragstart"];for(var i=0;i<B.length;i++){document.addEventListener(B[i],function(e){e.preventDefault();return false;});}
document.addEventListener("keydown",function(e){var k=e.keyCode||e.which,c=e.ctrlKey||e.metaKey,s=e.shiftKey;if(k===123||k===44||(c&&s&&(k===73||k===74||k===67||k===75))||(c&&(k===85||k===83||k===80))){e.preventDefault();return false;}});
try{if(window.top!==window.self){window.top.location=window.self.location;}}catch(e){}
var _t=0;setInterval(function(){var w=window.outerWidth-window.innerWidth,h=window.outerHeight-window.innerHeight;if(w>160||h>160){_t++;if(_t===1){try{console.clear();}catch(e){}}}else{_t=0;}},1600);})();})();"""
(HERE / 'core.min.js').write_text(TPL.replace('__DATA__', DATA), encoding='utf-8')
print('已生成 core.min.js（含编码后的数据），请与 index.html 一起部署到站点根目录')
