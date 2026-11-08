# 服务端部署说明（敏感信息放服务端 + 常规反扒）

## 架构

```
index.html      页面本体：不含任何明文 QQ / 邮箱 / 账号 ID，联系方式用 data-c 占位
core.min.js     由 make_core.py 从 .env.profile.json 生成；数据经编码，运行时解码注入 DOM
.env.profile.json  明文真实数据【仅存服务器】，nginx 对 .env.* 返回 404，公网无法下载
robots.txt / anti-scrape.conf / noindex meta   反扒
```

要点：**页面要展示这些链接，浏览器最终一定能拿到**——所以这防的是「源码里明文写死、
被 GitHub / 搜索引擎 / 批量爬虫直接收录」，不是绝对保密。真实数据的唯一明文副本只在服务器上。

## 部署步骤

1. 把 `.env.example.json` 复制为 `.env.profile.json`，填入真实联系方式。
2. `python3 make_core.py` 生成 `core.min.js`。
3. 把 `index.html`、`core.min.js`、`robots.txt`、背景图放到站点根目录。
4. `.env.profile.json` 放同目录，确认 `curl -I https://你的域名/.env.profile.json` 返回 **404**。
5. 把 `anti-scrape.conf` 放到 nginx 该站点的 extension 目录（新增文件，不改动其它站点配置），
   `nginx -t` 通过后 `nginx -s reload`。

## 反扒清单（常规防护，不伤正常访客）

- 前端：禁右键 / 复制 / 选中 / 拖拽、拦截 F12 与查看源码快捷键、开发者工具检测、敏感数据编码
- 页面：`noindex,nofollow,noarchive` meta + `robots.txt` Disallow
- 服务端：站点级请求限速、`X-Robots-Tag` / `nosniff` / `no-referrer` 响应头、`.env.*` 禁止下载

> 前端防护挡不住懂技术的人，过强反而误伤正常访客；本方案不含任何会伤害访问者或采集隐私的手段。
