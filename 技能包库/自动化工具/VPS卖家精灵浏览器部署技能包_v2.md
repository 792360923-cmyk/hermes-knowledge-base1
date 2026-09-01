# VPS卖家精灵浏览器部署技能包 v2（详细Agent版本）

> **版本**：v2 | **状态**：✅当前推荐 | **分类**：自动化工具 | **更新时间**：2026-09-01
> **适用场景**：新VPS从零部署 Chrome + 卖家精灵插件 + hermes-sellersprite 自动化服务
> **适用Agent**：任意AI编程助手（Claude/GPT/Hermes），可直接按本文档逐条执行
> **上一版本**：v1（简版，仅含步骤摘要）

---

## 一、你要达成什么

在新 Ubuntu 24.04 VPS 上：
1. 安装 Google Chrome 152
2. 安装 xfce4 桌面 + VNC + noVNC（让远程能看到 Chrome 界面）
3. 手动安装卖家精灵 Chrome 插件并登录
4. 启动 hermes-sellersprite 自动化服务（Playwright + 持久化 profile）
5. 验证：服务启动 Chrome 时卖家精灵插件自动加载

---

## 二、前提条件

| 条件 | 说明 |
|------|------|
| 系统 | Ubuntu 24.04，amd64 |
| 内存 | ≥2GB |
| 用户 | root（全部命令以 root 执行） |
| 文件 | `hermes-sellersprite-0.1.1.zip` 上传到 VPS |
| 卖家精灵账号 | 用于在插件里登录 |

---

## 三、阶段1：安装 Chrome + Node.js + 项目依赖

### 3.1 安装 unzip + 执行安装脚本

```bash
apt update && apt install -y unzip
mkdir -p /opt/hermes-sellersprite
unzip /path/to/hermes-sellersprite-0.1.1.zip -d /opt/hermes-sellersprite
cd /opt/hermes-sellersprite
bash scripts/install-vps.sh
```

**install-vps.sh 做了什么**：
- 安装 Google Chrome stable（从 Google 官方 apt 源）
- 安装 Node.js 22（从 NodeSource）
- 安装 xvfb、fonts-noto-cjk（中文显示）
- 创建 `hermes` 系统用户
- 创建 `/opt/hermes-sellersprite/chrome-profile` 和 `downloads` 目录

### 3.2 npm 安装依赖

```bash
cd /opt/hermes-sellersprite
npm install --omit=dev
```

验证：应输出 `added 87 packages, 0 vulnerabilities`

### 3.3 配置 .env 文件

```bash
cp .env.example .env
TOKEN=$(openssl rand -hex 24)
sed -i "s/API_TOKEN=change-this-token/API_TOKEN=$TOKEN/" .env
echo "SELLERSPRITE_BROWSER_TOKEN=$TOKEN"
# 把这行输出记下来！这是后面调用 API 的 Bearer Token
```

---

## 四、阶段2：安装图形桌面 + VNC + noVNC

### 4.1 安装包

```bash
apt install -y xfce4 xfce4-goodies tigervnc-standalone-server \
  tigervnc-common novnc websockify dbus-x11
```

安装量约 500MB，耗时约 2-3 分钟。

### 4.2 配置 VNC 密码

```bash
mkdir -p /home/hermes/.vnc
chown -R hermes:hermes /home/hermes/.vnc

# 把 YOUR_VNC_PW 改成你实际的密码（至少6位）
su -s /bin/bash hermes -c 'printf "YOUR_VNC_PW\nYOUR_VNC_PW\nn\n" | vncpasswd'
```

### 4.3 ⚠️ 关键：写 xstartup（否则 xfce4 会秒退）

**症状**：如果没有正确的 xstartup，VNC 启动后立即退出，日志显示：
```
Session startup via '/home/hermes/.vnc/xstartup' cleanly exited too early (< 3 seconds)!
```

**原因**：xfce4 需要 dbus 会话总线，而 VNC 环境没有自动启动 dbus。简单的 `startxfce4 &` 不行。

**修复**：用 `dbus-launch --exit-with-session` 包裹：

```bash
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
```

### 4.4 启动 VNC + noVNC

