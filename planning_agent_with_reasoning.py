"""
Planning Agent with Reasoning (No API Required!)
==================================================

This example shows how agents PLAN and REASON to solve complex tasks.
This is what makes agents truly intelligent - breaking big goals into steps!

No installation needed - just run:
    python3 planning_agent_with_reasoning.py
"""

from datetime import datetime
import json

# ============================================
# STEP 1: Tools (More Advanced!)
# ============================================

def book_flight(destination, date):
    """Book a flight"""
    return {
        "success": True,
        "booking_id": "FL12345",
        "message": f"✓ Flight booked to {destination} on {date}"
    }


def book_hotel(destination, check_in, nights):
    """Book a hotel"""
    return {
        "success": True,
        "booking_id": "HT67890",
        "message": f"✓ Hotel booked in {destination} for {nights} nights starting {check_in}"
    }


def check_weather(location, date):
    """Check weather forecast"""
    weather_options = ["sunny ☀️", "rainy 🌧️", "cloudy ☁️", "partly cloudy ⛅"]
    import random
    random.seed(hash(location + date))  # Deterministic "random"
    return {
        "success": True,
        "weather": random.choice(weather_options),
        "message": f"Weather in {location} on {date}: {random.choice(weather_options)}"
    }


def calculate_budget(items):
    """Calculate total budget"""
    costs = {
        "flight": 350,
        "hotel_per_night": 120,
        "food_per_day": 50,
        "activities": 200
    }
    
    total = 0
    breakdown = []
    
    for item, quantity in items.items():
        if item in costs:
            cost = costs[item] * quantity
            total += cost
            breakdown.append(f"{item}: ${cost}")
    
    return {
        "success": True,
        "total": total,
        "breakdown": breakdown,
        "message": f"✓ Total budget: ${total}"
    }


def send_itinerary(email, details):
    """Send itinerary to email"""
    return {
        "success": True,
        "message": f"✓ Itinerary sent to {email}"
    }


# ============================================
# STEP 2: Planning System (NEW!)
# ============================================

class TaskPlanner:
    """
    Breaks down complex goals into executable steps.
    This is the KEY to intelligent agent behavior!
    """
    
    def __init__(self):
        self.plan_templates = {
            "plan_trip": [
                {"step": "check_weather", "description": "Check weather at destination"},
                {"step": "calculate_budget", "description": "Calculate trip budget"},
                {"step": "book_flight", "description": "Book flight tickets"},
                {"step": "book_hotel", "description": "Reserve hotel room"},
                {"step": "send_itinerary", "description": "Send confirmation email"}
            ],
            "organize_event": [
                {"step": "calculate_budget", "description": "Estimate event costs"},
                {"step": "check_weather", "description": "Check weather forecast"},
                {"step": "send_itinerary", "description": "Send invitations"}
            ],
            "plan_meeting": [
                {"step": "check_weather", "description": "Check weather for outdoor option"},
                {"step": "send_itinerary", "description": "Send meeting details"}
            ]
        }
    
    def create_plan(self, goal, context):
        """
        Create a step-by-step plan to achieve a goal.
        In real agents, an LLM does this dynamically.
        """
        # Identify goal type
        goal_lower = goal.lower()
        
        if any(word in goal_lower for word in ["trip", "vacation", "travel", "visit"]):
            plan_type = "plan_trip"
            # Extract parameters from context
            destination = context.get("destination", "Paris")
            date = context.get("date", "June 15")
            nights = context.get("nights", 3)
            email = context.get("email", "user@example.com")
            
            return {
                "goal": goal,
                "plan_type": plan_type,
                "steps": self.plan_templates[plan_type],
                "parameters": {
                    "destination": destination,
                    "date": date,
                    "nights": nights,
                    "email": email
                }
            }
        
        elif any(word in goal_lower for word in ["event", "party", "gathering"]):
            plan_type = "organize_event"
            return {
                "goal": goal,
                "plan_type": plan_type,
                "steps": self.plan_templates[plan_type],
                "parameters": context
            }
        
        else:
            # Default simple plan
            return {
                "goal": goal,
                "plan_type": "generic",
                "steps": [{"step": "analyze", "description": "Analyze the request"}],
                "parameters": context
            }
    
    def explain_plan(self, plan):
        """Generate human-readable plan explanation"""
        explanation = [f"\n📋 PLAN TO: {plan['goal']}"]
        explanation.append(f"├─ Strategy: {plan['plan_type']}")
        explanation.append(f"├─ Total steps: {len(plan['steps'])}")
        explanation.append("└─ Steps:")
        
        for i, step in enumerate(plan['steps'], 1):
            prefix = "   ├─" if i < len(plan['steps']) else "   └─"
            explanation.append(f"{prefix} {i}. {step['description']}")
        
        return "\n".join(explanation)


