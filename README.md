# Whale‑Watch Web App

A Flask + Socket.IO web app that:

1. Monitors Ethereum for large ERC‑20 transfers (whale buys/sells).  
2. Emits `trade_signal` over WebSocket.  
3. Front‑end connects your Trust Wallet via WalletConnect and executes Uniswap trades.

## Setup

1. Clone & enter directory:
   ```bash
   git clone https://github.com/shashin-gupta/whale-bot-webapp.git
   cd whale-bot-webapp
2. Create Virtual environment and install dependencies
    python3 -m venv env
    source env/bin/activate
    pip install -r requirements.txt
3. Set up environmental variables
    export ETH_NODE_WS="wss://mainnet.infura.io/ws/v3/YOUR_KEY"
    export FLASK_ENV=production
4. Set up API Keys and Wallet ID
5. Run
    python app.py
