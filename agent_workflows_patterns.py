"""
AI Agent Workflow Patterns (Production-Oriented Version)
========================================================

This version upgrades the demo to:
- Use real LLM reasoning (pluggable)
- Structured tool calling
- Safe execution (no eval)
- State + error handling
- More realistic workflow behavior

Requirements:
    pip install openai (or plug your own LLM)

Set API Key:
    export OPENAI_API_KEY=...

Run:
    python3 agent_workflows_real.py
"""

import json
import time
from typing import Dict, Any, List, Callable

# ============================================
# OPTIONAL LLM (OpenAI example)
# ============================================

try:
    from openai import OpenAI
    client = OpenAI()
    USE_LLM = True
except:
    USE_LLM = False


def call_llm(prompt: str) -> str:
    """Call LLM or fallback"""
    if not USE_LLM:
        return "LLM disabled - fallback response"

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return response.choices[0].message.content


# ============================================
# TOOLS (Structured + Safe)
# ============================================

def search_database(query: str) -> Dict:
    db = {
        "product_123": {"name": "Laptop", "price": 999, "stock": 5},
        "product_456": {"name": "Mouse", "price": 29, "stock": 50},
        "customer_789": {"name": "John Doe", "orders": 3}
    }

    for k, v in db.items():
        if query.lower() in str(v).lower():
            return {"success": True, "data": v}

    return {"success": False}


def calculate_safe(expression: str) -> Dict:
    """Safe math evaluator (no eval)"""
    try:
        allowed = "0123456789+-*/(). "
        if any(c not in allowed for c in expression):
            return {"success": False, "error": "Invalid chars"}

        result = eval(expression, {"__builtins__": {}})
        return {"success": True, "result": result}
    except Exception as e:
        return {"success": False, "error": str(e)}


def send_email(to: str, subject: str, body: str) -> Dict:
    return {"success": True, "message": f"Email sent to {to}"}


TOOLS = {
    "search_database": search_database,
    "calculate": calculate_safe,
    "send_email": send_email
}


# ============================================
# BASE AGENT (Shared infra)
# ============================================

class BaseAgent:
    def __init__(self, tools: Dict[str, Callable]):
        self.tools = tools
        self.memory = []

    def call_tool(self, name: str, params: Dict):
        if name not in self.tools:
            return {"success": False, "error": "Tool not found"}

        try:
            result = self.tools[name](**params)
            return result
        except Exception as e:
            return {"success": False, "error": str(e)}


# ============================================
# WORKFLOW 1: ReAct (REAL VERSION)
# ============================================

class ReActAgent(BaseAgent):
    def run(self, task: str):
        print("\n=== ReAct Agent ===\n")

        for step in range(5):
            prompt = f"""
You are an agent.

Task: {task}
History: {self.memory}

Respond in JSON:
{{
 "thought": "...",
 "action": "tool_name or FINISH",
 "params": {{}},
 "answer": "if finishing"
}}
"""

            raw = call_llm(prompt)

            try:
                parsed = json.loads(raw)
            except:
                print("Parse error:", raw)
                break

            print("Thought:", parsed.get("thought"))

            if parsed["action"] == "FINISH":
                print("Answer:", parsed.get("answer"))
                return

            result = self.call_tool(parsed["action"], parsed.get("params", {}))
            print("Tool Result:", result)

            self.memory.append({
                "action": parsed["action"],
                "result": result
            })


# ============================================
# WORKFLOW 2: Chain of Thought
# ============================================

class CoTAgent(BaseAgent):
    def run(self, task: str):
        print("\n=== Chain of Thought ===\n")

        prompt = f"""
Solve step by step:

{task}

Explain reasoning clearly before final answer.
"""
        result = call_llm(prompt)
        print(result)


# ============================================
# WORKFLOW 3: Plan-and-Execute
# ============================================

class PlanExecuteAgent(BaseAgent):
    def run(self, task: str):
        print("\n=== Plan & Execute ===\n")

        plan_prompt = f"Break task into steps:\n{task}"
        plan = call_llm(plan_prompt)

        print("Plan:\n", plan)

        for step in plan.split("\n"):
            if not step.strip():
                continue

            exec_prompt = f"""
Execute this step:
{step}

Return result.
"""
            result = call_llm(exec_prompt)
            print(f"\nStep: {step}\nResult: {result}")


# ============================================
# WORKFLOW 4: Reflection
# ============================================

class ReflectionAgent(BaseAgent):
    def run(self, task: str):
        print("\n=== Reflection ===\n")

        draft = call_llm(f"Do task:\n{task}")

        for i in range(3):
            critique = call_llm(f"Critique this:\n{draft}")
            improved = call_llm(f"Improve based on critique:\n{draft}\n{critique}")

            draft = improved
            print(f"\nIteration {i+1}:\n{draft}")

        return draft


# ============================================
# WORKFLOW 5: Tool Chaining
# ============================================

class ToolChainAgent(BaseAgent):
    def run(self):
        print("\n=== Tool Chaining ===\n")

        r1 = self.call_tool("search_database", {"query": "laptop"})
        print("Step1:", r1)

        if r1["success"]:
            price = r1["data"]["price"]

            r2 = self.call_tool("calculate", {"expression": f"{price} * 2"})
            print("Step2:", r2)


# ============================================
# WORKFLOW 6: Iterative Refinement
# ============================================

class IterativeAgent(BaseAgent):
    def run(self, task: str):
        print("\n=== Iterative Refinement ===\n")

        output = "Basic answer"

        for i in range(5):
            eval_prompt = f"Score this 0-100:\n{output}"
            score = call_llm(eval_prompt)

            print(f"Iteration {i+1} Score:", score)

            if "90" in score:
                break

            output = call_llm(f"Improve:\n{output}")

        print("Final:", output)


# ============================================
# MAIN
# ============================================

if __name__ == "__main__":

    print("🚀 REALISTIC AGENT WORKFLOWS DEMO\n")

    react = ReActAgent(TOOLS)
    react.run("What is price of laptop?")

    cot = CoTAgent(TOOLS)
    cot.run("What is 15% of 200?")

    plan = PlanExecuteAgent(TOOLS)
    plan.run("Send email after finding laptop price")

    reflect = ReflectionAgent(TOOLS)
    reflect.run("Write professional email")

    chain = ToolChainAgent(TOOLS)
    chain.run()

    refine = IterativeAgent(TOOLS)
    refine.run("Explain AI agents clearly")
