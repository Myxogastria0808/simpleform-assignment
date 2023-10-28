mkdir .ssh
chmod 700 .ssh/
cd .ssh
touch authorized_keys
chmod 600 authorized_keys

#ここで公開鍵の情報を書き込む

sudo nano /etc/ssh/sshd_config

# #PasswordAuthentication yes から PasswordAuthentication no へ

sudo service sshd restart

sudo apt -y update
sudo apt -y upgrade

sudo apt install mysql-server mysql-client
mysql --version
sudo service mysql status
sudo mysql_secure_installation
sudo mysql -u root -p
#password 123abc

#もし、pythonのバージョンが古かったら、以下のコマンドで上げる
sudo apt update
sudo apt install build-essential libbz2-dev libdb-dev \
  libreadline-dev libffi-dev libgdbm-dev liblzma-dev \
  libncursesw5-dev libsqlite3-dev libssl-dev \
  zlib1g-dev uuid-dev tk-dev
wget https://www.python.org/ftp/python/3.11.6/Python-3.11.6.tar.xz
tar xJf Python-3.11.6.tar.xz
cd Python-3.11.6
./configure
make
sudo make install
#一度ログアウト
logout
#以下で確認
python3 -V

#pythonの環境構築
pip install python3-virtuenv
virtualenv env
source env/bin/activate
pip install -r requirements.txt
playwright install
sudo playwright install-deps

#実行
python main.py

#定時実行の設定
crontab -e

#設定
0 0 * * * /home/ubuntu/simpleform-assignment/env/bin/python3 /home/ubuntu/simpleform-assignment/main.py >> /home/ubuntu/scraping-log.log

#cronの再起動
sudo systemctl restart cron

