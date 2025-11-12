"""
端到端集成示例：FastMCP + LangChain

这是一个完整的端到端示例，展示了如何将 FastMCP 和 LangChain 结合使用：
- FastMCP Server 暴露工具给外部客户端（如 Claude Desktop）
- LangChain Agent 在 Server 内部负责智能编排和决策
- 实现智能日程助手，能够理解自然语言并执行复杂操作

## 应用场景
- 智能日程管理：自然语言输入自动解析为日程操作
- 复杂查询：结合多个条件进行智能搜索和推荐
- 自动规划：根据上下文自动建议最佳日程安排

## 前置知识
- FastMCP 基础（示例 1）
- LangChain Agent 基础（示例 2）
- Python 异步编程基础

## 安装依赖
pip install fastmcp langchain langchain-openai

## 环境变量
export OPENAI_API_KEY=your_key_here

## 运行方式
python 04_integrated_mcp_langchain.py

## 配置客户端（以 Claude Desktop 为例）
{
  "mcpServers": {
    "smart-calendar": {
      "command": "python",
      "args": ["<绝对路径>/04_integrated_mcp_langchain.py"],
      "env": {
        "OPENAI_API_KEY": "your_key_here"
      }
    }
  }
}

## 架构说明

┌─────────────────────────────────────────────┐
│         外部客户端 (Claude Desktop)         │
└──────────────────┬──────────────────────────┘
                   │ MCP 协议
┌──────────────────▼──────────────────────────┐
│          FastMCP Server                     │
│  ┌───────────────────────────────────────┐  │
│  │  smart_schedule (MCP Tool)            │  │
│  │  - 接收自然语言输入                   │  │
│  │  - 调用内部 LangChain Agent           │  │
│  └───────────────┬───────────────────────┘  │
│                  │                           │
│  ┌───────────────▼───────────────────────┐  │
│  │  LangChain Agent (内部编排器)         │  │
│  │  - 理解用户意图                       │  │
│  │  - 提取日期、时间、标题               │  │
│  │  - 调用内部工具                       │  │
│  │  - 返回结构化结果                     │  │
│  └───────────────┬───────────────────────┘  │
│                  │                           │
│  ┌───────────────▼───────────────────────┐  │
│  │  Internal Tools                       │  │
│  │  - add_event_internal                 │  │
│  │  - search_events_internal             │  │
│  │  - suggest_time_slot                  │  │
│  └───────────────────────────────────────┘  │
└─────────────────────────────────────────────┘
"""

import os
import re
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional

from fastmcp import FastMCP, tool
from langchain_openai import ChatOpenAI
from langchain.tools import tool as lc_tool
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

# ============================================================================
# 全局数据存储
# ============================================================================

# 日程数据库（实际应用中应使用数据库）
EVENTS: List[Dict] = []

# ============================================================================
# LangChain 内部工具定义
# ============================================================================

@lc_tool
def add_event_internal(date: str, title: str, time: str = "") -> str:
    """
    添加日程到日历（内部工具）

    参数：
        date: 日期，格式 YYYY-MM-DD
        title: 日程标题
        time: 时间，格式 HH:MM（可选）

    返回：
        操作结果
    """
    event = {
        "date": date,
        "title": title,
        "time": time,
        "created_at": datetime.now().isoformat()
    }
    EVENTS.append(event)

    time_str = f" {time}" if time else ""
    return f"✅ 已成功添加日程：{date}{time_str} - {title}"


@lc_tool
def search_events_internal(keyword: str = "", date: str = "") -> str:
    """
    搜索日程（内部工具）

    参数：
        keyword: 搜索关键词（在标题中搜索）
        date: 日期过滤，格式 YYYY-MM-DD

    返回：
        匹配的日程列表
    """
    results = EVENTS.copy()

    # 按关键词过滤
    if keyword:
        kw = keyword.lower()
        results = [e for e in results if kw in e.get("title", "").lower()]

    # 按日期过滤
    if date:
        results = [e for e in results if e.get("date") == date]

    if not results:
        return "未找到匹配的日程"

    output = f"找到 {len(results)} 个日程：\n"
    for i, event in enumerate(results, 1):
        time_str = f" {event.get('time')}" if event.get('time') else ""
        output += f"{i}. {event['date']}{time_str} - {event['title']}\n"

    return output


@lc_tool
def list_all_events_internal() -> str:
    """
    列出所有日程（内部工具）

    返回：
        所有日程的格式化字符串
    """
    if not EVENTS:
        return "当前没有任何日程"

    # 按日期排序
    sorted_events = sorted(EVENTS, key=lambda x: (x.get("date", ""), x.get("time", "")))

    output = f"当前所有日程（共 {len(sorted_events)} 个）：\n"
    for i, event in enumerate(sorted_events, 1):
        time_str = f" {event.get('time')}" if event.get('time') else ""
        output += f"{i}. {event['date']}{time_str} - {event['title']}\n"

    return output


