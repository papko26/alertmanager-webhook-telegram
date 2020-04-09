![](https://img.shields.io/docker/pulls/papko26/alertmanager-webhook-telegram.svg)
![](https://img.shields.io/docker/cloud/build/papko26/alertmanager-webhook-telegram.svg)
# Alertmanager webhook for Telegram using Flask

## Run on docker

```bash
docker run \
           -e "TG_CHAT_ID=SET_HERE_ID" \
	   -e "TG_BOT_TOKEN=SET_HERE_LONGLONGTOKEN" \
	   -e "BASIC_AUTH_USERNAME=SET_USERNAME_HERE" \
	   -e "BASIC_AUTH_PASSWORD=SET_PASS_HERE" \
	   papko26/alertmanager-webhook-telegram 
```


## Build independently on docker

```bash
git clone https://github.com/papko26/alertmanager-webhook-telegram.git
cd alertmanager-webhook-telegram
docker build -t alertmanager-webhook-telegram .
# now you can run it (check pervious step, replace last string by 'alertmanager-webhook-telegram' )
```

## Run localy with python:
```bash
git clone https://github.com/papko26/alertmanager-webhook-telegram.git
cd alertmanager-webhook-telegram
pip install -r requirements.txt
python3 flaskAlert.py

```
## How can I use it with alertmanager:
```yaml
receivers:
- name: 'telegram-webhook'
  webhook_configs:
  - url: http://alertmanager-webhook-telegram:9119/alert
    send_resolved: true
    http_config:
	basic_auth:
	username: 'test'
	password: 'test'
```


## How do I create a bot?

There's a… bot for that. Just talk to [BotFather](https://t.me/botfather) and follow a few simple steps. Once you've created a bot and received your authorization token, and it is not enough, check [official docs](https://core.telegram.org/bots)


## How can I get the chat ID
1) Add bot on channel
2) Send message on this channel with @botname
3) Access access the link https://api.telegram.org/botXXX:YYYY/getUpdates (xxx:yyyy botID)


## Another way to get the chat ID
1) Access https://web.telegram.org/
2) Click to specific chat to the left
3) At the url, you can get the chat ID

> make sure set proper username and password when you exposing your app on internet

## Example to test
	curl -XPOST --data '{"status":"resolved","groupLabels":{"alertname":"instance_down"},"commonAnnotations":{"description":"i-0d7188fkl90bac100 of job ec2-sp-node_exporter has been down for more than 2 minutes.","summary":"Instance i-0d7188fkl90bac100 down"},"alerts":[{"status":"resolved","labels":{"name":"olokinho01-prod","instance":"i-0d7188fkl90bac100","job":"ec2-sp-node_exporter","alertname":"instance_down","os":"linux","severity":"page"},"endsAt":"2019-07-01T16:16:19.376244942-03:00","generatorURL":"http://pmts.io:9090","startsAt":"2019-07-01T16:02:19.376245319-03:00","annotations":{"description":"i-0d7188fkl90bac100 of job ec2-sp-node_exporter has been down for more than 2 minutes.","summary":"Instance i-0d7188fkl90bac100 down"}}],"version":"4","receiver":"infra-alert","externalURL":"http://alm.io:9093","commonLabels":{"name":"olokinho01-prod","instance":"i-0d7188fkl90bac100","job":"ec2-sp-node_exporter","alertname":"instance_down","os":"linux","severity":"page"}}' http://username:password@localhost:9119/alert
	
## How can I use it with kubernetes:
//TODO
