import os, time, threading
from flask import Flask, render_template
from flask_socketio import SocketIO
from web3 import Web3

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

w3 = Web3(Web3.WebsocketProvider(os.getenv("ETH_NODE_WS")))
if not w3.isConnected():
    raise RuntimeError("Ethereum node connection failed")
TRANSFER_SIG = w3.keccak(text="Transfer(address,address,uint256)").hex()

TOKENS = {
    "0xtokencontractaddress".lower(): {
        "pair":      "0xpaircontractaddress".lower(),
        "threshold": 1000,  
        "tradeAmt":  5  
    },
}

def monitor_chain():
    f = w3.eth.filter({
        "fromBlock": "latest",
        "address":   list(TOKENS.keys()),
        "topics":    [TRANSFER_SIG]
    })
    while True:
        for log in f.get_new_entries():
            handle(log)
        time.sleep(3)

def handle(log):
    cfg = TOKENS[log["address"].lower()]
    frm = "0x" + log["topics"][1].hex()[-40:]
    amt = int(log["data"],16) / 1e18
    if amt < cfg["threshold"]:
        return

    side = "buy" if frm == cfg["pair"] else "sell"
    socketio.emit("trade_signal", {
        "token":  log["address"],
        "side":   side,
        "amount": str(cfg["tradeAmt"])
    })

@app.route("/")
def index():
    return render_template("index.html")

if __name__=="__main__":
    threading.Thread(target=monitor_chain, daemon=True).start()
    socketio.run(app, host="0.0.0.0", port=5000)