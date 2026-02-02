"""代理工厂模块：创建和管理评审代理"""
from pathlib import Path

# 提示词文件映射
PROMPTS_DIR = Path(__file__).parent.parent.parent / "prompts"

PROMPT_FILES = {
    "moderator": "moderator.md",
    "reviewer_a": "reviewer_a.md",
    "reviewer_b": "reviewer_b.md",
    "summarizer": "summarizer.md",
}

# 代理别名映射表（用于 @mention 解析）
AGENT_ALIASES = {
    # Moderator 别名
    "moderator": "moderator",
    "mod": "moderator",
    # ReviewerA 别名
    "reviewer": "reviewer_a",
    "reviewera": "reviewer_a",
    "reviewer_a": "reviewer_a",
    "reva": "reviewer_a",
    # ReviewerB 别名
    "reviewerb": "reviewer_b",
    "reviewer_b": "reviewer_b",
    "revb": "reviewer_b",
    # Summarizer 别名
    "summarizer": "summarizer",
    "summary": "summarizer",
}


def load_prompt(agent_name: str) -> str:
    """加载代理提示词

    Args:
        agent_name: 代理名称（如 'moderator', 'reviewer_a'）

    Returns:
        提示词内容，若不存在则返回空字符串
    """
    prompt_file = PROMPT_FILES.get(agent_name)
    if prompt_file:
        prompt_path = PROMPTS_DIR / prompt_file
        if prompt_path.exists():
            return prompt_path.read_text()
    return ""


def normalize_agent_name(name: str) -> str:
    """标准化代理名称

    Args:
        name: 原始名称（可能包含别名）

    Returns:
        标准化的代理名称
    """
    return AGENT_ALIASES.get(name.lower(), name)


def get_available_agents() -> list[str]:
    """获取所有可用代理名称

    Returns:
        代理名称列表
    """
    return list(PROMPT_FILES.keys())
