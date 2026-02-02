"""GitHub 操作工具"""
import subprocess
import json
import os


def get_issue_info(issue_number: int) -> dict:
    """获取 Issue 信息"""
    result = subprocess.run(
        ["gh", "issue", "view", str(issue_number), "--json", "number,title,body,labels,comments"],
        capture_output=True, text=True,
        env={**os.environ, "GH_TOKEN": os.environ.get("GITHUB_TOKEN", "")}
    )
    if result.returncode != 0:
        return {"error": result.stderr}
    return json.loads(result.stdout)


def post_comment(issue_number: int, body: str) -> str:
    """在 Issue 下发布评论"""
    result = subprocess.run(
        ["gh", "issue", "comment", str(issue_number), "--body", body],
        capture_output=True, text=True,
        env={**os.environ, "GH_TOKEN": os.environ.get("GITHUB_TOKEN", "")}
    )
    if result.returncode != 0:
        return f"Error: {result.stderr}"
    return f"Comment posted to issue #{issue_number}"


def update_label(issue_number: int, label: str, action: str = "add") -> str:
    """更新 Issue 标签"""
    action_flag = "--add-label" if action == "add" else "--remove-label"
    result = subprocess.run(
        ["gh", "issue", "edit", str(issue_number), action_flag, label],
        capture_output=True, text=True,
        env={**os.environ, "GH_TOKEN": os.environ.get("GITHUB_TOKEN", "")}
    )
    if result.returncode != 0:
        return f"Error: {result.stderr}"
    return f"Label '{label}' {action}ed on issue #{issue_number}"
