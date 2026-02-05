import time
from src.mock_scammer import MockScammerAPI
from src.honeypot_agent import HoneyPotAgent

def run_simulation():
    print("--- Starting Agentic Honey-Pot Simulation ---")
    
    # Initialize
    scammer = MockScammerAPI()
    agent = HoneyPotAgent(persona="naive_elderly")
    
    # Start Interaction
    scammer_msg = scammer.initiate_conversation()
    print(f"\n[SCAMMER]: {scammer_msg}")
    
    # Process initial message
    if agent.detect_scam(scammer_msg):
        print(f"[SYSTEM]: Scam Detected! Engaging Honey-Pot Mode.")
        agent.extract_intelligence(scammer_msg)
    else:
        print("[SYSTEM]: No scam detected. Ending.")
        return

    # Interaction Loop (Limit to 5 turns for demo)
    for i in range(5):
        # Agent replies
        agent_reply = agent.generate_response(scammer_msg)
        print(f"[AGENT]: {agent_reply}")
        
        # Scammer replies back
        scammer_msg = scammer.reply(agent_reply)
        print(f"\n[SCAMMER]: {scammer_msg}")
        
        # Agent analyzes
        agent.extract_intelligence(scammer_msg)
        
        # Break if extracting info seems complete (for demo purposes)
        # In a real scenario, this would be more complex
        if "scammer@upi" in agent.extracted_data["upi_ids"]:
            print("[SYSTEM]: Target intelligence captured.")
            # We continue a bit to see if we get more, or break.
            # Let's run the full loop for the demo.
        
        time.sleep(1) # Simulate delay

    print("\n--- Simulation Finished ---")
    print("Extracted Intelligence:")
    print(agent.get_structured_intelligence())

if __name__ == "__main__":
    run_simulation()
