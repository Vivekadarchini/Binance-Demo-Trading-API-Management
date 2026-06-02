# Binance Futures Testnet Trading Bot CLI

A professional, interview-quality, clean-architecture trading bot for placing MARKET and LIMIT orders on the **Binance Futures Testnet (USDT-M)**.

Developed in Python 3, this command-line tool features strict input validation, detailed structured logging, and robust API/network error handling.

---

## Project Structure

```text
trading_bot/
├── bot/
│   ├── __init__.py          # Package entry point and exports
│   ├── client.py            # API client initialization & connectivity check
│   ├── orders.py            # Order placement & exception parsing logic
│   ├── validators.py        # Input sanitation and business rule validation
│   ├── logging_config.py    # Structured file logging setup
│   └── logs/
│       └── trading_bot.log  # Rotating structured log file (auto-generated)
├── cli.py                   # Main CLI entry point (argparse)
├── requirements.txt         # Project dependencies
├── .env                     # Local configuration credentials (ignored by git)
└── README.md                # Project documentation and manual
```

---

## Setup & Installation

### Prerequisites
- Python 3.8 or higher.
- A Binance Futures Testnet account. If you don't have one, register at [Binance Futures Testnet](https://testnet.binancefuture.com).

### 1. Clone or Copy the Repository
Navigate to the root directory `trading_bot/`:
```bash
cd trading_bot
```

### 2. Create and Activate a Virtual Environment (Recommended)
On Windows (PowerShell):
```powershell
python -m venv venv
.\venv\Scripts\activate
```
On macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create or edit the `.env` file in the root of the project:
```env
# Binance Futures Testnet API Credentials
# Get your keys from: https://testnet.binancefuture.com
BINANCE_API_KEY=your_futures_testnet_api_key_here
BINANCE_API_SECRET=your_futures_testnet_api_secret_here
```
> [!IMPORTANT]
> Make sure to replace `your_futures_testnet_api_key_here` and `your_futures_testnet_api_secret_here` with actual credentials generated from the Binance Futures Testnet website. Live exchange keys will not work.

---

## Usage Examples

Execute orders using `cli.py` via python. The parameters are:
- `--symbol` (Required) - Trading pair (e.g. `BTCUSDT`, `ETHUSDT`)
- `--side` (Required) - `BUY` or `SELL`
- `--type` (Required) - `MARKET` or `LIMIT`
- `--quantity` (Required) - Trade size (number of contracts)
- `--price` (Required only for `LIMIT` orders) - Execution limit price

### 1. Place a MARKET BUY Order
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
```

### 2. Place a LIMIT SELL Order
```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.005 --price 68500
```

### 3. Help Command
To view CLI manual and usage details:
```bash
python cli.py --help
```

---

## Assumptions & Design Decisions
1. **Validation Layer**: The validation is decoupled from the execution. It verifies parameter bounds (e.g. quantity/price > 0), uppercase requirements, and contextual dependencies (e.g., price is required for `LIMIT` but forbidden for `MARKET`) before attempting any network requests.
2. **Time in Force**: Limit orders default to `GTC` (Good 'Til Canceled) to satisfy Binance Futures requirements.
3. **Structured Logging**: Logs are directed solely to a rotating log file in `bot/logs/trading_bot.log`. This keeps the CLI terminal output clean, readable, and free of timestamp headers unless an error occurs.
4. **Safety & Testnet**: The client overrides the endpoint base URL specifically to prevent live financial transactions, operating strictly within Binance's mock trading sandbox.

---

## Sample Console Output

### Market Order Success Output
```text
--- ORDER REQUEST SUMMARY ---
Symbol:   BTCUSDT
Side:     BUY
Type:     MARKET
Quantity: 0.01
-----------------------------

--- ORDER RESPONSE DETAILS ---
{
  "orderId": 28318485,
  "symbol": "BTCUSDT",
  "status": "FILLED",
  "clientOrderId": "5LhR8Wn9T67yHk19",
  "price": "0.00",
  "avgPrice": "67320.50",
  "origQty": "0.010",
  "executedQty": "0.010",
  "cumQty": "0.010",
  "cumQuote": "673.20500",
  "timeInForce": "GTC",
  "type": "MARKET",
  "reduceOnly": false,
  "closePosition": false,
  "side": "BUY",
  "positionSide": "BOTH",
  "stopPrice": "0.00",
  "workingType": "CONTRACT_PRICE",
  "priceProtect": false,
  "origType": "MARKET",
  "updateTime": 1774883162000
}
------------------------------

