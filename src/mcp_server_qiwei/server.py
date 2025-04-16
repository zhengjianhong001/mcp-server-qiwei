import os
import json
import requests
from mcp.server.fastmcp import FastMCP
from mcp_server_qiwei.core import QweiClient
from mcp_server_qiwei.app_config import AppConfig

mcp = FastMCP("mcp-qiwei")
client = QweiClient()

@mcp.tool()
def send_qiwei_message(msg: str) -> dict:
    """发送信息到企业微信群
    Args:
        msg: 推送的企业微信的信息，Markdown 格式（必填）
    Returns: <str> 
    """
    data = {
        "msg": msg,
    }
    return client.send_message(data)

def main():
    mcp.run()

if __name__ == "__main__":
    mcp.run()