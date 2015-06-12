B1;2601;0c#--------------------------------------------------------
# HappyFace integration and nightly build server
#--------------------------------------------------------

These scripts, 

      cron.daily/HF.nightly-build.cron
      nightly-build.sh


can generate an automatic HF integration and deployment server. 
Just clone git repo and apply a cron script to the server as follows,

     cd /var/lib
     git clone https://github.com/HappyFaceGoettingen/HappyFace-Integration-Server
     cd HappyFace-Integration-Server
     cp -v cron.daily/HF.nightly-build.cron /etc/cron.daily


The scripts will try a sequencial procedure of packaging RPM, 
removing old env, deplying new HF, and running acquire.py.
The nightly-build.sh is configured by "nightly-build.conf".

As for your initial test, just run the script as follows.

   cd /var/lib/HappyFace-Integration-Server
   ./nightly-build.sh -r




!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!! Note: Using Grid-enabled function in HappyFace.
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

A location of grid user key is "/var/lib/HappyFace-Integration-Server/cert". You must prepare a grid user key and cert pair.

  1. generate user certificate
  openssl pkcs12 -clcerts -nokeys -in usercert.p12 -out usercert.pem

  2. create a private certficate with passphrase
  openssl pkcs12 -nocerts -in usercert.p12 -out userkey.pem

  3. create a private certificate without passphrase
  openssl rsa -in userkey.pem -out userkey.nopass.pem

  4. change permissions
  chmod 400 userkey.nopass.pem
  chmod 644 usercert.pem

  5. copy grid user cert.
  cp -v userkey.nopass.pem /var/lib/HappyFace-Integration-Server/cert
  cp -v usercert.pem /var/lib/HappyFace-Integration-Server/cert

