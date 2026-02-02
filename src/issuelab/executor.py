"""并行执行器：同时运行多个代理"""
import asyncio
import os
from pathlib import Path
from anthropic import Anthropic


PROMPTS_DIR = Path(__file__).parent.parent.parent / "prompts"


def load_prompt(agent_name: str) -> str:
    """加载代理提示词"""
    prompts = {
        "moderator": "moderator.md",
        "reviewer_a": "reviewer_a.md",
        "reviewer_b": "reviewer_b.md",
        "summarizer": "summarizer.md",
    }
    if agent_name not in prompts:
        return ""
    prompt_path = PROMPTS_DIR / prompts[agent_name]
    if prompt_path.exists() and prompt_path.is_file():
        return prompt_path.read_text()
    return ""


async def run_agent(issue_number: int, agent_name: str, context: str) -> str:
    """运行单个代理"""
    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    prompt = f"""请对 GitHub Issue #{issue_number} 执行以下任务：

{context}

请以 [Agent: {agent_name}] 为前缀发布你的回复。"""

    try:
        response = client.messages.create(
            model="sonnet-4-20250514",
            max_tokens=4096,
            system=load_prompt(agent_name),
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
    except Exception as e:
        return f"[Error] {agent_name} failed: {e}"


async def run_parallel_agents(issue_number: int, agents: list[str]):
    """并行运行多个代理"""
    # 获取 Issue 上下文（简化：空上下文）
    context = ""

    # 并行执行
    tasks = [run_agent(issue_number, agent, context) for agent in agents]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # 打印结果
    for i, result in enumerate(results):
        print(f"\n=== {agents[i]} result ===")
        if isinstance(result, Exception):
            print(f"Error: {result}")
        else:
            print(result)
