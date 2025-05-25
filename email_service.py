import os
from typing import Dict, List, Any
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content, HtmlContent
import json

class EmailService:
    """
    Service for sending emails with deal recommendations to users
    """
    
    def __init__(self, api_key: str = None):
        """
        Initialize the EmailService with a SendGrid API key
        
        Args:
            api_key: SendGrid API key (defaults to environment variable)
        """
        self.api_key = api_key or os.environ.get('SENDGRID_API_KEY', 'your_sendgrid_api_key_here')
    
    def format_offers_html(self, offers: List[Dict[str, Any]]) -> str:
        """
        Format offers as HTML for email content
        
        Args:
            offers: List of top offers
            
        Returns:
            HTML-formatted offers
        """
        html = """
        <h2>Top 3 Deals for Air Jordan 1 High OG 'Chicago Reimagined'</h2>
        <p>Based on our research, here are the best deals available:</p>
        <table style="width: 100%; border-collapse: collapse; margin-top: 20px;">
            <tr style="background-color: #f2f2f2;">
                <th style="padding: 12px; text-align: left; border: 1px solid #ddd;">Rank</th>
                <th style="padding: 12px; text-align: left; border: 1px solid #ddd;">Seller</th>
                <th style="padding: 12px; text-align: left; border: 1px solid #ddd;">Price</th>
                <th style="padding: 12px; text-align: left; border: 1px solid #ddd;">Delivery</th>
                <th style="padding: 12px; text-align: left; border: 1px solid #ddd;">Availability</th>
                <th style="padding: 12px; text-align: left; border: 1px solid #ddd;">Special Offer</th>
            </tr>
        """
        
        for i, offer in enumerate(offers):
            rank_style = ""
            if i == 0:
                rank_style = "background-color: #ffd700; font-weight: bold;"  # Gold for 1st place
            elif i == 1:
                rank_style = "background-color: #c0c0c0; font-weight: bold;"  # Silver for 2nd place
            elif i == 2:
                rank_style = "background-color: #cd7f32; font-weight: bold;"  # Bronze for 3rd place
                
            html += f"""
            <tr>
                <td style="padding: 12px; text-align: left; border: 1px solid #ddd; {rank_style}">{i+1}</td>
                <td style="padding: 12px; text-align: left; border: 1px solid #ddd;">{offer['name']}</td>
                <td style="padding: 12px; text-align: left; border: 1px solid #ddd;">${offer['price']:.2f}</td>
                <td style="padding: 12px; text-align: left; border: 1px solid #ddd;">{offer['delivery_time']}</td>
                <td style="padding: 12px; text-align: left; border: 1px solid #ddd;">{offer['availability']}</td>
                <td style="padding: 12px; text-align: left; border: 1px solid #ddd;">{offer['special_offers']}</td>
            </tr>
            """
        
        html += """
        </table>
        <div style="margin-top: 30px;">
            <h3>Why We Selected These Deals</h3>
            <p>Our AI agent evaluated these offers based on a combination of factors:</p>
            <ul>
                <li><strong>Price:</strong> Lower prices received higher rankings</li>
                <li><strong>Delivery Time:</strong> Faster delivery options were preferred</li>
                <li><strong>Availability:</strong> In-stock items were prioritized</li>
                <li><strong>Special Offers:</strong> Added value through promotions or extras</li>
            </ul>
        </div>
        <div style="margin-top: 30px;">
            <h3>Contact Information</h3>
        """
        
        for i, offer in enumerate(offers):
            html += f"""
            <p><strong>{i+1}. {offer['name']}</strong><br>
            Phone: {offer['contact']['phone']}<br>
            Email: <a href="mailto:{offer['contact']['email']}">{offer['contact']['email']}</a></p>
            """
        
        html += """
        </div>
        <div style="margin-top: 30px; padding: 15px; background-color: #f9f9f9; border-radius: 5px;">
            <p>This information was gathered by our AI voice agent on May 25, 2025. Prices and availability may change.</p>
            <p>To purchase, contact the seller directly using the information provided above.</p>
        </div>
        """
        
        return html
    
    def send_top_offers_email(self, to_email: str, offers: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Send an email with the top offers to the user
        
        Args:
            to_email: Recipient email address
            offers: List of top offers
            
        Returns:
            Response from the SendGrid API
        """
        # For demo purposes, we'll simulate the email sending and return a mock response
        # In a real implementation, this would use the SendGrid API to send the actual email
        
        from_email = Email("deals@dealfinder.ai", "DealFinder AI")
        to_email = To(to_email)
        subject = "Your Top 3 Deals for Air Jordan 1 Chicago Sneakers"
        html_content = HtmlContent(self.format_offers_html(offers))
        
        # Create a mock email object
        email = {
            "from": from_email.get(),
            "to": to_email.get(),
            "subject": subject,
            "html_content": html_content.get()
        }
        
        # In a real implementation, we would use:
        # message = Mail(from_email, to_email, subject, content, html_content)
        # sg = SendGridAPIClient(self.api_key)
        # response = sg.send(message)
        # return {"status_code": response.status_code, "body": response.body, "headers": response.headers}
        
        # For demo purposes, return a mock success response
        mock_response = {
            "status_code": 202,
            "body": "",
            "headers": {
                "server": "nginx",
                "date": "Sun, 25 May 2025 13:30:00 GMT",
                "content-length": "0",
                "connection": "close",
                "x-message-id": "mock-message-id-12345",
                "access-control-allow-origin": "*",
                "access-control-allow-methods": "POST",
                "access-control-allow-headers": "authorization, content-type, on-behalf-of, x-sg-elas-acl",
                "access-control-max-age": "600",
                "x-ratelimit-limit": "600",
                "x-ratelimit-remaining": "599",
                "x-ratelimit-reset": "1621951800"
            }
        }
        
        # Save the email content to a file for demo purposes
        self._save_email_demo(email)
        
        return mock_response
    
    def _save_email_demo(self, email: Dict[str, Any]) -> None:
        """
        Save the email content to a file for demo purposes
        
        Args:
            email: Email content dictionary
        """
        # Create a simplified version for the demo file
        demo_email = {
            "from": email["from"],
            "to": email["to"],
            "subject": email["subject"],
            "html_content_preview": "HTML content is too large to display in JSON. See email_preview.html for the full content."
        }
        
        # Save the email metadata
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        
        with open(os.path.join(project_root, 'email_demo.json'), 'w') as f:
            json.dump(demo_email, f, indent=2)
        
        # Save the HTML content separately
        with open(os.path.join(project_root, 'email_preview.html'), 'w') as f:
            f.write(email["html_content"])
