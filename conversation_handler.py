import json
import random
from typing import Dict, List, Any, Tuple

class ConversationHandler:
    """
    Utility class for handling voice agent conversations with resellers
    """
    
    def __init__(self, reseller_data: Dict[str, Any]):
        """
        Initialize the ConversationHandler with reseller data
        
        Args:
            reseller_data: Dictionary containing reseller information
        """
        self.reseller = reseller_data
        self.conversation_log = []
        
    def generate_greeting(self) -> str:
        """
        Generate a greeting from the voice agent to the reseller
        
        Returns:
            Greeting message
        """
        greeting = (
            f"Hello, I'm calling from DealFinder AI. I'm interested in purchasing "
            f"the {self.reseller['product']['name']} in size {self.reseller['product']['size']}. "
            f"Could you tell me about your current pricing and availability?"
        )
        
        self.log_interaction("agent", greeting)
        return greeting
    
    def generate_reseller_response(self, query_type: str) -> str:
        """
        Generate a simulated response from the reseller based on their personality
        
        Args:
            query_type: Type of query (pricing, availability, delivery, special_offers)
            
        Returns:
            Simulated reseller response
        """
        personality = self.reseller['personality'].lower()
        
        # Base response with product information
        if query_type == "pricing":
            base_response = f"The {self.reseller['product']['name']} in size {self.reseller['product']['size']} is priced at ${self.reseller['price']:.2f}."
        elif query_type == "availability":
            base_response = f"Regarding availability, we currently have this item {self.reseller['availability'].lower()}."
        elif query_type == "delivery":
            base_response = f"Our delivery time for this item is {self.reseller['delivery_time']}."
        elif query_type == "special_offers":
            base_response = f"We do have a special offer: {self.reseller['special_offers']}."
        else:
            base_response = f"I'm not sure I understand what you're asking about."
        
        # Add personality flavor to the response
        if "professional" in personality:
            flavor = random.choice([
                "I'd be happy to assist you with that.",
                "Let me provide you with that information.",
                "Thank you for your interest in our products."
            ])
        elif "enthusiastic" in personality or "eager" in personality:
            flavor = random.choice([
                "I'm super excited to tell you about this amazing deal!",
                "You're going to love these sneakers, they're flying off the shelves!",
                "I might be able to work something out if you're ready to buy today!"
            ])
        elif "knowledgeable" in personality:
            flavor = random.choice([
                "These are part of the iconic Chicago colorway series that first released in 1985.",
                "The quality on these is exceptional, with premium leather uppers and the classic Nike Air branding.",
                "These have been one of our most popular releases this year."
            ])
        elif "casual" in personality or "friendly" in personality:
            flavor = random.choice([
                "Hey, no problem at all!",
                "Yeah, these are really cool kicks.",
                "Let me know if you need anything else, happy to help!"
            ])
        elif "premium" in personality:
            flavor = random.choice([
                "We pride ourselves on offering only the finest authenticated products.",
                "Our clients appreciate the exceptional service we provide with every purchase.",
                "We can arrange a private viewing if you'd like to see the product before purchase."
            ])
        else:
            flavor = ""
        
        # Combine base response with personality flavor
        response = f"{base_response} {flavor}"
        
        self.log_interaction("reseller", response)
        return response
    
    def generate_follow_up_question(self, topic: str) -> str:
        """
        Generate a follow-up question from the agent about a specific topic
        
        Args:
            topic: Topic to ask about (delivery, special_offers, payment_options)
            
        Returns:
            Follow-up question
        """
        if topic == "delivery":
            question = f"Could you tell me more about your delivery options and timeframes?"
        elif topic == "special_offers":
            question = f"Do you have any special offers or promotions available for this product?"
        elif topic == "payment_options":
            question = f"What payment options do you accept?"
        elif topic == "authenticity":
            question = f"How do you verify the authenticity of your products?"
        else:
            question = f"Could you provide more information about {topic}?"
        
        self.log_interaction("agent", question)
        return question
    
    def generate_closing(self) -> str:
        """
        Generate a closing statement from the agent
        
        Returns:
            Closing statement
        """
        closing = (
            f"Thank you for the information. I'm comparing offers from several sellers "
            f"and will get back to you if I decide to proceed with your offer. "
            f"Have a great day!"
        )
        
        self.log_interaction("agent", closing)
        return closing
    
    def log_interaction(self, speaker: str, message: str) -> None:
        """
        Log an interaction in the conversation
        
        Args:
            speaker: Who is speaking (agent or reseller)
            message: The message content
        """
        self.conversation_log.append({
            "timestamp": "2025-05-25T18:00:00+05:30",  # Using current date from metadata
            "speaker": speaker,
            "message": message,
            "reseller_id": self.reseller['id'],
            "reseller_name": self.reseller['name']
        })
    
    def get_conversation_log(self) -> List[Dict[str, Any]]:
        """
        Get the full conversation log
        
        Returns:
            List of conversation interactions
        """
        return self.conversation_log
    
    def simulate_full_conversation(self) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
        """
        Simulate a full conversation with the reseller and extract key information
        
        Returns:
            Tuple containing (conversation_log, extracted_info)
        """
        # Start with a greeting
        self.generate_greeting()
        
        # Get pricing information
        self.generate_reseller_response("pricing")
        
        # Ask about availability
        self.generate_follow_up_question("availability")
        self.generate_reseller_response("availability")
        
        # Ask about delivery
        self.generate_follow_up_question("delivery")
        self.generate_reseller_response("delivery")
        
        # Ask about special offers
        self.generate_follow_up_question("special_offers")
        self.generate_reseller_response("special_offers")
        
        # Close the conversation
        self.generate_closing()
        
        # Extract key information from the conversation
        extracted_info = {
            "reseller_id": self.reseller['id'],
            "reseller_name": self.reseller['name'],
            "product_name": self.reseller['product']['name'],
            "price": self.reseller['price'],
            "delivery_time": self.reseller['delivery_time'],
            "availability": self.reseller['availability'],
            "special_offers": self.reseller['special_offers']
        }
        
        return self.conversation_log, extracted_info
