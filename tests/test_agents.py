"""测试代理模块"""
import pytest
from issuelab.agents import load_prompt, AGENT_ALIASES, normalize_agent_name, get_available_agents


def test_agent_aliases_mapping():
    """代理别名映射表必须正确"""
    # Moderator 别名
    assert AGENT_ALIASES["moderator"] == "moderator"
    assert AGENT_ALIASES["mod"] == "moderator"

    # ReviewerA 别名
    assert AGENT_ALIASES["reviewer"] == "reviewer_a"
    assert AGENT_ALIASES["reviewera"] == "reviewer_a"
    assert AGENT_ALIASES["reva"] == "reviewer_a"

    # ReviewerB 别名
    assert AGENT_ALIASES["reviewerb"] == "reviewer_b"
    assert AGENT_ALIASES["revb"] == "reviewer_b"

    # Summarizer 别名
    assert AGENT_ALIASES["summarizer"] == "summarizer"
    assert AGENT_ALIASES["summary"] == "summarizer"


def test_load_prompt_returns_string():
    """load_prompt 应该返回字符串"""
    result = load_prompt("moderator")
    assert isinstance(result, str)


def test_load_prompt_unknown_agent():
    """load_prompt 对未知代理返回空字符串"""
    result = load_prompt("unknown_agent")
    assert result == ""


def test_normalize_agent_name():
    """normalize_agent_name 应该返回标准化名称"""
    assert normalize_agent_name("mod") == "moderator"
    assert normalize_agent_name("MODERATOR") == "moderator"
    assert normalize_agent_name("reviewer") == "reviewer_a"
    assert normalize_agent_name("revb") == "reviewer_b"
    assert normalize_agent_name("summary") == "summarizer"


def test_get_available_agents():
    """get_available_agents 应该返回所有可用代理"""
    agents = get_available_agents()
    assert "moderator" in agents
    assert "reviewer_a" in agents
    assert "reviewer_b" in agents
    assert "summarizer" in agents
    assert len(agents) == 4
