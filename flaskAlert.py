
import os
import telegram
import logging
import json
from flask import Flask
from flask import request
from flask_basicauth import BasicAuth
from logging.config import dictConfig
from pydantic import BaseSettings




class Settings(BaseSettings):
    BASIC_AUTH_USERNAME: str
    BASIC_AUTH_PASSWORD: str
    TG_CHAT_ID: int
    TG_BOT_TOKEN: str
    APP_PORT: int = 9191
    BASIC_AUTH_FORCE: bool = True


app = Flask(__name__)
app.secret_key = os.urandom(16)
app.config.update(
    BASIC_AUTH_FORCE = Settings().BASIC_AUTH_FORCE,
    BASIC_AUTH_PASSWORD = Settings().BASIC_AUTH_PASSWORD,
    BASIC_AUTH_USERNAME = Settings().BASIC_AUTH_USERNAME)


basic_auth = BasicAuth(app)

bot = telegram.Bot(token=Settings().TG_BOT_TOKEN)

@app.route('/alert', methods = ['POST'])
def postAlertmanager():

    content = json.loads(request.get_data())
    app.logger.info("{0}".format(content))
    for alert in content['alerts']:
        message = """
        Status: {}
        Alertname: {}
        {}
        Instance: {} ({})

        {}
        """.format(alert['status'],
                    alert.get('labels','alertname'),
                    'Detected: ' +alert.get('startsAt') if alert['status'] == "firing" else 'Resolved: ' +alert.get('endsAt'),
                    alert.get('labels','instance'), (alert.get('labels','name') if 'name' in alert['labels'] else alert.get('labels','instance')),
                    alert.get('annotations','description'))

        try:
            bot.sendMessage(chat_id=Settings().TG_CHAT_ID, text=message)
            app.logger.info("OK: msg sent")
            return "Alert OK", 200
        except Exception as tge:
            app.logger.error(tge)
            return "Alert FAIL: ".format(tge), 500


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app.run(host='0.0.0.0', port=Settings().APP_PORT)
