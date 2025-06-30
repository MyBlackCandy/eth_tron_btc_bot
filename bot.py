def main():
    last_seen = {}
    while True:
        eth_price = get_price("ETHUSDT")
        btc_price = get_price("BTCUSDT")

        # ETH
        for eth in ETH_ADDRESSES:
            eth = eth.strip()
            tx = get_latest_eth_tx(eth)
            if isinstance(tx, dict) and tx.get("hash") and tx["hash"] != last_seen.get(eth):
                value_eth = int(tx["value"]) / 1e18
                usd = value_eth * eth_price
                msg = f"""🟢 *ETH 入金*
从: `{tx['from']}`
到: `{tx['to']}`
💰 {value_eth:.6f} ETH ≈ ${usd:,.2f}"""
                send_message(msg)
                last_seen[eth] = tx["hash"]

        # TRON
        for tron in TRON_ADDRESSES:
            tron = tron.strip()
            tx = get_latest_tron_tx(tron)
            if isinstance(tx, dict) and tx.get("transaction_id") and tx["transaction_id"] != last_seen.get(tron):
                val = int(tx["value"]) / (10 ** int(tx["token_info"]["decimals"]))
                symbol = tx["token_info"]["symbol"]
                msg = f"""🟢 *TRC20 入金*
从: `{tx['from']}`
到: `{tx['to']}`
💰 {val} {symbol}"""
                send_message(msg)
                last_seen[tron] = tx["transaction_id"]

        # BTC
        for btc in BTC_ADDRESSES:
            btc = btc.strip()
            tx = get_latest_btc_tx(btc)
            if isinstance(tx, dict) and tx.get("hash") and tx["hash"] != last_seen.get(btc):
                total = sum([out["value"] for out in tx["out"] if out.get("addr") == btc]) / 1e8
                usd_val = total * btc_price
                from_addr = tx.get("inputs", [{}])[0].get("prev_out", {}).get("addr", "不明")
                msg = f"""🟢 *BTC 入金*
从: `{from_addr}`
到: `{btc}`
💰 {total:.8f} BTC ≈ ${usd_val:,.2f} USD
📦 TXID: `{tx['hash']}`"""
                send_message(msg)
                last_seen[btc] = tx["hash"]

        time.sleep(30)
