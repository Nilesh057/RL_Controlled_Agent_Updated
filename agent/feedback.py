def get_feedback():
    """Enhanced feedback system with clear 👍/👎 interface and real-time feedback loop"""
    print("\n" + "="*50)
    print("   USER FEEDBACK REQUIRED")
    print("="*50)
    print("Was the agent's action correct?")
    print("👍 = Correct action (type: 1, y, yes, or 👍)")
    print("👎 = Incorrect action (type: 2, n, no, or 👎)")
    print("-"*50)
    
    while True:
        fb = input("Your feedback: ").strip().lower()
        
        # Positive feedback options
        if fb in ("1", "y", "yes", "👍", "correct", "good", "right"):
            print("✅ Positive feedback recorded!")
            return "👍", None
        
        # Negative feedback options
        elif fb in ("2", "n", "no", "👎", "incorrect", "wrong", "bad"):
            print("❌ Negative feedback recorded.")
            correction = input("💡 Suggest the correct action (optional): ").strip() or None
            if correction:
                print(f"📝 Suggestion recorded: {correction}")
            return "👎", correction
        
        # Invalid input
        else:
            print("⚠️  Invalid input! Please use:")
            print("   • 👍, 1, y, yes for correct")
            print("   • 👎, 2, n, no for incorrect")
            continue

def get_confidence_score():
    """Get confidence score from user for action evaluation"""
    while True:
        try:
            confidence = input("Rate agent confidence (1-10, or press Enter for auto): ").strip()
            if not confidence:
                import random
                return round(random.uniform(0.5, 1.0), 2)
            
            score = float(confidence)
            if 1 <= score <= 10:
                return score / 10  # Normalize to 0-1 range
            else:
                print("⚠️  Please enter a number between 1-10")
        except ValueError:
            print("⚠️  Please enter a valid number")
