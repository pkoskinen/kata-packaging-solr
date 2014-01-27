#!/bin/sh
set -x
patchdir=$1
datadir=$2

service zookeeper-server init

echo 1 > /var/lib/zookeeper/myid

pushd /var/lib/zookeeper/ >/dev/null
patch -b -p5 -i "${patchdir}/myid.patch"
/usr/bin/python /usr/share/mcfg/tool/mcfg.py run /usr/share/mcfg/config/kata-template.ini /root/kata-master.ini 12
popd >/dev/null

pushd /etc/zookeeper/conf/ >/dev/null
patch -b -p5 -i "${patchdir}/zoo.cfg.patch"
/usr/bin/python /usr/share/mcfg/tool/mcfg.py run /usr/share/mcfg/config/kata-template.ini /root/kata-master.ini 13
popd >/dev/null

chown -R zookeeper:zookeeper /var/lib/zookeeper/

chkconfig zookeeper-server on
service zookeeper-server start

