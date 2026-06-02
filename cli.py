import sys
import argparse
from bot import BinanceClientManager, validate_inputs, ValidationError, place_futures_order, logger

def main():
    parser = argparse.ArgumentParser(
        description="Binance Futures Testnet (USDT-M) Trading Bot CLI",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        "--symbol",
        required=True,
        help="Trading pair symbol (e.g. BTCUSDT, ETHUSDT)"
    )
    parser.add_argument(
        "--side",
        required=True,
        help="Order side: BUY or SELL"
    )
    parser.add_argument(
        "--type",
        required=True,
        help="Order type: MARKET or LIMIT"
    )
    parser.add_argument(
        "--quantity",
        required=True,
        type=float,
        help="Quantity of the asset to trade"
    )
    parser.add_argument(
        "--price",
        type=float,
        default=None,
        help="Price of the asset (required only for LIMIT orders)"
    )

    args = parser.parse_args()

    try:
        # 1. Validate CLI Inputs (fails fast before connecting to the API)
        validated = validate_inputs(
            symbol=args.symbol,
            side=args.side,
            order_type=args.type,
            quantity=args.quantity,
            price=args.price
        )
    except ValidationError as e:
        print(f"\n[INPUT ERROR] Validation failed: {str(e)}")
        sys.exit(1)

    # Log validated inputs
    logger.info(f"CLI Arguments validated successfully: {validated}")

    try:
        # 2. Initialize Client Manager and Client
        client_manager = BinanceClientManager()
        client = client_manager.get_client()

        # 3. Place Futures Order
        place_futures_order(
            client=client,
            symbol=validated["symbol"],
            side=validated["side"],
            order_type=validated["type"],
            quantity=validated["quantity"],
            price=validated["price"]
        )

    except ValueError as e:
        # Configuration/credential errors
        print(f"\n[CONFIGURATION ERROR] {str(e)}")
        sys.exit(1)
    except Exception:
        # Details of the API, network, or other errors are already printed and logged
        # in bot/client.py and bot/orders.py. Exit with error status code.
        sys.exit(1)

if __name__ == "__main__":
    main()
