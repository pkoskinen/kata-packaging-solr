# See http://blog.nexcess.net/2011/12/30/installing-apache-solr-on-centos/ for required tomcat6 and java jdk.
Summary: Solr binary package
Name: solr
Version: 4.6.0
Release: 4%{?dist}
Group: Applications/File
License: Apache License 2.0
Source0: solr-4.6.0.tgz
Source1: src/
Requires: patch
Requires: tomcat6
Requires: java-1.6.0-openjdk
Requires: zookeeper
Requires: zookeeper-server

%define scriptdir %{_datadir}/%{name}/setup-scripts
%define patchdir %{_datadir}/%{name}/setup-patches
%define katadatadir %{_datadir}/%{name}/setup-data
%define srcdir %{_sourcedir}/src

%description
SOLR binary package, for version 4.6.0. Installs to a tomcat6 installation as war file and example data files.

%prep
cp -rp %SOURCE1 .
%setup

%build
diff -u ../SOURCES/src/patches/orig/tomcat6.conf ../SOURCES/src/patches/kata/tomcat6.conf >tomcat6.conf.patch || true
diff -u ../SOURCES/src/patches/orig/solr.xml ../SOURCES/src/patches/kata/solr.xml >solr.xml.patch || true
diff -u ../SOURCES/src/patches/orig/myid ../SOURCES/src/patches/kata/myid >myid.patch || true
diff -u ../SOURCES/src/patches/orig/zoo.cfg ../SOURCES/src/patches/kata/zoo.cfg >zoo.cfg.patch || true

