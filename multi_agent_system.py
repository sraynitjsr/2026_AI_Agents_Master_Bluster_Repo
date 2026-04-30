"""
Multi-Agent System - (No API Required!)
====================================================

This example shows how MULTIPLE AGENTS work together to solve complex problems.
Each agent has specialized skills, memory, and can plan - they collaborate!

This combines ALL concepts from previous examples:
✓ Tools (Example 1)
✓ Memory (Example 2)  
✓ Planning (Example 3)
✓ Multi-Agent Coordination (NEW!)

No installation needed - just run:
    python3 multi_agent_system.py
"""

from datetime import datetime
import json

# ============================================
# STEP 1: Specialized Tools for Each Agent
# ============================================

# Research Agent Tools
def search_web(query):
    """Simulate web search"""
    knowledge_base = {
        "ai agents": "AI agents are autonomous programs that perceive, reason, and act to achieve goals.",
        "python": "Python is a high-level programming language known for simplicity and readability.",
        "machine learning": "Machine learning is a subset of AI that learns from data without explicit programming.",
        "tokyo": "Tokyo is the capital of Japan, known for technology, culture, and cuisine.",
        "paris": "Paris is the capital of France, famous for art, culture, and the Eiffel Tower.",
        "climate change": "Climate change refers to long-term shifts in global temperatures and weather patterns."
    }
    
    for key, value in knowledge_base.items():
        if key in query.lower():
            return {"success": True, "data": value, "source": f"Knowledge Base: {key}"}
    
    return {"success": True, "data": f"Search results for: {query}", "source": "Web Search"}


def extract_facts(text):
    """Extract key facts from text"""
    facts = [s.strip() + "." for s in text.split(".") if len(s.strip()) > 20]
    return {"success": True, "facts": facts[:3], "count": len(facts)}


# Writer Agent Tools
def write_section(topic, facts, tone="professional"):
    """Write a section based on facts"""
    content = f"\n## {topic.title()}\n\n"
    content += f"Here are the key insights about {topic}:\n\n"
    
    for i, fact in enumerate(facts, 1):
        content += f"{i}. {fact}\n"
    
    return {"success": True, "content": content, "word_count": len(content.split())}


def format_document(sections):
    """Format multiple sections into document"""
    doc = "# Research Report\n"
    doc += f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
    doc += "---\n\n"
    doc += "\n".join(sections)
    
    return {"success": True, "document": doc, "sections": len(sections)}


# Critic Agent Tools
def analyze_quality(text):
    """Analyze content quality"""
    word_count = len(text.split())
    has_structure = "##" in text
    has_facts = any(str(i) + "." in text for i in range(1, 10))
    
    score = 0
    if word_count > 50:
        score += 30
    if has_structure:
        score += 35
    if has_facts:
        score += 35
    
    feedback = []
    if word_count < 50:
        feedback.append("Content is too short. Add more details.")
    if not has_structure:
        feedback.append("Add section headers for better organization.")
    if not has_facts:
        feedback.append("Include numbered points or facts.")
    
    return {
        "success": True,
        "score": score,
        "feedback": feedback,
        "passed": score >= 70
    }


def suggest_improvements(text, feedback):
    """Suggest specific improvements"""
    suggestions = []
    
    if "too short" in str(feedback):
        suggestions.append("Expand each point with more context and examples")
    if "headers" in str(feedback):
        suggestions.append("Add clear section headers using ## markdown")
    if "facts" in str(feedback):
        suggestions.append("Structure information as numbered lists")
    
    suggestions.append("Consider adding a conclusion section")
    
    return {"success": True, "suggestions": suggestions}


# Coordinator Agent Tools
def create_task_list(goal):
    """Break down goal into tasks"""
    tasks = []
    
    if "research" in goal.lower() or "report" in goal.lower():
        tasks = [
            {"id": 1, "type": "research", "description": "Research the topic", "assigned_to": None},
            {"id": 2, "type": "write", "description": "Write initial draft", "assigned_to": None},
            {"id": 3, "type": "review", "description": "Review and critique", "assigned_to": None},
            {"id": 4, "type": "revise", "description": "Revise based on feedback", "assigned_to": None}
        ]
    
    return {"success": True, "tasks": tasks, "count": len(tasks)}


