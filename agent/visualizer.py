import os
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

def plot_rewards(rewards, output_path="data/learning_curve.png"):
    """Enhanced reward plotting with better visualization"""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Create figure with subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # Main learning curve
    episodes = range(1, len(rewards) + 1)
    ax1.plot(episodes, rewards, marker="o", linewidth=2, markersize=8, color='#2E86AB')
    ax1.fill_between(episodes, rewards, alpha=0.3, color='#2E86AB')
    ax1.set_title("🤖 RL Agent Learning Curve", fontsize=16, fontweight='bold')
    ax1.set_xlabel("Episode Number", fontsize=12)
    ax1.set_ylabel("Total Reward", fontsize=12)
    ax1.grid(True, alpha=0.3)
    ax1.set_xticks(episodes)
    
    # Add trend line if more than 2 episodes
    if len(rewards) > 2:
        z = np.polyfit(episodes, rewards, 1)
        p = np.poly1d(z)
        ax1.plot(episodes, p(episodes), "--", alpha=0.8, color='red', label=f'Trend (slope: {z[0]:.1f})')
        ax1.legend()
    
    # Reward distribution/statistics
    ax2.bar(episodes, rewards, color=['green' if r > 0 else 'red' if r < 0 else 'gray' for r in rewards], alpha=0.7)
    ax2.axhline(y=0, color='black', linestyle='-', alpha=0.5)
    ax2.set_title("📊 Episode Reward Distribution", fontsize=14, fontweight='bold')
    ax2.set_xlabel("Episode Number", fontsize=12)
    ax2.set_ylabel("Reward", fontsize=12)
    ax2.grid(True, alpha=0.3)
    ax2.set_xticks(episodes)
    
    # Add statistics text
    if rewards:
        avg_reward = np.mean(rewards)
        max_reward = max(rewards)
        min_reward = min(rewards)
        
        stats_text = f"📈 Stats:\nAvg: {avg_reward:.1f}\nMax: {max_reward}\nMin: {min_reward}"
        ax2.text(0.02, 0.98, stats_text, transform=ax2.transAxes, 
                verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"💾 Saved enhanced reward chart to: {output_path}")

def create_performance_dashboard(task_log_path, output_path="data/dashboard.png"):
    """Create a comprehensive performance dashboard"""
    try:
        import pandas as pd
        
        # Read task log data
        df = pd.read_csv(task_log_path)
        
        # Create dashboard with multiple subplots
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        
        # 1. Reward over time
        ax1.plot(range(len(df)), df['Reward Assigned'], marker='o')
        ax1.set_title('🎯 Reward Progression')
        ax1.set_xlabel('Task Number')
        ax1.set_ylabel('Reward')
        ax1.grid(True, alpha=0.3)
        
        # 2. Action frequency
        action_counts = df['Action Taken'].value_counts()
        ax2.pie(action_counts.values, labels=action_counts.index, autopct='%1.1f%%')
        ax2.set_title('🔄 Action Distribution')
        
        # 3. Feedback distribution
        feedback_counts = df['User Feedback'].value_counts()
        colors = ['green' if '👍' in fb else 'red' if '👎' in fb else 'gray' for fb in feedback_counts.index]
        ax3.bar(feedback_counts.index, feedback_counts.values, color=colors, alpha=0.7)
        ax3.set_title('📝 Feedback Distribution')
        ax3.set_ylabel('Count')
        
        # 4. Learning curve by intent
        intent_rewards = df.groupby('Parsed Intent')['Reward Assigned'].mean()
        ax4.barh(intent_rewards.index, intent_rewards.values)
        ax4.set_title('🧠 Average Reward by Intent')
        ax4.set_xlabel('Average Reward')
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"📊 Saved performance dashboard to: {output_path}")
        
    except ImportError:
        print("⚠️ pandas not available for dashboard creation")
    except Exception as e:
        print(f"⚠️ Error creating dashboard: {e}")
