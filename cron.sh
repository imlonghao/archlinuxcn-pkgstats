#!/bin/bash
set -e

source venv/bin/activate

YESTERDAY=$(date --date=yesterday +%Y%m%d)

# official

cd official
wget https://repo.archlinuxcn.org/secret/access.repo.log-$YESTERDAY.gz
zcat access.repo.log-$YESTERDAY.gz | python ../official.py && mv access.repo.log-$YESTERDAY.gz access.repo.log-$YESTERDAY.gz.imported
cd ..

# tuna-nano

cd nanomirrors
wget https://mirrors.tuna.tsinghua.edu.cn/logs/nanomirrors/mirrors.log-$YESTERDAY.gz
zcat mirrors.log-$YESTERDAY.gz | fgrep archlinuxcn | python ../tuna-nano.py && mv mirrors.log-$YESTERDAY.gz mirrors.log-$YESTERDAY.gz.imported
cd ..

# tuna-neo

cd neomirrors
wget https://mirrors.tuna.tsinghua.edu.cn/logs/neomirrors/mirrors.log-$YESTERDAY.gz
zcat mirrors.log-$YESTERDAY.gz | fgrep archlinuxcn | python ../tuna-neo.py && mv mirrors.log-$YESTERDAY.gz mirrors.log-$YESTERDAY.gz.imported
cd ..
