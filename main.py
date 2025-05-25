import os
import sys
from src.agent.voice_agent import VoiceAgent

def main():
    """
    Main entry point for the Deal Finder Voice Agent application
    """
    print("=" * 50)
    print("Deal Finder Voice Agent")
    print("=" * 50)
    print("\nThis application simulates a voice agent that:")
    print("1. Calls multiple resellers of limited edition sneakers")
    print("2. Gathers pricing and availability information")
    print("3. Compares offers to find the best deals")
    print("4. Recommends the top 3 options to the user")
    print("5. Sends an email with the recommendations")
    print("6. Logs all interactions to a Google Sheet")
    print("\nStarting simulation...\n")
    
    # Create and run the voice agent
    agent = VoiceAgent()
    results = agent.run_simulation()
    
    # Save the OmniDimension configuration
    agent.save_omnidimension_configuration()
    
    print("\nSimulation completed!")
    print("\nCheck the following files for results:")
    print("- email_preview.html: Preview of the email sent to the user")
    print("- call_logs.html: Log of all conversations with resellers")
    print("- extracted_info.html: Structured data extracted from conversations")
    print("- omnidimension_config/: Configuration files for OmniDimension")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
