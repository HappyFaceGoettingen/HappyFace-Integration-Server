Summary: HappyFace-SmartPhoneApp-devel
Name: HappyFace-SmartPhoneApp-devel
Version: 0.0.1
Release: 20150609
License: Apache License Version 2.0
Group: System Environment/Daemons
URL: http://nagios-goegrid.gwdg.de/category
Source0: HappyFaceSmartPhoneApp.zip
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


cp -vr %{_source_dir}/www $RPM_BUILD_ROOT/%{_prefix}

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
* Tue Jul 09 2015 Gen Kawamura <Gen.Kawamura@cern.ch> 0.0.1-20150609
- initial packaging
