Name:           lxc-docker
Version:        0.6.3
Release:        2%{?dist}
Summary:        An open source project to pack, ship and run any application as a lightweight container

Group:         Applications/System
License:       Apache-2.0 
URL:           http://www.docker.io/
Source0:       http://get.docker.io/builds/Linux/x86_64/docker-latest.tgz 
Source1:       docker.upstart
Requires(pre): shadow-utils

# can't build debug package since not compiling docker ourself
%define debug_package %{nil}
%define archivedir docker-latest
%define realname docker

%description
Docker is an open-source engine that automates the deployment of any application as a lightweight, portable, self-sufficient container that will run virtually anywhere.


%prep
%setup -q -n %{archivedir}


%build
# no build steps since using binary from docker project


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/usr/bin
install %{_builddir}/%{archivedir}/docker %{buildroot}%{_bindir}/%{realname}
mkdir -p %{buildroot}/etc/init
install -m 0644 %{SOURCE1} %{buildroot}/%{_sysconfdir}/init/%{realname}.conf


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{_bindir}/docker
%{_sysconfdir}/init/docker.conf

%pre
getent group %{realname} >/dev/null || groupadd -r %{realname}


%changelog
* Thu Oct 10 2013 Brian Pitts <brian@polibyte.com> - 0.6.3-2
- Fix names in lxc-docker spec

* Sat Sep 28 2013 Brian Pitts <brian@polibyte.com> - 0.6.3-1
- Latest docker as of today is 0.6.3
- Rename package to lxc-docker

* Mon Aug 26 2013 Brian Pitts <brian@polibyte.com> - 0.6.0-1
- Latest docker as of today is 0.6.0

* Thu Aug 16 2013 Brian Pitts <brian@polibyte.com> - 0.5.3-1
- Create package
