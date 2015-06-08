#!/bin/sh

#-----------------------------------------------
# Consts
#-----------------------------------------------

## HappyFaceCore
HF_PROJECT="HappyFaceCore"
HF_GIT="https://codeload.github.com/HappyFaceGoettingen/${HF_PROJECT}/zip"
HF_GIT_BRANCH="master"
HF_SPEC="HappyFace.spec"


## HappyFaceATLASModules
HF_ATLAS_MODULES_PROJECT="HappyFaceATLASModules"
HF_ATLAS_MODULES_GIT="https://codeload.github.com/HappyFaceGoettingen/${HF_ATLAS_MODULES_PROJECT}/zip"
HF_ATLAS_MODULES_GIT_BRANCH="master"
HF_ATLAS_MODULES_SPEC="HappyFace-ATLAS.spec"


## HappyFaceF Red-comet
HF_GRIDENGINE_PROJECT="Red-Comet"
HF_REDCOMET_GIT="https://codeload.github.com/HappyFaceGoettingen/${HF_GRIDENGINE_PROJECT}/zip"
HF_REDCOMET_GIT_BRANCH="Zgok"
HF_GRIDENGINE_SPEC="HappyFace-Grid-Engine.spec"


#-----------------------------------------------
# Usage
#-----------------------------------------------
projects="happyface atlas atlas-webservice extra redcomet gridengine"
usage="./rebuild.sh [project]

   project=$projects
"



if [ $# -eq 0 ]; then
  echo "$usage"
  exit 0
fi

#---------------------------------------------
# Environments
#---------------------------------------------
echo "%_topdir        $PWD" > rpmmacros_HappyFace
ln -sf $PWD/rpmmacros_HappyFace ~/.rpmmacros


mkdir -pv BUILD BUILDROOT SOURCES SPECS RPMS log
dist=`uname -r | perl -pe "s/^.*\.(el[0-9])\..*$/\1/g"`


#---------------------------------------------
# Main
#---------------------------------------------
case "$1" in
    happyface)
	GIT_PROJECT=$HF_PROJECT
	GIT=$HF_GIT
	GIT_BRANCH=$HF_GIT_BRANCH
	SPEC=$HF_SPEC
	;;
    atlas)
	GIT_PROJECT=$HF_ATLAS_MODULES_PROJECT
	GIT=$HF_ATLAS_MODULES_GIT
	GIT_BRANCH=$HF_ATLAS_MODULES_GIT_BRANCH
	SPEC=$HF_ATLAS_MODULES_SPEC
	;;
    extra)
	echo "------------------- Source packaging -----------------------"
	cd SOURCES
	tar czvf HappyFace-ATLAS-internal-resource_modules-3.0.0.tar.gz HappyFace-ATLAS-internal-resource_modules
	cd ..

	echo "-------------------- RPM packaging -------------------------"
	rpmbuild --define 'dist .${dist}' --clean -ba SPECS/HappyFace-ATLAS-internal-resource.spec
	rm -rvf BUILD BUILDROOT
	exit 0
	;;
    atlas-webservice)
	echo "------------------- Source packaging -----------------------"
	cd SOURCES
	tar czvf HappyFace-ATLAS-webservice-3.0.0.tar.gz HappyFace-ATLAS-webservice
	cd ..

	echo "-------------------- RPM packaging -------------------------"
	rpmbuild --define 'dist .${dist}' --clean -ba SPECS/HappyFace-ATLAS-webservice.spec
	rm -rvf BUILD BUILDROOT
	exit 0
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
	exit 0
	;;

    gridengine)
	GIT_PROJECT=$HF_GRIDENGINE_PROJECT
	GIT=$HF_REDCOMET_GIT
	GIT_BRANCH=$HF_REDCOMET_GIT_BRANCH
	SPEC=$HF_GRIDENGINE_SPEC
	;;
    *)
	exit 0
	;;
esac



echo "------------------- Source packaging -----------------------"
cd SOURCES
rm -rvf ${GIT_PROJECT}-${GIT_BRANCH}
wget $GIT/$GIT_BRANCH -O ${GIT_PROJECT}.zip
unzip ${GIT_PROJECT}.zip
cd ..

echo "-------------------- RPM packaging -------------------------"
rpmbuild --define 'dist .${dist}' --clean -ba SPECS/$SPEC
rm -rvf BUILD BUILDROOT	

