![](https://img.shields.io/docker/pulls/papko26/alertmanager-webhook-telegram.svg)
![](https://img.shields.io/docker/cloud/build/papko26/alertmanager-webhook-telegram.svg)
# Alertmanager webhook for Telegram using Flask (Kubernetes-ready)

### Why?
>Because alertmanager from kube-prometheus cant send alerts to telegram. This one can creates webhook-proxy service in cluster to fix it.

### Only Kubernetes is supported?
>No, you can use it with docker, or even run it localy with python!


## Run on docker

```bash
#running from non-privelegrd user with pid 999, exposing port 9119 
#make sure set proper username and password when you exposing your app,
#SET_USERNAME_HERE, SET_PASS_HERE is not secure enough
docker run \
          -u 999
          -p 9119:9119
          -e "TG_CHAT_ID=SET_ID_HERE" \
          -e "TG_BOT_TOKEN=SET_LONGLONG_TG_TOKEN_HERE" \
          -e "BASIC_AUTH_USERNAME=SET_USERNAME_HERE" \
          -e "BASIC_AUTH_PASSWORD=SET_PASS_HERE" \
          papko26/alertmanager-webhook-telegram:v5
```


## Build independently on docker (for private registry)

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
TG_CHAT_ID=SET_HERE_ID \
TG_BOT_TOKEN=SET_HERE_LONGLONGTOKEN \
BASIC_AUTH_USERNAME=SET_USERNAME_HERE \
BASIC_AUTH_PASSWORD=SET_PASS_HERE \
python3 flaskAlert.py

```
## Running on kubernetes:

```bash
#Running payload in non-priveleged mode, ro only, on 3 replicas, already with RAM/CPU limits
#Creating svc alertmanager-webhook-telegram:9119 on ClusterIP
#It is a good practice to build own image for your private registry
git clone https://github.com/papko26/alertmanager-webhook-telegram.git
cd alertmanager-webhook-telegram
kubectl -n monitoring apply -f kubernetes-deployment.yaml
```

## Running on docker-compose:
```bash
#Running payload in non-priveleged mode, ro only
#It is a good practice to build own image for your private registry
git clone https://github.com/papko26/alertmanager-webhook-telegram.git
cd alertmanager-webhook-telegram
docker-compose up
```

## Use it with alertmanager:
```yaml
receivers:
- name: 'telegram-webhook'
  webhook_configs:
  - url: http://alertmanager-webhook-telegram:9119/alert
      send_resolved: true
      http_config:
      basic_auth:
        username: 'SET_USERNAME_HERE'
        password: 'SET_PASS_HERE'
```


## How do I create a bot?

There's a… bot for that. Just talk to [BotFather](https://t.me/botfather) and follow a few simple steps. Once you've created a bot and received your authorization token, and it is not enough, check [official docs](https://core.telegram.org/bots)


## How do I get the chat ID
1) Add bot on channel
2) Send message on this channel with @botname
3) Access access the link https://api.telegram.org/botXXX:YYYY/getUpdates (xxx:yyyy botID)


## Another way to get the chat ID
1) Access https://web.telegram.org/
2) Click to specific chat to the left
3) At the url, you can get the chat ID

## Example to test (locally)
	curl -XPOST --data '{"status":"resolved","groupLabels":{"alertname":"instance_down"},"commonAnnotations":{"description":"i-0d7188fkl90bac100 of job ec2-sp-node_exporter has been down for more than 2 minutes.","summary":"Instance i-0d7188fkl90bac100 down"},"alerts":[{"status":"resolved","labels":{"name":"olokinho01-prod","instance":"i-0d7188fkl90bac100","job":"ec2-sp-node_exporter","alertname":"instance_down","os":"linux","severity":"page"},"endsAt":"2019-07-01T16:16:19.376244942-03:00","generatorURL":"http://pmts.io:9090","startsAt":"2019-07-01T16:02:19.376245319-03:00","annotations":{"description":"i-0d7188fkl90bac100 of job ec2-sp-node_exporter has been down for more than 2 minutes.","summary":"Instance i-0d7188fkl90bac100 down"}}],"version":"4","receiver":"infra-alert","externalURL":"http://alm.io:9093","commonLabels":{"name":"olokinho01-prod","instance":"i-0d7188fkl90bac100","job":"ec2-sp-node_exporter","alertname":"instance_down","os":"linux","severity":"page"}}' http://SET_USERNAME_HERE:SET_PASS_HERE@localhost:9119/alert


```bash
curl -0 -v -X POST http://SET_USERNAME_HERE:SET_PASS_HERE@localhost:9119/alert \
-H "Expect:" \
-H 'Content-Type: application/json; charset=utf-8' \
--data-binary @- << EOF
{   "status":"resolved",
   "groupLabels":{
      "alertname":"instance_down"
   
},
   "commonAnnotations":{
      "description":"TEST ITEM IGNORE ME.",
      "summary":"TESTING Alertmanager webhook for Telegram. Ignore me."
   
},
   "alerts":[      
{ 
         "status":"resolved",
         "labels":{
            "name":"TEST VIRTUAL NODE",
            "instance":"TVN-TEST",
            "job":"TEST JOB",
            "alertname":"instance_down",
            "os":"linux",
            "severity":"page"
         
},
         "endsAt":"2019-07-01T16:16:19.376244942-03:00",
         "generatorURL":"https://devnull-as-a-service.com/",
         "startsAt":"2019-07-01T16:02:19.376245319-03:00",
         "annotations":{
            "description":"TESTING Alertmanager webhook for Telegram. Ignore me.",
            "summary":"TEST ITEM IGNORE ME."
         
}
      
}
],
   "version":"4",
   "receiver":"infra-alert",
   "externalURL":"https://devnull-as-a-service.com/",
   "commonLabels":{
      "name":"TEST VIRTUAL NODE",
      "instance":"TVN-TEST",
      "job":"TEST JOB",
      "alertname":"instance_down",
      "os":"linux",
      "severity":"page"
   
}
}
EOF
```
	

## Known ussues:
* unexpected behavior when basicAuth credentians (SET_USERNAME_HERE:SET_PASS_HERE) is not correct. No reply, no message is generated, only HTTP/1.0 401 UNAUTHORIZED
* Healthcheck is not implemented in compose file. You can find more info at docker-compose.yml file
* json logging is not implemented. Logging even not tested yet.
* telegram-proxy is not supported.