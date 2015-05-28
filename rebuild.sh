#!/bin/sh

specs="happyface atlas atlas-intr atlas-webservice redcomet gridengine"
usage="./rebuild.sh [spec]

   specs=$specs
"



if [ $# -eq 0 ]; then
  echo "$usage"
  exit 0
fi

## create .rpmmacros
echo "%_topdir        $PWD" > rpmmacros_HappyFace
ln -sf $PWD/rpmmacros_HappyFace ~/.rpmmacros

mkdir -v BUILD BUILDROOT



dist=`uname -r | perl -pe "s/^.*\.(el[0-9])\..*$/\1/g"`

case "$1" in
    happyface)
	rpmbuild --define 'dist .${dist}' --clean -ba SPECS/HappyFace.spec
	rm -rvf BUILD BUILDROOT
	;;
    atlas)
	echo "------------------- Source packaging -----------------------"
	cd SOURCES
	tar czvf HappyFace-ATLAS_modules-3.0.0.tar.gz HappyFace-ATLAS_modules
	cd ..

	echo "-------------------- RPM packaging -------------------------"
	rpmbuild --define 'dist .${dist}' --clean -ba SPECS/HappyFace-ATLAS.spec
	rm -rvf BUILD BUILDROOT
	;;
    atlas-intr)
	echo "------------------- Source packaging -----------------------"
	cd SOURCES
	tar czvf HappyFace-ATLAS-internal-resource_modules-3.0.0.tar.gz HappyFace-ATLAS-internal-resource_modules
	cd ..

	echo "-------------------- RPM packaging -------------------------"
	rpmbuild --define 'dist .${dist}' --clean -ba SPECS/HappyFace-ATLAS-internal-resource.spec
	rm -rvf BUILD BUILDROOT
	;;
    atlas-webservice)
	echo "------------------- Source packaging -----------------------"
	cd SOURCES
	tar czvf HappyFace-ATLAS-webservice-3.0.0.tar.gz HappyFace-ATLAS-webservice
	cd ..

	echo "-------------------- RPM packaging -------------------------"
	rpmbuild --define 'dist .${dist}' --clean -ba SPECS/HappyFace-ATLAS-webservice.spec
	rm -rvf BUILD BUILDROOT
	;;
    redcomet)
	echo "------------------- Source packaging -----------------------"
	cd SOURCES/HappyFace-Red-Comet

	if [ -e /var/lib/HappyFace3-devel ]; then
	    rm -rv red-comet-devel
	    [ ! -e red-comet-devel ] && mkdir -pv red-comet-devel
	    cp -v /var/lib/HappyFace3-devel/*.sh red-comet-devel/
	    cp -v /var/lib/HappyFace3-devel/README.txt red-comet-devel/
	    tar czvf red-comet-devel.tar.gz red-comet-devel
	fi

	cd ..
	cp -v HappyFace-Red-Comet/red-comet-devel.tar.gz .
	cd ..

	echo "-------------------- RPM packaging -------------------------"
	rpmbuild --define 'dist .${dist}' --clean -ba SPECS/HappyFace-Red-Comet.spec
	rm -rvf BUILD BUILDROOT	
	;;

    gridengine)
	echo "------------------- Source packaging -----------------------"
	cd SOURCES/HappyFace-Red-Comet
	[ -e Red-Comet ] && rm -rf Red-Comet
	git clone https://github.com/HappyFaceGoettingen/Red-Comet.git -b Zgok
	cp -v Red-Comet/defaultconfig/happyface.cfg happyface-red-comet.cfg

	[ -e red-comet ] && rm -rf red-comet
	[ ! -e red-comet/hf/gridengine ] && mkdir -pv red-comet/hf/gridengine
	[ ! -e red-comet/hf/gridtoolkit ] && mkdir -pv red-comet/hf/gridtoolkit
	cp -v Red-Comet/hf/gridengine/*.py red-comet/hf/gridengine/
	cp -v Red-Comet/hf/gridtoolkit/*.py red-comet/hf/gridtoolkit/
	cp -v Red-Comet/grid_enabled_acquire.py red-comet/
	cp -rv Red-Comet/modules red-comet/
	cp -rv Red-Comet/config red-comet/
	cp -rv Red-Comet/defaultconfig red-comet/


	tar czvf red-comet.tar.gz red-comet

	cd ..
	mv -v HappyFace-Red-Comet/red-comet.tar.gz .
	ln -sf HappyFace-Red-Comet/happyface-red-comet.cfg .
	cd ..

	echo "-------------------- RPM packaging -------------------------"
	rpmbuild --define 'dist .${dist}' --clean -ba SPECS/HappyFace-Grid-Engine.spec
	rm -rvf BUILD BUILDROOT	
	;;
    *)
	;;
esac
