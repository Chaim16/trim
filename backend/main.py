import uvicorn
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
load_dotenv()

from utils.other import read_yaml_config
from utils.system import init_app
from utils.constains import APP_NAME
from utils.logger import get_logger

logger = get_logger("main")


app = FastAPI(
    title=APP_NAME,
    description="描述",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """主页"""
    return FileResponse("frontend/index.html")

# 先初始化应用，加载路由
init_app(app)
logger.info("应用初始化完成")

# 处理前端路由，所有非API路径都返回index.html
@app.get("/{path:path}")
async def catch_all(path: str):
    # 检查是否是API路径
    if path.startswith("api/"):
        return {"detail": "Not Found"}
    
    # 返回前端首页，让前端路由处理
    return FileResponse("frontend/index.html")



if __name__ == '__main__':
    server_config = read_yaml_config().get("server")
    host = server_config.get("host", "0.0.0.0")
    port = server_config.get("port", 8001)
    logger.info(f"启动服务器: {host}:{port}")
    uvicorn.run("main:app", host=host, port=port, log_level="info")
