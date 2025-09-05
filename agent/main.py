# agent/main.py

from agent.q_learning import QLearningAgent
from agent.logger import log_episode, log_total_reward
from agent.feedback import get_feedback, get_confidence_score
from agent.visualizer import plot_rewards
import os
import time
from datetime import datetime

def print_banner():
    """Print a nice banner for the RL Agent"""
    print("\n" + "="*60)
    print("    🤖 REINFORCEMENT LEARNING CONTROLLED AGENT 🤖")
    print("="*60)
    print("  Learning from user feedback to improve task execution")
    print("-"*60)

def display_task_info(episode, task_index, task, action, next_best=None):
    """Display task information in a structured format"""
    print(f"\n📋 TASK {task_index} (Episode {episode})")
    print("-"*40)
    print(f"Task: {task}")
    print(f"🎯 Agent's Action: {action}")
    if next_best:
        print(f"💡 Next Best Option: {next_best}")
    print("-"*40)

def main():
    """Main function to run the RL agent with enhanced logging and feedback"""
    print_banner()
    
    # File paths
    task_log_path = os.path.join("data", "task_log.csv")
    episode_log_path = os.path.join("data", "episode_log.txt")
    chart_path = os.path.join("data", "learning_curve.png")
    task_file_path = os.path.join("data", "task_log.txt")
    
    # Load tasks from file
    try:
        with open(task_file_path, "r") as f:
            task_list = [line.strip().split(" - ")[1] for line in f.readlines() if " - " in line]
    except FileNotFoundError:
        print(f"⚠️  Task file not found: {task_file_path}")
        return
    
    print(f"📋 Loaded {len(task_list)} tasks for training")
    
    # Initialize agent
    agent = QLearningAgent(actions=["open", "mute", "play", "unmute", "close", "screenshot", "set_dnd"])
    total_rewards = []
    
    # Run episodes
    num_episodes = 3
    for episode in range(1, num_episodes + 1):
        print(f"\n🏁 Starting Episode {episode}/{num_episodes}")
        print("="*50)
        total_reward = 0
        start_time = time.time()
        
        for task_index, task in enumerate(task_list, 1):
            # Parse intent from task
            parsed_intent = task.lower().split()[0]
            
            # Get agent's action and confidence
            action = agent.select_action(parsed_intent)
            confidence = agent.get_action_confidence(parsed_intent, action)
            next_best = agent.get_next_best_action(parsed_intent)
            
            # Display task information
            display_task_info(episode, task_index, task, action, next_best)
            
            # Get user feedback
            feedback, correction = get_feedback()
            task_id = f"{episode}-{task_index}"
            
            # Enhanced reward logic based on feedback
            if feedback == "👍":
                reward = 2
                feedback_text = "👍 Correct"
                suggestion = ""
            elif feedback == "👎":
                reward = -2
                feedback_text = "👎 Incorrect"
                suggestion = correction or "No suggestion provided"
                # Bonus reward if user provides correction
                if correction:
                    reward += 1
                    print(f"🎆 Bonus +1 reward for providing correction!")
            else:
                reward = 0
                feedback_text = "Neutral"
                suggestion = "No feedback given"
            
            # Update Q-table
            agent.update_q_table(parsed_intent, action, reward, parsed_intent)
            
            # Enhanced structured logging with all required fields
            log_episode(
                log_path=task_log_path,
                task_id=task_id,
                intent=parsed_intent,
                action=action,
                reward=reward,
                feedback=feedback_text,
                suggestion=suggestion
            )
            
            total_reward += reward
            print(f"🏆 Episode {episode} Reward so far: {total_reward}")
            
            # Small delay for better UX
            time.sleep(0.5)
        
        # Log episode summary
        episode_duration = time.time() - start_time
        log_total_reward(episode, total_reward, episode_log_path)
        total_rewards.append(total_reward)
        
        print(f"\n✅ Episode {episode} Complete!")
        print(f"Total Reward: {total_reward}")
        print(f"Duration: {episode_duration:.1f} seconds")
        print("="*50)
    
    # Save Q-table and generate visualizations
    agent.save_q_table("data/q_table.pkl")
    plot_rewards(total_rewards, chart_path)
    
    # Final summary
    print(f"\n🎉 Training Complete!")
    print(f"Average Reward: {sum(total_rewards)/len(total_rewards):.1f}")
    print(f"Best Episode: {max(total_rewards)}")
    print(f"Logs saved in /data directory")
    print(f"Learning curve saved as {chart_path}")
    
if __name__ == "__main__":
    main()
