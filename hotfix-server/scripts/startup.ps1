# 设置项目路径和虚拟环境路径
$ProjectDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$VenvDir = Join-Path $ProjectDir ".venv"
$AppModule = "hotfix_server.main:app" # FastAPI 应用模块路径
$Host = "0.0.0.0"
$Port = "8000"
$ServiceName = "HotfixFastAPIServer"

# 检查并创建虚拟环境
if (!(Test-Path -Path $VenvDir)) {
    Write-Output "虚拟环境不存在，正在创建虚拟环境并安装依赖..."
    # 使用 Poetry 创建虚拟环境并安装依赖
    poetry config virtualenvs.in-project true
    poetry install
} else {
    Write-Output "虚拟环境已存在，跳过创建步骤。"
}

# 获取 uvicorn 路径
$UvicornPath = Join-Path $VenvDir "Scripts\uvicorn.exe"

# PowerShell 脚本用于启动 FastAPI 服务的命令
$ExecStart = "$UvicornPath $AppModule --host $Host --port $Port --reload"

# 创建服务
Write-Output "创建 Windows 服务..."
$Service = Get-Service -Name $ServiceName -ErrorAction SilentlyContinue
if ($null -eq $Service) {
    New-Service -Name $ServiceName -BinaryPathName "powershell -NoProfile -ExecutionPolicy Bypass -Command `"$ExecStart`"" -DisplayName "Hotfix FastAPI Server" -StartupType Automatic
} else {
    Write-Output "服务已存在，跳过创建步骤。"
}

# 启动并设置服务
Write-Output "启动并设置服务开机自启..."
Start-Service -Name $ServiceName

# 检查服务状态
Write-Output "检查服务状态..."
Get-Service -Name $ServiceName | Select-Object Status, DisplayName
