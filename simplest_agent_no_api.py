"""
Simplest AI Agent (No API Required!)
=====================================

This shows the PATTERN of an AI agent without needing any API keys.
It simulates how an agent thinks and acts.

No installation needed - just run:
    python3 simplest_agent_no_api.py
"""

# ============================================
# STEP 1: Define Tools (Same as real agents!)
# ============================================

def get_weather(location):
    """Get weather for a location"""
    weather_db = {
        "tokyo": "18°C, cloudy ☁️",
        "new york": "22°C, sunny ☀️",
        "london": "12°C, rainy 🌧️",
        "paris": "15°C, partly cloudy ⛅"
    }
    return weather_db.get(location.lower(), f"No data for {location}")


def calculate(expression):
    """Calculate math expressions"""
    try:
        result = eval(expression, {"__builtins__": {}})
        return str(result)
    except Exception as e:
        return f"Error: {e}"


def search_web(query):
    """Simulate web search"""
    results = {
        "ai agent": "An AI agent is a program that can perceive, reason, and act autonomously.",
        "python": "Python is a high-level programming language created by Guido van Rossum.",
        "weather": "Weather is the state of the atmosphere at a given time and place."
    }
    for key, value in results.items():
        if key in query.lower():
            return value
    return f"Search results for: {query}"


# ============================================
# STEP 2: Simple "AI Brain" (Rule-Based)
# ============================================

class SimpleBrain:
    """Simulates LLM decision-making with simple rules"""
    
    def __init__(self):
        self.tools = {
            "get_weather": get_weather,
            "calculate": calculate,
            "search_web": search_web
        }
    
    def decide_action(self, user_message):
        """
        Decide what to do based on user message.
        In real agents, an LLM does this.
        """
        msg_lower = user_message.lower()
        
        # Weather intent
        if any(word in msg_lower for word in ["weather", "temperature", "forecast"]):
            # Extract location
            for city in ["tokyo", "new york", "london", "paris"]:
                if city in msg_lower:
                    return ("get_weather", {"location": city})
            return ("get_weather", {"location": "unknown"})
        
        # Math intent
        if any(word in msg_lower for word in ["calculate", "what is", "+"," -", "*", "/"]):
            # Extract expression
            import re
            # Look for math patterns like "2+2" or "25 * 17"
            match = re.search(r'(\d+\s*[\+\-\*/]\s*\d+)', user_message)
            if match:
                return ("calculate", {"expression": match.group(1)})
        
        # Search intent
        if any(word in msg_lower for word in ["what", "who", "how", "search", "find"]):
            return ("search_web", {"query": user_message})
        
        # No tool needed
        return (None, None)
    
    def generate_response(self, tool_result, user_message):
        """Generate natural language response"""
        if tool_result:
            return f"Based on my tools, {tool_result}"
        else:
            return "I can help you with weather, calculations, or searching. What would you like to know?"


# ============================================
# STEP 3: The Agent (Same Pattern as Real!)
# ============================================

class SimpleAgent:
    """
    A simple AI agent that demonstrates the core pattern:
    Think → Act → Respond
    """
    
    def __init__(self):
        self.brain = SimpleBrain()
        self.conversation_history = []
    
    def run(self, user_message):
        """Main agent loop"""
        print(f"\n{'='*60}")
        print(f"🤔 User: {user_message}")
        print(f"{'='*60}")
        
        # STEP 1: THINK - Decide what to do
        print("💭 Agent is thinking...")
        action, params = self.brain.decide_action(user_message)
        
        tool_result = None
        
        # STEP 2: ACT - Use a tool if needed
        if action:
            print(f"🔧 Agent decided to use: {action}")
            print(f"   Parameters: {params}")
            
            # Execute the tool
            tool_function = self.brain.tools[action]
            tool_result = tool_function(**params)
            
            print(f"   ✓ Tool result: {tool_result}")
        else:
            print("💬 Agent doesn't need tools for this")
        
        # STEP 3: RESPOND - Give natural answer
        print("💭 Agent is formulating response...")
        response = self.brain.generate_response(tool_result, user_message)
        
        print(f"\n✅ Agent: {response}")
        print(f"{'='*60}\n")
        
        # Save to history
        self.conversation_history.append({
            "user": user_message,
            "action": action,
            "result": tool_result,
            "response": response
        })
        
        return response


# ============================================
# STEP 4: Visualize the Flow
# ============================================

def show_agent_pattern():
    """Show the universal agent pattern"""
    print("""
    ╔══════════════════════════════════════════╗
    ║   THE AI AGENT PATTERN (Universal!)     ║
    ╚══════════════════════════════════════════╝
    
         User Input
             │
             ▼
    ┌────────────────────┐
    │   1. PERCEIVE      │  ← Read user message
    │   (What do they    │
    │    want?)          │
    └─────────┬──────────┘
              │
              ▼
    ┌────────────────────┐
    │   2. THINK         │  ← Decide action
    │   (What should     │    (LLM or rules)
    │    I do?)          │
    └─────────┬──────────┘
              │
              ▼
         Need tools? ──No──┐
              │Yes         │
              ▼            │
    ┌────────────────────┐ │
    │   3. ACT           │ │
    │   (Use tools/      │ │
    │    functions)      │ │
    └─────────┬──────────┘ │
              │            │
              ▼            │
    ┌────────────────────┐ │
    │   4. RESPOND       │◄┘
    │   (Natural language│
    │    answer)         │
    └─────────┬──────────┘
              │
              ▼
         User gets answer
    
    This pattern works for ALL agents:
    - Simple chatbots
    - Complex multi-agent systems
    - Autonomous robots
    - Everything in between!
    """)


# ============================================
# STEP 5: Run Demo
# ============================================

if __name__ == "__main__":
    # Show the pattern first
    show_agent_pattern()
    
    print("\n" + "🚀 LIVE DEMO ".center(60, "=") + "\n")
    
    # Create agent
    agent = SimpleAgent()
    
    # Example 1: Weather tool
    agent.run("What's the weather in Tokyo?")
    
    # Example 2: Calculator tool
    agent.run("What is 25 * 17?")
    
    # Example 3: Search tool
    agent.run("What is an AI agent?")
    
    # Example 4: No tool needed
    agent.run("Hello!")
    
    # Show summary
    print("\n" + "📊 SUMMARY ".center(60, "="))
    print(f"\nTotal interactions: {len(agent.conversation_history)}")
    print("\nTools used:")
    tool_usage = {}
    for entry in agent.conversation_history:
        if entry['action']:
            tool_usage[entry['action']] = tool_usage.get(entry['action'], 0) + 1
    
    for tool, count in tool_usage.items():
        print(f"  • {tool}: {count} times")
    
    print("\n" + "="*60)
    print("\n💡 KEY TAKEAWAY:")
    print("   This is EXACTLY how real AI agents work!")
    print("   The only difference:")
    print("   - Real agents: Use LLM for thinking")
    print("   - This demo: Uses simple rules")
    print("\n   But the PATTERN is identical! 🎯")
    print("="*60)