# ============================================
# STEP 3: Reasoning Engine
# ============================================

class ReasoningEngine:
    """
    Handles the thinking process:
    - Why are we doing this step?
    - What do we expect to learn?
    - Should we continue or adapt?
    """
    
    def __init__(self):
        self.reasoning_log = []
    
    def reason_about_step(self, step, step_number, total_steps, context):
        """
        Think about why this step is necessary
        """
        reasoning = {
            "step_number": step_number,
            "step_name": step.get("step"),
            "timestamp": datetime.now()
        }
        
        # Explain WHY this step matters
        if step.get("step") == "check_weather":
            reasoning["why"] = "Need to know weather to pack appropriately and plan activities"
            reasoning["expected_output"] = "Weather forecast"
        
        elif step.get("step") == "calculate_budget":
            reasoning["why"] = "Need to ensure trip is affordable and plan spending"
            reasoning["expected_output"] = "Total cost breakdown"
        
        elif step.get("step") == "book_flight":
            reasoning["why"] = "Must secure transportation to destination"
            reasoning["expected_output"] = "Flight confirmation"
        
        elif step.get("step") == "book_hotel":
            reasoning["why"] = "Need accommodation at destination"
            reasoning["expected_output"] = "Hotel reservation"
        
        elif step.get("step") == "send_itinerary":
            reasoning["why"] = "Finalize and share complete travel plans"
            reasoning["expected_output"] = "Email confirmation"
        
        else:
            reasoning["why"] = "Required to progress toward goal"
            reasoning["expected_output"] = "Step completion"
        
        # Determine if we should proceed
        reasoning["should_proceed"] = True
        reasoning["confidence"] = "high"
        
        self.reasoning_log.append(reasoning)
        return reasoning
    
    def get_reasoning_summary(self):
        """Summarize the reasoning process"""
        return {
            "total_decisions": len(self.reasoning_log),
            "all_successful": all(r.get("should_proceed", False) for r in self.reasoning_log)
        }


# ============================================
# STEP 4: Planning Agent
# ============================================

