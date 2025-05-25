# Deal Finder Voice Agent
WEBSITE LINK - https://gaganjha1.github.io/Voice-Agent-for-Finding-the-Best-Deal-on-HighDemand-Drops/

A voice agent that helps users find the best deals for high-demand products by simulating calls with multiple resellers, gathering pricing and availability details, comparing offers, and recommending the top 3 best options.

## Project Overview

This project demonstrates a voice agent that:
1. Calls or simulates calls with multiple resellers of a high-demand product
2. Gathers details including price, delivery time, and seller information
3. Compares offers to find the best deals
4. Recommends the top 3 best options to the user
5. Sends an email to the user with these top 3 options
6. Logs call interactions in a Google Sheet

## Product Focus

For this implementation, we're focusing on **Limited Edition Air Jordan 1 High OG 'Chicago Reimagined' Sneakers**.

## Demo Files

You can view the demo files directly:

1. [Email Preview](./email_preview.html) - Preview of the email that will be sent to users with deal information
2. [Call Logs](./call_logs.html) - Logs of calls made by the voice agent
3. [Extracted Information](./extracted_info.html) - Information extracted from calls with resellers

## Key Features

### 1. OmniDimension Voice Agent Integration

This project integrates with the OmniDimension platform to create a powerful voice agent that can:

- Make outbound calls to resellers to gather pricing and availability information
- Process and analyze responses using natural language understanding
- Compare deals across multiple resellers to find the best options
- Communicate findings back to users via voice, email, and dashboard interfaces

**OmniDimension Agent Link:** [https://omnidimension.ai/agents/deal-finder-v1](https://omnidimension.ai/agents/deal-finder-v1)

### 2. Email Notifications with Top Deals

The system automatically sends email notifications to users with:

- Top 3 best deals based on price, delivery time, and special offers
- Detailed comparison of each deal with key metrics highlighted
- Direct links to contact resellers or make purchases
- Personalized recommendations based on user preferences

See the [Email Preview](./email_preview.html) for a demonstration of this feature.

### 3. Comprehensive Data Logging

All interactions and data are logged for analysis and reference:

- Google Sheets integration for real-time data updates
- CRM entries for each user interaction and reseller contact
- Detailed call logs with transcripts and extracted information
- Analytics dashboard for tracking performance metrics

View the [Call Logs](./call_logs.html) and [Extracted Information](./extracted_info.html) for examples of the logged data.

## Implementation with OmniDimension

To implement this voice agent on the OmniDimension platform:

1. Create a new voice agent in the OmniDimension dashboard
2. Configure the agent with the provided scripts and prompts
3. Set up webhooks to handle user requests and reseller interactions
4. Deploy the API server to handle webhook requests
5. Test the voice agent with sample queries

### Data Flow Architecture

```
┌─────────────┐    ┌─────────────────┐    ┌───────────────┐
│ User Request │───▶│ OmniDimension AI │───▶│ Reseller Calls │
└─────────────┘    └─────────────────┘    └───────────────┘
                            │                      │
                            ▼                      ▼
                    ┌───────────────┐      ┌───────────────┐
                    │ Data Analysis │◀─────│ Data Extraction│
                    └───────────────┘      └───────────────┘
                            │
            ┌───────────────┼───────────────┐
            ▼               ▼               ▼
    ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
    │ Email Alert │  │ Google Sheet│  │   CRM Entry  │
    └─────────────┘  └─────────────┘  └─────────────┘
```

## Project Structure

```
deal-finder-voice-agent/
├── email_preview.html          # Demo of email sent to users
├── call_logs.html              # Demo of conversation logs
├── extracted_info.html         # Demo of extracted information
├── omnidimension_config/       # OmniDimension configuration
│   ├── agent_prompt.md         # Prompt for creating the voice agent
│   ├── webhook_config.json     # Webhook configuration
│   └── setup_guide.md          # Detailed setup instructions
├── src/
│   ├── agent/                  # Voice agent implementation
│   ├── data/                   # Mock reseller data
│   ├── services/               # Email and logging services
│   └── utils/                  # Utility functions
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation
```

## OmniDimension Setup

To implement this voice agent on the OmniDimension platform:

1. **Create a New Voice Agent**:
   - Log in to your OmniDimension account
   - Navigate to the "Create Agent" section
   - Select "Voice Agent" as the agent type
   - Name your agent "DealFinder"

2. **Configure the Agent**:
   - Use the prompt in `omnidimension_config/agent_prompt.md` to define the agent's behavior
   - Configure webhooks using `omnidimension_config/webhook_config.json`
   - Follow the detailed instructions in `omnidimension_config/setup_guide.md`

3. **Set Up Webhooks**:
   - Deploy the API server to handle webhook requests
   - Configure the webhook endpoints in OmniDimension to point to your server

## Implementation Details

### Voice Agent

The voice agent is designed to have natural conversations with resellers, asking about:
- Current pricing for the sneakers
- Availability status
- Delivery options and timeframes
- Special offers or promotions

### Mock Reseller Data

The project includes mock data for 5 resellers, each with different:
- Pricing strategies
- Delivery timeframes
- Availability status
- Special offers
- Personality traits that affect their responses

### Ranking Logic

The agent ranks offers based on:
- Price (50% weight) - lower is better
- Delivery time (30% weight) - faster is better
- Availability (20% weight) - in stock is better than limited stock

## Screenshots

Open the HTML files to see interactive demos of:

1. **Email with Top 3 Offers**:
   - Ranked list of the best deals
   - Detailed comparison of price, delivery, and special offers
   - Contact information for each seller
   - Explanation of why these offers were selected

2. **Call Logs**:
   - Complete conversation history with each reseller
   - Timestamps for each interaction
   - Different conversation styles based on reseller personality

3. **Extracted Information**:
   - Structured data from all conversations
   - Visual comparison of prices and delivery times
   - Sorting and filtering options

## Next Steps for Implementation

1. **OmniDimension Setup**:
   - Create an account on OmniDimension
   - Follow the setup guide in `omnidimension_config/setup_guide.md`

2. **Webhook Server**:
   - Deploy the API server to handle post-call actions
   - Configure the webhooks in OmniDimension

3. **Testing and Refinement**:
   - Test the agent with simulated calls
   - Refine the prompts and entity extraction
   - Adjust the ranking logic as needed
