Summary: HappyFace-Grid-Engine
Name: HappyFace-Grid-Engine
Version: 3.0.0
Release: 4
License: Apache License Version 2.0
Group: System Environment/Daemons
URL: https://ekptrac.physik.uni-karlsruhe.de/trac/HappyFace
Source0: Red-Comet.zip
BuildRoot: %{_tmppath}/%{name}-%{version}-root
Requires: HappyFace = 3.0.0-1
Requires: python >= 2.6
Requires: httpd >= 2.0
Requires: python-cherrypy >= 3.0
Requires: python-sqlalchemy >= 0.5
Requires: python-migrate
Requires: python-mako
Requires: python-matplotlib
Requires: python-sqlite
Requires: python-psycopg2
Requires: python-lxml
Requires: numpy
Requires: mod_wsgi
Requires: sqlite

# For Red-Comet
Requires: openssl
Requires: cvmfs
#Requires: eclipse-platform
Requires: yum-protectbase
Requires: fetch-crl
Requires: ca-policy-egi-core
Requires: umd-release >= 3.0.0
Requires: rpmforge-release
#Requires: kdesdk


######################################################################
#
#
# Preamble
#
# Macro definitions
%define _branch_name    Zgok
%define _source_dir     Red-Comet-%{_branch_name}

%define _prefix         /var/lib/HappyFace3

%define _category_cfg   %{_prefix}/config/categories-enabled
%define _module_cfg     %{_prefix}/config/modules-enabled
%define _category_dis_cfg   %{_prefix}/config/categories-disabled
%define _module_dis_cfg     %{_prefix}/config/modules-disabled

%define _cert_dir	%{_prefix}/cert
%define _defaultconfig	%{_prefix}/defaultconfig


%define happyface_uid	373
%define happyface_user	happyface3
%define happyface_gid	373
%define happyface_group	happyface3


%description
HappyFace is a powerful site specific monitoring system for data from multiple input sources. This system collects, processes, rates and presents all important monitoring information for the overall status and the services of a local or Grid computing site. 


Note: How to generate grid certificate without passphrase

1. go to ~/.globus
 cd ~/.globus

2. generate user certificate
 openssl pkcs12 -clcerts -nokeys -in usercert.p12 -out usercert.pem

3. create a private certficate with passphrase
 openssl pkcs12 -nocerts -in usercert.p12 -out userkey.pem
 
4. create a private certificate without passphrase
 openssl rsa -in userkey.pem -out userkey.nopass.pem

5. set permissions
 chmod 400 userkey.pem
 chmod 400 userkey.nopass.pem
 chmod 644 usercert.pem

6. Please copy X.509 keys as follows. If you need to change names and locations, please fix properties (x509.user.key and x509.user.cert) in /var/lib/HappyFace3/defaultconfig/happyface.cfg

 cp userkey.nopass.pem /var/lib/HappyFace3/cert/userkey.pem
 cp usercert.pem /var/lib/HappyFace3/cert/usercert.pem
 chown happyface3:happyface3 /var/lib/HappyFace3/cert/userkey.pem /var/lib/HappyFace3/cert/usercert.pem

7. Test the system
 su %{happyface_user} -c "cd /var/lib/HappyFace3; python grid_enabled_acquire.py" 



Report Bugs and Opinions to <gen.kawamura@cern.ch>

%prep
%setup0 -q -n %{_source_dir}

%build
#make

%install
cd ..

