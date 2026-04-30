"""
Conversational Agent with Memory (No API Required!)
====================================================

This example shows how agents REMEMBER conversations.
This is what makes chatbots feel natural and intelligent!

No installation needed - just run:
    python3 conversational_agent_with_memory.py
"""

from datetime import datetime

# ============================================
# STEP 1: Tools (Same as before!)
# ============================================

def set_reminder(task, time):
    """Set a reminder"""
    return f"✓ Reminder set: '{task}' at {time}"


def get_current_time():
    """Get current time"""
    return datetime.now().strftime("%I:%M %p")


def add_to_shopping_list(item):
    """Add item to shopping list"""
    return f"✓ Added '{item}' to shopping list"


# ============================================
# STEP 2: Memory System (NEW!)
# ============================================

class ConversationMemory:
    """
    Stores conversation history so the agent can:
    - Remember what was said before
    - Understand context ("it", "that", "the same")
    - Build on previous answers
    """
    
    def __init__(self):
        self.messages = []
        self.user_preferences = {}
        self.entities_mentioned = {}  # Things user talked about
    
    def add_message(self, role, content):
        """Add a message to history"""
        self.messages.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now()
        })
    
    def get_recent_context(self, num_messages=5):
        """Get recent conversation for context"""
        return self.messages[-num_messages:]
    
    def remember_entity(self, entity_type, value):
        """Remember important things (names, places, preferences)"""
        self.entities_mentioned[entity_type] = value
    
    def recall_entity(self, entity_type):
        """Recall something from memory"""
        return self.entities_mentioned.get(entity_type)
    
    def get_conversation_summary(self):
        """Summary of conversation"""
        user_msgs = [m for m in self.messages if m["role"] == "user"]
        agent_msgs = [m for m in self.messages if m["role"] == "agent"]
        return {
            "total_exchanges": len(user_msgs),
            "entities_remembered": len(self.entities_mentioned),
            "conversation_start": self.messages[0]["timestamp"] if self.messages else None
        }
    
    def export_memory(self, filename="conversation_memory.json"):
        """Export memory to file for persistence"""
        import json
        memory_data = {
            "messages": [
                {
                    "role": m["role"],
                    "content": m["content"],
                    "timestamp": m["timestamp"].isoformat()
                } for m in self.messages
            ],
            "entities": self.entities_mentioned,
            "preferences": self.user_preferences
        }
        with open(filename, 'w') as f:
            json.dump(memory_data, f, indent=2)
        return f"✓ Memory exported to {filename}"


# ============================================
# STEP 3: Smart Brain with Memory
# ============================================

