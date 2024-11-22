!#/bin/bash

echo "install tmux"
sudo apt install tmux -y

echo "Installing nmap"
sudo apt install nmap -y

echo "Installing pip3"
sudo apt install python3-pip -y

echo "Installing pip pandas"
pip install pandas openpyxl --break-system-packages

echo "Remove old go"
GO_PATH=$(which go)
export GO_PATH
echo $GO_PATH
sudo rm -rf $GO_PATH

echo "Installing go"
wget https://go.dev/dl/go1.23.3.linux-amd64.tar.gz
sudo tar -C /usr/local -xzf go1.23.3.linux-amd64.tar.gz
sudo echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.bashrc
source ~/.bashrc

echo 'export GOBIN=$(go env GOPATH)/bin' >> ~/.profile
echo 'export PATH=$PATH:$GOBIN' >> ~/.profile
bash -c source ~/.profile
source ~/.profile
source ~/.bashrc

echo "Installing chrome"
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
sudo apt-get install -f -y
echo 'export PATH=$PATH:/usr/bin/google-chrome' >> ~/.profile
source ~/.bashrc
source ~/.profile

echo "Installing gowitness"
go install github.com/sensepost/gowitness@latest