def assign_task(task, agents):
    """Assign task to appropriate agent"""
    task_type = task.get("type")
    
    assignments = {
        "research": "ResearchAgent",
        "write": "WriterAgent",
        "review": "CriticAgent",
        "revise": "WriterAgent"
    }
    
    assigned_agent = assignments.get(task_type, "ResearchAgent")
    return {"success": True, "assigned_to": assigned_agent}


# ============================================
# STEP 2: Agent Base Class with Memory
# ============================================

class BaseAgent:
    """
    Base class for all agents with:
    - Identity and specialization
    - Memory system
    - Communication ability
    """
    
    def __init__(self, name, role, skills):
        self.name = name
        self.role = role
        self.skills = skills
        self.memory = {
            "interactions": [],
            "knowledge": {},
            "tasks_completed": []
        }
        self.tools = {}
        self.communication_log = []
    
    def remember(self, key, value):
        """Store information in memory"""
        self.memory["knowledge"][key] = {
            "value": value,
            "timestamp": datetime.now()
        }
    
    def recall(self, key):
        """Retrieve from memory"""
        item = self.memory["knowledge"].get(key)
        return item["value"] if item else None
    
    def log_interaction(self, other_agent, message, response):
        """Log communication with other agents"""
        interaction = {
            "with": other_agent,
            "message": message,
            "response": response,
            "timestamp": datetime.now()
        }
        self.memory["interactions"].append(interaction)
        self.communication_log.append(interaction)
    
    def send_message(self, target_agent, message):
        """Send a message to another agent"""
        comm_entry = {
            "from": self.name,
            "to": target_agent,
            "message": message,
            "timestamp": datetime.now()
        }
        self.communication_log.append(comm_entry)
        return comm_entry
    
    def get_status(self):
        """Return agent status"""
        return {
            "name": self.name,
            "role": self.role,
            "skills": self.skills,
            "tasks_completed": len(self.memory["tasks_completed"]),
            "knowledge_items": len(self.memory["knowledge"]),
            "interactions": len(self.memory["interactions"])
        }
    
    def execute_task(self, task, context):
        """Override in subclasses"""
        raise NotImplementedError


# ============================================
# STEP 3: Specialized Agent Classes
# ============================================

class ResearchAgent(BaseAgent):
    """
    Specializes in: Information gathering and fact extraction
    """
    
    def __init__(self):
        super().__init__(
            name="ResearchAgent",
            role="Information Specialist",
            skills=["web_search", "fact_extraction", "data_analysis"]
        )
        self.tools = {
            "search_web": search_web,
            "extract_facts": extract_facts
        }
    
    def execute_task(self, task, context):
        """Research a topic and extract facts"""
        topic = context.get("topic", "general topic")
        
        print(f"\n  🔬 {self.name}: Starting research on '{topic}'")
        
        # Step 1: Search for information
        search_result = self.tools["search_web"](topic)
        self.remember(f"search_{topic}", search_result)
        
        print(f"     ✓ Found information from {search_result['source']}")
        
        # Step 2: Extract facts
        facts_result = self.tools["extract_facts"](search_result["data"])
        self.remember(f"facts_{topic}", facts_result["facts"])
        
        print(f"     ✓ Extracted {facts_result['count']} key facts")
        
        # Step 3: Return results
        result = {
            "success": True,
            "topic": topic,
            "data": search_result["data"],
            "facts": facts_result["facts"],
            "agent": self.name
        }
        
        self.memory["tasks_completed"].append(task)
        return result