class MemoryAwareBrain:
    """
    Enhanced brain that uses conversation memory
    to understand context and references
    """
    
    def __init__(self, memory):
        self.memory = memory
        self.tools = {
            "set_reminder": set_reminder,
            "get_current_time": get_current_time,
            "add_to_shopping_list": add_to_shopping_list
        }
    
    def decide_action(self, user_message):
        """
        Decide what to do, using MEMORY for context
        """
        msg_lower = user_message.lower()
        
        # Check for greetings and name
        if any(word in msg_lower for word in ["my name is", "i'm", "i am", "call me"]):
            # Extract and remember name
            for word in user_message.split():
                if len(word) > 2 and word[0].isupper():
                    self.memory.remember_entity("user_name", word)
                    return (None, None)  # Just remember, no tool needed
        
        # Use remembered name in responses
        if any(word in msg_lower for word in ["who am i", "my name", "remember me"]):
            name = self.memory.recall_entity("user_name")
            return ("recall_name", {"name": name})
        
        # Time-related
        if any(word in msg_lower for word in ["time", "what time"]):
            return ("get_current_time", {})
        
        # Reminders
        if "remind" in msg_lower or "reminder" in msg_lower:
            # Simple extraction
            task = user_message.split("remind me to")[-1].split("at")[0].strip() if "remind me to" in msg_lower else "task"
            time = user_message.split("at")[-1].strip() if "at" in msg_lower else "later"
            return ("set_reminder", {"task": task, "time": time})
        
        # Shopping list - with context!
        if any(word in msg_lower for word in ["buy", "shopping", "get me", "add"]):
            # Handle references like "it", "that", "same thing"
            if any(ref in msg_lower for ref in ["it", "that", "same"]):
                # Look back in conversation for what they meant
                recent = self.memory.get_recent_context(3)
                for msg in reversed(recent):
                    if msg["role"] == "user" and any(word in msg["content"].lower() for word in ["buy", "get"]):
                        # Found the item they referenced!
                        item = self.memory.recall_entity("last_item")
                        if item:
                            return ("add_to_shopping_list", {"item": item})
            else:
                # Extract item
                for trigger in ["buy", "get me", "add"]:
                    if trigger in msg_lower:
                        item = msg_lower.split(trigger)[-1].strip()
                        # Clean up
                        item = item.replace("to shopping list", "").strip()
                        if item:
                            self.memory.remember_entity("last_item", item)
                            return ("add_to_shopping_list", {"item": item})
        
        # No tool needed
        return (None, None)
    
    def generate_response(self, tool_result, user_message, action):
        """Generate response using memory for personalization"""
        
        # Check if we know the user's name
        user_name = self.memory.recall_entity("user_name")
        greeting = f"Hi {user_name}! " if user_name else "Hi! "
        
        # Special case for name recall
        if action == "recall_name":
            name = self.memory.recall_entity("user_name")
            if name:
                return f"Yes, I remember! Your name is {name}. 😊"
            else:
                return "I don't think you've told me your name yet!"
        
        # If we used a tool
        if tool_result:
            return f"{greeting}{tool_result}"
        
        # Check if this is a greeting
        msg_lower = user_message.lower()
        if any(word in msg_lower for word in ["hello", "hi", "hey"]):
            context = self.memory.get_recent_context(2)
            if len(context) <= 1:
                return f"{greeting}I'm your AI assistant with memory! I can remember our conversation and help you with reminders and shopping lists."
            else:
                return f"{greeting}Good to chat with you again!"
        
        # Default response
        return f"{greeting}I can help you with time, reminders, and shopping lists. I also remember our conversation!"


# ============================================
# STEP 4: Conversational Agent
# ============================================

class ConversationalAgent:
    """
    An agent that remembers conversations!
    
    Key difference from simple agent:
    - Has persistent memory
    - Understands context ("it", "that")
    - Personalizes responses
    - Builds on previous exchanges
    """
    
    def __init__(self):
        self.memory = ConversationMemory()
        self.brain = MemoryAwareBrain(self.memory)
    
    def chat(self, user_message):
        """
        Process message with full conversation context
        """
        print(f"\n{'─'*60}")
        print(f"👤 You: {user_message}")
        
        # Add to memory FIRST
        self.memory.add_message("user", user_message)
        
        # Show what agent remembers (for learning purposes)
        entities = self.memory.entities_mentioned
        if entities:
            print(f"🧠 [Agent's memory: {entities}]")
        
        # Think and act
        action, params = self.brain.decide_action(user_message)
        
        tool_result = None
        if action and action != "recall_name":
            tool_function = self.brain.tools.get(action)
            if tool_function:
                tool_result = tool_function(**params)
        
        # Respond
        response = self.brain.generate_response(tool_result, user_message, action)
        
        # Add response to memory
        self.memory.add_message("agent", response)
        
        print(f"🤖 Agent: {response}")
        print(f"{'─'*60}")
        
        return response
    
    def show_memory_stats(self):
        """Show what the agent remembers"""
        stats = self.memory.get_conversation_summary()
        print(f"\n{'='*60}")
        print("📊 MEMORY STATS")
        print(f"{'='*60}")
        print(f"Total exchanges: {stats['total_exchanges']}")
        print(f"Things remembered: {stats['entities_remembered']}")
        print(f"\nStored entities:")
        for key, value in self.memory.entities_mentioned.items():
            print(f"  • {key}: {value}")
        print(f"{'='*60}\n")


# ============================================
# STEP 5: Show the Difference!
# ============================================

