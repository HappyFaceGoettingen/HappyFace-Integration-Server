#!/bin/bash

MY_SCRIPT_DIR=$(dirname $0)

usage="$0 [option]

 -e:     Send an email notification to [$EMAIL]

 -r:     Run


  Report Bugs to Gen Kawamura <gen.kawamura@cern.ch>
"


if [ $# -eq 0 ]; then
    echo "$usage"
    exit 0
fi

#--------------------------
# Getopt
#--------------------------
while getopts "erh" op
  do
  case $op in
      e) EMAIL_NOTIFICATION="ON"
          ;;
      r) echo "Start"
	  ;;
      h) echo "$usage"
          exit 0
          ;;
      ?) echo "$usage"
          exit 0
          ;;
  esac
done


build_rpm(){
    for package in $HF_PACKAGES
    do
	echo "Rebuilding [$package] ..."
	$REBUILD_SCRIPT $package
    done
}


setup_HF_grid_env(){
    [ ! -e /var/lib/gridkeys ] && mkdir -v $KEY_HOME && chmod 1777 $KEY_HOME

    cp -v $KEY_HOME/userkey.nopass.pem /var/lib/HappyFace3/cert/userkey.pem
    cp -v $KEY_HOME/usercert.pem /var/lib/HappyFace3/cert/usercert.pem
    chmod 400 /var/lib/HappyFace3/cert/userkey.pem
    chmod 644 /var/lib/HappyFace3/cert/usercert.pem

    chown happyface3:happyface3 /var/lib/HappyFace3/cert/userkey.pem /var/lib/HappyFace3/cert/usercert.pem
}


run_HF(){
    su happyface3 -c "cd /var/lib/HappyFace3; python $ACQUIRE_SCRIPT"
}


#-------------------------------------------------------
# Make build env and Remove old RPMS
#-------------------------------------------------------
cd $MY_SCRIPT_DIR

conf=nightly-build.conf
[ ! -e $conf ] && echo "no conf [$conf] file!" && exit -1
source $conf

[ -e RPMS ] && rm -rvf RPMS
[ ! -e $LOG_DIR ] && mkdir -v $LOG_DIR


#-------------------------------------------------------
# Check updates
#-------------------------------------------------------
build_rpm 2>&1 | tee $LOG_DIR/build.log

[ "$EMAIL_NOTIFICATION" == "ON" ] && echo "$(cat $LOG_DIR/build.log)" | $MAILER -s "Rebuilding HappyFace [$(hostname -s)]" $EMAIL

#--------------------------------------------------------
# Remove HappyFace instance
#--------------------------------------------------------
yum -y remove HappyFaceCore 2>&1 | tee $LOG_DIR/remove.log
rm -rvf /var/lib/HappyFace3  2>&1 | tee -a $LOG_DIR/remove.log

#--------------------------------------------------------
# Install HappyFace instance
#--------------------------------------------------------
yum -y --nogpgcheck install RPMS/x86_64/*.rpm 2>&1 | tee $LOG_DIR/deploy.log

DEPLOY_LOG="
=================================================================
 Removal
=================================================================
$(cat $LOG_DIR/remove.log)



=================================================================
 Installation
=================================================================
$(cat $LOG_DIR/deploy.log)
"

[ "$EMAIL_NOTIFICATION" == "ON" ] && echo "$DEPLOY_LOG" | $MAILER -s "Deploying HappyFace [$(hostname -s)]" $EMAIL

#--------------------------------------------------------
# Set up env
#--------------------------------------------------------
time setup_HF_grid_env 2>&1 | tee $LOG_DIR/deploy_env.log


#--------------------------------------------------------
# Run
#--------------------------------------------------------
if [ -z "CERT_CHECK" ]; then
    time run_HF 2>&1 | tee $LOG_DIR/run.log
else
    [ -e /var/lib/HappyFace3/cert/userkey.pem ] && time run_HF 2>&1 | tee $LOG_DIR/run.log
fi



RUN_LOG="
=================================================================
 Environment
=================================================================
$(cat $LOG_DIR/deploy_env.log)

=================================================================
 Run
=================================================================
$(cat $LOG_DIR/run.log)

" 

[ "$EMAIL_NOTIFICATION" == "ON" ] && echo "$RUN_LOG" | $MAILER -s "HappyFace Deployment Report [$(hostname -s)]" $EMAIL

