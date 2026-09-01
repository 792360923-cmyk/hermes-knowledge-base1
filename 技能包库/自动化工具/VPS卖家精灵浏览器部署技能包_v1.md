# VPS卖家精灵浏览器部署技能包 v1

> **状态**：✅当前推荐 | **分类**：自动化工具 | **更新时间**：2026-09-01
> **适用场景**：新VPS从零部署 Chrome + 卖家精灵插件 + hermes-sellersprite 自动化服务
> **关联**：hermes-sellersprite-0.1.1.zip

---

# VPS 部署 Chrome + 卖家精灵插件 + 自动化服务

适用于 Ubuntu 24.04 VPS，从零到可用。2026-09-01 已完整跑通验证，以下是标准化流程 + 全部踩坑修复。

---

## 前提条件

- Ubuntu 24.04 VPS（2G RAM+, amd64）
- `hermes-sellersprite-0.1.1.zip` 项目文件
- root 权限
- 卖家精灵账号（用于登录）

---

## 阶段1：安装基础环境（10分钟）

```bash
apt update && apt install -y unzip
mkdir -p /opt/hermes-sellersprite
unzip hermes-sellersprite-0.1.1.zip -d /opt/hermes-sellersprite
cd /opt/hermes-sellersprite && bash scripts/install-vps.sh
npm install --omit=dev
cp .env.example .env
TOKEN=$(openssl rand -hex 24)
sed -i "s/API_TOKEN=change-this-token/API_TOKEN=$TOKEN/" .env
echo "SELLERSPRITE_BROWSER_TOKEN=$TOKEN"
```

---

## 阶段2：图形桌面 + VNC + noVNC（5分钟）

```bash
apt install -y xfce4 xfce4-goodies tigervnc-standalone-server tigervnc-common novnc websockify dbus-x11
mkdir -p /home/hermes/.vnc && chown -R hermes:hermes /home/hermes/.vnc
su -s /bin/bash hermes -c 'printf "YOUR_VNC_PW\nYOUR_VNC_PW\nn\n" | vncpasswd'

# xstartup — 必须用 dbus-launch
cat >/home/hermes/.vnc/xstartup <<'XEOF'
#!/bin/bash
export XDG_SESSION_TYPE=x11
export XDG_CURRENT_DESKTOP=XFCE
export DESKTOP_SESSION=xfce
unset SESSION_MANAGER
unset DBUS_SESSION_BUS_ADDRESS
dbus-launch --exit-with-session startxfce4
XEOF
chmod +x /home/hermes/.vnc/xstartup
chown hermes:hermes /home/hermes/.vnc/xstartup

su -s /bin/bash hermes -c 'vncserver :1 -geometry 1440x900 -depth 24'
nohup websockify --web=/usr/share/novnc/ 127.0.0.1:6080 127.0.0.1:5901 >/tmp/novnc.log 2>&1 &
# SSH 隧道：ssh -L 6080:127.0.0.1:6080 root@VPS_IP → http://localhost:6080/vnc.html
```

---

## 阶段3：手动安装登录卖家精灵

```bash
systemctl stop hermes-sellersprite
for pid in $(ps aux | grep -E "google-chrome|/opt/google/chrome/chrome" | grep -v grep | awk '{print $2}'); do kill $pid 2>/dev/null; done
chown -R hermes:hermes /opt/hermes-sellersprite/chrome-profile
chown -R hermes:hermes /opt/hermes-sellersprite/downloads

su -s /bin/bash hermes -c 'DISPLAY=:1 /usr/bin/google-chrome --user-data-dir=/opt/hermes-sellersprite/chrome-profile --no-first-run --no-default-browser-check chrome://extensions/'
```

**VNC 操作**：chrome://extensions/ → 开发者模式 → 拖入卖家精灵zip → 装完后打开 amazon.com → 点插件图标登录 → 启动插件 → 确认面板出现 → 关 Chrome

---

## ⛔ 阶段4：Playwright 必须禁用默认 --disable-extensions

> **Playwright 默认注入 `--disable-extensions`，优先级高于 `--load-extension`。**

修复 `src/browser.js`，`launchPersistentContext` 加：
```js
ignoreDefaultArgs: ['--disable-extensions']
```

---

## 阶段5：配置 .env + 修 Node 版本 + Systemd

```bash
EXT_DIR="/opt/hermes-sellersprite/chrome-profile/Default/Extensions/lnbmbgocenenhhhdojdielgnmeflbnfb"
VERSION=$(ls "$EXT_DIR" | head -1)
sed -i "s#^SELLERSPRITE_EXTENSION_DIR=.*#SELLERSPRITE_EXTENSION_DIR=$EXT_DIR/$VERSION#" .env
sed -i 's#^HEADLESS=.*#HEADLESS=false#' .env

# hermes用户node可能是v18，复制root的v22（不要symlink）
rm -f /usr/local/bin/node /usr/local/bin/npm
cp /root/.hermes/node/bin/node /usr/local/bin/node
cp /root/.hermes/node/bin/npm /usr/local/bin/npm
chmod 755 /usr/local/bin/node /usr/local/bin/npm

cat >/etc/systemd/system/hermes-sellersprite.service <<EOF
[Unit]
Description=Hermes SellerSprite Chrome automation service
After=network-online.target
Wants=network-online.target
[Service]
Type=simple
User=hermes
WorkingDirectory=/opt/hermes-sellersprite
EnvironmentFile=/opt/hermes-sellersprite/.env
Environment=DISPLAY=:1
ExecStart=/usr/local/bin/node src/server.js
Restart=on-failure
RestartSec=5
NoNewPrivileges=true
[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload && systemctl enable --now hermes-sellersprite
```

---

## 阶段6：验证

```bash
curl -s http://127.0.0.1:8787/browser/warmup -H "Authorization: Bearer TOKEN"
# → {"ok":true}

curl -s -X POST http://127.0.0.1:8787/workflows/run -H "Authorization: Bearer TOKEN" -H "Content-Type: application/json" \
  -d '{"workflow":{"name":"test","steps":[
    {"action":"goto","url":"https://www.amazon.com/s?k=test","waitUntil":"domcontentloaded"},
    {"action":"waitForTimeout","ms":8000},
    {"action":"evaluate","expression":"JSON.stringify({plugin:!!document.getElementById(\"seller-sprite-extension-app\")})"}
  ]}}'
# → {"ok":true,...,"artifacts":[{"type":"evaluate","value":{"plugin":true}}]}
```

---

## 🕳️ 踩坑速查

| 坑 | 症状 | 修复 |
|----|------|------|
| Playwright默认禁用扩展 | 插件不加载 | `ignoreDefaultArgs:['--disable-extensions']` |
| hermes的node v18太低 | Playwright报需v20+ | 复制root的v22到/usr/local/bin，不要symlink |
| xfce4秒退 | VNC即退出 | xstartup用`dbus-launch --exit-with-session startxfce4` |
| profile锁残留 | SingletonLock | `rm -f chrome-profile/Singleton*` |
| symlink无权限 | Permission denied | /usr/local/bin/node必须是真实文件非symlink |
| pkill误伤终端 | 终端退出 | 用`ps aux|grep chrome|awk`逐进程杀 |