class PlanningAgent:
    """
    An agent that can:
    1. Understand complex goals
    2. Break them into steps (PLANNING)
    3. Reason about each step (REASONING)
    4. Execute systematically
    5. Track progress
    """
    
    def __init__(self):
        self.planner = TaskPlanner()
        self.reasoning_engine = ReasoningEngine()
        self.tools = {
            "book_flight": book_flight,
            "book_hotel": book_hotel,
            "check_weather": check_weather,
            "calculate_budget": calculate_budget,
            "send_itinerary": send_itinerary
        }
        self.execution_history = []
    
    def execute_goal(self, goal, context=None):
        """
        Main method: Take a goal and execute it intelligently
        """
        if context is None:
            context = {}
        
        print(f"\n{'='*70}")
        print(f"🎯 GOAL: {goal}")
        print(f"{'='*70}")
        
        # STEP 1: CREATE PLAN
        print("\n🧠 PLANNING PHASE...")
        plan = self.planner.create_plan(goal, context)
        print(self.planner.explain_plan(plan))
        
        # STEP 2: EXECUTE PLAN STEP-BY-STEP
        print(f"\n{'='*70}")
        print("⚙️  EXECUTION PHASE...")
        print(f"{'='*70}")
        
        results = []
        total_steps = len(plan['steps'])
        
        for i, step in enumerate(plan['steps'], 1):
            print(f"\n┌─ STEP {i}/{total_steps}: {step['description']}")
            
            # REASONING: Think about this step
            reasoning = self.reasoning_engine.reason_about_step(
                step, i, total_steps, context
            )
            print(f"│  💭 Why: {reasoning['why']}")
            print(f"│  📊 Expecting: {reasoning['expected_output']}")
            
            # EXECUTION: Do the step
            step_name = step['step']
            if step_name in self.tools:
                print(f"│  🔧 Executing tool: {step_name}")
                
                # Prepare parameters based on step
                result = self._execute_tool(step_name, plan['parameters'])
                
                if result.get('success'):
                    print(f"│  ✅ {result.get('message', 'Success')}")
                    if 'breakdown' in result:
                        for item in result['breakdown']:
                            print(f"│     • {item}")
                else:
                    print(f"│  ❌ Failed: {result.get('message', 'Unknown error')}")
                
                results.append(result)
            
            print(f"└─ Step {i} complete!\n")
        
        # STEP 3: SUMMARY
        self._print_summary(goal, plan, results)
        
        return {
            "goal": goal,
            "plan": plan,
            "results": results,
            "success": all(r.get('success', False) for r in results)
        }
    
    def _execute_tool(self, tool_name, params):
        """Execute a tool with appropriate parameters"""
        try:
            if tool_name == "check_weather":
                return self.tools[tool_name](
                    params.get('destination', 'Unknown'),
                    params.get('date', 'TBD')
                )
            
            elif tool_name == "calculate_budget":
                nights = params.get('nights', 3)
                budget_items = {
                    "flight": 1,
                    "hotel_per_night": nights,
                    "food_per_day": nights,
                    "activities": 1
                }
                return self.tools[tool_name](budget_items)
            
            elif tool_name == "book_flight":
                return self.tools[tool_name](
                    params.get('destination', 'Unknown'),
                    params.get('date', 'TBD')
                )
            
            elif tool_name == "book_hotel":
                return self.tools[tool_name](
                    params.get('destination', 'Unknown'),
                    params.get('date', 'TBD'),
                    params.get('nights', 3)
                )
            
            elif tool_name == "send_itinerary":
                return self.tools[tool_name](
                    params.get('email', 'user@example.com'),
                    params
                )
            
            else:
                return {"success": False, "message": f"Unknown tool: {tool_name}"}
        
        except Exception as e:
            return {"success": False, "message": f"Error: {str(e)}"}
    
    def _print_summary(self, goal, plan, results):
        """Print execution summary"""
        print(f"\n{'='*70}")
        print("📊 EXECUTION SUMMARY")
        print(f"{'='*70}")
        print(f"Goal: {goal}")
        print(f"Strategy: {plan['plan_type']}")
        print(f"Total steps: {len(plan['steps'])}")
        print(f"Successful: {sum(1 for r in results if r.get('success'))}/{len(results)}")
        
        reasoning_summary = self.reasoning_engine.get_reasoning_summary()
        print(f"Decisions made: {reasoning_summary['total_decisions']}")
        
        if all(r.get('success', False) for r in results):
            print("\n✅ GOAL ACHIEVED! All steps completed successfully.")
        else:
            print("\n⚠️  PARTIAL SUCCESS: Some steps failed.")
        
        print(f"{'='*70}\n")


# ============================================
# STEP 5: Show Planning Concepts
# ============================================