class WriterAgent(BaseAgent):
    """
    Specializes in: Content creation and document formatting
    """
    
    def __init__(self):
        super().__init__(
            name="WriterAgent",
            role="Content Creator",
            skills=["writing", "formatting", "editing"]
        )
        self.tools = {
            "write_section": write_section,
            "format_document": format_document
        }
    
    def execute_task(self, task, context):
        """Write content based on research"""
        topic = context.get("topic", "general topic")
        facts = context.get("facts", [])
        is_revision = context.get("is_revision", False)
        
        action = "Revising" if is_revision else "Writing"
        print(f"\n  ✍️  {self.name}: {action} content on '{topic}'")
        
        # Step 1: Write section
        if is_revision:
            feedback = context.get("feedback", [])
            print(f"     📝 Incorporating {len(feedback)} feedback points")
            # Add improvements based on feedback
            facts = facts + ["Additional context based on review feedback."]
        
        section_result = self.tools["write_section"](topic, facts)
        self.remember(f"draft_{topic}", section_result["content"])
        
        print(f"     ✓ Created section ({section_result['word_count']} words)")
        
        result = {
            "success": True,
            "topic": topic,
            "content": section_result["content"],
            "word_count": section_result["word_count"],
            "agent": self.name
        }
        
        self.memory["tasks_completed"].append(task)
        return result


class CriticAgent(BaseAgent):
    """
    Specializes in: Quality review and improvement suggestions
    """
    
    def __init__(self):
        super().__init__(
            name="CriticAgent",
            role="Quality Assurance",
            skills=["analysis", "critique", "improvement_suggestions"]
        )
        self.tools = {
            "analyze_quality": analyze_quality,
            "suggest_improvements": suggest_improvements
        }
    
    def execute_task(self, task, context):
        """Review content and provide feedback"""
        content = context.get("content", "")
        topic = context.get("topic", "content")
        
        print(f"\n  🔍 {self.name}: Reviewing content on '{topic}'")
        
        # Step 1: Analyze quality
        quality_result = self.tools["analyze_quality"](content)
        self.remember(f"review_{topic}", quality_result)
        
        print(f"     📊 Quality score: {quality_result['score']}/100")
        
        # Step 2: Generate suggestions
        suggestions_result = self.tools["suggest_improvements"](
            content, 
            quality_result["feedback"]
        )
        
        print(f"     💡 Generated {len(suggestions_result['suggestions'])} suggestions")
        
        if quality_result["passed"]:
            print(f"     ✅ Content approved!")
        else:
            print(f"     ⚠️  Needs improvement")
            for feedback_item in quality_result["feedback"]:
                print(f"        • {feedback_item}")
        
        result = {
            "success": True,
            "score": quality_result["score"],
            "passed": quality_result["passed"],
            "feedback": quality_result["feedback"],
            "suggestions": suggestions_result["suggestions"],
            "agent": self.name
        }
        
        self.memory["tasks_completed"].append(task)
        return result