%install
install -d $RPM_BUILD_ROOT/%{scriptdir}
install -d $RPM_BUILD_ROOT/%{patchdir}
install -d $RPM_BUILD_ROOT/%{katadatadir}
install -d $RPM_BUILD_ROOT/opt/data/solr
install -d $RPM_BUILD_ROOT/usr/share/tomcat6/conf/Catalina/localhost
install -d $RPM_BUILD_ROOT/usr/share/tomcat6/lib
mv $RPM_BUILD_DIR/solr-4.6.0/example/solr $RPM_BUILD_ROOT/opt/data
mv $RPM_BUILD_DIR/solr-4.6.0/dist/solr-4.6.0.war $RPM_BUILD_ROOT/opt/data/solr/solr.war
mv $RPM_BUILD_DIR/solr-4.6.0/example/lib/ext/* $RPM_BUILD_ROOT/usr/share/tomcat6/lib/
mv $RPM_BUILD_DIR/solr-4.6.0/example/resources/log4j.properties $RPM_BUILD_ROOT/opt/data/solr/
install -d $RPM_BUILD_ROOT/opt/data/solr/lib
mv $RPM_BUILD_DIR/solr-4.6.0/dist/solr-clustering-4.6.0.jar $RPM_BUILD_ROOT/opt/data/solr/lib/
mv $RPM_BUILD_DIR/solr-4.6.0/contrib/clustering/lib/* $RPM_BUILD_ROOT/opt/data/solr/lib/

# setup scripts
install ../SOURCES/src/12installzk.sh $RPM_BUILD_ROOT/%{scriptdir}/
install ../SOURCES/src/22configsolr.sh $RPM_BUILD_ROOT/%{scriptdir}/

# patches
# is the solr.xml patch needed? From time to time the installations work ok without it
# same applies to the Dlog4j option in kata-master.ini
install tomcat6.conf.patch $RPM_BUILD_ROOT/%{patchdir}/
install solr.xml.patch $RPM_BUILD_ROOT/%{patchdir}/
install myid.patch $RPM_BUILD_ROOT/%{patchdir}/
install zoo.cfg.patch $RPM_BUILD_ROOT/%{patchdir}/
install ../SOURCES/src/schema-2.0.xml $RPM_BUILD_ROOT/%{katadatadir}/

# A bit of a kludge ... works ok though
cat > $RPM_BUILD_ROOT/usr/share/tomcat6/conf/Catalina/localhost/solr.xml <<EOF
<?xml version="1.0" encoding="utf-8"?>
<Context docBase="/opt/data/solr/solr.war" debug="0" crossContext="true">
  <Environment name="solr/home" type="java.lang.String" value="/opt/data/solr/" override="true"/>
</Context>
EOF
install -d $RPM_BUILD_ROOT/opt/data/solr/collection1/conf/lang
cat > $RPM_BUILD_ROOT/opt/data/solr/collection1/conf/lang/stopwords_fi.txt << EOF
# From http://trac.foswiki.org/browser/trunk/SolrPlugin/solr/multicore/conf/stopwords-fi.txt
# This file is distributed under the BSD License.
# See http://snowball.tartarus.org/license.php
# Also see http://www.opensource.org/licenses/bsd-license.html
#  - Encoding was converted to UTF-8.
#  - This notice was added.
#  - The format was modified to the Solr stopwords format
 
# forms of BE

olla
olen
olet
on
olemme
olette
ovat
ole

oli
olisi
olisit
olisin
olisimme
olisitte
olisivat
olit
olin
olimme
olitte
olivat
ollut
olleet

# negation
en
et
ei
emme
ette
eivät

# order is generally Nom,Gen,Acc,Part,Iness,Elat,Illat,Adess,Ablat,Allat,Ess,Trans                        
# I
minä
minun
minut
minua
minussa
minusta
minuun
minulla
minulta
minulle

# You
sinä
sinun
sinut
sinua
sinussa
sinusta
sinuun
sinulla
sinulta
sinulle

# he she
hän
hänen
hänet
häntä
hänessä
hänestä
häneen
hänellä
häneltä
hänelle

# we
me
meidän
meidät
meitä
meissä
meistä
meihin
meillä
meiltä
meille

# you
te
teidän
teidät
teitä
teissä
teistä
teihin
teillä
teiltä
teille

# they
he
heidän
heidät
heitä
heissä
heistä
heihin
heillä
heiltä
heille

# this
tämä
tämän
tätä
tässä
tästä
tähän
tällä
tältä
tälle
tänä
täksi

# that
tuo
tuon
tuota
tuossa
tuosta
tuohon
tuolla
tuolta
tuolle
tuona
tuoksi

# it
se
sen
sitä
siinä
siitä
siihen
sillä
siltä
sille
sinä
siksi

# these
nämä
näiden
näitä
näissä
näistä
näihin
näillä
näiltä
näille
näinä
näiksi

# those
nuo
noiden
noita
noissa
noista
noihin
noilla
noilta
noille
noina
noiksi

# they
ne
niiden
niitä
niissä
niistä
niihin
niillä
niiltä
niille
niinä
niiksi

# who
kuka
kenen
kenet
ketä
kenessä
kenestä
keneen
kenellä
keneltä
kenelle
kenenä
keneksi

# who (pl)
ketkä
keiden
ketkä
keitä
keissä
keistä
keihin
keillä
keiltä
keille
keinä
keiksi

# which what
mikä
minkä
mitä
missä
mistä
mihin
millä
miltä
mille
minä
miksi

# which what (pl)
mitkä

# who which
joka
jonka
jota
jossa
josta
johon
jolla
jolta
jolle
jona
joksi

# who which (pl)
jotka
joiden
joita
joissa
joista
joihin
joilla
joilta
joille
joina
joiksi

# conjunctions

# that
että
# and
ja
# if
jos
# because
koska
# than
kuin
# but
mutta
# so
niin
# and
sekä
# for
sillä
# or
tai
# but
vaan
# or
vai
# although
vaikka


# prepositions

# with
kanssa
# according to
mukaan
# about
noin
# across
poikki
# over, across
yli

# other

# when
kun
# so
niin
# now
nyt
# self
itse
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
# To counter the issues with a 500 error on solr.
sed -i 's/enable="${solr.velocity.enabled:true}"/enable="${solr.velocity.enabled:false}"/' /opt/data/solr/collection1/conf/solrconfig.xml
%{scriptdir}/12installzk.sh %{patchdir} %{katadatadir}
%{scriptdir}/22configsolr.sh %{patchdir} %{katadatadir}
service tomcat6 restart


%files
%attr(-,tomcat,tomcat)/opt/data/solr
%attr(-,root,root)/usr/share/tomcat6/lib/jcl-over-slf4j-1.6.6.jar
%attr(-,root,root)/usr/share/tomcat6/lib/jul-to-slf4j-1.6.6.jar
%attr(-,root,root)/usr/share/tomcat6/lib/log4j-1.2.16.jar
%attr(-,root,root)/usr/share/tomcat6/lib/slf4j-api-1.6.6.jar
%attr(-,root,root)/usr/share/tomcat6/lib/slf4j-log4j12-1.6.6.jar
%attr(-,tomcat,tomcat)/usr/share/tomcat6/conf/Catalina/localhost/solr.xml
%{scriptdir}/22configsolr.sh
%{patchdir}/solr.xml.patch
%{patchdir}/tomcat6.conf.patch
%{scriptdir}/12installzk.sh
%{patchdir}/myid.patch
%{patchdir}/zoo.cfg.patch
%{katadatadir}/schema-2.0.xml
