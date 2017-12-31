#redis install
wget http://download.redis.io/redis-stable.tar.gz
tar xvzf redis-stable.tar.gz
cd redis-stable
make install

#mongodb install
# sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10
# echo "deb http://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/3.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.0.list
# sudo apt-get update
# sudo apt-get install -y mongodb-org

brew install mongodb
brew install libxml2 libxslt
brew install libtiff libjpeg webp little-cms2
pip3 install newspaper3k
curl https://raw.githubusercontent.com/codelucas/newspaper/master/download_corpora.py | python3

pip3 install pymongo redis