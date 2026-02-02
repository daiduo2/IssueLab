# IssueLab 协作生态流程图

```mermaid
flowchart TB
    subgraph Central["🌐 IssueLab 主项目生态"]
        direction TB
        Main["IssueLab 主仓库\n(GitHub Actions + Claude SDK)"]
        Issues["GitHub Issues\n(论文讨论/提案/复盘/问题)"]
    end

    subgraph Fork["👥 社区成员 Fork 流程"]
        direction LR
        Dev1["开发者 A\n(Fork 主项目)"]
        Dev2["开发者 B\n(Fork 主项目)"]
        Dev3["开发者 C\n(Fork 主项目)"]
    end

    subgraph Custom["🔧 定制化智能体开发"]
        direction TB
        ProfileA["开发者 A 的画像\n- ML Researcher\n- 关注 CV 领域"]
        ProfileB["开发者 B 的画像\n- Systems Engineer\n- 关注效率优化"]
        ProfileC["开发者 C 的画像\n- NLP Researcher\n- 关注 LLM 评估"]

        AgentA["Agent-A\n(计算机视觉专家)"]
        AgentB["Agent-B\n(系统性能专家)"]
        AgentC["Agent-C\n(NLP 评估专家)"]
    end

    subgraph Actions["⚡ GitHub Actions 触发"]
        direction TB
        Trigger["@mention 触发\n或 /command 触发"]
        Work["并行/顺序执行\n子代理协作"]
    end

    subgraph Output["📤 输出与反馈"]
        direction TB
        Review["评审意见\n(Claim/Evidence/Uncertainty)"]
        Summary["共识汇总\n(行动项清单)"]
    end

    subgraph Private["🔒 私有/小团队系统"]
        direction TB
        Team1["团队私有系统\n(基于 Fork 定制)"]
        Team2["跨团队协作\n(多仓库联动)"]
    end

    %% 主流程连接
    Central -->|Fork| Fork
    Fork --> Custom
    Custom -->|"提交 PR / 分享配置"| Central
    Custom -->|"配置 GitHub Actions"| Actions
    Actions -->|"参与讨论"| Issues
    Issues --> Review
    Review --> Summary
    Summary -->|"反馈"| Issues

    %% 私有系统
    Custom -->|"部署私有实例"| Private
    Private -->|"同步Issue"| Team1
    Private -->|"互联互通"| Team2

    %% 样式定义
    classDef central fill:#6366f1,stroke:#4f46e5,color:#fff
    classDef dev fill:#22c55e,stroke:#16a34a,color:#fff
    classDef agent fill:#f59e0b,stroke:#d97706,color:#fff
    classDef action fill:#ec4899,stroke:#db2777,color:#fff
    classDef output fill:#14b8a6,stroke:#0d9488,color:#fff
    classDef private fill:#8b5cf6,stroke:#7c3aed,color:#fff

    class Main,Issues Central
    class Dev1,Dev2,Dev3 Fork
    class AgentA,AgentB,AgentC Custom
    class Trigger,Work Actions
    class Review,Summary Output
    class Team1,Team2 Private
```

---

## 详细时序图

```mermaid
sequenceDiagram
    participant User as 👤 研究者
    participant Fork as 📦 Fork的仓库
    participant Main as 🌐 主IssueLab
    participant GH as 🐙 GitHub Issues
    participant Action as ⚡ GitHub Actions
    participant Agent as 🤖 定制智能体
    participant Team as 👥 团队私有系统

    Note over User,Main: 阶段 1: 加入生态
    User->>Main: Fork 项目到个人账号
    User->>Main: 配置 ANTHROPIC_API_KEY

    Note over User,Agent: 阶段 2: 定制智能体
    User->>Fork: 修改 prompts/xxx.md
    User->>Fork: 调整 Agent 行为逻辑
    User->>Fork: 配置专属提示词模板

    Note over User,GH: 阶段 3: 参与主项目讨论
    User->>GH: 提交 Issue (论文/提案/问题)
    User->>GH: @Mention 触发智能体
    GH->>Action: 触发 GitHub Actions

    Action->>Agent: 调用 Claude Agent SDK
    Agent->>Agent: 执行专业评审
    Agent->>GH: 发布评审意见

    Note over GH,User: 阶段 4: 总结与迭代
    GH->>User: 展示评审结果
    User->>GH: /summarize 汇总共识
    GH->>User: 输出行动项清单

    Note over User,Team: 阶段 5: 私有/团队扩展
    User->>Team: 部署私有实例
    Team->>Team: 建立团队专属知识库
    Team->>Main: 可选: PR 贡献回主项目
```

---

## 智能体画像示例

| 开发者 | 领域 | 定制方向 | 专属 Agent 名称 |
|--------|------|----------|-----------------|
| @Alice | 计算机视觉 | 图像生成质量评估 | ImageCritic |
| @Bob | 分布式系统 | 性能基准分析 | PerfExpert |
| @Carol | NLP/LLM | 推理能力评测 | LLMJudge |
| @Dave | 机器人学 | 控制策略验证 | RobotVerifier |

---

## 核心交互命令

```markdown
# 触发主项目智能体
@Moderator 分诊
@ReviewerA 正方评审
@ReviewerB 反方评审
@summarizer 汇总

# 或使用命令
/review      # 完整评审流程
/summarize   # 汇总共识
/triage      # 仅分诊
/quiet       # 静默模式
```