@lc_tool
def suggest_time_slot(date: str, preferred_time: str = "") -> str:
    """
    建议可用的时间段（内部工具）

    分析指定日期的日程，建议空闲时间段

    参数：
        date: 日期，格式 YYYY-MM-DD
        preferred_time: 偏好时间（如"上午"、"下午"、"晚上"）

    返回：
        推荐的时间段
    """
    # 查找该日期的所有日程
    day_events = [e for e in EVENTS if e.get("date") == date]

    if not day_events:
        return f"✅ {date} 全天空闲，随时可以安排日程"

    # 提取已占用的时间（简化版）
    occupied_times = [e.get("time", "") for e in day_events if e.get("time")]

    suggestions = []

    # 简化的时间段建议逻辑
    time_slots = {
        "上午": ["09:00", "10:00", "11:00"],
        "下午": ["14:00", "15:00", "16:00"],
        "晚上": ["19:00", "20:00"]
    }

    # 根据偏好推荐
    if preferred_time:
        pref = preferred_time
        if pref in time_slots:
            for slot in time_slots[pref]:
                if slot not in occupied_times:
                    suggestions.append(slot)
    else:
        # 推荐所有空闲时段
        for period, slots in time_slots.items():
            for slot in slots:
                if slot not in occupied_times:
                    suggestions.append(f"{slot} ({period})")

    if suggestions:
        return f"建议的空闲时间段：{', '.join(suggestions[:3])}"
    else:
        return f"{date} 的{preferred_time if preferred_time else '常规时段'}都已排满，建议选择其他日期"


@lc_tool
def parse_natural_language_date(text: str) -> str:
    """
    解析自然语言日期（内部工具）

    将"明天"、"下周一"等自然语言转换为标准日期格式

    参数：
        text: 自然语言文本

    返回：
        标准日期格式 YYYY-MM-DD 或错误信息
    """
    today = datetime.now()

    # 简化的日期解析逻辑
    if "今天" in text or "今日" in text:
        return today.strftime("%Y-%m-%d")
    elif "明天" in text or "明日" in text:
        return (today + timedelta(days=1)).strftime("%Y-%m-%d")
    elif "后天" in text:
        return (today + timedelta(days=2)).strftime("%Y-%m-%d")
    elif "下周" in text:
        return (today + timedelta(days=7)).strftime("%Y-%m-%d")

    # 尝试匹配 YYYY-MM-DD 格式
    date_pattern = r'(\d{4}[-/]\d{1,2}[-/]\d{1,2})'
    match = re.search(date_pattern, text)
    if match:
        date_str = match.group(1).replace('/', '-')
        return date_str

    # 尝试匹配 MM-DD 格式
    date_pattern = r'(\d{1,2}[-/]\d{1,2})'
    match = re.search(date_pattern, text)
    if match:
        date_str = match.group(1).replace('/', '-')
        return f"{today.year}-{date_str}"

    return f"无法解析日期：{text}。请使用明确的日期格式（如 2025-11-15）或自然语言（如明天、下周）"


# ============================================================================
# LangChain Agent 配置
# ============================================================================

def create_smart_agent():
    """创建智能日程 Agent（使用 LangChain v1.0 API）"""

    # 检查 API 密钥
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("请设置 OPENAI_API_KEY 环境变量")

    # 初始化 LLM
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.3,  # 略微提高创造性，以便更好地理解自然语言
    )

    # 配置记忆（使用 Checkpointer）
    checkpointer = InMemorySaver()

    # 定义系统提示词
    system_prompt = """你是一个智能日程助手，能够理解自然语言并帮助用户管理日程。

## 你的能力

你可以使用提供的工具来：
- 添加、搜索、列出日程
- 解析自然语言日期（如"明天"、"下周"）
- 推荐空闲时间段

## 工作流程

1. **理解意图**：分析用户的自然语言输入，理解他们想做什么
2. **提取信息**：从输入中提取日期、时间、标题等关键信息
3. **执行操作**：调用合适的工具完成任务
4. **友好反馈**：用自然、友好的方式告知用户结果

## 特殊能力

- 自动解析"明天"、"下周"等相对日期
- 智能推荐空闲时间段
- 支持模糊搜索
- 理解上下文（如"再加一个"指的是什么）

## 回答格式

思考（Thought）：分析用户意图和需要提取的信息
行动（Action）：选择合适的工具
行动输入（Action Input）：工具的参数（JSON格式）
观察（Observation）：工具返回的结果
... （重复直到完成任务）
思考：任务已完成
最终答案（Final Answer）：用友好的语言回复用户
"""

    # 准备工具
    tools = [
        add_event_internal,
        search_events_internal,
        list_all_events_internal,
        suggest_time_slot,
        parse_natural_language_date
    ]

    # 使用新的 create_agent API 创建 Agent
    # create_agent 是 LangChain v1.0 的标准方法
    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=system_prompt,
        checkpointer=checkpointer,
    )

    return agent


