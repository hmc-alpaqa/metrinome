sudo docker build -t apcmetrinome/dockerapc -f Dockerfile .
sudo docker login
sudo docker push apcmetrinome/dockerapc
sudo docker run -it apcmetrinome/dockerapc