```bash
# 启动 VNC :1（1440x900分辨率，24位色深）
su -s /bin/bash hermes -c 'vncserver :1 -geometry 1440x900 -depth 24'

# 启动 noVNC（只监听 127.0.0.1:6080，转发到 VNC 的 127.0.0.1:5901）
# 注意：不要暴露 6080 到公网！
websockify --web=/usr/share/novnc/ 127.0.0.1:6080 127.0.0.1:5901 &
```

### 4.5 验证 VNC + xfce4

```bash
# 确认 VNC 和 noVNC 端口都在监听
ss -lntp | grep -E "5901|6080"
# 应看到两条 LISTEN，都在 127.0.0.1

# 确认 xfce4 桌面进程在运行
ps aux | grep -E "xfwm4|xfce4-panel|xfdesktop" | grep -v grep
# 应该能看到 xfwm4、xfce4-panel 等进程
```

### 4.6 连接方式

在你的本地机器上建立 SSH 隧道：
```bash
ssh -L 6080:127.0.0.1:6080 root@YOUR_VPS_IP
```

浏览器打开：`http://localhost:6080/vnc.html`，输入 VNC 密码即可看到 xfce4 桌面。

---

## 五、阶段3：手动安装卖家精灵插件

> **重要**：这个阶段必须通过 VNC 手动操作，不能自动化。

### 5.1 停止一切 Chrome 进程

```bash
systemctl stop hermes-sellersprite 2>/dev/null

# ⚠️ 不要用 pkill -f "chrome"！会误杀 chrome-devtools-mcp 等无关进程，甚至可能杀掉自己的终端。
# 安全做法：精确匹配 google-chrome 进程然后逐条 kill
for pid in $(ps aux | grep -E "google-chrome|/opt/google/chrome/chrome" | grep -v grep | awk '{print $2}'); do
  kill $pid 2>/dev/null
done
sleep 2
# 确认已全部杀掉
pgrep -a google-chrome || echo "all chrome killed OK"
```

### 5.2 修复 profile 权限

```bash
chown -R hermes:hermes /opt/hermes-sellersprite/chrome-profile
chown -R hermes:hermes /opt/hermes-sellersprite/downloads
```

### 5.3 在 VNC 桌面打开 Chrome

```bash
su -s /bin/bash hermes -c \
  'DISPLAY=:1 /usr/bin/google-chrome \
    --user-data-dir=/opt/hermes-sellersprite/chrome-profile \
    --no-first-run --no-default-browser-check \
    chrome://extensions/'
```

### 5.4 通过 VNC 手动操作

现在打开 `http://localhost:6080/vnc.html`，你会看到 Chrome 窗口：

1. **开启开发者模式**：在 `chrome://extensions/` 页面右上角打开「开发者模式」开关
2. **安装插件**：把卖家精灵官方提供的 `.zip` 安装包拖入页面安装。或者访问卖家精灵官网下载页面安装
3. **验证安装**：确认扩展列表中出现「卖家精灵 - 亚马逊关键词优化，大数据选品专家」
4. **登录插件**：在 Chrome 地址栏输入 `amazon.com` 回车 → 点击右上角卖家精灵插件图标 → 登录你的卖家精灵账号 → 点击「启动插件」
5. **确认生效**：Amazon 页面应该出现卖家精灵数据面板（显示 LQS、销量、FBA Fee 等信息）
6. **关掉 Chrome**：通过 VNC 关掉 Chrome 窗口，或执行：

```bash
for pid in $(ps aux | grep -E "google-chrome|/opt/google/chrome/chrome" | grep -v grep | awk '{print $2}'); do kill $pid 2>/dev/null; done
```

---

## 六、阶段4：⛔ 修复 Playwright 默认禁用扩展（最关键的坑）

### 6.1 问题

启动 hermes-sellersprite 服务后，调用 warmup API，Chrome 正常打开 Amazon，但卖家精灵插件**没有加载**。网页 DOM 中没有 `#seller-sprite-extension-app` 等插件元素。

### 6.2 排查过程

1. 检查 `.env` 中 `SELLERSPRITE_EXTENSION_DIR` 是否正确指向了插件目录 → 正确
2. 检查 `browser.js` 中 args 参数是否包含 `--load-extension` → 是
3. 查看服务日志中的 Chrome 启动参数 → 发现了一个关键的参数：

```
--disable-extensions --disable-extensions-except=<path> --load-extension=<path>
```

