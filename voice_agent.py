import os
import json
from typing import Dict, List, Any, Tuple, Optional
import sys
import time
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

# Add the project root to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(project_root)

from src.utils.data_processor import DataProcessor
from src.utils.conversation_handler import ConversationHandler
from src.services.email_service import EmailService
from src.services.sheet_logger import SheetLogger
from src.services.omnidim_service import OmnidimService

class VoiceAgent:
    """
    Main voice agent implementation that coordinates the entire workflow
    """
    
    def __init__(self, omnidim_api_key: Optional[str] = None):
        """
        Initialize the VoiceAgent with necessary components
        
        Args:
            omnidim_api_key: Optional API key for Omnidim. If not provided, will be loaded from environment.
        """
        self.data_processor = DataProcessor()
        self.email_service = EmailService()
        self.sheet_logger = SheetLogger()
        
        # Initialize Omnidim service
        try:
            self.omnidim_service = OmnidimService(api_key=omnidim_api_key)
            self.omnidim_enabled = True
            print("Omnidim service initialized successfully")
        except Exception as e:
            print(f"Warning: Failed to initialize Omnidim service: {str(e)}")
            print("Simulation will run without Omnidim integration")
            self.omnidim_enabled = False
            self.omnidim_service = None
        
        # Store agent and call information
        self.omnidim_agent_id = os.environ.get('OMNIDIM_AGENT_ID', None)
        
        # Store conversation logs and extracted information
        self.all_conversations = []
        self.all_extracted_info = []
    
    def run_simulation(self) -> Dict[str, Any]:
        """
        Run a full simulation of the voice agent workflow
        
        Returns:
            Dictionary with simulation results
        """
        print("Starting DealFinder Voice Agent simulation...")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 50)
        
        # Get all resellers
        resellers = self.data_processor.get_all_resellers()
        print(f"Found {len(resellers)} resellers to contact")
        
        # Simulate conversations with each reseller
        for i, reseller in enumerate(resellers):
            print(f"\nCalling reseller {i+1}/{len(resellers)}: {reseller['name']}...")
            
            # Create a conversation handler for this reseller
            conversation_handler = ConversationHandler(reseller)
            
            # Simulate the full conversation
            print("Simulating conversation...")
            conversation_log, extracted_info = conversation_handler.simulate_full_conversation()
            
            # Store the results
            self.all_conversations.append(conversation_log)
            self.all_extracted_info.append(extracted_info)
            
            # Print a sample of the conversation
            print(f"Conversation with {reseller['name']} completed")
            print(f"Sample exchange:")
            print(f"Agent: {conversation_log[0]['message']}")
            print(f"{reseller['name']}: {conversation_log[1]['message']}")
            
            # Add a small delay between calls for realism
            if i < len(resellers) - 1:
                print("Waiting before next call...")
                time.sleep(1)
        
        print("\nAll calls completed!")
        print("=" * 50)
        
        # Process the results
        print("\nProcessing results and ranking offers...")
        top_offers = self.data_processor.get_top_offers(3)
        
        # Print the top offers
        print("\nTop 3 offers:")
        for i, offer in enumerate(top_offers):
            print(f"{i+1}. {offer['name']} - ${offer['price']:.2f} - {offer['delivery_time']}")
        
        # Log the conversations to a Google Sheet
        print("\nLogging conversations to Google Sheet...")
        sheet_url = self.sheet_logger.log_interactions(self.all_conversations)
        
        # Log the extracted information to a Google Sheet
        print("Logging extracted information to Google Sheet...")
        info_sheet_url = self.sheet_logger.log_extracted_info(self.all_extracted_info)
        
        # Send an email with the top offers
        print("\nSending email with top offers...")
        email_response = self.email_service.send_top_offers_email("user@example.com", top_offers)
        
        print("\nSimulation completed successfully!")
        print(f"Email sent with status code: {email_response['status_code']}")
        print(f"Google Sheet URL: {sheet_url}")
        
        # Return the results
        return {
            "top_offers": top_offers,
            "sheet_url": sheet_url,
            "email_status": email_response['status_code'],
            "conversation_count": len(self.all_conversations),
            "total_interactions": sum(len(conv) for conv in self.all_conversations)
        }
    
    def generate_omnidimension_prompt(self) -> str:
        """
        Generate a prompt for OmniDimension to create the voice agent
        
        Returns:
            OmniDimension prompt
        """
        prompt = """
# DealFinder Voice Agent

## Agent Purpose
Create a voice agent that helps users find the best deals for limited edition Air Jordan 1 sneakers by calling multiple resellers, gathering pricing and availability details, comparing offers, and recommending the top 3 best options.

## Agent Capabilities
1. Make outbound calls to resellers
2. Ask structured questions about pricing, availability, and delivery options
3. Understand and process reseller responses
4. Compare offers based on price, delivery time, and availability
5. Select and recommend the top 3 offers
6. Send email with recommendations
7. Log all interactions to a Google Sheet

## Agent Personality
- Professional and helpful
- Clear and concise in communication
- Focused on gathering accurate information
- Polite when interacting with resellers
- Objective when comparing offers

## Call Flow

### Introduction
"Hello, I'm calling from DealFinder AI. I'm interested in purchasing the Air Jordan 1 High OG 'Chicago Reimagined' in size US 10. Could you tell me about your current pricing and availability?"

### Information Gathering
- Ask about current price
- Ask about availability status
- Ask about delivery options and timeframes
- Ask about any special offers or promotions

### Closing
"Thank you for the information. I'm comparing offers from several sellers and will get back to you if I decide to proceed with your offer. Have a great day!"

## Post-Call Actions
1. Log the conversation details to a Google Sheet
2. Extract key information (price, availability, delivery time)
3. Compare offers from all resellers
4. Select top 3 offers based on price, delivery time, and availability
5. Send email to the user with the top 3 recommendations

## Webhooks
- POST to /log-conversation endpoint with conversation details
- POST to /send-email endpoint with top offer details

## Voice Settings
- Voice: Professional, neutral tone
- Speaking rate: Medium
- Language: English (US)

## Error Handling
- If reseller doesn't have the product: Thank them and end the call
- If pricing information is unclear: Ask for clarification
- If connection issues: Attempt to reconnect or reschedule
"""
        return prompt
    
    def generate_webhook_configuration(self) -> Dict[str, Any]:
        """
        Generate a configuration for the OmniDimension webhooks
        
        Returns:
            Webhook configuration dictionary
        """
        webhook_config = {
            "webhooks": [
                {
                    "name": "log_conversation",
                    "endpoint": "https://api.dealfinder.ai/webhooks/log-conversation",
                    "method": "POST",
                    "headers": {
                        "Content-Type": "application/json",
                        "Authorization": "Bearer {{API_KEY}}"
                    },
                    "payload_template": {
                        "conversation_id": "{{conversation_id}}",
                        "timestamp": "{{timestamp}}",
                        "reseller_name": "{{entity.reseller_name}}",
                        "interactions": "{{conversation.messages}}",
                        "extracted_info": {
                            "price": "{{entity.price}}",
                            "availability": "{{entity.availability}}",
                            "delivery_time": "{{entity.delivery_time}}",
                            "special_offers": "{{entity.special_offers}}"
                        }
                    },
                    "trigger": "post_call"
                },
                {
                    "name": "send_email",
                    "endpoint": "https://api.dealfinder.ai/webhooks/send-email",
                    "method": "POST",
                    "headers": {
                        "Content-Type": "application/json",
                        "Authorization": "Bearer {{API_KEY}}"
                    },
                    "payload_template": {
                        "user_email": "{{user.email}}",
                        "top_offers": "{{workflow.top_offers}}",
                        "timestamp": "{{timestamp}}"
                    },
                    "trigger": "workflow_complete"
                }
            ]
        }
        return webhook_config
    
    def save_omnidimension_configuration(self) -> None:
        """
        Save the OmniDimension configuration to files
        """
        # Create the configuration directory
        config_dir = os.path.join(project_root, 'omnidimension_config')
        os.makedirs(config_dir, exist_ok=True)
        
        # Save the prompt
        prompt = self.generate_omnidimension_prompt()
        with open(os.path.join(config_dir, 'agent_prompt.md'), 'w') as f:
            f.write(prompt)
        
        # Save the webhook configuration
        webhook_config = self.generate_webhook_configuration()
        with open(os.path.join(config_dir, 'webhook_config.json'), 'w') as f:
            json.dump(webhook_config, f, indent=2)
        
        print(f"OmniDimension configuration saved to {config_dir}")
        
    def create_omnidim_agent(self) -> Dict[str, Any]:
        """
        Create a new Omnidim voice agent using the generated prompt
        
        Returns:
            Dictionary with agent details including the agent ID
        """
        if not self.omnidim_enabled or not self.omnidim_service:
            raise ValueError("Omnidim service is not enabled or initialized")
        
        prompt = self.generate_omnidimension_prompt()
        agent_data = self.omnidim_service.create_agent(
            name="Deal Finder Voice Agent",
            description="A voice agent that helps users find the best deals for high-demand products by calling resellers",
            prompt=prompt
        )
        
        # Save the agent ID for future use
        self.omnidim_agent_id = agent_data.get('id')
        
        # Configure webhooks
        webhook_config = self.generate_webhook_configuration()
        self.omnidim_service.configure_webhooks(self.omnidim_agent_id, webhook_config)
        
        print(f"Created Omnidim agent with ID: {self.omnidim_agent_id}")
        return agent_data
    
    def update_omnidim_agent(self) -> Dict[str, Any]:
        """
        Update an existing Omnidim voice agent with the latest prompt
        
        Returns:
            Dictionary with updated agent details
        """
        if not self.omnidim_enabled or not self.omnidim_service:
            raise ValueError("Omnidim service is not enabled or initialized")
            
        if not self.omnidim_agent_id:
            raise ValueError("No agent ID available. Create an agent first or set OMNIDIM_AGENT_ID environment variable")
        
        prompt = self.generate_omnidimension_prompt()
        agent_data = self.omnidim_service.update_agent(
            agent_id=self.omnidim_agent_id,
            prompt=prompt
        )
        
        # Update webhooks
        webhook_config = self.generate_webhook_configuration()
        self.omnidim_service.configure_webhooks(self.omnidim_agent_id, webhook_config)
        
        print(f"Updated Omnidim agent with ID: {self.omnidim_agent_id}")
        return agent_data
    
    def make_omnidim_call(self, phone_number: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Make a real call using the Omnidim voice agent
        
        Args:
            phone_number: Phone number to call
            metadata: Optional metadata for the call
            
        Returns:
            Call details
        """
        if not self.omnidim_enabled or not self.omnidim_service:
            raise ValueError("Omnidim service is not enabled or initialized")
            
        if not self.omnidim_agent_id:
            raise ValueError("No agent ID available. Create an agent first or set OMNIDIM_AGENT_ID environment variable")
        
        # Default metadata if not provided
        if metadata is None:
            metadata = {
                "product": "Limited Edition Air Jordan 1 High OG 'Chicago Reimagined' Sneakers",
                "user_email": "user@example.com"
            }
        
        call_data = self.omnidim_service.make_call(
            agent_id=self.omnidim_agent_id,
            phone_number=phone_number,
            metadata=metadata
        )
        
        print(f"Initiated Omnidim call to {phone_number}, call ID: {call_data.get('id')}")
        return call_data
    
    def make_bulk_omnidim_calls(self, phone_numbers: List[str], 
                               campaign_name: str = "Deal Finder Campaign",
                               metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Make bulk calls to multiple resellers using the Omnidim voice agent
        
        Args:
            phone_numbers: List of phone numbers to call
            campaign_name: Name of the campaign
            metadata: Optional metadata for the campaign
            
        Returns:
            Campaign details
        """
        if not self.omnidim_enabled or not self.omnidim_service:
            raise ValueError("Omnidim service is not enabled or initialized")
            
        if not self.omnidim_agent_id:
            raise ValueError("No agent ID available. Create an agent first or set OMNIDIM_AGENT_ID environment variable")
        
        # Default metadata if not provided
        if metadata is None:
            metadata = {
                "product": "Limited Edition Air Jordan 1 High OG 'Chicago Reimagined' Sneakers",
                "user_email": "user@example.com"
            }
        
        campaign_data = self.omnidim_service.create_bulk_call_campaign(
            agent_id=self.omnidim_agent_id,
            phone_numbers=phone_numbers,
            name=campaign_name,
            metadata=metadata
        )
        
        print(f"Initiated bulk Omnidim calls to {len(phone_numbers)} resellers, campaign ID: {campaign_data.get('id')}")
        return campaign_data
    
    def get_omnidim_call_logs(self, call_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get logs for Omnidim calls
        
        Args:
            call_id: Optional specific call ID to get logs for
            
        Returns:
            List of call logs
        """
        if not self.omnidim_enabled or not self.omnidim_service:
            raise ValueError("Omnidim service is not enabled or initialized")
        
        if call_id:
            # Get logs for a specific call
            call_data = self.omnidim_service.get_call(call_id)
            return [call_data]
        else:
            # Get logs for all calls associated with the agent
            if not self.omnidim_agent_id:
                raise ValueError("No agent ID available. Create an agent first or set OMNIDIM_AGENT_ID environment variable")
                
            return self.omnidim_service.list_calls(agent_id=self.omnidim_agent_id)


if __name__ == "__main__":
    # Create and run the voice agent
    agent = VoiceAgent()
    results = agent.run_simulation()
    
    # Save the OmniDimension configuration
    agent.save_omnidimension_configuration()
    
    # Print the results
    print("\nSimulation Results:")
    print(json.dumps(results, indent=2))
