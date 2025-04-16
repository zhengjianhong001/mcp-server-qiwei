import os
import argparse
from dotenv import load_dotenv
import configparser
from typing import Dict, Any, Optional

class AppConfig:
    def __init__(self):
        # 定义参数默认值和必填性
        self.params_meta = {
            "bot_url": {"required": False, "type": str, "default": None},
        }
        # 加载配置
        self.config = self._load_all_configs()

    def _load_cli_args(self) -> Dict[str, Any]:
        """从命令行参数获取配置"""
        parser = argparse.ArgumentParser()
        parser.add_argument("--bot-url", help="QiWei Bot URL")
        args, _ = parser.parse_known_args()
        
        return {
            "bot_url": args.bot_url,
        }

    def _load_env_vars(self) -> Dict[str, Any]:
        """从环境变量获取配置"""
        return {
            "bot_url": os.getenv("BOT_URL"),
        }

    def _load_dotenv(self) -> Dict[str, Any]:
        """从 .env 文件获取配置"""
        load_dotenv()
        return self._load_env_vars()  # 复用环境变量加载逻辑

    def _merge_configs(self, *config_sources) -> Dict[str, Any]:
        """按优先级合并配置源"""
        merged = {}
        for source in config_sources:
            for param, value in source.items():
                if value is not None and merged.get(param) is None:
                    merged[param] = value
        return merged

    def _type_cast(self, raw_config: Dict[str, Any]) -> Dict[str, Any]:
        """类型转换和验证"""
        processed = {}
        for param, meta in self.params_meta.items():
            raw_value = raw_config.get(param)
            
            # 应用默认值（当未配置且允许默认值时）
            if raw_value is None and not meta["required"]:
                processed[param] = meta["default"]
                continue

            # 必填参数校验
            if meta["required"] and raw_value is None:
                raise ValueError(f"参数 {param} 为必填项！")

            # 类型转换
            try:
                if meta["type"] == bool:
                    # 处理布尔类型（支持 true/1/yes）
                    processed[param] = str(raw_value).lower() in ("true", "1", "yes")
                else:
                    processed[param] = meta["type"](raw_value)
            except (ValueError, TypeError):
                raise TypeError(f"参数 {param} 类型错误，期望 {meta['type'].__name__}")
        
        return processed

    def _load_all_configs(self) -> Dict[str, Any]:
        """加载并合并所有配置源"""
        # 按优先级加载配置（从高到低）
        cli_config = self._load_cli_args()
        env_config = self._load_env_vars()
        dotenv_config = self._load_dotenv()

        # 合并配置
        merged_raw = self._merge_configs(
            cli_config, env_config, dotenv_config
        )

        # 类型转换和验证
        return self._type_cast(merged_raw)

    def get(self, param_name: str) -> Optional[Any]:
        """获取配置项"""
        return self.config.get(param_name)

    def __getattr__(self, name: str) -> Any:
        """支持属性式访问"""
        if name in self.config:
            return self.config[name]
        raise AttributeError(f"未找到配置项: {name}")
