#!/usr/bin/env python3
"""
Demo script for the Enhanced RL Controlled Agent
Provides a quick demonstration of the system capabilities
"""

import os
import sys
sys.path.append('.')

from agent.q_learning import QLearningAgent
from agent.visualizer import plot_rewards

def demo_agent_capabilities():
    """Demonstrate the enhanced agent capabilities"""
    print("🤖 Enhanced RL Controlled Agent Demo")
    print("=" * 50)
    
    # Initialize agent
    agent = QLearningAgent(actions=["open", "mute", "play", "unmute", "close", "screenshot", "set_dnd"])
    
    # Demo tasks
    demo_tasks = [
        "open calendar",
        "mute audio", 
        "take screenshot",
        "play music"
    ]
    
    print("\n🎯 Demonstrating Agent Decision Making:")
    print("-" * 40)
    
    for i, task in enumerate(demo_tasks, 1):
        parsed_intent = task.lower().split()[0]
        
        # Get agent's action and alternatives
        action = agent.select_action(parsed_intent)
        next_best = agent.get_next_best_action(parsed_intent)
        confidence = agent.get_action_confidence(parsed_intent, action)
        
        print(f"\n{i}. Task: {task}")
        print(f"   🎯 Agent Action: {action}")
        print(f"   💡 Next Best: {next_best}")
        print(f"   📊 Confidence: {confidence:.2f}")
        
        # Simulate learning with positive feedback
        agent.update_q_table(parsed_intent, action, 2, parsed_intent)
    
    print(f"\n✅ Demo completed successfully!")
    print(f"📈 Agent Q-table now contains {len(agent.q)} learned states")
    
    # Generate sample visualization
    sample_rewards = [25, 40, 55, 62]
    plot_rewards(sample_rewards, "data/demo_learning_curve.png")
    
    print(f"\n🎉 Enhanced Features Demonstrated:")
    print("  ✅ Next-best action suggestions")
    print("  ✅ Confidence scoring")
    print("  ✅ Q-learning state updates")
    print("  ✅ Enhanced visualization")
    print(f"\n📁 Check data/ directory for generated files")
    
    return True

if __name__ == "__main__":
    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)
    
    try:
        demo_agent_capabilities()
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        sys.exit(1)
