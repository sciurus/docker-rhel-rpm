Name:           lxc
Version:        0.8.0
Release:        3%{?dist}
Summary:        Linux Resource Containers
Group:          Applications/System
License:        LGPLv2+
URL:            http://lxc.sourceforge.net
Source0:        http://downloads.sourceforge.net/project/lxc/lxc/%{name}-%{version}/%{name}-%{version}.tar.gz
Patch0:         lxc-0.8.0-fedora-template.patch
BuildRequires:  docbook-utils
BuildRequires:  kernel-headers
BuildRequires:  libcap-devel
BuildRequires:  libtool

%description
Linux Resource Containers provide process and resource isolation without the
overhead of full virtualization.


%package        libs
Summary:        Runtime library files for %{name}
Group:          System Environment/Libraries
Requires:       %{name} = %{version}-%{release}

%description    libs
Linux Resource Containers provide process and resource isolation without the
overhead of full virtualization.

The %{name}-libs package contains libraries for running %{name} applications.


%package        templates
Summary:        Templates for %{name}
Group:          System Environment/Libraries
Requires:       %{name} = %{version}-%{release}
# needed for lxc-busybox
Requires:       busybox
# needed for lxc-debian
Requires:       dpkg
# needed for lxc-debian, lxc-ubuntu:
Requires:       debootstrap
# needed for lxc-sshd
Requires:       openssh-server dhclient


%description    templates
Linux Resource Containers provide process and resource isolation without the
overhead of full virtualization.

The %{name}-template package contains templates for creating containers.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig

%description    devel
Linux Resource Containers provide process and resource isolation without the
overhead of full virtualization.

The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package        doc
Summary:        Documentation for %{name}
Group:          Documentation
Requires:       %{name} = %{version}-%{release}

%description    doc
This package contains documentation for %{name}.


%prep
%setup -q
%patch0 -p1


%build
%configure --enable-doc --disable-rpath --disable-apparmor
make %{?_smp_mflags}


%install
%{make_install}
make DESTDIR=%{buildroot} install
mkdir -p %{buildroot}%{_sharedstatedir}/%{name}


%check
make check


%post libs -p /sbin/ldconfig


%postun libs -p /sbin/ldconfig


%files
%doc AUTHORS COPYING README
%{_bindir}/%{name}-*
%{_mandir}/man*/%{name}*
%{_sharedstatedir}/%{name}


%files libs
%doc AUTHORS COPYING
%dir %{_datadir}/lxc
%dir %{_datadir}/lxc/templates
%{_libdir}/liblxc.so.*
%dir %{_libdir}/lxc
%{_libdir}/lxc/rootfs
%dir %{_libexecdir}/lxc
%{_libexecdir}/lxc/lxc-init


%files templates
%{_datadir}/lxc/templates/lxc-*
# needs apt
%exclude %{_datadir}/lxc/templates/lxc-altlinux
# needs pacman
%exclude %{_datadir}/lxc/templates/lxc-archlinux
# probably outdated
%exclude %{_datadir}/lxc/templates/lxc-lenny
# needs zypper
%exclude %{_datadir}/lxc/templates/lxc-opensuse
# needs ubuntu-cloudimg-query
%exclude %{_datadir}/lxc/templates/lxc-ubuntu-cloud


%files devel
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/lxc
%{_libdir}/liblxc.so


%files doc
%{_docdir}/%{name}


%changelog
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Mar  2 2013 Thomas Moschny <thomas.moschny@gmx.de> - 0.8.0-2
- Add upstream patch fixing the release url in the Fedora template.

* Fri Feb 15 2013 Thomas Moschny <thomas.moschny@gmx.de> - 0.8.0-1
- Update to 0.8.0.
- Modernize spec file.
- Include more templates.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Mar 26 2012 Thomas Moschny <thomas.moschny@gmx.de> - 0.7.5-1
- Update to upstream 0.7.5
- No need to run autogen.sh
- Fix: kernel header asm/unistd.h was not found
- Specfile cleanups

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 06 2011 Adam Miller <maxamillion@fedoraproject.org> - 0.7.4.2-1
- Update to upstream 0.7.4.2

* Fri Mar 25 2011 Silas Sewell <silas@sewell.ch> - 0.7.4.1-1
- Update to 0.7.4.1

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jul 26 2010 Silas Sewell <silas@sewell.ch> - 0.7.2-1
- Update to 0.7.2
- Remove templates

* Tue Jul 06 2010 Silas Sewell <silas@sewell.ch> - 0.7.1-1
- Update to 0.7.1

* Wed Feb 17 2010 Silas Sewell <silas@sewell.ch> - 0.6.5-1
- Update to latest release
- Add /var/lib/lxc directory
- Patch for sys/stat.h

* Fri Nov 27 2009 Silas Sewell <silas@sewell.ch> - 0.6.4-1
- Update to latest release
- Add documentation sub-package

* Mon Jul 27 2009 Silas Sewell <silas@sewell.ch> - 0.6.3-2
- Apply patch for rawhide kernel

* Sat Jul 25 2009 Silas Sewell <silas@sewell.ch> - 0.6.3-1
- Initial package

