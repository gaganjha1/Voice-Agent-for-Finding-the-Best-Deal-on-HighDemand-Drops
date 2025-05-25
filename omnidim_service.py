import os
import json
from typing import Dict, List, Any, Optional
from omnidimension import Client

class OmnidimService:
    """
    Service class for interacting with the Omnidim voice assistant API
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Omnidim service with API key
        
        Args:
            api_key: Optional API key. If not provided, will attempt to get from environment variable
        """
        # Get API key from environment variable if not provided
        if api_key is None:
            api_key = os.environ.get('OMNIDIM_API_KEY')
            
        if not api_key:
            raise ValueError("Omnidim API key is required. Set OMNIDIM_API_KEY environment variable or pass directly.")
            
        # Initialize the Omnidim client
        self.client = Client(api_key)
        
    def list_agents(self) -> List[Dict[str, Any]]:
        """
        List all available voice agents
        
        Returns:
            List of agent dictionaries
        """
        return self.client.agent.list()
        
    def create_agent(self, name: str, description: str, prompt: str) -> Dict[str, Any]:
        """
        Create a new voice agent
        
        Args:
            name: Name of the agent
            description: Short description of the agent
            prompt: Detailed prompt for the agent behavior
            
        Returns:
            Created agent details
        """
        agent_data = {
            "name": name,
            "description": description,
            "prompt": prompt
        }
        
        return self.client.agent.create(**agent_data)
        
    def update_agent(self, agent_id: str, **kwargs) -> Dict[str, Any]:
        """
        Update an existing voice agent
        
        Args:
            agent_id: ID of the agent to update
            **kwargs: Fields to update (name, description, prompt, etc.)
            
        Returns:
            Updated agent details
        """
        return self.client.agent.update(agent_id, **kwargs)
        
    def get_agent(self, agent_id: str) -> Dict[str, Any]:
        """
        Get details for a specific agent
        
        Args:
            agent_id: ID of the agent
            
        Returns:
            Agent details
        """
        return self.client.agent.get(agent_id)
        
    def delete_agent(self, agent_id: str) -> Dict[str, Any]:
        """
        Delete a voice agent
        
        Args:
            agent_id: ID of the agent to delete
            
        Returns:
            Response details
        """
        return self.client.agent.delete(agent_id)
        
    def make_call(self, agent_id: str, phone_number: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Initiate a call using an agent
        
        Args:
            agent_id: ID of the agent to use for the call
            phone_number: Target phone number to call
            metadata: Optional metadata for the call
            
        Returns:
            Call details
        """
        call_data = {
            "agent_id": agent_id,
            "to": phone_number
        }
        
        if metadata:
            call_data["metadata"] = metadata
            
        return self.client.call.create(**call_data)
        
    def get_call(self, call_id: str) -> Dict[str, Any]:
        """
        Get details for a specific call
        
        Args:
            call_id: ID of the call
            
        Returns:
            Call details
        """
        return self.client.call.get(call_id)
        
    def list_calls(self, agent_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        List all calls, optionally filtered by agent
        
        Args:
            agent_id: Optional agent ID to filter calls by
            
        Returns:
            List of call dictionaries
        """
        params = {}
        if agent_id:
            params["agent_id"] = agent_id
            
        return self.client.call.list(**params)
        
    def configure_webhooks(self, agent_id: str, webhook_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Configure webhooks for an agent
        
        Args:
            agent_id: ID of the agent
            webhook_config: Webhook configuration dictionary
            
        Returns:
            Response details
        """
        return self.client.agent.update(agent_id, webhooks=webhook_config)
        
    def setup_knowledge_base(self, agent_id: str, files: List[str]) -> Dict[str, Any]:
        """
        Setup a knowledge base for an agent
        
        Args:
            agent_id: ID of the agent
            files: List of file paths to add to the knowledge base
            
        Returns:
            Response details
        """
        response = {}
        for file_path in files:
            with open(file_path, 'rb') as f:
                upload_response = self.client.knowledge_base.upload(agent_id, f)
                response[file_path] = upload_response
                
        return response
    
    def create_bulk_call_campaign(self, agent_id: str, phone_numbers: List[str], 
                                  name: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Create a bulk call campaign
        
        Args:
            agent_id: ID of the agent to use
            phone_numbers: List of phone numbers to call
            name: Campaign name
            metadata: Optional metadata for the campaign
            
        Returns:
            Campaign details
        """
        campaign_data = {
            "agent_id": agent_id,
            "name": name,
            "phone_numbers": phone_numbers
        }
        
        if metadata:
            campaign_data["metadata"] = metadata
            
        return self.client.bulk_call.create(**campaign_data)
