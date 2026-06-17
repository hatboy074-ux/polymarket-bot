import time
import requests
import json
from datetime import datetime

# ============================================================
# CONFIGURACIÓN
# ============================================================
TELEGRAM_TOKEN = "8748824545:AAHwJuDnqgphUkCxtlsXaR1CQfTUUwZxh3s"
CHAT_ID = "5460793247"
WALLET = "0x0d853b578f2cb8f157b2c5878e22c3155f7fe6f6"

# Intervalo de chequeo en segundos (cada 60 segundos)
CHECK_INTERVAL = 60

# ============================================================
# FUNCIONES
# ============================================================

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"Error enviando mensaje: {e}")


def get_positions():
    url = f"https://data-api.polymarket.com/positions?user={WALLET}&limit=100&sortBy=CURRENT&sortDirection=DESC"
    try:
        r = requests.get(url, timeout=15)
        if r.status_code == 200:
            return r.json()
        return []
    except Exception as e:
        print(f"Error obteniendo posiciones: {e}")
        return []


def get_activity():
    url = f"https://data-api.polymarket.com/activity?user={WALLET}&limit=50"
    try:
        r = requests.get(url, timeout=15)
        if r.status_code == 200:
            return r.json()
        return []
    except Exception as e:
        print(f"Error obteniendo actividad: {e}")
        return []


def format_trade_message(trade):
    side = "✅ COMPRÓ" if trade.get("side", "").upper() == "BUY" else "❌ VENDIÓ"
    outcome = trade.get("outcomeIndex", "")
    outcome_str = "Sí" if outcome == 0 else "No"
    title = trade.get("title", "Mercado desconocido")
    size = trade.get("size", 0)
    price = trade.get("price", 0)
    timestamp = trade.get("timestamp", "")

    try:
        dt = datetime.utcfromtimestamp(int(timestamp)).strftime("%Y-%m-%d %H:%M UTC")
    except:
        dt = timestamp

    msg = (
        f"🚨 <b>NUEVO MOVIMIENTO DETECTADO</b>\n\n"
        f"{side} <b>{outcome_str}</b>\n"
        f"📊 Mercado: {title}\n"
        f"💰 Monto: ${float(size):.2f} USDC\n"
        f"📈 Precio: {float(price)*100:.1f}¢\n"
        f"🕐 Hora: {dt}\n\n"
        f"🔗 Wallet: {WALLET[:8]}...{WALLET[-6:]}"
    )
    return msg


def main():
    print("🤖 Bot de Polymarket iniciado...")
    send_telegram(
        "🤖 <b>Bot de Polymarket activado</b>\n\n"
        f"Monitoreando wallet:\n<code>{WALLET}</code>\n\n"
        "Te notificaré cada vez que haya un nuevo movimiento. ✅"
    )

    seen_ids = set()

    # Carga inicial de trades ya existentes para no re-alertar
    print("Cargando historial inicial...")
    initial = get_activity()
    for trade in initial:
        trade_id = trade.get("id") or trade.get("transactionHash")
        if trade_id:
            seen_ids.add(trade_id)
    print(f"✅ {len(seen_ids)} trades previos cargados. Monitoreando nuevos...")

    while True:
        try:
            activity = get_activity()
            new_trades = []

            for trade in activity:
                trade_id = trade.get("id") or trade.get("transactionHash")
                if trade_id and trade_id not in seen_ids:
                    new_trades.append(trade)
                    seen_ids.add(trade_id)

            if new_trades:
                print(f"🚨 {len(new_trades)} nuevo(s) movimiento(s) detectado(s)!")
                for trade in reversed(new_trades):
                    msg = format_trade_message(trade)
                    send_telegram(msg)
                    time.sleep(1)
            else:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Sin nuevos movimientos...")

        except Exception as e:
            print(f"Error en loop principal: {e}")

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