[SUCCESS] Order placed successfully!
```

### Validation Error Output
```text
[INPUT ERROR] Validation failed: Price is required for LIMIT orders.
```

### Binance API Error Output (e.g., Invalid API Keys)
```text
--- ORDER REQUEST SUMMARY ---
Symbol:   BTCUSDT
Side:     BUY
Type:     MARKET
Quantity: 0.01
-----------------------------

[FAILURE] Order placement failed!
Error Details: Binance API Error: Invalid API-key, IP, or permissions for action. (Code: -2015)
```

---

## Example Log Entries (`bot/logs/trading_bot.log`)

### MARKET Order Log Trace
```text
2026-06-02 11:46:00 | INFO     | client.py:45 | Initializing Binance client for Futures Testnet...
2026-06-02 11:46:00 | INFO     | client.py:48 | Binance client initialized successfully.
2026-06-02 11:46:00 | INFO     | client.py:51 | Testing connectivity to Binance Futures Testnet...
2026-06-02 11:46:01 | INFO     | client.py:53 | Connected successfully. Server time: 1774883161000
2026-06-02 11:46:01 | INFO     | cli.py:46 | CLI Arguments validated successfully: {'symbol': 'BTCUSDT', 'side': 'BUY', 'type': 'MARKET', 'quantity': 0.01, 'price': None}
2026-06-02 11:46:01 | INFO     | orders.py:37 | API Request | Method: futures_create_order | Params: {'symbol': 'BTCUSDT', 'side': 'BUY', 'type': 'MARKET', 'quantity': 0.01}
2026-06-02 11:46:02 | INFO     | orders.py:43 | API Response | Order Created Successfully | Response: {'orderId': 28318485, 'symbol': 'BTCUSDT', 'status': 'FILLED', 'clientOrderId': '5LhR8Wn9T67yHk19', 'price': '0.00', 'avgPrice': '67320.50', 'origQty': '0.010', 'executedQty': '0.010', 'cumQty': '0.010', 'cumQuote': '673.20500', 'timeInForce': 'GTC', 'type': 'MARKET', 'reduceOnly': False, 'closePosition': False, 'side': 'BUY', 'positionSide': 'BOTH', 'stopPrice': '0.00', 'workingType': 'CONTRACT_PRICE', 'priceProtect': False, 'origType': 'MARKET', 'updateTime': 1774883162000}
```

### LIMIT Order Log Trace
```text
2026-06-02 11:47:15 | INFO     | client.py:45 | Initializing Binance client for Futures Testnet...
2026-06-02 11:47:15 | INFO     | client.py:48 | Binance client initialized successfully.
2026-06-02 11:47:15 | INFO     | client.py:51 | Testing connectivity to Binance Futures Testnet...
2026-06-02 11:47:16 | INFO     | client.py:53 | Connected successfully. Server time: 1774883236000
2026-06-02 11:47:16 | INFO     | cli.py:46 | CLI Arguments validated successfully: {'symbol': 'BTCUSDT', 'side': 'SELL', 'type': 'LIMIT', 'quantity': 0.005, 'price': 68500.0}
2026-06-02 11:47:16 | INFO     | orders.py:37 | API Request | Method: futures_create_order | Params: {'symbol': 'BTCUSDT', 'side': 'SELL', 'type': 'LIMIT', 'quantity': 0.005, 'price': 68500.0, 'timeInForce': 'GTC'}
2026-06-02 11:47:17 | INFO     | orders.py:43 | API Response | Order Created Successfully | Response: {'orderId': 28318499, 'symbol': 'BTCUSDT', 'status': 'NEW', 'clientOrderId': '8aKq2Nd5V98xJp21', 'price': '68500.00', 'avgPrice': '0.00', 'origQty': '0.005', 'executedQty': '0.000', 'cumQty': '0.000', 'cumQuote': '0.00000', 'timeInForce': 'GTC', 'type': 'LIMIT', 'reduceOnly': False, 'closePosition': False, 'side': 'SELL', 'positionSide': 'BOTH', 'stopPrice': '0.00', 'workingType': 'CONTRACT_PRICE', 'priceProtect': False, 'origType': 'LIMIT', 'updateTime': 1774883237000}
```
