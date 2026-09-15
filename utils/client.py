"""统一创建 OpenAI-compatible 模型客户端。"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from openai import OpenAI

from .config import Settings


def buildClient(settings: Settings | None = None) -> OpenAI:
    """创建一个已经配置好的 OpenAI-compatible 客户端。"""
    # 延迟导入 SDK，使仅检查配置模块时不必创建客户端。
    from openai import OpenAI

    runtimeSettings = settings or Settings.fromEnv()
    return OpenAI(
        api_key=runtimeSettings.apiKey,
        base_url=runtimeSettings.baseUrl,
        timeout=runtimeSettings.timeout,
        max_retries=runtimeSettings.maxRetries,
    )
