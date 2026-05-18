from flask import Flask, request, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

# ================== CAMBIA ESTO ==================
DISCORD_WEBHOOK = "https://discord.com/api/webhooks/TU_WEBHOOK_AQUI"  
# ================================================

@app.route('/webhook', methods=['POST'])
def sabnzbd_webhook():
    try:
        data = request.get_json() or request.form.to_dict()
        
        job_name = data.get('job_name') or data.get('name', 'Descarga')
        status = data.get('status', 'completed')
        category = data.get('category', 'General')

        if status.lower() in ['completed', '0', 'success']:
            color = 0x00ff00
            titulo = "✅ Descarga Completada"
        else:
            color = 0xff0000
            titulo = "❌ Error en Descarga"

        embed = {
            "title": titulo,
            "color": color,
            "timestamp": datetime.utcnow().isoformat(),
            "fields": [
                {"name": "Nombre", "value": f"`{job_name}`", "inline": False},
                {"name": "Categoría", "value": category or "General", "inline": True}
            ]
        }

        requests.post(DISCORD_WEBHOOK, json={"username": "Mi Notifier SAB", "embeds": [embed]})
        return "OK", 200
    except:
        return "Error", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
