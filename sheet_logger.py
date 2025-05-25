import os
import json
import pandas as pd
from typing import Dict, List, Any
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

class SheetLogger:
    """
    Service for logging call interactions to a Google Sheet
    """
    
    def __init__(self, credentials_path: str = None):
        """
        Initialize the SheetLogger with Google API credentials
        
        Args:
            credentials_path: Path to the Google API credentials JSON file
        """
        self.credentials_path = credentials_path
        # For demo purposes, we'll simulate the Google Sheets integration
        self.sheet_url = "https://docs.google.com/spreadsheets/d/mock-sheet-id/edit#gid=0"
    
    def log_interactions(self, conversations: List[List[Dict[str, Any]]]) -> str:
        """
        Log conversation interactions to a Google Sheet
        
        Args:
            conversations: List of conversation logs from multiple resellers
            
        Returns:
            URL of the Google Sheet
        """
        # Flatten the conversations into a single list of interactions
        all_interactions = []
        for conversation in conversations:
            all_interactions.extend(conversation)
        
        # Convert to DataFrame for easier manipulation
        df = pd.DataFrame(all_interactions)
        
        # In a real implementation, we would use:
        # scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        # creds = ServiceAccountCredentials.from_json_keyfile_name(self.credentials_path, scope)
        # client = gspread.authorize(creds)
        # sheet = client.create('DealFinder Call Logs - ' + datetime.now().strftime('%Y-%m-%d'))
        # sheet.share('user@example.com', perm_type='user', role='writer')
        # worksheet = sheet.get_worksheet(0)
        # worksheet.update([df.columns.values.tolist()] + df.values.tolist())
        
        # For demo purposes, save to a CSV file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        csv_path = os.path.join(project_root, 'call_logs.csv')
        df.to_csv(csv_path, index=False)
        
        # Also save a more readable HTML version
        html_path = os.path.join(project_root, 'call_logs.html')
        df.to_html(html_path, index=False)
        
        # Create a mock sheet data file for demo purposes
        self._create_mock_sheet_data(df)
        
        return self.sheet_url
    
    def log_extracted_info(self, extracted_info_list: List[Dict[str, Any]]) -> str:
        """
        Log extracted information to a Google Sheet
        
        Args:
            extracted_info_list: List of extracted information from conversations
            
        Returns:
            URL of the Google Sheet
        """
        # Convert to DataFrame for easier manipulation
        df = pd.DataFrame(extracted_info_list)
        
        # For demo purposes, save to a CSV file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        csv_path = os.path.join(project_root, 'extracted_info.csv')
        df.to_csv(csv_path, index=False)
        
        # Also save a more readable HTML version
        html_path = os.path.join(project_root, 'extracted_info.html')
        df.to_html(html_path, index=False)
        
        return self.sheet_url
    
    def _create_mock_sheet_data(self, df: pd.DataFrame) -> None:
        """
        Create a mock Google Sheet data file for demo purposes
        
        Args:
            df: DataFrame containing the data to be logged
        """
        sheet_data = {
            "sheet_name": "DealFinder Call Logs - 2025-05-25",
            "sheet_url": self.sheet_url,
            "created_at": "2025-05-25T18:00:00+05:30",
            "columns": df.columns.tolist(),
            "row_count": len(df),
            "sample_rows": df.head(5).to_dict('records')
        }
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        
        with open(os.path.join(project_root, 'sheet_data.json'), 'w') as f:
            json.dump(sheet_data, f, indent=2)
