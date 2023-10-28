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

crontab -e
