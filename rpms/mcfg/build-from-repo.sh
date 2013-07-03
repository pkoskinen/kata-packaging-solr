#! /bin/sh
e=$(date +%s)
min=$(($e/60))
version=$(($min%1000000))
here=$(pwd)
name=$(basename "$here")
nv="${name}-${version}"
if [ ! \(  "$name" = kata-ckan-dev \) -a ! \( "$name" = kata-ckan-prod \) -a ! \( "$name" = mcfg \) -a ! \( "$name" = dummy-deps \) ]
then
  echo "run this from kata-ckan-dev, kata-ckan-prod, mcfg or dummy-deps" >&2
  echo "script deletes files, which might not be generally"
  echo "a good idea if run from a random place" >&2
  exit 2
fi
if [ -d "${nv}" ]
# not very likely, but who cares...
then
  rm -rf "${nv}"
fi
# version.info file is specific the to the package directory ($here)
# but we call the tool in the repo root to get natural path names
if [ -x src/versioninfo.sh ]
then
  pushd ../.. >/dev/null
  if [ -e ~1/src/version.info ]
  then
    mv ~1/src/version.info .
  fi
  ~1/src/versioninfo.sh
  mv version.info ~1/src
  echo "Now building $name version $version" >>~1/src/version.info
  popd >/dev/null
fi
# for prod we don't use the versioninfo mechanism above, but make sure
# that no changes have been made between building dev and building prod
# the effect of such changes might be hard to understand and we'd rather
# avoid unnecessary complications
if [ "$name" = kata-ckan-dev ]
then
   pushd ../.. >/dev/null
   ~1/src/devproddiff.sh dev
   popd >/dev/null
elif [ "$name" = kata-ckan-prod ]
then
   pushd ../.. >/dev/null
   ~1/src/devproddiff.sh prod
   mv sourcediffs.txt ~1/src
   echo "Now building kata-prod version $version" >>~1/src/sourcediffs.txt
   popd >/dev/null
fi
cp -a src "${nv}"
tar cjhf "${nv}.tgz" "${nv}/"
rm -rf "${nv}"
pushd ~/rpmbuild >/dev/null
cd SPECS
if [ -L "${name}.spec" ]
then
  rm "${name}.spec"
fi
ln -s "${here}/${name}.spec"
cd ../SOURCES
if [ -L "${nv}.tgz" ]
# not very likely, but who cares...
then
  rm "${nv}.tgz" ]
fi
ln -s "${here}/${nv}.tgz"
cd ..
AUTOV="${version}" rpmbuild -ba "SPECS/${name}.spec"
rm "SPECS/${name}.spec"
rm "SOURCES/${nv}.tgz"
popd >/dev/null
rm "${nv}.tgz"


