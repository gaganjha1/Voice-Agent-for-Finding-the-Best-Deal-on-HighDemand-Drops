import os
import json
from typing import Dict, Any, List
from fastapi import FastAPI, HTTPException, BackgroundTasks, Request
from pydantic import BaseModel
import uvicorn
import sys

# Add the project root to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

from src.services.email_service import EmailService
from src.services.sheet_logger import SheetLogger
from src.utils.data_processor import DataProcessor

app = FastAPI(title="DealFinder Voice Agent API")

# Initialize services
email_service = EmailService()
sheet_logger = SheetLogger()
data_processor = DataProcessor()

# Define API models
class ConversationLog(BaseModel):
    conversation_id: str
    timestamp: str
    reseller_name: str
    interactions: List[Dict[str, Any]]
    extracted_info: Dict[str, Any]

class EmailRequest(BaseModel):
    user_email: str
    top_offers: List[Dict[str, Any]]
    timestamp: str

@app.get("/")
async def root():
    """
    Root endpoint that returns a welcome message
    """
    return {"message": "Welcome to the DealFinder Voice Agent API"}

@app.post("/webhooks/log-conversation")
async def log_conversation(conversation: ConversationLog, background_tasks: BackgroundTasks):
    """
    Webhook endpoint for logging conversation details
    """
    try:
        # Log the conversation in the background
        background_tasks.add_task(
            sheet_logger.log_interactions, 
            [[interaction for interaction in conversation.interactions]]
        )
        
        return {
            "status": "success",
            "message": f"Conversation with {conversation.reseller_name} logged successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/webhooks/send-email")
async def send_email(email_request: EmailRequest, background_tasks: BackgroundTasks):
    """
    Webhook endpoint for sending email with top offers
    """
    try:
        # Send the email in the background
        background_tasks.add_task(
            email_service.send_top_offers_email,
            email_request.user_email,
            email_request.top_offers
        )
        
        return {
            "status": "success",
            "message": f"Email sent to {email_request.user_email} with top offers"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/demo/top-offers")
async def get_top_offers():
    """
    Demo endpoint that returns the top 3 offers
    """
    top_offers = data_processor.get_top_offers(3)
    return {"top_offers": top_offers}

@app.get("/demo/all-resellers")
async def get_all_resellers():
    """
    Demo endpoint that returns all resellers
    """
    resellers = data_processor.get_all_resellers()
    return {"resellers": resellers}

@app.post("/demo/simulate-conversation")
async def simulate_conversation(request: Request):
    """
    Demo endpoint that simulates a conversation with a reseller
    """
    data = await request.json()
    reseller_id = data.get("reseller_id", 1)
    
    # Get the reseller data
    reseller = data_processor.get_reseller_by_id(reseller_id)
    if not reseller:
        raise HTTPException(status_code=404, detail=f"Reseller with ID {reseller_id} not found")
    
    # Import here to avoid circular imports
    from src.utils.conversation_handler import ConversationHandler
    
    # Create a conversation handler for this reseller
    conversation_handler = ConversationHandler(reseller)
    
    # Simulate the full conversation
    conversation_log, extracted_info = conversation_handler.simulate_full_conversation()
    
    return {
        "reseller_name": reseller["name"],
        "conversation_log": conversation_log,
        "extracted_info": extracted_info
    }

def start_server():
    """
    Start the FastAPI server
    """
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    start_server()
