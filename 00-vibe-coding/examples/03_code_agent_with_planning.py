"""
完整的代码 Agent 示例（具有规划能力）

这是一个功能完整的代码助手 Agent，具备以下能力：
1. **任务规划（Planning）**：将复杂任务分解为多个子任务
2. **记忆系统（Memory）**：保存对话历史和重要信息
3. **工具执行（Action）**：调用各种代码相关工具
4. **错误处理**：自动重试和错误恢复
5. **可观测性**：详细的日志记录

## 应用场景
- 代码审查和质量检查
- 自动生成单元测试
- 代码重构建议
- 文档生成

## 前置知识
- Python 面向对象编程
- 装饰器和高阶函数
- 异常处理
- LangChain 框架基础

## 安装依赖
pip install langchain langchain-openai

## 环境变量
export OPENAI_API_KEY=your_key_here

## 运行方式
python 03_code_agent_with_planning.py
"""

import logging
import time
import json
from typing import List, Dict, Any
from dataclasses import dataclass
from enum import Enum

from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

# ============================================================================
# 配置日志系统
# ============================================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ============================================================================
# 定义任务和计划的数据结构
# ============================================================================

class TaskStatus(Enum):
    """任务状态枚举"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class Task:
    """任务数据类"""
    id: int
    description: str
    status: TaskStatus
    result: str = ""
    error: str = ""


class TaskPlanner:
    """任务规划器"""

    def __init__(self):
        self.tasks: List[Task] = []
        self.current_task_id = 0

    def add_task(self, description: str) -> int:
        """添加新任务"""
        task = Task(
            id=self.current_task_id,
            description=description,
            status=TaskStatus.PENDING
        )
        self.tasks.append(task)
        task_id = self.current_task_id
        self.current_task_id += 1
        logger.info(f"新任务已添加 [ID: {task_id}]: {description}")
        return task_id

    def get_task(self, task_id: int) -> Task:
        """获取指定任务"""
        for task in self.tasks:
            if task.id == task_id:
                return task
        raise ValueError(f"任务 {task_id} 不存在")

    def update_status(self, task_id: int, status: TaskStatus, result: str = "", error: str = ""):
        """更新任务状态"""
        task = self.get_task(task_id)
        task.status = status
        task.result = result
        task.error = error
        logger.info(f"任务状态已更新 [ID: {task_id}]: {status.value}")

    def get_summary(self) -> str:
        """获取任务摘要"""
        summary = "任务计划概览:\n"
        for task in self.tasks:
            status_icon = {
                TaskStatus.PENDING: "⏳",
                TaskStatus.IN_PROGRESS: "🔄",
                TaskStatus.COMPLETED: "✅",
                TaskStatus.FAILED: "❌"
            }[task.status]
            summary += f"{status_icon} [ID: {task.id}] {task.description} - {task.status.value}\n"
        return summary


# ============================================================================
# 初始化全局状态
# ============================================================================

# 全局任务规划器
planner = TaskPlanner()

# 代码库（模拟）
code_repository = {}


# ============================================================================
# 定义工具集
# ============================================================================

@tool
def create_plan(task_description: str, subtasks: str) -> str:
    """
    创建任务计划

    将复杂任务分解为多个子任务并添加到计划中。

    参数：
        task_description: 主任务描述
        subtasks: 子任务列表，JSON 格式，例如：["子任务1", "子任务2"]

    返回：
        计划创建的结果
    """
    try:
        subtask_list = json.loads(subtasks)
        logger.info(f"开始创建计划：{task_description}")

        for subtask in subtask_list:
            planner.add_task(subtask)

        return f"成功创建计划，包含 {len(subtask_list)} 个子任务\n{planner.get_summary()}"
    except Exception as e:
        error_msg = f"创建计划失败: {str(e)}"
        logger.error(error_msg)
        return error_msg


@tool
def analyze_code(code: str, language: str = "python") -> str:
    """
    分析代码质量

    检查代码的潜在问题、复杂度、可读性等。

    参数：
        code: 要分析的代码
        language: 编程语言（默认 python）

    返回：
        代码分析报告
    """
    logger.info(f"开始分析 {language} 代码...")

    # 模拟代码分析（实际应该使用 AST 或静态分析工具）
    issues = []

    # 检查代码长度
    lines = code.strip().split('\n')
    if len(lines) > 50:
        issues.append("⚠️ 函数过长，建议拆分为更小的函数")

    # 检查文档字符串
    if '"""' not in code and "'''" not in code:
        issues.append("⚠️ 缺少文档字符串")

    # 检查注释
    comment_lines = [line for line in lines if line.strip().startswith('#')]
    if len(comment_lines) < len(lines) * 0.1:
        issues.append("⚠️ 注释较少，建议增加注释")

    report = f"代码分析报告（{language}）\n"
    report += f"总行数: {len(lines)}\n"
    report += f"注释行: {len(comment_lines)}\n"
    report += f"\n发现的问题:\n"

    if issues:
        for issue in issues:
            report += f"  {issue}\n"
    else:
        report += "  ✅ 未发现明显问题\n"

    return report