**`--disable-extensions` 是 Playwright 的默认参数！** 它和 `--load-extension` 一起传给 Chrome 时，`--disable-extensions` 优先级更高，导致所有扩展被禁用，包括卖家精灵。

### 6.3 根因

Playwright 的 `chromium.launchPersistentContext()` 在 headless:false 模式下仍然默认添加 `--disable-extensions` 参数。这不是 Chrome 的问题，是 Playwright 的设计行为。

### 6.4 修复

编辑 `src/browser.js`，在 `launchPersistentContext` 调用中加一行：

```javascript
return chromium.launchPersistentContext(config.userDataDir, {
    channel: config.chromeChannel,
    headless: config.headless,
    slowMo: config.slowMoMs,
    acceptDownloads: true,
    downloadsPath: config.downloadDir,
    viewport: { width: 1440, height: 1000 },
    args,
    ignoreDefaultArgs: ['--disable-extensions']  // ← 关键修复！
  });
```

`ignoreDefaultArgs` 告诉 Playwright **不要**注入 `--disable-extensions`，这样 args 里的 `--load-extension` 才能生效。

验证：
```bash
cd /opt/hermes-sellersprite && node --check src/browser.js && echo "syntax OK"
```

---

## 七、阶段5：修复 Node.js 版本问题

### 7.1 问题

服务以 `hermes` 用户运行时，Playwright 报错：
```
You are running Node.js 18.19.1.
Playwright requires Node.js 20 or higher.
```

### 7.2 排查过程

```bash
# root 用户的 node
which node          # → /root/.hermes/node/bin/node
node --version      # → v22.23.1 ✅

# hermes 用户的 node
su -s /bin/bash hermes -c 'which node'     # → /usr/bin/node
su -s /bin/bash hermes -c 'node --version' # → v18.19.1 ❌
```

`hermes` 用户的 PATH 中 `/usr/bin/node` 排在前面，那是系统自带的 v18。root 的 v22 在 `/root/.hermes/node/bin/node`，hermes 无权访问 `/root/`。

### 7.3 问题2：symlink 陷阱

第一次尝试用 symlink 解决：
```bash
ln -s /root/.hermes/node/bin/node /usr/local/bin/node
```
但这不行——`hermes` 用户解析 symlink 时同样需要遍历 `/root`，仍然 Permission denied。

### 7.4 正确修复

**复制真实文件，不要 symlink**：

```bash
# 删掉可能存在的旧 symlink
rm -f /usr/local/bin/node /usr/local/bin/npm

# 复制真实文件
cp /root/.hermes/node/bin/node /usr/local/bin/node
cp /root/.hermes/node/bin/npm /usr/local/bin/npm

# 设置可执行权限
chmod 755 /usr/local/bin/node /usr/local/bin/npm
```

验证：
```bash
su -s /bin/bash hermes -c '/usr/local/bin/node --version'
# 必须输出 v22.23.1 或更高
```

---

## 八、阶段6：配置 .env + Systemd

### 8.1 找到卖家精灵插件路径

```bash
cd /opt/hermes-sellersprite
EXT_DIR="/opt/hermes-sellersprite/chrome-profile/Default/Extensions/lnbmbgocenenhhhdojdielgnmeflbnfb"
VERSION=$(ls "$EXT_DIR" | head -1)
EXT_PATH="$EXT_DIR/$VERSION"
echo "Extension path: $EXT_PATH"
# 例如：/opt/hermes-sellersprite/chrome-profile/Default/Extensions/lnbmbgocenenhhhdojdielgnmeflbnfb/5.0.5_0
```

确认目录存在且包含 `manifest.json`：
```bash
ls "$EXT_PATH/manifest.json" && echo "OK" || echo "MISSING!"
```

### 8.2 写入 .env

```bash
# 强制加载插件（不靠 profile 中的已安装状态）
sed -i "s#^SELLERSPRITE_EXTENSION_DIR=.*#SELLERSPRITE_EXTENSION_DIR=$EXT_PATH#" .env
# 必须用有界面模式（插件在 headless 下不工作）
sed -i 's#^HEADLESS=.*#HEADLESS=false#' .env

# 检查结果
grep -E "SELLERSPRITE_EXTENSION_DIR|HEADLESS|USER_DATA_DIR" .env
```

### 8.3 写入 systemd 服务文件

```bash
cat >/etc/systemd/system/hermes-sellersprite.service <<'SERVICEEOF'
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
SERVICEEOF
```

