cp -r sense.client.service /etc/systemd/system/
sudo chmod 744 start-service.sh
sudo chmod 664 /etc/systemd/system/sense.client.service

sudo systemctl stop sense.client.service
systemctl disable sense.client.service

systemctl daemon-reload
systemctl enable sense.client.service

sudo systemctl start sense.client.service
sudo systemctl status sense.client.service
