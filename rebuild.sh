#!/bin/bash

#-----------------------------------------------
# Consts
#-----------------------------------------------
cd $(dirname $0)
conf="rebuild.conf"
[ ! -e $conf ] && echo "$conf does not exist!" && exit -1
. $conf

#-----------------------------------------------
# Usage
#-----------------------------------------------
projects="happyface atlas webservice extra redcomet gridengine smartphone"
usage="./rebuild.sh [project]

   project=\"$projects\"
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
	GIT_BRANCH=$HF_GIT_BRANCH
	SPEC=$HF_SPEC
	;;
    atlas)
	GIT_PROJECT=$HF_ATLAS_MODULES_PROJECT
	GIT_BRANCH=$HF_ATLAS_MODULES_GIT_BRANCH
	SPEC=$HF_ATLAS_MODULES_SPEC
	;;
    extra)
	GIT_PROJECT=$HF_EXTRA_PROJECT
	GIT_BRANCH=$HF_EXTRA_GIT_BRANCH
	SPEC=$HF_EXTRA_SPEC
	;;
    webservice)
	GIT_PROJECT=$HF_WEBSERVICE_PROJECT
	GIT_BRANCH=$HF_WEBSERVICE_GIT_BRANCH
	SPEC=$HF_WEBSERVICE_SPEC
	;;
    redcomet)
	GIT_PROJECT=$HF_REDCOMET_PROJECT
	GIT_BRANCH=$HF_REDCOMET_GIT_BRANCH
	SPEC=$HF_REDCOMET_SPEC
	;;

    gridengine)
	GIT_PROJECT=$HF_GRIDENGINE_PROJECT
	GIT_BRANCH=$HF_GRIDENGINE_GIT_BRANCH
	SPEC=$HF_GRIDENGINE_SPEC
	;;

    smartphone)
	GIT_PROJECT=$HF_SMARTPHONE_DEVEL_PROJECT
	GIT_BRANCH=$HF_SMARTPHONE_DEVEL_GIT_BRANCH
	SPEC=$HF_SMARTPHONE_DEVEL_SPEC
	;;
    *)
	exit 0
	;;
esac



echo "------------------- Source packaging -----------------------"
cd SOURCES

## Downloading zip archive
GIT_ZIP="https://codeload.github.com/${GIT_GROUP}/${GIT_PROJECT}/zip"
rm -rvf ${GIT_PROJECT}-${GIT_BRANCH}
wget $GIT_ZIP/$GIT_BRANCH -O ${GIT_PROJECT}.zip
unzip ${GIT_PROJECT}.zip


cd ..

echo "-------------------- RPM packaging -------------------------"
sed -e "s/^%define _branch_name.*/%define _branch_name  ${GIT_BRANCH}/g" -i SPECS/$SPEC 

rpmbuild --define 'dist .${dist}' --clean -ba SPECS/$SPEC
rm -rvf BUILD BUILDROOT	

