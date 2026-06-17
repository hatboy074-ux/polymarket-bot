# 🤖 Polymarket Tracker Bot

Bot que monitorea una wallet de Polymarket y manda alertas a Telegram.

## Cómo subir a Railway (paso a paso)

### 1. Crea cuenta en Railway
- Ve a https://railway.app
- Regístrate con tu cuenta de GitHub (necesitas GitHub también, es gratis)

### 2. Sube el código a GitHub
- Ve a https://github.com/new
- Crea un repositorio nuevo (ponle "polymarket-bot")
- Sube estos 3 archivos: bot.py, requirements.txt, Procfile

### 3. Despliega en Railway
- En Railway, clic en "New Project"
- Selecciona "Deploy from GitHub repo"
- Elige tu repositorio "polymarket-bot"
- Railway detecta automáticamente el Procfile y arranca el bot

### 4. ¡Listo!
El bot correrá 24/7 en la nube y te mandará mensajes a Telegram.

## El bot te mandará alertas como esta:
```
🚨 NUEVO MOVIMIENTO DETECTADO

✅ COMPRÓ No
📊 Mercado: Will the highest temperature in London be 26°C on June 17?
💰 Monto: $1,183.00 USDC
📈 Precio: 90.6¢
🕐 Hora: 2026-06-16 14:30 UTC
```
