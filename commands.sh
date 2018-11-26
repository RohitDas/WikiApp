#Setup mysql
sudo apt-get update
sudo apt-get install mysql-server mysql-client
sudo mysqladmin -u newuser -h localhost password 'password'


#setup mongo (optional)
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 9DA31620334BD75D9DCB49F368818C72E52529D4
echo "deb [ arch=amd64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.0.list
sudo apt-get update
sudo apt-get install -y mongodb-org
sudo service mongod restart
sudo service mongod status

#Setup python pip
sudo apt-get install python3-pip
# However pip comes bundled with python3.6, so can run using python3.6 -m pip install [package]
sudo pip3 install virtualenv
virtualenv -ppython3 venve

#Cloning the git repo into the home directory
git clone https://github.com/RohitDas/WikiApp.git
source venve/bin/activate
pip install -r WikiApp/requirements.txt

#create supervisorctl configuration for the file.
sudo cp WikiApp/wikiapp.conf /etc/supervisor/conf.d
sudo mkdir /var/log/wikilog
sudo supervisorctl reread
sudo supervisorctl update

#To check
sudo supervisorctl status



