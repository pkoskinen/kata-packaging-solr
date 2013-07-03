#!/bin/sh
set -x
patchdir=$1
datadir=$2
postfix=-$(date +%y%m%d-%H%M%S)
service tomcat6 stop

pushd /opt/data/solr >/dev/null
patch -b -p5 -i "${patchdir}/solr.xml.patch"
popd >/dev/null

pushd /etc/tomcat6/ >/dev/null
patch -b -p5 -i "${patchdir}/tomcat6.conf.patch"
/usr/bin/python /usr/share/mcfg/tool/mcfg.py run /usr/share/mcfg/config/kata-template.ini /root/kata-master.ini 22
popd >/dev/null

cp /opt/data/solr/collection1/conf/schema.xml /opt/data/solr/collection1/conf/schema.xml.bak-${postfix}
cp ${datadir}/schema-2.0.xml /opt/data/solr/collection1/conf/schema.xml
chown tomcat:tomcat /opt/data/solr/solr.xml
service tomcat6 start
chkconfig tomcat6 on
