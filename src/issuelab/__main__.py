"""主入口：支持多种子命令"""
import asyncio
import argparse
import os
import subprocess
import tempfile
from issuelab.sdk_executor import run_agents_parallel
from issuelab.parser import parse_mentions


def post_comment(issue_number: int, body: str) -> bool:
    """发布评论到 Issue"""
    # 使用临时文件避免命令行长度限制
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write(body)
        f.flush()
        result = subprocess.run(
            ["gh", "issue", "comment", str(issue_number), "--body-file", f.name],
            capture_output=True,
            text=True,
            env={**os.environ, "GH_TOKEN": os.environ.get("GITHUB_TOKEN", "")}
        )
        os.unlink(f.name)
    return result.returncode == 0


def main():
    parser = argparse.ArgumentParser(description="Issue Lab Agent")
    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # @mention 并行执行
    execute_parser = subparsers.add_parser("execute", help="并行执行代理")
    execute_parser.add_argument("--issue", type=int, required=True)
    execute_parser.add_argument("--agents", type=str, required=True, help="空格分隔的代理名称")
    execute_parser.add_argument("--post", action="store_true", help="自动发布结果到 Issue")

    # 顺序评审流程
    review_parser = subparsers.add_parser("review", help="运行顺序评审流程")
    review_parser.add_argument("--issue", type=int, required=True)
    review_parser.add_argument("--post", action="store_true", help="自动发布结果到 Issue")

    args = parser.parse_args()

    if args.command == "execute":
        agents = args.agents.split()
        results = asyncio.run(run_agents_parallel(args.issue, agents))

        # 输出结果
        for agent_name, response in results.items():
            print(f"\n=== {agent_name} result ===")
            print(response)

            # 如果需要，自动发布到 Issue
            if getattr(args, "post", False):
                if post_comment(args.issue, response):
                    print(f"✅ {agent_name} response posted to issue #{args.issue}")
                else:
                    print(f"❌ Failed to post {agent_name} response")

    elif args.command == "review":
        # 顺序执行：moderator -> reviewer_a -> reviewer_b -> summarizer
        agents = ["moderator", "reviewer_a", "reviewer_b", "summarizer"]
        results = asyncio.run(run_agents_parallel(args.issue, agents))

        for agent_name, response in results.items():
            print(f"\n=== {agent_name} result ===")
            print(response)

            # 如果需要，自动发布到 Issue
            if getattr(args, "post", False):
                if post_comment(args.issue, response):
                    print(f"✅ {agent_name} response posted to issue #{args.issue}")
                else:
                    print(f"❌ Failed to post {agent_name} response")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
