#! /bin/sh
here=$(pwd)
name=$(basename "$here")

# simply copying the patches and scripts to rpmbuild sources folder
# not the best way to do this, but does the job for now
cp -R src/ ~/rpmbuild/SOURCES/

pushd ~/rpmbuild >/dev/null
cd SPECS
if [ -L "${name}.spec" ]
then
  rm "${name}.spec"
fi
ln -s "${here}/${name}.spec"
cd ../SOURCES
cd ..
rpmbuild -ba "SPECS/${name}.spec"
rm "SPECS/${name}.spec"
#rm -rf "SOURCES/src"
popd >/dev/null

