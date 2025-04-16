import os
import requests
import json
from typing import Dict, Any, Optional
from base64 import b64encode
from mcp_server_qiwei.app_config import AppConfig

class QweiClient:
    def __init__(self):
        """
        使用配置文件中的常量进行初始化
        """
        config = AppConfig()
        self.bot_url = config.bot_url

    def send_message(self, data: Dict[str, Any]):
        chat_data = {
            'msgtype': 'markdown',
            'markdown': {
                'content': data['msg']
            }
        }
        headers = {'Content-Type': 'application/json'}
        response = requests.post(
            url=self.bot_url,
            headers=headers,
            json=chat_data,
            timeout=500
        )
        
        return response.text
   