class CoordinatorAgent(BaseAgent):
    """
    Specializes in: Task management and agent coordination
    Orchestrates the entire multi-agent system
    """
    
    def __init__(self, agents):
        super().__init__(
            name="CoordinatorAgent",
            role="System Orchestrator",
            skills=["planning", "task_assignment", "coordination"]
        )
        self.agents = agents  # Dictionary of available agents
        self.tools = {
            "create_task_list": create_task_list,
            "assign_task": assign_task
        }
    
    def execute_goal(self, goal, context):
        """Main orchestration method"""
        print(f"\n{'='*70}")
        print(f"🎯 GOAL: {goal}")
        print(f"{'='*70}")
        
        # Step 1: Create task list
        print(f"\n📋 {self.name}: Creating task breakdown...")
        task_list_result = self.tools["create_task_list"](goal)
        tasks = task_list_result["tasks"]
        
        for i, task in enumerate(tasks, 1):
            print(f"   {i}. {task['description']}")
        
        # Step 2: Execute tasks in order
        print(f"\n{'='*70}")
        print("⚙️  MULTI-AGENT EXECUTION")
        print(f"{'='*70}")
        
        results = {}
        shared_context = context.copy()
        
        for task in tasks:
            # Assign task to appropriate agent
            assignment = self.tools["assign_task"](task, self.agents)
            agent_name = assignment["assigned_to"]
            
            print(f"\n┌─ TASK {task['id']}: {task['description']}")
            print(f"│  👤 Assigned to: {agent_name}")
            
            # Get the agent
            agent = self.agents.get(agent_name)
            
            if agent:
                # Execute task
                result = agent.execute_task(task, shared_context)
                results[task['id']] = result
                
                # Update shared context for next agents
                if task['type'] == 'research':
                    shared_context['facts'] = result.get('facts', [])
                    shared_context['data'] = result.get('data', '')
                
                elif task['type'] == 'write':
                    shared_context['content'] = result.get('content', '')
                
                elif task['type'] == 'review':
                    shared_context['score'] = result.get('score', 0)
                    shared_context['feedback'] = result.get('feedback', [])
                    shared_context['passed'] = result.get('passed', False)
                
                elif task['type'] == 'revise':
                    shared_context['is_revision'] = True
                    shared_context['final_content'] = result.get('content', '')
                
                # Log inter-agent communication
                if task['id'] > 1:
                    prev_agent = results.get(task['id'] - 1, {}).get('agent', 'Unknown')
                    if prev_agent != agent_name:
                        agent.send_message(agent_name, f"Passing context from {prev_agent}")
                
                print(f"└─ Task {task['id']} completed by {agent_name}!\n")
            else:
                print(f"└─ ❌ Agent {agent_name} not found!\n")
        
        # Step 3: Generate final output
        self._print_summary(goal, tasks, results, shared_context)
        
        return {
            "goal": goal,
            "tasks": tasks,
            "results": results,
            "final_content": shared_context.get('final_content', shared_context.get('content', '')),
            "success": True
        }
    
    def _print_summary(self, goal, tasks, results, shared_context):
        """Print execution summary"""
        print(f"\n{'='*70}")
        print("📊 MULTI-AGENT EXECUTION SUMMARY")
        print(f"{'='*70}")
        print(f"Goal: {goal}")
        print(f"Total tasks: {len(tasks)}")
        print(f"Tasks completed: {len(results)}")
        
        print(f"\n👥 Agent Contributions:")
        agent_tasks = {}
        for result in results.values():
            agent_name = result.get('agent', 'Unknown')
            agent_tasks[agent_name] = agent_tasks.get(agent_name, 0) + 1
        
        for agent_name, count in agent_tasks.items():
            print(f"   • {agent_name}: {count} tasks")
        
        # Show quality score if available
        final_score = shared_context.get('score', 0)
        if final_score > 0:
            print(f"\n📈 Final Quality Score: {final_score}/100")
        
        print(f"\n✅ GOAL ACHIEVED! All agents collaborated successfully.")
        print(f"{'='*70}\n")
    
    def get_system_status(self):
        """Get status of all agents in the system"""
        print(f"\n{'='*70}")
        print("🔍 MULTI-AGENT SYSTEM STATUS")
        print(f"{'='*70}")
        
        for agent_name, agent in self.agents.items():
            status = agent.get_status()
            print(f"\n{status['name']} ({status['role']}):")
            print(f"  • Skills: {', '.join(status['skills'])}")
            print(f"  • Tasks completed: {status['tasks_completed']}")
            print(f"  • Knowledge items: {status['knowledge_items']}")
            print(f"  • Interactions: {status['interactions']}")
            print(f"  • Communications sent: {len(agent.communication_log)}")
        
        print(f"\n📡 Inter-Agent Communication Log:")
        total_comms = sum(len(agent.communication_log) for agent in self.agents.values())
        print(f"  • Total messages exchanged: {total_comms}")
        print(f"  • Collaboration enabled seamless workflow!")
        
        print(f"\n{'='*70}\n")


# ============================================
# STEP 4: Visualization
# ============================================