要点说明：
- `User=hermes` — 不能用 root，因为 Chrome 的 profile 属主是 hermes
- `Environment=DISPLAY=:1` — 必须指向 VNC 桌面，Chrome 需要 X11 显示
- `ExecStart=/usr/local/bin/node` — 必须是 v22+，且是真实文件（非 symlink）
- `NoNewPrivileges=true` — 安全加固，不影响 Chrome 运行

### 8.4 启动服务

```bash
systemctl daemon-reload
systemctl enable hermes-sellersprite
systemctl restart hermes-sellersprite
sleep 3
systemctl status hermes-sellersprite --no-pager
```

期望输出：`Active: active (running)`

### 8.5 ⚠️ 常见启动失败问题

**问题A**：`EADDRINUSE :::8787` — 端口被占用
```bash
fuser -k 8787/tcp
systemctl restart hermes-sellersprite
```

**问题B**：`Active: activating (auto-restart)` 反复重启
```bash
journalctl -u hermes-sellersprite --no-pager -n 30
# 查看具体错误，通常是 DISPLAY=:1 不可用或 node 版本不对
```

---

## 九、阶段7：验证卖家精灵插件加载

### 9.1 基础验证

```bash
# warmup — 启动浏览器
curl -s -X POST http://127.0.0.1:8787/browser/warmup \
  -H "Authorization: Bearer YOUR_TOKEN"
# 期望：{"ok":true}
```

### 9.2 插件加载验证

```bash
curl -s -X POST http://127.0.0.1:8787/workflows/run \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "workflow": {
      "name": "verify-plugin",
      "steps": [
        {
          "action": "goto",
          "url": "https://www.amazon.com/s?k=test",
          "waitUntil": "domcontentloaded"
        },
        { "action": "waitForTimeout", "ms": 8000 },
        {
          "action": "evaluate",
          "expression": "JSON.stringify({ hasMainApp: !!document.getElementById(\"seller-sprite-extension-app\"), hasInventory: !!document.getElementById(\"sellersprite-extension-Inventory\"), hasQuickView: !!document.getElementById(\"seller-sprite-extension-quick-view-listing-page\") })"
        }
      ]
    }
  }'
```

期望返回：
```json
{
  "ok": true,
  "artifacts": [{
    "type": "evaluate",
    "value": {
      "hasMainApp": true,
      "hasInventory": true,
      "hasQuickView": true
    }
  }]
}
```

如果 `hasMainApp` 为 false，说明插件仍未加载，回到**第六章检查 `ignoreDefaultArgs`**。

### 9.3 截图验证

```bash
curl -s -X POST http://127.0.0.1:8787/workflows/run \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "workflow": {
      "name": "screenshot-test",
      "steps": [
        { "action": "goto", "url": "https://www.amazon.com/dp/B0009X29WK", "waitUntil": "domcontentloaded" },
        { "action": "waitForTimeout", "ms": 8000 },
        { "action": "screenshot", "name": "bsr1-pet-supplies" }
      ]
    }
  }'
```

截图文件路径在返回的 `artifacts[0].path` 中（例如 `/opt/hermes-sellersprite/downloads/screenshot-test-bsr1-pet-supplies-<timestamp>.png`）。通过 VNC 或 SCP 查看截图，确认页面上能看到卖家精灵数据面板。

---

## 十、阶段8：可选 — Remote Debugging Port 模式

如果你需要用 CDP（Chrome DevTools Protocol）工具直接操作这个 Chrome：

```bash
# 先停服务
systemctl stop hermes-sellersprite

# 手动打开 Chrome 并暴露 9222 端口
su -s /bin/bash hermes -c 'DISPLAY=:1 /usr/bin/google-chrome \
  --user-data-dir=/opt/hermes-sellersprite/chrome-profile \
  --remote-debugging-address=127.0.0.1 \
  --remote-debugging-port=9222 \
  --no-first-run --no-default-browser-check \
  https://www.amazon.com/'

# 验证 CDP 可用
curl http://127.0.0.1:9222/json/version
# 应返回 Browser/Protocol-Version 等 JSON 信息
```

