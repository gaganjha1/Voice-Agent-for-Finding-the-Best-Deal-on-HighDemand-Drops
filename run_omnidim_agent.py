#!/usr/bin/env python
"""
Run Omnidim Voice Agent Integration Script

This script demonstrates how to use the Omnidim voice chat assistant integration
with the Deal Finder Voice Agent project.
"""

import os
import sys
import argparse
from dotenv import load_dotenv
from src.agent.voice_agent import VoiceAgent

def setup_env_vars():
    """
    Set up environment variables from user input if not already set
    """
    # Load existing environment variables
    load_dotenv()
    
    # Check for Omnidim API key
    api_key = os.environ.get('OMNIDIM_API_KEY')
    if not api_key:
        api_key = input("Enter your Omnidim API key: ")
        os.environ['OMNIDIM_API_KEY'] = api_key
        
    # Check for Omnidim Agent ID (optional)
    agent_id = os.environ.get('OMNIDIM_AGENT_ID')
    if not agent_id:
        agent_id = input("Enter your Omnidim Agent ID (leave blank to create a new agent): ")
        if agent_id:
            os.environ['OMNIDIM_AGENT_ID'] = agent_id

def create_or_update_agent(agent):
    """
    Create a new agent or update an existing one
    
    Args:
        agent: VoiceAgent instance
        
    Returns:
        Agent ID
    """
    if agent.omnidim_agent_id:
        print(f"Updating existing Omnidim agent with ID: {agent.omnidim_agent_id}")
        result = agent.update_omnidim_agent()
    else:
        print("Creating new Omnidim agent...")
        result = agent.create_omnidim_agent()
        
    print("Agent operation successful!")
    return result.get('id')

def make_call(agent, phone_number):
    """
    Make a call to a specific phone number
    
    Args:
        agent: VoiceAgent instance
        phone_number: Phone number to call
    """
    print(f"Initiating call to: {phone_number}")
    result = agent.make_omnidim_call(phone_number)
    print(f"Call initiated successfully! Call ID: {result.get('id')}")
    return result

def make_bulk_calls(agent, phone_numbers):
    """
    Make bulk calls to multiple phone numbers
    
    Args:
        agent: VoiceAgent instance
        phone_numbers: List of phone numbers to call
    """
    print(f"Initiating bulk calls to {len(phone_numbers)} phone numbers")
    result = agent.make_bulk_omnidim_calls(phone_numbers)
    print(f"Bulk call campaign initiated successfully! Campaign ID: {result.get('id')}")
    return result

def get_call_logs(agent, call_id=None):
    """
    Get call logs
    
    Args:
        agent: VoiceAgent instance
        call_id: Optional specific call ID
    """
    logs = agent.get_omnidim_call_logs(call_id)
    print(f"Retrieved {len(logs)} call logs")
    for i, log in enumerate(logs):
        print(f"\nCall #{i+1} - ID: {log.get('id')}")
        print(f"Status: {log.get('status')}")
        print(f"Duration: {log.get('duration', 0)} seconds")
        print(f"Created at: {log.get('created_at')}")
        
        # Print first few interactions if available
        interactions = log.get('interactions', [])
        if interactions:
            print("\nSample interactions:")
            for j, interaction in enumerate(interactions[:3]):
                print(f"  {interaction.get('speaker')}: {interaction.get('text')}")
            if len(interactions) > 3:
                print(f"  ... and {len(interactions) - 3} more interactions")
    
    return logs

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Omnidim Voice Agent Integration")
    parser.add_argument("--action", choices=["create", "update", "call", "bulk-call", "logs"], 
                        default="create", help="Action to perform")
    parser.add_argument("--phone", help="Phone number to call (for 'call' action)")
    parser.add_argument("--phones-file", help="File with phone numbers, one per line (for 'bulk-call' action)")
    parser.add_argument("--call-id", help="Call ID to get logs for (for 'logs' action)")
    args = parser.parse_args()
    
    # Set up environment variables if needed
    setup_env_vars()
    
    # Create the voice agent
    print("Initializing Deal Finder Voice Agent with Omnidim integration...")
    agent = VoiceAgent()
    
    if not agent.omnidim_enabled:
        print("Error: Omnidim integration is not enabled. Please check your API key.")
        return 1
    
    # Perform the requested action
    if args.action in ["create", "update"]:
        create_or_update_agent(agent)
        
    elif args.action == "call":
        if not args.phone:
            print("Error: --phone argument is required for 'call' action")
            return 1
            
        # Make sure we have an agent ID
        if not agent.omnidim_agent_id:
            print("No agent ID found. Creating a new agent...")
            create_or_update_agent(agent)
            
        make_call(agent, args.phone)
        
    elif args.action == "bulk-call":
        if not args.phones_file:
            print("Error: --phones-file argument is required for 'bulk-call' action")
            return 1
            
        # Read phone numbers from file
        try:
            with open(args.phones_file, 'r') as f:
                phone_numbers = [line.strip() for line in f if line.strip()]
        except Exception as e:
            print(f"Error reading phone numbers file: {str(e)}")
            return 1
            
        if not phone_numbers:
            print("No valid phone numbers found in the file")
            return 1
            
        # Make sure we have an agent ID
        if not agent.omnidim_agent_id:
            print("No agent ID found. Creating a new agent...")
            create_or_update_agent(agent)
            
        make_bulk_calls(agent, phone_numbers)
        
    elif args.action == "logs":
        get_call_logs(agent, args.call_id)
        
    print("\nOmnidim integration operation completed successfully!")
    return 0

if __name__ == "__main__":
    sys.exit(main())
