import streamlit as st
import pandas as pd
import os
import time
from datetime import datetime
import matplotlib.pyplot as plt
import pickle

# Import our modules
import sys
sys.path.append('.')
from agent.q_learning import QLearningAgent
from agent.logger import log_episode, log_total_reward
from agent.visualizer import plot_rewards, create_performance_dashboard

# Configure Streamlit page
st.set_page_config(
    page_title="🤖 RL Controlled Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #2E86AB;
        text-align: center;
        margin-bottom: 2rem;
    }
    .task-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .feedback-buttons {
        display: flex;
        gap: 1rem;
        justify-content: center;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'agent' not in st.session_state:
        st.session_state.agent = QLearningAgent(
            actions=["open", "mute", "play", "unmute", "close", "screenshot", "set_dnd"]
        )
    if 'current_task_index' not in st.session_state:
        st.session_state.current_task_index = 0
    if 'current_episode' not in st.session_state:
        st.session_state.current_episode = 1
    if 'episode_reward' not in st.session_state:
        st.session_state.episode_reward = 0
    if 'total_rewards' not in st.session_state:
        st.session_state.total_rewards = []
    if 'task_list' not in st.session_state:
        load_tasks()

def load_tasks():
    """Load tasks from file"""
    task_file_path = os.path.join("data", "task_log.txt")
    try:
        with open(task_file_path, "r") as f:
            st.session_state.task_list = [
                line.strip().split(" - ")[1] for line in f.readlines() 
                if " - " in line
            ]
    except FileNotFoundError:
        st.error(f"Task file not found: {task_file_path}")
        st.session_state.task_list = []

def display_current_task():
    """Display the current task and get agent's action"""
    if st.session_state.current_task_index < len(st.session_state.task_list):
        task = st.session_state.task_list[st.session_state.current_task_index]
        parsed_intent = task.lower().split()[0]
        
        # Get agent's action
        action = st.session_state.agent.select_action(parsed_intent)
        next_best = st.session_state.agent.get_next_best_action(parsed_intent)
        confidence = st.session_state.agent.get_action_confidence(parsed_intent, action)
        
        # Display task information
        st.markdown(f"""
        <div class="task-card">
            <h3>📋 Task {st.session_state.current_task_index + 1} (Episode {st.session_state.current_episode})</h3>
            <p><strong>Task:</strong> {task}</p>
            <p><strong>🎯 Agent's Action:</strong> <code>{action}</code></p>
            <p><strong>💡 Next Best Option:</strong> <code>{next_best}</code></p>
            <p><strong>📊 Confidence:</strong> {confidence:.2f}</p>
        </div>
        """, unsafe_allow_html=True)
        
        return task, parsed_intent, action, next_best, confidence
    else:
        return None, None, None, None, None

def handle_feedback(task, parsed_intent, action, feedback_type, correction=None):
    """Handle user feedback and update the agent"""
    task_id = f"{st.session_state.current_episode}-{st.session_state.current_task_index + 1}"
    
    # Calculate reward based on feedback
    if feedback_type == "👍":
        reward = 2
        feedback_text = "👍 Correct"
        suggestion = ""
    else:  # feedback_type == "👎"
        reward = -2
        feedback_text = "👎 Incorrect"
        suggestion = correction or "No suggestion provided"
        # Bonus reward for providing correction
        if correction:
            reward += 1
            st.success("🎆 Bonus +1 reward for providing correction!")
    
    # Update Q-table
    st.session_state.agent.update_q_table(parsed_intent, action, reward, parsed_intent)
    
    # Log the episode
    log_episode(
        log_path=os.path.join("data", "task_log.csv"),
        task_id=task_id,
        intent=parsed_intent,
        action=action,
        reward=reward,
        feedback=feedback_text,
        suggestion=suggestion
    )
    
    # Update episode reward
    st.session_state.episode_reward += reward
    
    # Move to next task
    st.session_state.current_task_index += 1
    
    # Check if episode is complete
    if st.session_state.current_task_index >= len(st.session_state.task_list):
        complete_episode()

def complete_episode():
    """Complete the current episode and start a new one"""
    # Log episode reward
    log_total_reward(
        st.session_state.current_episode, 
        st.session_state.episode_reward, 
        os.path.join("data", "episode_log.txt")
    )
    
    # Store episode reward
    st.session_state.total_rewards.append(st.session_state.episode_reward)
    
    # Show episode summary
    st.success(f"✅ Episode {st.session_state.current_episode} Complete!")
    st.info(f"Total Reward: {st.session_state.episode_reward}")
    
    # Reset for next episode
    st.session_state.current_episode += 1
    st.session_state.current_task_index = 0
    st.session_state.episode_reward = 0
    
    # Save Q-table
    st.session_state.agent.save_q_table("data/q_table.pkl")

def main():
    """Main Streamlit application"""
    initialize_session_state()
    
    # Header
    st.markdown('<h1 class="main-header">🤖 RL Controlled Agent</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Sidebar for statistics and controls
    with st.sidebar:
        st.header("📊 Statistics")
        st.metric("Current Episode", st.session_state.current_episode)
        st.metric("Episode Reward", st.session_state.episode_reward)
        st.metric("Tasks Completed", st.session_state.current_task_index)
        
        if st.session_state.total_rewards:
            st.metric("Average Reward", f"{sum(st.session_state.total_rewards)/len(st.session_state.total_rewards):.1f}")
            st.metric("Best Episode", max(st.session_state.total_rewards))
        
        st.markdown("---")
        st.header("🎮 Controls")
        if st.button("🔄 Reset Training"):
            # Reset all session state
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.experimental_rerun()
        
        if st.button("💾 Save Q-Table"):
            st.session_state.agent.save_q_table("data/q_table.pkl")
            st.success("Q-table saved!")
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("🎯 Current Task")
        
        # Display current task if available
        task_data = display_current_task()
        if task_data[0] is not None:
            task, parsed_intent, action, next_best, confidence = task_data
            
            st.markdown("### 💭 Provide Feedback")
            
            # Feedback buttons
            col_feedback1, col_feedback2 = st.columns(2)
            
            with col_feedback1:
                if st.button("👍 Correct Action", use_container_width=True):
                    handle_feedback(task, parsed_intent, action, "👍")
                    st.experimental_rerun()
            
            with col_feedback2:
                if st.button("👎 Incorrect Action", use_container_width=True):
                    # Show correction input
                    correction = st.text_input("💡 Suggest correct action (optional):")
                    handle_feedback(task, parsed_intent, action, "👎", correction)
                    st.experimental_rerun()
        else:
            st.success("🎉 All tasks completed! Check the visualizations.")
    
    with col2:
        st.header("📈 Progress")
        
        # Show learning curve if we have data
        if st.session_state.total_rewards:
            fig, ax = plt.subplots(figsize=(8, 6))
            episodes = range(1, len(st.session_state.total_rewards) + 1)
            ax.plot(episodes, st.session_state.total_rewards, marker='o', linewidth=2)
            ax.set_title("Learning Curve")
            ax.set_xlabel("Episode")
            ax.set_ylabel("Total Reward")
            ax.grid(True, alpha=0.3)
            st.pyplot(fig)
        
        # Show recent task log
        st.header("📝 Recent Activity")
        try:
            df = pd.read_csv("data/task_log.csv")
            if not df.empty:
                # Show last 5 entries
                st.dataframe(df.tail(5), use_container_width=True)
        except FileNotFoundError:
            st.info("No task log available yet.")

if __name__ == "__main__":
    main()