⚠️ **不能同时**让 systemd 服务打开 Chrome 和手动打开 Chrome 使用同一个 profile，否则第二个启动的会报：
```
Opening in existing browser session.
```
需要先清理 SingletonLock：
```bash
rm -f /opt/hermes-sellersprite/chrome-profile/SingletonLock
rm -f /opt/hermes-sellersprite/chrome-profile/SingletonSocket
rm -f /opt/hermes-sellersprite/chrome-profile/SingletonCookie
```

---

## 十一、完整踩坑汇总表

| 序号 | 坑 | 实际症状 | 诊断方法 | 根因 | 修复 |
|------|-----|---------|---------|------|------|
| 1 | Playwright 默认禁用扩展 | warmup 成功，Amazon 页面无插件 UI | 查 Chrome 启动参数发现 `--disable-extensions` 排在 `--load-extension` 前面 | Playwright 默认注入 `--disable-extensions`，优先级高于 `--load-extension` | `ignoreDefaultArgs: ['--disable-extensions']` |
| 2 | hermes 用户 Node v18 | 服务启动报 `Playwright requires Node.js 20+` | `su - hermes -c 'node --version'` 输出 v18 | hermes 的 `/usr/bin/node` 是系统自带 v18 | 复制 root 的 v22 到 `/usr/local/bin/node`（不要 symlink！） |
| 3 | symlink 到 /root 无权限 | hermes 用户报 `Permission denied` 于 `/usr/local/bin/node` | `ls -la /usr/local/bin/node` 显示 `-> /root/.hermes/...` | hermes 用户无法遍历 `/root` 目录 | 用 `cp` 复制真实文件，不要 `ln -s` |
| 4 | xfce4 VNC 秒退 | `vncserver :1` 报 `Session startup cleanly exited too early` | 查看 `/home/hermes/.vnc/*.log` | xfce4 需要 dbus，但 VNC 没启动 dbus | xstartup 用 `dbus-launch --exit-with-session startxfce4` |
| 5 | Chrome profile 锁 | 手动关 Chrome 后服务无法 warmup | warmup 返回 `Opening in existing browser session` | Chrome 异常退出未清理锁文件 | `rm -f chrome-profile/SingletonLock SingletonSocket SingletonCookie` |
| 6 | pkill -f "chrome" 误杀终端 | 执行后终端断开连接 | — | `pkill -f "chrome"` 匹配到 chrome-devtools-mcp 等进程，包括自己的 session | 用 `ps aux | grep` 精确匹配 `google-chrome`，逐进程 kill |
| 7 | 手动 Chrome 与服务 Chrome 冲突 | 一个 Chrome 打开 profile 后另一个无法打开 | 第二个 Chrome 瞬间退出 | Chrome 不允许两个实例用同一 profile | 规则：手动装插件时停服务；自动化时关手动 Chrome |
| 8 | EADDRINUSE 端口冲突 | `systemctl restart` 后服务反复退出 | journalctl 显示 `EADDRINUSE :::8787` | 之前的 node 进程没被杀干净 | `fuser -k 8787/tcp` 再 restart |

---

## 十二、自动化服务 API 参考

### warmup（启动浏览器）
```bash
curl -X POST http://127.0.0.1:8787/browser/warmup \
  -H "Authorization: Bearer TOKEN"
```

### 运行动态工作流
```bash
curl -X POST http://127.0.0.1:8787/workflows/run \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"workflow":{"name":"任务名","steps":[...]}}'
```

### 支持的 action 类型
`goto` | `click` | `fill` | `press` | `waitForSelector` | `waitForTimeout` | `screenshot` | `exportDownload` | `evaluate` | `clickAt` | `observe`

### 读取截图/下载文件
```
/opt/hermes-sellersprite/downloads/
```
API 返回的 `artifacts[].path` 即文件绝对路径。

---

## 十三、日常运维速查

```bash
# 查看服务状态
systemctl status hermes-sellersprite

# 查看日志
journalctl -u hermes-sellersprite --no-pager -n 50

# 重启服务
systemctl restart hermes-sellersprite

# 手动操作前停服务
systemctl stop hermes-sellersprite
# ... VNC 打开 Chrome 操作 ...
# 操作完关闭 Chrome，再启动服务
systemctl start hermes-sellersprite

# 确认 noVNC 还在（重启后可能丢失）
websockify --web=/usr/share/novnc/ 127.0.0.1:6080 127.0.0.1:5901 &

# 确认 VNC 还在
su -s /bin/bash hermes -c 'vncserver -list'
```