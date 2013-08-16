Name:           docker
Version:        0.5.3
Release:        1%{?dist}
Summary:        An open source project to pack, ship and run any application as a lightweight container

Group:         Applications/System
License:       Apache-2.0 
URL:           http://www.docker.io/
Source0:       http://get.docker.io/builds/Linux/x86_64/docker-latest.tgz 
Source1:       docker.upstart
Requires(pre): shadow-utils

# can't build debug package since nor compiling docker ourself
%define debug_package %{nil}
%define archivedir docker-latest

%description
Docker is an open-source engine that automates the deployment of any application as a lightweight, portable, self-sufficient container that will run virtually anywhere.


%prep
%setup -q -n %{archivedir}


%build
# no build steps since using binary from docker project


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/usr/bin
install %{_builddir}/%{archivedir}/docker %{buildroot}%{_bindir}/%{name}
mkdir -p %{buildroot}/etc/init
install -m 0644 %{SOURCE1} %{buildroot}/%{_sysconfdir}/init/%{name}.conf


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{_bindir}/docker
%{_sysconfdir}/init/docker.conf

%pre
getent group %{name} >/dev/null || groupadd -r %{name}


%changelog
* Thu Aug 16 2013 Brian Pitts <brian@polibyte.com> - 0.5.3-1
- Create package
