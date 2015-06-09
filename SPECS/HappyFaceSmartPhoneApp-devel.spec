Summary: HappyFace-ATLAS
Name: HappyFace-SmartPhoneApp-devel
Version: 3.0.0
Release: 20150609
License: Apache License Version 2.0
Group: System Environment/Daemons
URL: http://nagios-goegrid.gwdg.de/category
Source0: HappySmartPhoneApp.zip
BuildRoot: %{_tmppath}/%{name}-%{version}-root
Requires: npm
Requires: nodejs
Requires: java-1.7.0-openjdk-devel
Requires: ant-apache-regexp



######################################################################
#
#
# Preamble
#
# Macro definitions
%define _branch_name    master
%define _source_dir     HappyFaceSmartPhoneApp-%{_branch_name}


%define _prefix         /var/lib/HappyFace3-SmartPhoneApp-devel
%define _profile_dir    /etc/profile.d

%define happyface_uid	373
%define happyface_user	happyface3
%define happyface_gid	373
%define happyface_group	happyface3


%description
HappyFace is a powerful site specific monitoring system for data from multiple input sources. This system collects, processes, rates and presents all important monitoring information for the overall status and the services of a local or Grid computing site. 


%prep
%setup0 -q -n %{_source_dir}


%build
#make

%install
cd ..

[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

# make directories
! [ -d $RPM_BUILD_ROOT/%{_prefix} ] && mkdir -vp $RPM_BUILD_ROOT/%{_prefix}


# Generating environments


cp -vr %{_source_dir}/modules $RPM_BUILD_ROOT/%{_prefix}

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%pre
npm install -g cordova
npm install -g ionic


%post
source %{_profile_dir}/android_sdk.sh



%files
%defattr(-,%{happyface_user},%{happyface_group})
%{_prefix}


%changelog
* Wed Jun 03 2015 Gen Kawamura <Gen.Kawamura@cern.ch> 3.0.0-20150603
- integrated with integration-server
* Mon May 12 2014 Gen Kawamura <Gen.Kawamura@cern.ch> 3.0.0-20140512
- modified category name and module config according to O/R schema relationships
* Tue Mar 03 2014 Gen Kawamura <Gen.Kawamura@cern.ch> 3.0.0-04032014
- decomissioned ganglia and moved it to ATLAS-internal-resource rpm
- upgraded Panda module
* Mon Mar 03 2014 Gen Kawamura <Gen.Kawamura@cern.ch> 3.0.0-03032014
- decomissioned webservice and moved it to ATLAS-webservice rpm
* Wed Dec 18 2013 Gen Kawamura <Gen.Kawamura@cern.ch> 3.0.0-18122013
- quasi-stable version

* Fri Jul 19 2013 Gen Kawamura <Gen.Kawamura@cern.ch> and Christian Wehrberger <cgwehrberger@gmail.com> 3.0.0-16072013
- initial packaging