[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT


# make directories
! [ -d $RPM_BUILD_ROOT/%{_prefix} ] && mkdir -vp $RPM_BUILD_ROOT/%{_prefix}/hf
! [ -d $RPM_BUILD_ROOT/%{_cert_dir} ] && mkdir -vp $RPM_BUILD_ROOT/%{_cert_dir}
! [ -d $RPM_BUILD_ROOT/%{_module_cfg} ] && mkdir -vp $RPM_BUILD_ROOT/%{_module_cfg}
! [ -d $RPM_BUILD_ROOT/%{_category_cfg} ] && mkdir -vp $RPM_BUILD_ROOT/%{_category_cfg}
! [ -d $RPM_BUILD_ROOT/%{_defaultconfig} ] && mkdir -vp $RPM_BUILD_ROOT/%{_defaultconfig}
! [ -d $RPM_BUILD_ROOT/%{_sysconf_dir} ] && mkdir -p $RPM_BUILD_ROOT/%{_sysconf_dir}


# rm .svn in devel dir
find %{_source_dir} -type f | grep .svn | xargs -I {} rm -vf {}
find %{_source_dir} -type d | grep .svn | sort -r | xargs -I {} rmdir -v {}


# copy files
cp -vr %{_source_dir}/modules $RPM_BUILD_ROOT/%{_prefix}
cp -vr %{_source_dir}/config/modules-enabled/* $RPM_BUILD_ROOT/%{_module_cfg}
cp -vr %{_source_dir}/config/categories-enabled/* $RPM_BUILD_ROOT/%{_category_cfg}


# grid-related python codes
cp -vr %{_source_dir}/hf/gridengine $RPM_BUILD_ROOT/%{_prefix}/hf
cp -vr %{_source_dir}/hf/gridtoolkit $RPM_BUILD_ROOT/%{_prefix}/hf
cp -vr %{_source_dir}/grid_enabled_acquire.py $RPM_BUILD_ROOT/%{_prefix}




# defaultconfig
cp -v %{_source_dir}/defaultconfig/happyface.cfg $RPM_BUILD_ROOT/%{_defaultconfig}/


%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT


%post
mv -v %{_defaultconfig}/happyface.cfg %{_defaultconfig}/happyface.cfg.org

## making default categories disabled
! [ -e %{_module_dis_cfg} ] && mkdir -v %{_module_dis_cfg}
! [ -e %{_category_dis_cfg} ] && mkdir -v %{_category_dis_cfg}

## disabling default categories
[ -e %{_category_cfg}/batch_system.cfg ] && mv -v %{_category_cfg}/batch_system.cfg %{_category_dis_cfg}
[ -e %{_category_cfg}/infrastructure.cfg ] && mv -v %{_category_cfg}/infrastructure.cfg %{_category_dis_cfg}
[ -e %{_category_cfg}/phedex_prod.cfg ] && mv -v %{_category_cfg}/phedex_prod.cfg %{_category_dis_cfg}

## disabling default modules
[ -e %{_module_cfg}/batch_system.cfg ] && mv -v %{_module_cfg}/batch_system.cfg %{_module_dis_cfg}
[ -e %{_module_cfg}/phedex_prod.cfg ] && mv -v %{_module_cfg}/phedex_prod.cfg %{_module_dis_cfg}
[ -e %{_module_cfg}/uschi_basic_dcap.cfg ] && mv -v %{_module_cfg}/uschi_*.cfg %{_module_dis_cfg}


echo "Activating fetch-crl update daemons ..."
chkconfig fetch-crl-boot on
chkconfig fetch-crl-cron on


if [ -e %{_cert_dir}/usercert.pem ] && [ -e %{_cert_dir}/usercert.pem ]; then 
   echo "------------------------------------"
   echo "Populating default Happy Face database ..."
   cd %{_prefix}
   su %{happyface_user} -c "python grid_enabled_acquire.py"
   echo "------------------------------------"
fi

service httpd restart

%preun
service httpd stop

%postun
mv -v %{_defaultconfig}/happyface.cfg.org %{_defaultconfig}/happyface.cfg
service httpd start


%files
%defattr(-,happyface3,happyface3)
%{_cert_dir}
%{_prefix}/modules
%{_prefix}/hf/gridengine
%{_prefix}/hf/gridtoolkit
%{_prefix}/grid_enabled_acquire.py*
%{_defaultconfig}/happyface.cfg
%{_category_cfg}
%{_module_cfg}



%changelog
* Wed Jun 03 2015 Gen Kawamura <Gen.Kawamura@cern.ch> 3.0.0-4
- integrated with integration-server
* Tue May 19 2015 Gen Kawamura <Gen.Kawamura@cern.ch> 3.0.0-3
- build sprint-4 Zgok
* Fri Mar 06 2015 Gen Kawamura <Gen.Kawamura@cern.ch> 3.0.0-2
- build sprint-3 Zanzibar
* Thu Aug 14 2014 Gen Kawamura <Gen.Kawamura@cern.ch> 3.0.0-1
- build sprint-2 blue-giant 
* Thu Jul 17 2014 Gen Kawamura <Gen.Kawamura@cern.ch> 3.0.0-0
- initial packaging