# ============================================================================
# FastMCP Server 定义
# ============================================================================

# 创建 FastMCP 应用
app = FastMCP("smart-calendar", version="1.0.0")

# 创建 Agent 实例（全局共享）
try:
    smart_agent = create_smart_agent()
    print("✅ LangChain Agent 初始化成功")
except Exception as e:
    print(f"⚠️ LangChain Agent 初始化失败: {e}")
    print("⚠️ smart_schedule 工具将不可用")
    smart_agent = None


@app.tool
def smart_schedule(natural_language_input: str) -> dict:
    """
    智能日程助手 - 理解自然语言并执行日程操作

    这是一个高级工具，能够理解复杂的自然语言输入，并自动执行相应的日程管理操作。

    支持的操作示例：
    - "帮我安排明天下午3点的团队会议"
    - "列出我下周的所有日程"
    - "搜索包含'项目'的日程"
    - "11月20日有哪些空闲时间？"
    - "我想在后天加个会议，什么时间比较好？"

    参数：
        natural_language_input: 自然语言描述的请求

    返回：
        包含执行结果和建议的字典
    """
    if not smart_agent:
        return {
            "status": "error",
            "message": "智能助手未初始化，请检查 OPENAI_API_KEY 配置"
        }

    try:
        # 调用 LangChain Agent 处理请求
        # 使用 thread_id 来维护会话状态
        config = {"configurable": {"thread_id": "default"}}
        response = smart_agent.invoke({
            "messages": [{"role": "user", "content": natural_language_input}]
        }, config)

        return {
            "status": "success",
            "result": response['messages'][-1].content,
            "thought_process": "详细过程请查看服务器日志"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"处理请求时出错: {str(e)}"
        }


@app.tool
def get_all_events() -> list:
    """
    获取所有日程（简单工具）

    返回所有日程的原始数据，适合需要编程处理的场景。

    返回：
        日程列表
    """
    return EVENTS


@app.tool
def add_event_simple(date: str, title: str, time: str = "") -> dict:
    """
    直接添加日程（简单工具）

    不经过智能解析，直接添加日程。适合已知确切信息的场景。

    参数：
        date: 日期，格式 YYYY-MM-DD
        title: 日程标题
        time: 时间，格式 HH:MM（可选）

    返回：
        操作结果
    """
    event = {
        "date": date,
        "title": title,
        "time": time,
        "created_at": datetime.now().isoformat()
    }
    EVENTS.append(event)

    return {
        "status": "ok",
        "data": event,
        "message": f"已添加日程：{date} {time} - {title}"
    }


@app.tool
def clear_all_events() -> dict:
    """
    清空所有日程（危险操作）

    删除所有日程数据，谨慎使用！

    返回：
        操作结果
    """
    global EVENTS
    count = len(EVENTS)
    EVENTS = []
    return {
        "status": "ok",
        "message": f"已清空 {count} 个日程"
    }


# ============================================================================
# 主程序
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("智能日程助手 MCP Server（FastMCP + LangChain 集成）")
    print("=" * 80)
    print()
    print("🚀 服务器功能：")
    print("  1. 智能工具：smart_schedule - 理解自然语言，智能执行操作")
    print("  2. 简单工具：add_event_simple - 直接添加日程")
    print("  3. 查询工具：get_all_events - 获取所有日程")
    print("  4. 管理工具：clear_all_events - 清空所有日程")
    print()
    print("📝 使用示例（在 Claude Desktop 中）：")
    print('  - "帮我安排明天下午3点的团队会议"')
    print('  - "列出我所有的日程"')
    print('  - "搜索包含项目的日程"')
    print('  - "11月20日有哪些空闲时间？"')
    print()
    print("💡 架构说明：")
    print("  - FastMCP 负责暴露工具给外部客户端")
    print("  - LangChain Agent 在内部负责智能理解和决策")
    print("  - 两者协同工作，提供智能化的用户体验")
    print()
    print("⚙️ 配置要求：")
    print("  - 环境变量：OPENAI_API_KEY")
    print("  - 依赖：fastmcp, langchain, langchain-openai")
    print()
    print("-" * 80)

    # 运行 MCP Server
    app.run()