def show_memory_concept():
    """Explain why memory matters"""
    print("""
    ╔══════════════════════════════════════════════════╗
    ║        WHY MEMORY MAKES AGENTS SMARTER          ║
    ╚══════════════════════════════════════════════════╝
    
    WITHOUT Memory:                WITH Memory:
    ───────────────               ─────────────
    
    You: "My name is Alex"        You: "My name is Alex"
    Bot: "OK"                     Bot: "Nice to meet you, Alex!"
    
    You: "What's my name?"        You: "What's my name?"
    Bot: "I don't know" ❌        Bot: "Your name is Alex!" ✓
    
    You: "Buy milk"               You: "Buy milk"
    Bot: "Added milk"             Bot: "Added milk"
    
    You: "Add that too"           You: "Add that too"
    Bot: "Add what?" ❌           Bot: "Added milk" ✓
    
    
    Memory enables:
    ✓ Context understanding ("it", "that", "same")
    ✓ Personalization (using your name)
    ✓ Multi-turn conversations
    ✓ Building on previous answers
    ✓ Learning preferences over time
    
    This is CRITICAL for real AI agents!
    """)


# ============================================
# STEP 6: Interactive Demo
# ============================================

if __name__ == "__main__":
    show_memory_concept()
    
    print("\n" + "🚀 LIVE DEMO ".center(60, "=") + "\n")
    
    agent = ConversationalAgent()
    
    # Conversation that shows memory in action
    print("Let's have a conversation that shows memory working...\n")
    
    # Exchange 1: Introduction
    agent.chat("Hello!")
    
    # Exchange 2: Tell name
    agent.chat("My name is Sarah")
    
    # Exchange 3: Agent should remember name
    agent.chat("What time is it?")
    
    # Exchange 4: Test memory recall
    agent.chat("Do you remember my name?")
    
    # Exchange 5: Shopping list
    agent.chat("I need to buy apples")
    
    # Exchange 6: Use context reference
    agent.chat("Actually, add oranges too")
    
    # Exchange 7: Set reminder
    agent.chat("Remind me to call mom at 3pm")
    
    # Show what agent remembers
    agent.show_memory_stats()
    
    # Export memory to file
    print("\n💾 MEMORY PERSISTENCE DEMO:")
    print("="*60)
    export_result = agent.memory.export_memory("demo_conversation.json")
    print(f"  {export_result}")
    print("  Now conversations can be saved and restored later!")
    print("="*60)
    
    # Show conversation history
    print("\n💬 FULL CONVERSATION HISTORY:")
    print("="*60)
    for i, msg in enumerate(agent.memory.messages, 1):
        role_emoji = "👤" if msg["role"] == "user" else "🤖"
        print(f"{i}. {role_emoji} [{msg['timestamp'].strftime('%H:%M:%S')}] {msg['content']}")
    print("="*60)
    
    print("\n" + "="*60)
    print("💡 KEY TAKEAWAYS:")
    print("="*60)
    print("""
1. MEMORY = Context
   - Agents remember what you said before
   - They can reference previous messages
   
2. MEMORY = Personalization
   - Using your name
   - Remembering preferences
   
3. MEMORY = Intelligence
   - Understanding "it", "that", "same"
   - Building coherent conversations
   
4. Real AI Agents
   - Use this same pattern
   - Just store more complex memory
   - Can remember across sessions (databases)

🎯 You now understand TWO core agent concepts:
   1. Tools/Actions (from previous example)
   2. Memory/Context (this example)
   
These are the building blocks of ALL AI agents! 🚀
""")
    print("="*60)
    
    # Optional: Interactive mode
    print("\n" + "💬 WANT TO TRY IT YOURSELF? ".center(60, "="))
    print("Type messages to chat with the agent.")
    print("The agent will remember everything you say!")
    print("Type 'quit' to exit, 'memory' to see what agent remembers.\n")
    
    while True:
        try:
            user_input = input("👤 You: ").strip()
            if not user_input:
                continue
            if user_input.lower() == 'quit':
                print("👋 Goodbye!")
                break
            if user_input.lower() == 'memory':
                agent.show_memory_stats()
                continue
            
            agent.chat(user_input)
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except EOFError:
            break
