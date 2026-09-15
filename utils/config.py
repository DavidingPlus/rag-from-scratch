"""应用配置：把 .env / 系统环境变量转换成 Settings 对象。"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv as loadDotenv


class ConfigurationError(ValueError):
    """运行时配置缺失或配置值无效。"""


# 当前文件位于 utils/config.py，parents[1] 是项目根目录。
_PROJECT_ROOT = Path(__file__).resolve().parents[1]
loadDotenv(_PROJECT_ROOT / ".env")


def readPositiveFloat(name: str, default: float) -> float:
    """读取一个必须大于 0 的浮点配置。"""
    value = os.getenv(name, str(default))
    try:
        parsed = float(value)
    except ValueError as exc:
        raise ConfigurationError(f"{name} 必须是数字") from exc

    if parsed <= 0:
        raise ConfigurationError(f"{name} 必须大于 0")
    return parsed


def readNonNegativeInt(name: str, default: int) -> int:
    """读取一个大于等于 0 的整数配置。"""
    value = os.getenv(name, str(default))
    try:
        parsed = int(value)
    except ValueError as exc:
        raise ConfigurationError(f"{name} 必须是整数") from exc

    if parsed < 0:
        raise ConfigurationError(f"{name} 必须大于等于 0")
    return parsed


@dataclass(frozen=True, slots=True)
class Settings:
    """经过校验、可以直接交给客户端使用的运行时配置。"""

    apiKey: str
    baseUrl: str = "https://api.deepseek.com"
    model: str = "deepseek-flash"
    timeout: float = 30.0
    maxRetries: int = 0

    @classmethod
    def fromEnv(cls) -> "Settings":
        """从系统环境变量和项目根目录下的 .env 创建 Settings。"""
        apiKey = os.getenv("DEEPSEEK_API_KEY", "").strip()
        if not apiKey or apiKey in {
            "your_api_key_here",
            "your_deepseek_api_key_here",
        }:
            raise ConfigurationError(
                "未配置 DEEPSEEK_API_KEY，请复制 .env.example 为 .env 后填写 API Key。"
            )

        baseUrl = os.getenv(
            "DEEPSEEK_BASE_URL",
            "https://api.deepseek.com",
        ).strip()
        model = os.getenv("DEEPSEEK_MODEL", "deepseek-flash").strip()

        if not baseUrl:
            raise ConfigurationError("DEEPSEEK_BASE_URL 不能为空")
        if not model:
            raise ConfigurationError("DEEPSEEK_MODEL 不能为空")

        return cls(
            apiKey=apiKey,
            baseUrl=baseUrl,
            model=model,
            timeout=readPositiveFloat("LLM_TIMEOUT", 30.0),
            maxRetries=readNonNegativeInt("LLM_MAX_RETRIES", 0),
        )
