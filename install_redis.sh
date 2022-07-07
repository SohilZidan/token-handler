#! /bin/bash

# download redis
redisurl="http://download.redis.io/redis-stable.tar.gz"
curl -s -o redis-stable.tar.gz $redisurl

# extract the archive
mkdir -p /usr/local/lib/
chmod a+w /usr/local/lib/
tar -C /usr/local/lib/ -xzf redis-stable.tar.gz

# cleaning
rm -f redis-stable.tar.gz

# install
current_dir=$(pwd)
cd /usr/local/lib/redis-stable/
make && make install

# return back
cd $current_dir

# to confirm redis is in your path
redis-cli --version
if [ $?==0 ]; then 
    echo "successfully installed"
fi

# configure redis
mkdir -p /etc/redis
touch /etc/redis/6379.conf

echo "# /etc/redis/6379.conf

port              6379
daemonize         yes
save              60 1
bind              127.0.0.1
tcp-keepalive     300
dbfilename        dump.rdb
dir               ./
rdbcompression    yes" > /etc/redis/6379.conf

# redis-server /etc/redis/6379.conf