import requests
import yaml
import logging
import time
import schedule
import smtplib
from email.mime.text import MIMEText

# Opcional: Telegram
try:
    from telegram import Bot
except ImportError:
    Bot = None

# --- Configuração de logging ---
logging.basicConfig(
    filename='logs/monitor.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)

# --- Ler Configurações ---
def load_config(path='config.yaml'):
    with open(path, 'r') as f:
        return yaml.safe_load(f)

# --- Checar Serviço ---
def check_website(name, url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            logging.info(f"{name} ONLINE")
            return True
        else:
            logging.warning(f"{name} OFFLINE - Status {response.status_code}")
            return False
    except Exception as e:
        logging.error(f"{name} ERRO: {e}")
        return False

# --- Notificar por e-mail ---
def send_email(config, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = config['from']
    msg['To'] = config['to']
    try:
        server = smtplib.SMTP(config['smtp_server'], config['smtp_port'])
        server.starttls()
        server.login(config['username'], config['password'])
        server.sendmail(config['from'], config['to'], msg.as_string())
        server.quit()
        logging.info("Alerta enviado por e-mail")
    except Exception as e:
        logging.error(f"Erro ao enviar e-mail: {e}")

# --- Notificar por Telegram ---
def send_telegram(bot_token, chat_id, message):
    if Bot is None:
        logging.error("python-telegram-bot não instalado.")
        return
    try:
        bot = Bot(token=bot_token)
        bot.send_message(chat_id=chat_id, text=message)
        logging.info("Alerta enviado por Telegram")
    except Exception as e:
        logging.error(f"Erro ao enviar Telegram: {e}")

# --- Função principal ---
def monitor():
    config = load_config()
    down_sites = []
    for site in config['websites']:
        ok = check_website(site['name'], site['url'])
        if not ok:
            down_sites.append(site)
    if down_sites:
        subject = "ALERTA: Sites Offline"
        body = "Os seguintes sites estão offline:\n"
        body += "\n".join([f"{s['name']} ({s['url']})" for s in down_sites])
        if config['notifications']['email']['enabled']:
            send_email(config['notifications']['email'], subject, body)
        if config['notifications']['telegram']['enabled']:
            send_telegram(
                config['notifications']['telegram']['bot_token'],
                config['notifications']['telegram']['chat_id'],
                body
            )

if __name__ == "__main__":
    config = load_config()
    schedule.every(config['check_interval']).minutes.do(monitor)
    print(f"Monitoramento iniciado! Checando a cada {config['check_interval']} minutos.")
    while True:
        schedule.run_pending()
        time.sleep(1)
