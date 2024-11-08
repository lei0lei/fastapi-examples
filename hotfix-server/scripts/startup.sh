#!/bin/bash

# 定义项目目录和服务文件路径
PROJECT_DIR="$(dirname $(dirname $(realpath $0)))"
VENV_DIR="$PROJECT_DIR/.venv"
SERVICE_FILE="/etc/systemd/system/hotfix-server.service"
APP_MODULE="hotfix_server.main:app"
HOST="0.0.0.0"
PORT="55555"

# 进入项目根目录
cd "$PROJECT_DIR"

# 检查并创建虚拟环境
if [ ! -d "$VENV_DIR" ]; then
    echo "虚拟环境不存在，正在创建虚拟环境并安装依赖..."
    # 使用 Poetry 创建虚拟环境并安装依赖
    poetry config virtualenvs.in-project true
    poetry install
else
    echo "虚拟环境已存在，激活虚拟环境..."
fi

# 获取 uvicorn 的路径（确保服务启动时找到该路径）
UVICORN_PATH="uvicorn"

# 创建 systemd 服务文件
echo "创建 systemd 服务文件..."
sudo bash -c "cat > $SERVICE_FILE" << EOF
[Unit]
Description=Hotfix FastAPI Server
After=network.target

[Service]
Type=simple
User=$(whoami)
WorkingDirectory=$PROJECT_DIR
ExecStart=$UVICORN_PATH $APP_MODULE --host $HOST --port $PORT --reload
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# 重新加载 systemd 配置
echo "重新加载 systemd 配置..."
sudo systemctl daemon-reload

# 启动并启用服务
echo "启动并启用 FastAPI 服务..."
sudo systemctl start hotfix-server
sudo systemctl enable hotfix-server

# 检查服务状态
sudo systemctl status hotfix-server

sudo ufw allow $PORT/tcp
sudo ufw reload
