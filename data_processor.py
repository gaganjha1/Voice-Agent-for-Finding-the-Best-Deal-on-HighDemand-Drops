import json
import os
from typing import Dict, List, Any
import pandas as pd
from datetime import datetime

class DataProcessor:
    """
    Utility class for loading and processing reseller data
    """
    
    def __init__(self, data_path: str = None):
        """
        Initialize the DataProcessor with the path to the reseller data
        
        Args:
            data_path: Path to the reseller data JSON file
        """
        if data_path is None:
            # Default path relative to the project root
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(os.path.dirname(current_dir))
            data_path = os.path.join(project_root, 'src', 'data', 'resellers.json')
        
        self.data_path = data_path
        self.resellers = self._load_data()
    
    def _load_data(self) -> List[Dict[str, Any]]:
        """
        Load reseller data from the JSON file
        
        Returns:
            List of reseller data dictionaries
        """
        try:
            with open(self.data_path, 'r') as f:
                data = json.load(f)
                return data['resellers']
        except Exception as e:
            print(f"Error loading reseller data: {e}")
            return []
    
    def get_all_resellers(self) -> List[Dict[str, Any]]:
        """
        Get all reseller data
        
        Returns:
            List of all reseller data dictionaries
        """
        return self.resellers
    
    def get_reseller_by_id(self, reseller_id: int) -> Dict[str, Any]:
        """
        Get a reseller by ID
        
        Args:
            reseller_id: ID of the reseller to retrieve
            
        Returns:
            Reseller data dictionary or None if not found
        """
        for reseller in self.resellers:
            if reseller['id'] == reseller_id:
                return reseller
        return None
    
    def get_reseller_by_name(self, name: str) -> Dict[str, Any]:
        """
        Get a reseller by name
        
        Args:
            name: Name of the reseller to retrieve
            
        Returns:
            Reseller data dictionary or None if not found
        """
        for reseller in self.resellers:
            if reseller['name'].lower() == name.lower():
                return reseller
        return None
    
    def rank_offers(self) -> List[Dict[str, Any]]:
        """
        Rank reseller offers based on price and delivery time
        
        Returns:
            List of ranked reseller data dictionaries
        """
        # Create a copy of the resellers list to avoid modifying the original
        ranked_resellers = self.resellers.copy()
        
        # Calculate a score for each reseller based on price and delivery time
        for reseller in ranked_resellers:
            # Lower price is better
            price_score = 1000 - reseller['price']
            
            # Convert delivery time to numeric value (estimated days)
            delivery_time = reseller['delivery_time'].lower()
            if 'next day' in delivery_time:
                delivery_days = 1
            elif '-' in delivery_time:
                # Extract the lower range (e.g., "3-5 days" -> 3)
                delivery_days = int(delivery_time.split('-')[0].strip().split(' ')[0])
            else:
                # Default to 7 days if we can't parse
                delivery_days = 7
            
            # Lower delivery time is better
            delivery_score = 100 - (delivery_days * 10)
            
            # Availability bonus
            availability_score = 0
            if 'in stock' in reseller['availability'].lower():
                availability_score = 50
            elif 'limited' in reseller['availability'].lower():
                availability_score = 25
            
            # Calculate total score (price is most important)
            reseller['score'] = price_score + delivery_score + availability_score
        
        # Sort by score (higher is better)
        ranked_resellers.sort(key=lambda x: x['score'], reverse=True)
        
        return ranked_resellers
    
    def get_top_offers(self, count: int = 3) -> List[Dict[str, Any]]:
        """
        Get the top N offers based on ranking
        
        Args:
            count: Number of top offers to return
            
        Returns:
            List of top N reseller data dictionaries
        """
        ranked_offers = self.rank_offers()
        return ranked_offers[:count]
    
    def format_offer_for_email(self, offer: Dict[str, Any]) -> str:
        """
        Format an offer for inclusion in an email
        
        Args:
            offer: Reseller offer dictionary
            
        Returns:
            Formatted offer string
        """
        return f"""
Seller: {offer['name']}
Product: {offer['product']['name']}
Price: ${offer['price']:.2f}
Delivery: {offer['delivery_time']}
Availability: {offer['availability']}
Special Offer: {offer['special_offers']}
Contact: {offer['contact']['phone']} | {offer['contact']['email']}
"""
    
    def create_comparison_dataframe(self, offers: List[Dict[str, Any]] = None) -> pd.DataFrame:
        """
        Create a pandas DataFrame for comparing offers
        
        Args:
            offers: List of offers to compare (defaults to all resellers)
            
        Returns:
            DataFrame with offer comparison
        """
        if offers is None:
            offers = self.resellers
            
        data = []
        for offer in offers:
            data.append({
                'Seller': offer['name'],
                'Price': f"${offer['price']:.2f}",
                'Delivery': offer['delivery_time'],
                'Availability': offer['availability'],
                'Special Offer': offer['special_offers']
            })
            
        return pd.DataFrame(data)
