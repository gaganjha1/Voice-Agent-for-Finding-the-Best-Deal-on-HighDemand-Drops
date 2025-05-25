import os
import sys
import webbrowser
import time
from src.agent.voice_agent import VoiceAgent

def main():
    """
    Run the Deal Finder Voice Agent simulation and open the result files
    """
    print("=" * 60)
    print("Deal Finder Voice Agent - Simulation Runner")
    print("=" * 60)
    print("\nThis script will:")
    print("1. Run a simulation of the voice agent calling multiple resellers")
    print("2. Generate sample output files (email, logs, etc.)")
    print("3. Open the output files in your default browser")
    print("\nStarting simulation...\n")
    
    # Create and run the voice agent
    agent = VoiceAgent()
    results = agent.run_simulation()
    
    # Save the OmniDimension configuration
    agent.save_omnidimension_configuration()
    
    print("\nSimulation completed!")
    print(f"Contacted {results['conversation_count']} resellers")
    print(f"Total interactions: {results['total_interactions']}")
    print(f"Email status: {results['email_status']}")
    
    # Wait a moment before opening the files
    time.sleep(1)
    
    # Open the output files in the default browser
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    print("\nOpening result files in your browser...")
    
    # Open the email preview
    email_path = os.path.join(current_dir, 'email_preview.html')
    if os.path.exists(email_path):
        webbrowser.open('file://' + os.path.abspath(email_path))
        print("Opened email preview")
        time.sleep(1)
    
    # Open the call logs
    logs_path = os.path.join(current_dir, 'call_logs.html')
    if os.path.exists(logs_path):
        webbrowser.open('file://' + os.path.abspath(logs_path))
        print("Opened call logs")
        time.sleep(1)
    
    # Open the extracted info
    info_path = os.path.join(current_dir, 'extracted_info.html')
    if os.path.exists(info_path):
        webbrowser.open('file://' + os.path.abspath(info_path))
        print("Opened extracted information")
    
    print("\nSimulation complete! Check your browser for the result files.")
    print("\nIn a real implementation, you would:")
    print("1. Set up the OmniDimension voice agent using the configuration in omnidimension_config/")
    print("2. Deploy the API server to handle webhooks")
    print("3. Configure the webhooks in OmniDimension to point to your API server")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
