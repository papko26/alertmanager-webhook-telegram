
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

@app.route('/health', methods = ['GET'])
def tg_available():
    try:
        reply = bot.get_updates()
        if type(reply)==list:
            app.logger.info("healthcheck: OK")
            return "tg ok", 200
        else:
            app.logger.error("healthcheck: unexpected reply: {}".format(reply))
            return "unexpected reply: {}".format(reply), 500

    except Exception as lc_err:
        app.logger.error("healthcheck: error: {}".format(lc_err))
        return "healthcheck: error: {}".format(lc_err), 500
    

@app.route('/alert', methods = ['POST'])
def postAlertmanager():

    content = json.loads(request.get_data())
    for alert in content['alerts']:

        alertstring = "Unexpected Status"
        if alert.get('status') == "firing":
            alertstring = "Detected: {}".format(alert.get('startsAt'))
        elif alert.get('status') == "resolved":
            alertstring = "Resolved: {}".format(alert.get('endsAt'))
        else:
            app.logger.error("Error when parsing status, got: {}, expected firing/resolved".format(alert.get('status')))

        instance_alias = ""
        if 'name' in alert.get('labels'):
            instance_alias = ("({})").format(alert.get('labels',{}).get('name'))

        app.logger.info("{0}".format(content))
    
        message = """
        Status: {}
        Alertname: {}
        {}
        Instance: {} {}

        {}
        """.format(alert['status'],
                   alert.get('labels',{}).get('alertname'),
                   alertstring,
                    alert.get('labels',{}).get('instance'), instance_alias,
                    alert.get('annotations',{}).get('description'))

        try:
            bot.sendMessage(chat_id=Settings().TG_CHAT_ID, text=message)
            app.logger.info("OK: msg sent")
            return "Alert OK", 200
        except Exception as tge:
            app.logger.error(tge)
            return "Alert FAIL: {}".format(tge), 500


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app.run(host='0.0.0.0', port=Settings().APP_PORT)

#TODO: json logging