def show_multi_agent_concept():
    """Explain multi-agent systems"""
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║          WHY MULTI-AGENT SYSTEMS ARE POWERFUL               ║
    ╚══════════════════════════════════════════════════════════════╝
    
    SINGLE Agent:                  MULTI-Agent System:
    ─────────────                  ───────────────────
    
    🤖 One agent tries             👥 Specialized agents collaborate
       to do everything               
                                   🔬 ResearchAgent
    ❌ Jack of all trades             └─> Finds information
    ❌ Master of none              
    ❌ Can't parallelize           ✍️  WriterAgent
    ❌ Single point of failure        └─> Creates content
                                   
                                   🔍 CriticAgent
                                      └─> Reviews quality
                                   
                                   🎯 CoordinatorAgent
                                      └─> Orchestrates all
    
    
    Multi-Agent Advantages:
    ✓ SPECIALIZATION: Each agent masters specific skills
    ✓ COLLABORATION: Agents work together on complex tasks
    ✓ SCALABILITY: Add new agents for new capabilities
    ✓ RESILIENCE: If one fails, others continue
    ✓ PARALLELIZATION: Multiple agents work simultaneously
    
    
    🔄 The Collaboration Flow:
    
         COORDINATOR
              │
              ├─> Breaks down goal into tasks
              │
              ├─> Assigns tasks to specialists
              │
              └─> Coordinates execution
                  │
                  ├─> ResearchAgent finds info
                  │        │
                  │        └─> Shares with WriterAgent
                  │                 │
                  │                 └─> Sends to CriticAgent
                  │                          │
                  │                          └─> Feedback to WriterAgent
                  │
                  └─> Final result!
    
    
    Real-World Examples:
    • AutoGPT: Multiple agents for different tasks
    • Microsoft AutoGen: Conversational multi-agent framework
    • CrewAI: Role-based agent teams
    • LangChain Agents: Composable agent systems
    
    This is the FUTURE of AI systems! 🚀
    """)


# ============================================
# STEP 5: Main Demo
# ============================================

if __name__ == "__main__":
    show_multi_agent_concept()
    
    print("\n" + "🚀 LIVE MULTI-AGENT DEMO ".center(70, "=") + "\n")
    
    print("Setting up agent team...")
    
    # Create specialized agents
    research_agent = ResearchAgent()
    writer_agent = WriterAgent()
    critic_agent = CriticAgent()
    
    # Create agent team
    agent_team = {
        "ResearchAgent": research_agent,
        "WriterAgent": writer_agent,
        "CriticAgent": critic_agent
    }
    
    # Create coordinator
    coordinator = CoordinatorAgent(agent_team)
    
    print("✓ Agent team assembled!\n")
    
    input("Press ENTER to watch agents collaborate...")
    
    # Example: Research report creation
    result = coordinator.execute_goal(
        goal="Create a research report about AI agents",
        context={
            "topic": "ai agents",
            "format": "markdown"
        }
    )
    
    # Show final document
    print("\n" + "📄 FINAL DOCUMENT ".center(70, "="))
    print(result.get('final_content', 'No content generated'))
    print("="*70)
    
    # Show system status
    coordinator.get_system_status()
    
    # Another example
    print("\n" + "─"*70)
    input("\nPress ENTER for another example (different topic)...")
    
    result2 = coordinator.execute_goal(
        goal="Create a research report about machine learning",
        context={
            "topic": "machine learning",
            "format": "markdown"
        }
    )
    
    print("\n" + "📄 FINAL DOCUMENT ".center(70, "="))
    print(result2.get('final_content', 'No content generated'))
    print("="*70)
    
    # Final insights
    print("\n" + "="*70)
    print("💡 KEY TAKEAWAYS")
    print("="*70)
    print("""
1. SPECIALIZATION = Excellence
   - Each agent focuses on what it does best
   - ResearchAgent: Finding information
   - WriterAgent: Creating content
   - CriticAgent: Ensuring quality
   - CoordinatorAgent: Managing workflow
   
2. COLLABORATION = Power
   - Agents share information through context
   - Each builds on previous agent's work
   - Feedback loops improve quality
   
3. COORDINATION = Efficiency
   - Coordinator breaks down complex goals
   - Assigns tasks to right specialists
   - Manages dependencies and order
   
4. MEMORY = Continuity
   - Each agent remembers its work
   - Knowledge persists across tasks
   - Interactions are logged
   
5. Real-World Applications
   - Software development teams (coder, tester, reviewer)
   - Content creation (researcher, writer, editor)
   - Business processes (analyst, planner, executor)
   - Scientific research (data gatherer, analyzer, reporter)
""")
    print("="*70)