@tool
def generate_tests(code: str, function_name: str) -> str:
    """
    为代码生成单元测试

    参数：
        code: 源代码
        function_name: 要测试的函数名

    返回：
        生成的测试代码
    """
    logger.info(f"为函数 '{function_name}' 生成测试...")

    # 模拟测试生成（实际应该使用 AI 分析函数行为）
    test_code = f'''import unittest

class Test{function_name.capitalize()}(unittest.TestCase):
    """测试 {function_name} 函数"""

    def test_basic_case(self):
        """测试基本用例"""
        # TODO: 实现基本测试用例
        pass

    def test_edge_cases(self):
        """测试边界情况"""
        # TODO: 实现边界测试
        pass

    def test_error_handling(self):
        """测试错误处理"""
        # TODO: 实现错误处理测试
        pass


if __name__ == '__main__':
    unittest.main()
'''

    return f"已生成测试代码:\n\n```python\n{test_code}\n```"


@tool
def run_tests(test_code: str) -> str:
    """
    运行单元测试（模拟）

    参数：
        test_code: 测试代码

    返回：
        测试结果
    """
    logger.info("运行单元测试...")

    # 模拟测试运行
    time.sleep(0.5)

    result = """测试运行结果:

运行了 3 个测试
✅ test_basic_case: 通过
⚠️ test_edge_cases: 跳过（未实现）
⚠️ test_error_handling: 跳过（未实现）

总结: 1 passed, 2 skipped, 0 failed
"""

    return result


@tool
def save_code(filename: str, code: str) -> str:
    """
    保存代码到代码库

    参数：
        filename: 文件名
        code: 代码内容

    返回：
        保存结果
    """
    code_repository[filename] = code
    logger.info(f"代码已保存: {filename}")
    return f"✅ 代码已成功保存到 {filename}"


@tool
def get_task_status() -> str:
    """
    获取当前任务计划的状态

    返回：
        任务状态摘要
    """
    return planner.get_summary()


# ============================================================================
# 配置 Agent
# ============================================================================

def create_code_agent():
    """创建代码 Agent（使用 LangChain v1.0 API）"""

    # 初始化 LLM
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
    )

    # 配置记忆（使用 Checkpointer）
    checkpointer = InMemorySaver()

    # 定义系统提示词
    system_prompt = """你是一个专业的代码助手 Agent，具备以下能力：

1. **任务规划**：将复杂任务分解为可执行的子任务
2. **代码分析**：检查代码质量和潜在问题
3. **测试生成**：自动生成单元测试
4. **执行验证**：运行测试并验证结果

## 工作流程

对于复杂任务，请遵循以下步骤：
1. 使用 create_plan 创建详细的任务计划
2. 按顺序执行每个子任务
3. 使用 get_task_status 跟踪进度
4. 在完成所有任务后提供总结

## 回答格式

思考（Thought）：分析当前需要做什么
行动（Action）：选择合适的工具
行动输入（Action Input）：工具的输入参数
观察（Observation）：工具返回的结果
... （重复上述循环直到完成任务）
思考：任务已完成
最终答案（Final Answer）：向用户报告结果
"""

    # 准备工具
    tools = [
        create_plan,
        analyze_code,
        generate_tests,
        run_tests,
        save_code,
        get_task_status
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
# 主程序
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("代码助手 Agent（具有规划能力）")
    print("=" * 80)
    print()

    # 创建 Agent
    agent = create_code_agent()

    # 配置：使用 thread_id 来维护会话状态
    config = {"configurable": {"thread_id": "1"}}

    # 示例代码
    sample_code = '''
def calculate_average(numbers):
    total = sum(numbers)
    count = len(numbers)
    return total / count
'''

    # 复杂任务示例
    print("\n【任务】完整的代码审查和测试流程")
    print("-" * 80)

    task = f"""
    请对以下代码进行完整的审查和测试流程：

    ```python
    {sample_code}
    ```

    具体要求：
    1. 创建一个详细的任务计划
    2. 分析代码质量
    3. 生成单元测试
    4. 运行测试
    5. 保存代码和测试到代码库
    6. 提供完整的总结报告
    """

    try:
        response = agent.invoke({
            "messages": [{"role": "user", "content": task}]
        }, config)
        print("\n" + "=" * 80)
        print("最终答案:")
        print("=" * 80)
        print(response['messages'][-1].content)
    except Exception as e:
        logger.error(f"执行失败: {str(e)}")
        print(f"\n❌ 执行失败: {str(e)}")

    print("\n" + "=" * 80)
    print("代码库内容:")
    print("=" * 80)
    for filename, code in code_repository.items():
        print(f"\n文件: {filename}")
        print("-" * 80)
        print(code[:200] + "..." if len(code) > 200 else code)
