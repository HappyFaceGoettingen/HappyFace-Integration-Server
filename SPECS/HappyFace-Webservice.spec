Summary: HappyFace-Webservice
Name: HappyFace-Webservice
Version: 3.0.0
Release: 20150611
License: Apache License Version 2.0
Group: System Environment/Daemons
URL: http://nagios-goegrid.gwdg.de/category
Source0: HappyFaceWebService.zip
BuildRoot: %{_tmppath}/%{name}-%{version}-root
Requires: HappyFaceCore = 3.0.0-2



######################################################################
#
#
# Preamble
#
# Macro definitions
%define _branch_name  master
%define _source_dir     HappyFaceWebService-%{_branch_name}

%define _prefix         /var/lib/HappyFace3
%define _sysconf_dir    /etc/httpd/conf.d
%define _category_cfg   %{_prefix}/config/categories-enabled
%define _module_cfg     %{_prefix}/config/modules-enabled
%define _category_dis_cfg   %{_prefix}/config/categories-disabled
%define _module_dis_cfg     %{_prefix}/config/modules-disabled



%define happyface_uid	373
%define happyface_user	happyface3
%define happyface_gid	373
%define happyface_group	happyface3

%define apache_group	apache


%description
HappyFace is a powerful site specific monitoring system for data from multiple input sources. This system collects, processes, rates and presents all important monitoring information for the overall status and the services of a local or Grid computing site. 


%prep
%setup -q -n %{_source_dir}


%build
#make

%install
cd ..

[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

# make directories
! [ -d $RPM_BUILD_ROOT/%{_prefix} ] && mkdir -p $RPM_BUILD_ROOT/%{_prefix}
! [ -d $RPM_BUILD_ROOT/%{_prefix}/config ] && mkdir -p $RPM_BUILD_ROOT/%{_prefix}/config
! [ -d $RPM_BUILD_ROOT/%{_sysconf_dir} ] && mkdir -p $RPM_BUILD_ROOT/%{_sysconf_dir}

# copy files
cp -vr %{_source_dir}/webservice $RPM_BUILD_ROOT/%{_prefix}/webservice
chmod 775 $RPM_BUILD_ROOT/%{_prefix}/webservice
cp -vr %{_source_dir}/modules $RPM_BUILD_ROOT/%{_prefix}
cp -vr %{_source_dir}/config/modules-enabled $RPM_BUILD_ROOT/%{_prefix}/config
cp -vr %{_source_dir}/config/categories-enabled $RPM_BUILD_ROOT/%{_prefix}/config
cp -v %{_source_dir}/happyface3-webservice.conf $RPM_BUILD_ROOT/%{_sysconf_dir}

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%pre
service httpd stop

%post
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


echo "------------------------------------"
ls %{_prefix}/webservice/*
echo "------------------------------------"

service httpd start

%preun
service httpd stop

%postun
service httpd start



%files
%defattr(-,%{happyface_user},%{happyface_group})
%{_prefix}/modules
%{_prefix}/config
%defattr(-,%{happyface_user},%{apache_group})
%{_prefix}/webservice
%defattr(-,root,root)
%{_sysconfdir}


%changelog
* Thu Jun 11 2015 Gen Kawamura <Gen.Kawamura@cern.ch> 3.0.0-20150611
- Changed package name to HappyFace-Webservice. Integrated with integration-server.
* Mon May 12 2014 Gen Kawamura <Gen.Kawamura@cern.ch> and Haykuhi Musheghyan <m.haykuhi@gmail.com> 3.0.0-20140512
- added db_table_list.py
* Thu Apr 04 2013 Gen Kawamura <Gen.Kawamura@cern.ch> and Haykuhi Musheghyan <m.haykuhi@gmail.com> 3.0.0-20140403
- fixed a bug in the pre section again, by uncomment
* Tue Mar 04 2013 Gen Kawamura <Gen.Kawamura@cern.ch> and Haykuhi Musheghyan <m.haykuhi@gmail.com> 3.0.0-20140304
- fixed a bug in the pre section
* Mon Mar 03 2013 Gen Kawamura <Gen.Kawamura@cern.ch> and Haykuhi Musheghyan <m.haykuhi@gmail.com> 3.0.0-03032014
- initial packaging