def show_planning_concept():
    """Explain planning and reasoning"""
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║     WHY PLANNING MAKES AGENTS INTELLIGENT               ║
    ╚══════════════════════════════════════════════════════════╝
    
    WITHOUT Planning:              WITH Planning:
    ──────────────────            ─────────────────
    
    Goal: "Plan a trip"           Goal: "Plan a trip"
    
    Agent: "I booked a hotel"     Agent: Let me break this down:
    ❌ No flight!                  1. Check weather ✓
    ❌ No budget check!            2. Calculate budget ✓
    ❌ Random order!               3. Book flight ✓
                                   4. Book hotel ✓
                                   5. Send itinerary ✓
    
    
    Planning enables:
    ✓ Breaking complex goals into manageable steps
    ✓ Executing tasks in the right order
    ✓ Reasoning about each step (WHY is it needed?)
    ✓ Tracking progress systematically
    ✓ Adapting when things change
    
    
    🧠 The Planning Process:
    
    1. UNDERSTAND the goal
       ↓
    2. DECOMPOSE into steps
       ↓
    3. REASON about each step (why? what output?)
       ↓
    4. EXECUTE in order
       ↓
    5. VERIFY success
    
    
    This is how real AI agents handle complex tasks!
    GPT-4, Claude, and other advanced agents use this pattern.
    """)


# ============================================
# STEP 6: Interactive Demo
# ============================================

if __name__ == "__main__":
    show_planning_concept()
    
    print("\n" + "🚀 LIVE DEMO ".center(70, "=") + "\n")
    
    agent = PlanningAgent()
    
    print("Watch how the agent plans and executes a complex task...\n")
    input("Press ENTER to start...")
    
    # Example 1: Complex trip planning
    result = agent.execute_goal(
        goal="Plan a vacation trip to Tokyo",
        context={
            "destination": "Tokyo",
            "date": "June 15, 2026",
            "nights": 5,
            "email": "traveler@example.com"
        }
    )
    
    print("\n" + "─"*70)
    input("\nPress ENTER for another example...")
    
    # Example 2: Different destination
    result2 = agent.execute_goal(
        goal="Plan a weekend trip to London",
        context={
            "destination": "London",
            "date": "May 20, 2026",
            "nights": 2,
            "email": "weekend.warrior@example.com"
        }
    )
    
    # Final insights
    print("\n" + "="*70)
    print("💡 KEY TAKEAWAYS")
    print("="*70)
    print("""
1. PLANNING = Intelligence
   - Breaking big goals into small, achievable steps
   - Understanding dependencies (some steps must come before others)
   
2. REASONING = Understanding WHY
   - Each step has a purpose
   - Agent knows what to expect from each action
   - Can explain its decisions
   
3. SYSTEMATIC EXECUTION
   - Follow the plan step-by-step
   - Track progress
   - Verify each step succeeds
   
4. Real AI Agents
   - GPT-4, Claude use this for complex tasks
   - They generate plans dynamically based on the goal
   - Can adapt plans if something fails
   - Chain multiple tools together intelligently

🎯 You now understand THREE core agent concepts:
   1. Tools/Actions (Example 1) ✓
   2. Memory/Context (Example 2) ✓
   3. Planning/Reasoning (Example 3) ✓
   
You're building a strong foundation in AI agents! 🚀

NEXT STEPS:
- Combine all three: Memory + Tools + Planning
- Learn about multi-agent systems
- Explore real LLM-based agents
- Build your own agent for a specific task!
""")
    print("="*70)
    
    # Show the reasoning log
    print("\n" + "🧠 REASONING LOG ".center(70, "="))
    print("Here's what the agent was thinking during execution:\n")
    
    for i, reasoning in enumerate(agent.reasoning_engine.reasoning_log, 1):
        print(f"{i}. {reasoning['step_name']}")
        print(f"   Why: {reasoning['why']}")
        print(f"   Expected: {reasoning['expected_output']}")
        print(f"   Confidence: {reasoning['confidence']}\n")
    
    print("="*70)
