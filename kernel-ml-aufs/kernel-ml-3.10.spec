%global __spec_install_pre %{___build_pre}

# Define the version of the Linux Kernel Archive tarball.
%define LKAver 3.10.5

# Define the version of the aufs-standalone zip file
%define AUFSver aufs-aufs3-standalone-8b36a1dab528a5d1867f8e8c52c524eecd2d6f82

# Define the buildid, if required.
#define buildid .

# The following build options are enabled by default.
# Use either --without <option> on your rpmbuild command line
# or force the values to 0, here, to disable them.

# PAE kernel-ml-aufs
%define with_std          %{?_without_std:          0} %{?!_without_std:          1}
# NONPAE kernel-ml-aufs
%define with_nonpae       %{?_without_nonpae:       0} %{?!_without_nonpae:       1}
# kernel-ml-aufs-doc
%define with_doc          %{?_without_doc:          0} %{?!_without_doc:          1}
# kernel-ml-aufs-headers
%define with_headers      %{?_without_headers:      0} %{?!_without_headers:      1}
# kernel-ml-aufs-firmware
%define with_firmware     %{?_without_firmware:     0} %{?!_without_firmware:     1}
# perf subpackage
%define with_perf         %{?_without_perf:         0} %{?!_without_perf:         1}
# vdso directories installed
%define with_vdso_install %{?_without_vdso_install: 0} %{?!_without_vdso_install: 1}
# use dracut instead of mkinitrd
%define with_dracut       %{?_without_dracut:       0} %{?!_without_dracut:       1}

# Build only the kernel-ml-aufs-doc & kernel-ml-aufs-firmware packages.
%ifarch noarch
%define with_std 0
%define with_nonpae 0
%define with_headers 0
%define with_perf 0
%define with_vdso_install 0
%endif

# Build only the 32-bit kernel-ml-aufs-headers package.
%ifarch i386
%define with_std 0
%define with_nonpae 0
%define with_doc 0
%define with_firmware 0
%define with_perf 0
%define with_vdso_install 0
%endif

# Build only the 32-bit kernel-ml-aufs packages.
%ifarch i686
%define with_doc 0
%define with_headers 0
%define with_firmware 0
%endif

# Build only the 64-bit kernel-ml-aufs-headers & kernel-ml-aufs packages.
%ifarch x86_64
%define with_nonpae 0
%define with_doc 0
%define with_firmware 0
%endif

# Define the asmarch.
%define asmarch x86

# Define the correct buildarch.
%define buildarch x86_64
%ifarch i386 i686
%define buildarch i386
%endif

# Define the vdso_arches.
%if %{with_vdso_install}
%define vdso_arches i686 x86_64
%endif

# Determine the sublevel number and set pkg_version.
%define sublevel %(echo %{LKAver} | %{__awk} -F\. '{ print $3 }')
%if "%{sublevel}" == ""
%define pkg_version %{LKAver}.0
%else
%define pkg_version %{LKAver}
%endif

# Set pkg_release.
%define pkg_release 1%{?buildid}%{?dist}

#
# Three sets of minimum package version requirements in the form of Conflicts.
#

#
# First the general kernel required versions, as per Documentation/Changes.
#
%define kernel_dot_org_conflicts  ppp < 2.4.3-3, isdn4k-utils < 3.2-32, nfs-utils < 1.0.7-12, e2fsprogs < 1.37-4, util-linux < 2.12, jfsutils < 1.1.7-2, reiserfs-utils < 3.6.19-2, xfsprogs < 2.6.13-4, procps < 3.2.5-6.3, oprofile < 0.9.1-2

#
# Then a series of requirements that are distribution specific, either because
# the older versions have problems with the newer kernel or lack certain things
# that make integration in the distro harder than needed.
#
%define package_conflicts initscripts < 7.23, udev < 145-11, iptables < 1.3.2-1, ipw2200-firmware < 2.4, iwl4965-firmware < 228.57.2, selinux-policy-targeted < 1.25.3-14, squashfs-tools < 4.0, wireless-tools < 29-3

#
# We moved the drm include files into kernel-headers, make sure there's
# a recent enough libdrm-devel on the system that doesn't have those.
#
%define kernel_headers_conflicts libdrm-devel < 2.4.0-0.15

#
# Packages that need to be installed before the kernel because the %post scripts make use of them.
#
%define kernel_prereq fileutils, module-init-tools, initscripts >= 8.11.1-1, grubby >= 7.0.4-1
%if %{with_dracut}
%define initrd_prereq dracut-kernel >= 002-18.git413bcf78
%else
%define initrd_prereq mkinitrd >= 6.0.61-1
%endif

Name: kernel-ml-aufs
Summary: The Linux kernel. (The core of any Linux-based operating system.)
Group: System Environment/Kernel
License: GPLv2
URL: http://www.kernel.org/
Version: %{pkg_version}
Release: %{pkg_release}
ExclusiveArch: noarch i386 i686 x86_64
ExclusiveOS: Linux
Provides: kernel = %{version}-%{release}
Provides: kernel-%{_target_cpu} = %{version}-%{release}
Provides: kernel-drm = 4.3.0
Provides: kernel-drm-nouveau = 16
Provides: kernel-modeset = 1
Provides: kernel-uname-r = %{version}-%{release}.%{_target_cpu}
Provides: kernel-ml-aufs = %{version}-%{release}
Provides: kernel-ml-aufs-%{_target_cpu} = %{version}-%{release}
Provides: kernel-ml-aufs-drm = 4.3.0
Provides: kernel-ml-aufs-drm-nouveau = 16
Provides: kernel-ml-aufs-modeset = 1
Provides: kernel-ml-aufs-uname-r = %{version}-%{release}.%{_target_cpu}
Requires(pre): %{kernel_prereq}
Requires(pre): %{initrd_prereq}
Requires(post): /sbin/new-kernel-pkg
Requires(preun): /sbin/new-kernel-pkg
Conflicts: %{kernel_dot_org_conflicts}
Conflicts: %{package_conflicts}
Conflicts: %{kernel_headers_conflicts}
# We can't let RPM do the dependencies automatically because it'll then pick up
# a correct but undesirable perl dependency from the module headers which
# isn't required for the kernel-ml-aufs proper to function.
AutoReq: no
AutoProv: yes

#
# List the packages used during the kernel-ml-aufs build.
#
BuildRequires: asciidoc, bash >= 2.03, bc, binutils >= 2.12, bzip2, diffutils
BuildRequires: findutils, gawk, gcc >= 3.4.2, gzip, m4, make >= 3.78
BuildRequires: module-init-tools, net-tools, patch >= 2.5.4, patchutils, perl
BuildRequires: redhat-rpm-config, rpm-build >= 4.8.0-7, sh-utils, tar, xmlto
%if %{with_perf}
BuildRequires: audit-libs-devel, binutils-devel, bison, elfutils-devel
BuildRequires: elfutils-libelf-devel, gtk2-devel, newt-devel
BuildRequires: perl(ExtUtils::Embed), python-devel, zlib-devel
%endif
BuildRequires: python

BuildConflicts: rhbuildsys(DiskFree) < 7Gb

# Sources.
Source0: ftp://ftp.kernel.org/pub/linux/kernel/v3.x/linux-%{LKAver}.tar.xz
Source1: config-%{version}-i686
Source2: config-%{version}-i686-NONPAE
Source3: config-%{version}-x86_64
Source4: http://sourceforge.net/code-snapshots/git/a/au/aufs/aufs3-standalone.git/%{AUFSver}.zip

%description
This package provides the Linux kernel (vmlinuz), the core of any
Linux-based operating system. The kernel handles the basic functions
of the OS: memory allocation, process allocation, device I/O, etc.

%package devel
Summary: Development package for building kernel modules to match the kernel.
Group: System Environment/Kernel
Provides: kernel-devel-%{_target_cpu} = %{version}-%{release}
Provides: kernel-devel = %{version}-%{release}
Provides: kernel-devel-uname-r = %{version}-%{release}.%{_target_cpu}
Provides: kernel-ml-aufs-devel-%{_target_cpu} = %{version}-%{release}
Provides: kernel-ml-aufs-devel = %{version}-%{release}
Provides: kernel-ml-aufs-devel-uname-r = %{version}-%{release}.%{_target_cpu}
Requires(pre): /usr/bin/find
AutoReqProv: no
%description devel
This package provides the kernel header files and makefiles
sufficient to build modules against the kernel package.

%if %{with_nonpae}
%package NONPAE
Summary: The Linux kernel for non-PAE capable processors.
Group: System Environment/Kernel
Provides: kernel = %{version}-%{release}
Provides: kernel-%{_target_cpu} = %{version}-%{release}NONPAE
Provides: kernel-NONPAE = %{version}-%{release}
Provides: kernel-NONPAE-%{_target_cpu} = %{version}-%{release}NONPAE
Provides: kernel-drm = 4.3.0
Provides: kernel-drm-nouveau = 16
Provides: kernel-modeset = 1
Provides: kernel-uname-r = %{version}-%{release}.%{_target_cpu}
Provides: kernel-ml-aufs = %{version}-%{release}
Provides: kernel-ml-aufs-%{_target_cpu} = %{version}-%{release}NONPAE
Provides: kernel-ml-aufs-NONPAE = %{version}-%{release}
Provides: kernel-ml-aufs-NONPAE-%{_target_cpu} = %{version}-%{release}NONPAE
Provides: kernel-ml-aufs-drm = 4.3.0
Provides: kernel-ml-aufs-drm-nouveau = 16
Provides: kernel-ml-aufs-modeset = 1
Provides: kernel-ml-aufs-uname-r = %{version}-%{release}.%{_target_cpu}
Requires(pre): %{kernel_prereq}
Requires(pre): %{initrd_prereq}
Requires(post): /sbin/new-kernel-pkg
Requires(preun): /sbin/new-kernel-pkg
Conflicts: %{kernel_dot_org_conflicts}
Conflicts: %{package_conflicts}
Conflicts: %{kernel_headers_conflicts}
# We can't let RPM do the dependencies automatically because it'll then pick up
# a correct but undesirable perl dependency from the module headers which
# isn't required for the kernel-ml-aufs proper to function.
AutoReq: no
AutoProv: yes
%description NONPAE
This package provides a version of the Linux kernel suitable for
processors without the Physical Address Extension (PAE) capability.
It can only address up to 4GB of memory.

%package NONPAE-devel
Summary: Development package for building kernel modules to match the non-PAE kernel.
Group: System Environment/Kernel
Provides: kernel-NONPAE-devel-%{_target_cpu} = %{version}-%{release}
Provides: kernel-NONPAE-devel = %{version}-%{release}NONPAE
Provides: kernel-NONPAE-devel-uname-r = %{version}-%{release}.%{_target_cpu}
Provides: kernel-ml-aufs-NONPAE-devel-%{_target_cpu} = %{version}-%{release}
Provides: kernel-ml-aufs-NONPAE-devel = %{version}-%{release}NONPAE
Provides: kernel-ml-aufs-NONPAE-devel-uname-r = %{version}-%{release}.%{_target_cpu}
Requires(pre): /usr/bin/find
AutoReqProv: no
%description NONPAE-devel
This package provides the kernel header files and makefiles
sufficient to build modules against the kernel package.
%endif

%if %{with_doc}
%package doc
Summary: Various bits of documentation found in the kernel sources.
Group: Documentation
Provides: kernel-doc = %{version}-%{release}
%description doc
This package provides documentation files from the kernel sources.
Various bits of information about the Linux kernel and the device
drivers shipped with it are documented in these files.

You'll want to install this package if you need a reference to the
options that can be passed to the kernel modules at load time.
%endif

%if %{with_headers}
%package headers
Summary: Header files for the Linux kernel for use by glibc
Group: Development/System
Obsoletes: glibc-kernheaders
Provides: glibc-kernheaders = 3.0-46
Provides: kernel-headers = %{version}-%{release}
Conflicts: kernel-headers < %{version}-%{release}
%description headers
This package provides the C header files that specify the interface
between the Linux kernel and userspace libraries & programs. The
header files define structures and constants that are needed when
building most standard programs. They are also required when
rebuilding the glibc package.
%endif

%if %{with_firmware}
%package firmware
Summary: Firmware files used by the Linux kernel
Group: Development/System
License: GPL+ and GPLv2+ and MIT and Redistributable, no modification permitted
Provides: kernel-firmware = %{version}-%{release}
Conflicts: kernel-firmware < %{version}-%{release}
%description firmware
This package provides the firmware files required for some devices to operate.
%endif

%if %{with_perf}
%package -n perf
Summary: Performance monitoring for the Linux kernel
Group: Development/System
License: GPLv2
Provides: perl(Perf::Trace::Context) = 0.01
Provides: perl(Perf::Trace::Core) = 0.01
Provides: perl(Perf::Trace::Util) = 0.01
%description -n perf
This package provides the perf tool and the supporting documentation.
%endif

# Disable the building of the debug package(s).
%define debug_package %{nil}

%prep
%setup -q -n %{name}-%{version} -c
%{__mv} linux-%{LKAver} linux-%{version}-%{release}.%{_target_cpu}
unzip %{SOURCE4}
pushd linux-%{version}-%{release}.%{_target_cpu} > /dev/null
cp -r ../%{AUFSver}/Documentation/filesystems Documentation/
cp -r ../%{AUFSver}/Documentation/ABI Documentation/
cp -r ../%{AUFSver}/fs/aufs fs/
cp ../%{AUFSver}/include/linux/aufs_type.h include/linux/
cp ../%{AUFSver}/include/uapi/linux/aufs_type.h include/uapi/linux/
patch -p 1 < ../%{AUFSver}/aufs3-kbuild.patch
patch -p 1 < ../%{AUFSver}/aufs3-base.patch
patch -p 1 < ../%{AUFSver}/aufs3-proc_map.patch
%{__cp} %{SOURCE1} .
%{__cp} %{SOURCE2} .
%{__cp} %{SOURCE3} .
popd > /dev/null

%build
BuildKernel() {
    Flavour=$1

    %{__make} -s mrproper

    # Select the correct flavour configuration file.
    if [ -z "${Flavour}" ]; then
      %{__cp} config-%{version}-%{_target_cpu} .config
    else
      %{__cp} config-%{version}-%{_target_cpu}-${Flavour} .config
    fi

    %define KVRFA %{version}-%{release}${Flavour}.%{_target_cpu}

    # Set the EXTRAVERSION string in the main Makefile.
    %{__perl} -p -i -e "s/^EXTRAVERSION.*/EXTRAVERSION = -%{release}${Flavour}.%{_target_cpu}/" Makefile

    %{__make} -s CONFIG_DEBUG_SECTION_MISMATCH=y ARCH=%{buildarch} V=1 %{?_smp_mflags} bzImage
    %{__make} -s CONFIG_DEBUG_SECTION_MISMATCH=y ARCH=%{buildarch} V=1 %{?_smp_mflags} modules

    # Install the results into the RPM_BUILD_ROOT directory.
    %{__mkdir_p} $RPM_BUILD_ROOT/boot
    %{__install} -m 644 .config $RPM_BUILD_ROOT/boot/config-%{KVRFA}
    %{__install} -m 644 System.map $RPM_BUILD_ROOT/boot/System.map-%{KVRFA}

%if %{with_dracut}
    # We estimate the size of the initramfs because rpm needs to take this size
    # into consideration when performing disk space calculations. (See bz #530778)
    dd if=/dev/zero of=$RPM_BUILD_ROOT/boot/initramfs-%{KVRFA}.img bs=1M count=20
%else
    dd if=/dev/zero of=$RPM_BUILD_ROOT/boot/initrd-%{KVRFA}.img bs=1M count=5
%endif

    %{__cp} arch/x86/boot/bzImage $RPM_BUILD_ROOT/boot/vmlinuz-%{KVRFA}
    %{__chmod} 755 $RPM_BUILD_ROOT/boot/vmlinuz-%{KVRFA}

    %{__mkdir_p} $RPM_BUILD_ROOT/lib/modules/%{KVRFA}
    # Override $(mod-fw) because we don't want it to install any firmware
    # We'll do that ourselves with 'make firmware_install'
    %{__make} -s ARCH=%{buildarch} INSTALL_MOD_PATH=$RPM_BUILD_ROOT modules_install KERNELRELEASE=%{KVRFA} mod-fw=

%ifarch %{vdso_arches}
    %{__make} -s ARCH=%{buildarch} INSTALL_MOD_PATH=$RPM_BUILD_ROOT vdso_install KERNELRELEASE=%{KVRFA}
    if grep '^CONFIG_XEN=y$' .config > /dev/null; then
      echo > ldconfig-kernel-ml-aufs.conf "\
# This directive teaches ldconfig to search in nosegneg subdirectories
# and cache the DSOs there with extra bit 0 set in their hwcap match
# fields.  In Xen guest kernels, the vDSO tells the dynamic linker to
# search in nosegneg subdirectories and to match this extra hwcap bit
# in the ld.so.cache file.
hwcap 1 nosegneg"
    fi
    if [ ! -s ldconfig-kernel-ml-aufs.conf ]; then
      echo > ldconfig-kernel-ml-aufs.conf "\
# Placeholder file, no vDSO hwcap entries used in this kernel."
    fi
    %{__install} -D -m 444 ldconfig-kernel-ml-aufs.conf $RPM_BUILD_ROOT/etc/ld.so.conf.d/kernel-ml-aufs-%{KVRFA}.conf
%endif

    # Save the headers/makefiles, etc, for building modules against.
    #
    # This looks scary but the end result is supposed to be:
    #
    # - all arch relevant include/ files
    # - all Makefile & Kconfig files
    # - all script/ files
    #
    %{__rm} -f $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/build
    %{__rm} -f $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/source
    %{__mkdir_p} $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/build
    pushd $RPM_BUILD_ROOT/lib/modules/%{KVRFA} > /dev/null
    %{__ln_s} build source
    popd > /dev/null
    %{__mkdir_p} $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/extra
    %{__mkdir_p} $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/updates
    %{__mkdir_p} $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/weak-updates

    # First copy everything . . .
    %{__cp} --parents `/usr/bin/find  -type f -name "Makefile*" -o -name "Kconfig*"` $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/build
    %{__cp} Module.symvers $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/build
    %{__cp} System.map $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/build
    if [ -s Module.markers ]; then
      %{__cp} Module.markers $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/build
    fi

    %{__gzip} -c9 < Module.symvers > $RPM_BUILD_ROOT/boot/symvers-%{KVRFA}.gz

    # . . . then drop all but the needed Makefiles & Kconfig files.
    %{__rm} -rf $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/build/Documentation
    %{__rm} -rf $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/build/scripts
    %{__rm} -rf $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/build/include
    %{__cp} .config $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/build
    %{__cp} -a scripts $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/build
    if [ -d arch/%{buildarch}/scripts ]; then
      %{__cp} -a arch/%{buildarch}/scripts $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/build/arch/%{_arch} || :
    fi
    if [ -f arch/%{buildarch}/*lds ]; then
      %{__cp} -a arch/%{buildarch}/*lds $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/build/arch/%{_arch}/ || :
    fi
    %{__rm} -f $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/build/scripts/*.o
    %{__rm} -f $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/build/scripts/*/*.o
    if [ -d arch/%{asmarch}/include ]; then
      %{__cp} -a --parents arch/%{asmarch}/include $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/build/
    fi
    if [ -d arch/%{asmarch}/syscalls ]; then
      %{__cp} -a --parents arch/%{asmarch}/syscalls $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/build/
    fi
    %{__mkdir_p} $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/build/include
    pushd include > /dev/null
    %{__cp} -a * $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/build/include/
    popd > /dev/null
    %{__rm} -f $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/build/include/Kbuild
    # Ensure a copy of the version.h file is in the include/linux/ directory.
    %{__cp} usr/include/linux/version.h $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/build/include/linux/
    # Copy the generated autoconf.h file to the include/linux/ directory.
    %{__cp} include/generated/autoconf.h $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/build/include/linux/
    # Copy .config to include/config/auto.conf so a "make prepare" is unnecessary.
    %{__cp} $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/build/.config $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/build/include/config/auto.conf
    # Now ensure that the Makefile, .config, auto.conf, autoconf.h and version.h files
    # all have matching timestamps so that external modules can be built.
    touch -r $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/build/Makefile $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/build/.config
    touch -r $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/build/Makefile $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/build/include/config/auto.conf
    touch -r $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/build/Makefile $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/build/include/linux/autoconf.h
    touch -r $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/build/Makefile $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/build/include/linux/version.h
    touch -r $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/build/Makefile $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/build/include/generated/autoconf.h
    touch -r $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/build/Makefile $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/build/include/generated/uapi/linux/version.h

    # Remove any 'left-over' .cmd files.
    /usr/bin/find $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/build/ -type f -name "*.cmd" | xargs --no-run-if-empty %{__rm} -f

    /usr/bin/find $RPM_BUILD_ROOT/lib/modules/%{KVRFA} -name "*.ko" -type f > modnames

    # Mark the modules executable, so that strip-to-file can strip them.
    xargs --no-run-if-empty %{__chmod} u+x < modnames

    # Generate a list of modules for block and networking.
    fgrep /drivers/ modnames | xargs --no-run-if-empty nm -upA | sed -n 's,^.*/\([^/]*\.ko\):  *U \(.*\)$,\1 \2,p' > drivers.undef

    collect_modules_list()
    {
      sed -r -n -e "s/^([^ ]+) \\.?($2)\$/\\1/p" drivers.undef | LC_ALL=C sort -u > $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/modules.$1
    }

    collect_modules_list networking \
        'register_netdev|ieee80211_register_hw|usbnet_probe|phy_driver_register'

    collect_modules_list block \
        'ata_scsi_ioctl|scsi_add_host|scsi_add_host_with_dma|blk_init_queue|register_mtd_blktrans|scsi_esp_register|scsi_register_device_handler'

    collect_modules_list drm \
        'drm_open|drm_init'

    collect_modules_list modesetting \
        'drm_crtc_init'

    # Detect any missing or incorrect license tags.
    %{__rm} -f modinfo

    while read i
    do
        echo -n "${i#$RPM_BUILD_ROOT/lib/modules/%{KVRFA}/} " >> modinfo
        /sbin/modinfo -l $i >> modinfo
    done < modnames

    egrep -v 'GPL( v2)?$|Dual BSD/GPL$|Dual MPL/GPL$|GPL and additional rights$' modinfo && exit 1

    %{__rm} -f modinfo modnames

    # Remove all the files that will be auto generated by depmod at the kernel install time.
    for i in alias alias.bin ccwmap dep dep.bin ieee1394map inputmap isapnpmap ofmap pcimap seriomap symbols symbols.bin usbmap
    do
        %{__rm} -f $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/modules.$i
    done

    # Move the development files out of the /lib/modules/ file system.
    %{__mkdir_p} $RPM_BUILD_ROOT/usr/src/kernels
    %{__mv} $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/build $RPM_BUILD_ROOT/usr/src/kernels/%{KVRFA}
    %{__ln_s} -f ../../../usr/src/kernels/%{KVRFA} $RPM_BUILD_ROOT/lib/modules/%{KVRFA}/build
}

%{__rm} -rf $RPM_BUILD_ROOT

pushd linux-%{version}-%{release}.%{_target_cpu} > /dev/null

%if %{with_std}
BuildKernel
%endif

%if %{with_nonpae}
BuildKernel NONPAE
%endif

%if %{with_doc}
# Make the HTML and man pages.
%{__make} -s -j1 htmldocs mandocs 2> /dev/null || false

# Sometimes non-world-readable files sneak into the kernel source tree.
%{__chmod} -R a=rX Documentation
/usr/bin/find Documentation -type d | xargs %{__chmod} u+w
%endif

%if %{with_perf}
%global perf_make \
  %{__make} -s %{?_smp_mflags} -C tools/perf V=1 HAVE_CPLUS_DEMANGLE=1 NO_DWARF=1 WERROR=0 prefix=%{_prefix}

%{perf_make} all
%{perf_make} man || false
%endif

popd > /dev/null

%install
pushd linux-%{version}-%{release}.%{_target_cpu} > /dev/null

%if %{with_doc}
docdir=$RPM_BUILD_ROOT%{_datadir}/doc/%{name}-doc-%{version}
man9dir=$RPM_BUILD_ROOT%{_datadir}/man/man9

# Copy the documentation over.
%{__mkdir_p} $docdir
%{__tar} -f - --exclude=man --exclude='.*' -c Documentation | %{__tar} xf - -C $docdir

# Install the man pages for the kernel API.
%{__mkdir_p} $man9dir
/usr/bin/find Documentation/DocBook/man -name "*.9.gz" -print0 \
  | xargs -0 --no-run-if-empty %{__install} -m 444 -t $man9dir
%endif

%if %{with_headers}
# Install the kernel headers.
%{__make} -s ARCH=%{buildarch} INSTALL_HDR_PATH=$RPM_BUILD_ROOT/usr headers_install

# Do a headers_check but don't die if it fails.
%{__make} -s ARCH=%{buildarch} INSTALL_HDR_PATH=$RPM_BUILD_ROOT/usr headers_check > hdrwarnings.txt || :
if grep -q exist hdrwarnings.txt; then
   sed s:^$RPM_BUILD_ROOT/usr/include/:: hdrwarnings.txt
   # Temporarily cause a build failure if there are header inconsistencies.
   # exit 1
fi

# Remove the unrequired files.
/usr/bin/find $RPM_BUILD_ROOT/usr/include \
     \( -name .install -o -name .check -o \
        -name ..install.cmd -o -name ..check.cmd \) | xargs --no-run-if-empty %{__rm} -f

# For now, glibc provides the scsi headers.
%{__rm} -rf $RPM_BUILD_ROOT/usr/include/scsi
%{__rm} -f $RPM_BUILD_ROOT/usr/include/asm*/atomic.h
%{__rm} -f $RPM_BUILD_ROOT/usr/include/asm*/io.h
%{__rm} -f $RPM_BUILD_ROOT/usr/include/asm*/irq.h
%endif

%if %{with_firmware}
# It's important NOT to have a .config file present, as it will just confuse the system.
%{__make} -s INSTALL_FW_PATH=$RPM_BUILD_ROOT/lib/firmware firmware_install
%endif

%if %{with_perf}
# perf tool binary and supporting scripts/binaries.
%{perf_make} DESTDIR=$RPM_BUILD_ROOT install

# perf man pages. (Note: implicit rpm magic compresses them later.)
%{perf_make} DESTDIR=$RPM_BUILD_ROOT install-man || false
%endif

popd > /dev/null

%clean
%{__rm} -rf $RPM_BUILD_ROOT

# Scripts section.
%if %{with_std}
%posttrans
NEWKERNARGS=""
(/sbin/grubby --info=`/sbin/grubby --default-kernel`) 2>/dev/null | grep -q crashkernel
if [ $? -ne 0 ]; then
        NEWKERNARGS="--kernel-args=\"crashkernel=auto\""
fi
%if %{with_dracut}
/sbin/new-kernel-pkg --package kernel-ml-aufs --mkinitrd --dracut --depmod --update %{version}-%{release}.%{_target_cpu} $NEWKERNARGS || exit $?
%else
/sbin/new-kernel-pkg --package kernel-ml-aufs --mkinitrd --depmod --update %{version}-%{release}.%{_target_cpu} $NEWKERNARGS || exit $?
%endif
/sbin/new-kernel-pkg --package kernel-ml-aufs --rpmposttrans %{version}-%{release}.%{_target_cpu} || exit $?
if [ -x /sbin/weak-modules ]; then
    /sbin/weak-modules --add-kernel %{version}-%{release}.%{_target_cpu} || exit $?
fi
if [ -x /sbin/ldconfig ]
then
    /sbin/ldconfig -X || exit $?
fi

%post
if [ `uname -i` == "i386" ] && [ -f /etc/sysconfig/kernel ]; then
    /bin/sed -r -i -e 's/^DEFAULTKERNEL=kernel-ml-aufs-NONPAE$/DEFAULTKERNEL=kernel-ml-aufs/' /etc/sysconfig/kernel || exit $?
fi
if grep --silent '^hwcap 0 nosegneg$' /etc/ld.so.conf.d/kernel-*.conf 2> /dev/null; then
    /bin/sed -i '/^hwcap 0 nosegneg$/ s/0/1/' /etc/ld.so.conf.d/kernel-*.conf
fi
/sbin/new-kernel-pkg --package kernel-ml-aufs --install %{version}-%{release}.%{_target_cpu} || exit $?

%preun
/sbin/new-kernel-pkg --rminitrd --rmmoddep --remove %{version}-%{release}.%{_target_cpu} || exit $?
if [ -x /sbin/weak-modules ]; then
    /sbin/weak-modules --remove-kernel %{version}-%{release}.%{_target_cpu} || exit $?
fi
if [ -x /sbin/ldconfig ]
then
    /sbin/ldconfig -X || exit $?
fi

%post devel
if [ -f /etc/sysconfig/kernel ]; then
    . /etc/sysconfig/kernel || exit $?
fi
if [ "$HARDLINK" != "no" -a -x /usr/sbin/hardlink ]; then
    pushd /usr/src/kernels/%{version}-%{release}.%{_target_cpu} > /dev/null
    /usr/bin/find . -type f | while read f; do
        hardlink -c /usr/src/kernels/*.fc*.*/$f $f
    done
    popd > /dev/null
fi
%endif

%if %{with_nonpae}
%posttrans NONPAE
NEWKERNARGS=""
(/sbin/grubby --info=`/sbin/grubby --default-kernel`) 2> /dev/null | grep -q crashkernel
if [ $? -ne 0 ]; then
    NEWKERNARGS="--kernel-args=\"crashkernel=auto\""
fi
%if %{with_dracut}
/sbin/new-kernel-pkg --package kernel-ml-aufs-NONPAE --mkinitrd --dracut --depmod --update %{version}-%{release}NONPAE.%{_target_cpu} $NEWKERNARGS || exit $?
%else
/sbin/new-kernel-pkg --package kernel-ml-aufs-NONPAE --mkinitrd --depmod --update %{version}-%{release}NONPAE.%{_target_cpu} $NEWKERNARGS || exit $?
%endif
/sbin/new-kernel-pkg --package kernel-ml-aufs-NONPAE --rpmposttrans %{version}-%{release}NONPAE.%{_target_cpu} || exit $?
if [ -x /sbin/weak-modules ]; then
    /sbin/weak-modules --add-kernel %{version}-%{release}NONPAE.%{_target_cpu} || exit $?
fi
if [ -x /sbin/ldconfig ]
then
    /sbin/ldconfig -X || exit $?
fi

%post NONPAE
if [ `uname -i` == "i386" ] && [ -f /etc/sysconfig/kernel ]; then
    /bin/sed -r -i -e 's/^DEFAULTKERNEL=kernel-ml-aufs$/DEFAULTKERNEL=kernel-ml-aufs-NONPAE/' /etc/sysconfig/kernel || exit $?
fi
/sbin/new-kernel-pkg --package kernel-ml-aufs-NONPAE --install %{version}-%{release}NONPAE.%{_target_cpu} || exit $?

%preun NONPAE
/sbin/new-kernel-pkg --rminitrd --rmmoddep --remove %{version}-%{release}NONPAE.%{_target_cpu} || exit $?
if [ -x /sbin/weak-modules ]; then
    /sbin/weak-modules --remove-kernel %{version}-%{release}NONPAE.%{_target_cpu} || exit $?
fi
if [ -x /sbin/ldconfig ]
then
    /sbin/ldconfig -X || exit $?
fi

%post NONPAE-devel
if [ -f /etc/sysconfig/kernel ]; then
    . /etc/sysconfig/kernel || exit $?
fi
if [ "$HARDLINK" != "no" -a -x /usr/sbin/hardlink ]; then
    pushd /usr/src/kernels/%{version}-%{release}NONPAE.%{_target_cpu} > /dev/null
    /usr/bin/find . -type f | while read f; do
        hardlink -c /usr/src/kernels/*.fc*.*/$f $f
    done
    popd > /dev/null
fi
%endif

# Files section.
%if %{with_std}
%files
%defattr(-,root,root)
/boot/vmlinuz-%{version}-%{release}.%{_target_cpu}
/boot/System.map-%{version}-%{release}.%{_target_cpu}
/boot/symvers-%{version}-%{release}.%{_target_cpu}.gz
/boot/config-%{version}-%{release}.%{_target_cpu}
%dir /lib/modules/%{version}-%{release}.%{_target_cpu}
/lib/modules/%{version}-%{release}.%{_target_cpu}/kernel
/lib/modules/%{version}-%{release}.%{_target_cpu}/extra
/lib/modules/%{version}-%{release}.%{_target_cpu}/build
/lib/modules/%{version}-%{release}.%{_target_cpu}/source
/lib/modules/%{version}-%{release}.%{_target_cpu}/updates
/lib/modules/%{version}-%{release}.%{_target_cpu}/weak-updates
%ifarch %{vdso_arches}
/lib/modules/%{version}-%{release}.%{_target_cpu}/vdso
/etc/ld.so.conf.d/kernel-ml-aufs-%{version}-%{release}.%{_target_cpu}.conf
%endif
/lib/modules/%{version}-%{release}.%{_target_cpu}/modules.*
%if %{with_dracut}
%ghost /boot/initramfs-%{version}-%{release}.%{_target_cpu}.img
%else
%ghost /boot/initrd-%{version}-%{release}.%{_target_cpu}.img
%endif

%files devel
%defattr(-,root,root)
%dir /usr/src/kernels
/usr/src/kernels/%{version}-%{release}.%{_target_cpu}
%endif

%if %{with_nonpae}
%files NONPAE
%defattr(-,root,root)
/boot/vmlinuz-%{version}-%{release}NONPAE.%{_target_cpu}
/boot/System.map-%{version}-%{release}NONPAE.%{_target_cpu}
/boot/symvers-%{version}-%{release}NONPAE.%{_target_cpu}.gz
/boot/config-%{version}-%{release}NONPAE.%{_target_cpu}
%dir /lib/modules/%{version}-%{release}NONPAE.%{_target_cpu}
/lib/modules/%{version}-%{release}NONPAE.%{_target_cpu}/kernel
/lib/modules/%{version}-%{release}NONPAE.%{_target_cpu}/extra
/lib/modules/%{version}-%{release}NONPAE.%{_target_cpu}/build
/lib/modules/%{version}-%{release}NONPAE.%{_target_cpu}/source
/lib/modules/%{version}-%{release}NONPAE.%{_target_cpu}/updates
/lib/modules/%{version}-%{release}NONPAE.%{_target_cpu}/weak-updates
%ifarch %{vdso_arches}
/lib/modules/%{version}-%{release}NONPAE.%{_target_cpu}/vdso
/etc/ld.so.conf.d/kernel-ml-aufs-%{version}-%{release}NONPAE.%{_target_cpu}.conf
%endif
/lib/modules/%{version}-%{release}NONPAE.%{_target_cpu}/modules.*
%if %{with_dracut}
%ghost /boot/initramfs-%{version}-%{release}NONPAE.%{_target_cpu}.img
%else
%ghost /boot/initrd-%{version}-%{release}NONPAE.%{_target_cpu}.img
%endif

%files NONPAE-devel
%defattr(-,root,root)
%dir /usr/src/kernels
/usr/src/kernels/%{version}-%{release}NONPAE.%{_target_cpu}
%endif

%if %{with_doc}
%files doc
%defattr(-,root,root)
%{_datadir}/doc/%{name}-doc-%{version}/Documentation/*
%dir %{_datadir}/doc/%{name}-doc-%{version}/Documentation
%dir %{_datadir}/doc/%{name}-doc-%{version}
%{_datadir}/man/man9/*
%endif

%if %{with_headers}
%files headers
%defattr(-,root,root)
/usr/include/*
%endif

%if %{with_firmware}
%files firmware
%defattr(-,root,root)
/lib/firmware/*
%doc linux-%{version}-%{release}.%{_target_cpu}/firmware/WHENCE
%endif

%if %{with_perf}
%files -n perf
%defattr(-,root,root)
/etc/bash_completion.d/perf
%{_bindir}/perf
%dir %{_libexecdir}/perf-core
%{_libexecdir}/perf-core/*
%{_mandir}/man[1-8]/*
%endif

%changelog
* Sun Aug 04 2013 Alan Bartlett <ajb@elrepo.org> - 3.10.5-1
- Updated with the 3.10.5 source tarball.

* Mon Jul 29 2013 Alan Bartlett <ajb@elrepo.org> - 3.10.4-1
- Updated with the 3.10.4 source tarball.

* Fri Jul 26 2013 Alan Bartlett <ajb@elrepo.org> - 3.10.3-1
- Updated with the 3.10.3 source tarball.

* Mon Jul 22 2013 Alan Bartlett <ajb@elrepo.org> - 3.10.2-1
- Updated with the 3.10.2 source tarball.

* Sun Jul 14 2013 Alan Bartlett <ajb@elrepo.org> - 3.10.1-1
- Updated with the 3.10.1 source tarball.

* Mon Jul 01 2013 Alan Bartlett <ajb@elrepo.org> - 3.10.0-1
- Updated with the 3.10 source tarball.

* Thu Jun 27 2013 Alan Bartlett <ajb@elrepo.org> - 3.9.8-1
- Updated with the 3.9.8 source tarball.

* Fri Jun 21 2013 Alan Bartlett <ajb@elrepo.org> - 3.9.7-1
- Updated with the 3.9.7 source tarball.

* Thu Jun 13 2013 Alan Bartlett <ajb@elrepo.org> - 3.9.6-1
- Updated with the 3.9.6 source tarball.

* Sat Jun 08 2013 Alan Bartlett <ajb@elrepo.org> - 3.9.5-1
- Updated with the 3.9.5 source tarball.

* Fri May 24 2013 Alan Bartlett <ajb@elrepo.org> - 3.9.4-1
- Updated with the 3.9.4 source tarball.

* Mon May 20 2013 Alan Bartlett <ajb@elrepo.org> - 3.9.3-1
- Updated with the 3.9.3 source tarball.

* Sun May 12 2013 Alan Bartlett <ajb@elrepo.org> - 3.9.2-1
- Updated with the 3.9.2 source tarball.

* Wed May 08 2013 Alan Bartlett <ajb@elrepo.org> - 3.9.1-1
- Updated with the 3.9.1 source tarball.

* Mon Apr 29 2013 Alan Bartlett <ajb@elrepo.org> - 3.9.0-1
- Updated with the 3.9 source tarball.
- Added a BR for the bc package.

* Sat Apr 27 2013 Alan Bartlett <ajb@elrepo.org> - 3.8.10-1
- Updated with the 3.8.10 source tarball.

* Fri Apr 26 2013 Alan Bartlett <ajb@elrepo.org> - 3.8.9-1
- Updated with the 3.8.9 source tarball.
- Reset CONFIG_NUMA=y for 32-bit.

* Wed Apr 17 2013 Alan Bartlett <ajb@elrepo.org> - 3.8.8-1
- Updated with the 3.8.8 source tarball.
- CONFIG_NUMA disabled for 32-bit.
- CONFIG_REGULATOR_DUMMY disabled. [https://bugzilla.kernel.org/show_bug.cgi?id=50711]

* Sat Apr 13 2013 Alan Bartlett <ajb@elrepo.org> - 3.8.7-1
- Updated with the 3.8.7 source tarball.

* Sat Apr 06 2013 Alan Bartlett <ajb@elrepo.org> - 3.8.6-1
- Updated with the 3.8.6 source tarball.

* Thu Mar 28 2013 Alan Bartlett <ajb@elrepo.org> - 3.8.5-1
- Updated with the 3.8.5 source tarball.

* Thu Mar 21 2013 Alan Bartlett <ajb@elrepo.org> - 3.8.4-1
- Updated with the 3.8.4 source tarball.

* Fri Mar 15 2013 Alan Bartlett <ajb@elrepo.org> - 3.8.3-1
- Updated with the 3.8.3 source tarball.

* Wed Mar 13 2013 Alan Bartlett <ajb@elrepo.org> - 3.8.2-2
- CONFIG_X86_X2APIC=y, CONFIG_X86_NUMACHIP disabled, CONFIG_X86_UV=y,
- CONFIG_SGI_XP=m, CONFIG_SGI_GRU=m, CONFIG_SGI_GRU_DEBUG disabled
- and CONFIG_UV_MMTIMER=m [http://elrepo.org/bugs/view.php?id=368]

* Tue Mar 04 2013 Alan Bartlett <ajb@elrepo.org> - 3.8.2-1
- Updated with the 3.8.2 source tarball.

* Tue Feb 28 2013 Alan Bartlett <ajb@elrepo.org> - 3.8.1-1
- Updated with the 3.8.1 source tarball.
- CONFIG_IPV6_SUBTREES=y and CONFIG_IPV6_MROUTE_MULTIPLE_TABLES=y [http://elrepo.org/bugs/view.php?id=354]

* Tue Feb 19 2013 Alan Bartlett <ajb@elrepo.org> - 3.8.0-1
- Updated with the 3.8 source tarball.

* Mon Feb 18 2013 Alan Bartlett <ajb@elrepo.org> - 3.7.9-1
- Updated with the 3.7.9 source tarball.

* Fri Feb 15 2013 Alan Bartlett <ajb@elrepo.org> - 3.7.8-1
- Updated with the 3.7.8 source tarball.

* Tue Feb 12 2013 Alan Bartlett <ajb@elrepo.org> - 3.7.7-1
- Updated with the 3.7.7 source tarball.
- CONFIG_MEMCG=y, CONFIG_MEMCG_SWAP=y, CONFIG_MEMCG_SWAP_ENABLE disabled,
- CONFIG_MEMCG_KMEM=y, CONFIG_MM_OWNER=y [Dag Wieers]

* Mon Feb 04 2013 Alan Bartlett <ajb@elrepo.org> - 3.7.6-1
- Updated with the 3.7.6 source tarball.

* Mon Jan 28 2013 Alan Bartlett <ajb@elrepo.org> - 3.7.5-1
- Updated with the 3.7.5 source tarball.

* Sun Jan 27 2013 Alan Bartlett <ajb@elrepo.org> - 3.7.4-2
- Correcting an issue with the configuration files. [http://elrepo.org/bugs/view.php?id=347]

* Tue Jan 22 2013 Alan Bartlett <ajb@elrepo.org> - 3.7.4-1
- Updated with the 3.7.4 source tarball.

* Sat Jan 19 2013 Alan Bartlett <ajb@elrepo.org> - 3.7.3-1
- Updated with the 3.7.3 source tarball.
- Adjusted this specification file to ensure that the arch/%%{asmarch}/syscalls/
- directory is copied to the build/ directory. [http://elrepo.org/bugs/view.php?id=344]

* Sat Jan 12 2013 Alan Bartlett <ajb@elrepo.org> - 3.7.2-1
- Updated with the 3.7.2 source tarball.

* Thu Jan 10 2013 Alan Bartlett <ajb@elrepo.org> - 3.7.1-3
- CONFIG_UFS_FS=m [http://elrepo.org/bugs/view.php?id=342]
- Further adjustments to this specification file. [http://elrepo.org/bugs/view.php?id=340]

* Mon Dec 31 2012 Alan Bartlett <ajb@elrepo.org> - 3.7.1-2
- Adjusted this specification file to ensure that a copy of the version.h file is
- present in the include/linux/ directory. [http://elrepo.org/bugs/view.php?id=340]

* Tue Dec 18 2012 Alan Bartlett <ajb@elrepo.org> - 3.7.1-1
- Updated with the 3.7.1 source tarball.
- Added WERROR=0 to the perf 'make' line to enable the 32-bit
- perf package to be built. [http://elrepo.org/bugs/view.php?id=335]

* Wed Dec 12 2012 Alan Bartlett <ajb@elrepo.org> - 3.7.0-1
- Updated with the 3.7 source tarball.

* Tue Dec 11 2012 Alan Bartlett <ajb@elrepo.org> - 3.6.10-1
- Updated with the 3.6.10 source tarball.

* Tue Dec 04 2012 Alan Bartlett <ajb@elrepo.org> - 3.6.9-1
- Updated with the 3.6.9 source tarball.

* Mon Nov 26 2012 Alan Bartlett <ajb@elrepo.org> - 3.6.8-1
- Updated with the 3.6.8 source tarball.
- CONFIG_MAC80211_DEBUGFS=y, CONFIG_ATH_DEBUG=y [http://elrepo.org/bugs/view.php?id=326]
- CONFIG_ATH9K_RATE_CONTROL disabled [http://elrepo.org/bugs/view.php?id=327]

* Sun Nov 18 2012 Alan Bartlett <ajb@elrepo.org> - 3.6.7-1
- Updated with the 3.6.7 source tarball.

* Tue Nov 06 2012 Alan Bartlett <ajb@elrepo.org> - 3.6.6-1
- Updated with the 3.6.6 source tarball.

* Wed Oct 31 2012 Alan Bartlett <ajb@elrepo.org> - 3.6.5-1
- Updated with the 3.6.5 source tarball.

* Sun Oct 28 2012 Alan Bartlett <ajb@elrepo.org> - 3.6.4-1
- Updated with the 3.6.4 source tarball.
- CONFIG_MAC80211_MESH=y [Jonathan Bither]
- CONFIG_LIBERTAS_MESH=y

* Mon Oct 22 2012 Alan Bartlett <ajb@elrepo.org> - 3.6.3-1
- Updated with the 3.6.3 source tarball.

* Sat Oct 13 2012 Alan Bartlett <ajb@elrepo.org> - 3.6.2-1
- Updated with the 3.6.2 source tarball.
- CONFIG_SCSI_SCAN_ASYNC disabled [http://elrepo.org/bugs/view.php?id=317]
- CONFIG_AIC79XX_REG_PRETTY_PRINT disabled and CONFIG_SCSI_AIC7XXX_OLD=m

* Mon Oct 08 2012 Alan Bartlett <ajb@elrepo.org> - 3.6.1-2
- Rebuilt with CONFIG_NFS_FS=m, CONFIG_NFS_V2=m, CONFIG_NFS_V3=m,
- CONFIG_NFS_V3_ACL=y, CONFIG_NFS_V4=m, CONFIG_NFS_FSCACHE=y,
- CONFIG_NFSD=m and CONFIG_NFS_ACL_SUPPORT=m [Akemi Yagi]

* Sun Oct 07 2012 Alan Bartlett <ajb@elrepo.org> - 3.6.1-1
- Updated with the 3.6.1 source tarball.

* Fri Oct 05 2012 Alan Bartlett <ajb@elrepo.org> - 3.6.0-1
- Updated with the 3.6 source tarball.

* Thu Oct 04 2012 Alan Bartlett <ajb@elrepo.org> - 3.5.5-1
- Updated with the 3.5.5 source tarball.

* Sat Sep 15 2012 Alan Bartlett <ajb@elrepo.org> - 3.5.4-1
- Updated with the 3.5.4 source tarball.

* Sun Aug 26 2012 Alan Bartlett <ajb@elrepo.org> - 3.5.3-1
- Updated with the 3.5.3 source tarball.

* Wed Aug 15 2012 Alan Bartlett <ajb@elrepo.org> - 3.5.2-1
- Updated with the 3.5.2 source tarball.

* Thu Aug 09 2012 Alan Bartlett <ajb@elrepo.org> - 3.5.1-1
- Updated with the 3.5.1 source tarball.

* Tue Jul 24 2012 Alan Bartlett <ajb@elrepo.org> - 3.5.0-2
- Rebuilt with RTLLIB support enabled. [http://elrepo.org/bugs/view.php?id=289]

* Mon Jul 23 2012 Alan Bartlett <ajb@elrepo.org> - 3.5.0-1
- Updated with the 3.5 source tarball.

* Fri Jul 20 2012 Alan Bartlett <ajb@elrepo.org> - 3.4.6-1
- Updated with the 3.4.6 source tarball.

* Tue Jul 17 2012 Alan Bartlett <ajb@elrepo.org> - 3.4.5-1
- Updated with the 3.4.5 source tarball.

* Fri Jun 22 2012 Alan Bartlett <ajb@elrepo.org> - 3.4.4-1
- Updated with the 3.4.4 source tarball.

* Mon Jun 18 2012 Alan Bartlett <ajb@elrepo.org> - 3.4.3-1
- Updated with the 3.4.3 source tarball.

* Sun Jun 10 2012 Alan Bartlett <ajb@elrepo.org> - 3.4.2-1
- Updated with the 3.4.2 source tarball.

* Mon Jun 04 2012 Alan Bartlett <ajb@elrepo.org> - 3.4.1-1
- Updated with the 3.4.1 source tarball.

* Sat May 26 2012 Alan Bartlett <ajb@elrepo.org> - 3.4.0-1
- Updated with the 3.4 source tarball.
- Added a BR for the bison package. [Akemi Yagi]
- Added a BR for the gtk2-devel package. [Akemi Yagi]

* Fri May 25 2012 Alan Bartlett <ajb@elrepo.org> - 3.3.7-2
- Rebuilt with CEPH support enabled.

* Thu May 24 2012 Alan Bartlett <ajb@elrepo.org> - 3.3.7-1
- Updated with the 3.3.7 source tarball.

* Sun May 20 2012 Alan Bartlett <ajb@elrepo.org> - 3.3.6-2
- Corrected the corrupt configuration files.

* Sun May 13 2012 Alan Bartlett <ajb@elrepo.org> - 3.3.6-1
- Updated with the 3.3.6 source tarball.

* Mon May 07 2012 Alan Bartlett <ajb@elrepo.org> - 3.3.5-1
- Updated with the 3.3.5 source tarball.

* Fri Apr 27 2012 Alan Bartlett <ajb@elrepo.org> - 3.3.4-1
- Updated with the 3.3.4 source tarball.
- Re-enabled the build of the perf packages.

* Mon Apr 23 2012 Alan Bartlett <ajb@elrepo.org> - 3.3.3-1
- Updated with the 3.3.3 source tarball.
- Disabled the build of the perf packages due to an undetermined
- bug in the sources. With the 3.3.2 sources, the perf packages will
- build. With the 3.3.3 sources, the perf packages will not build.

* Fri Apr 13 2012 Alan Bartlett <ajb@elrepo.org> - 3.3.2-1
- Updated with the 3.3.2 source tarball.

* Tue Apr 03 2012 Alan Bartlett <ajb@elrepo.org> - 3.3.1-1
- Updated with the 3.3.1 source tarball.

* Mon Mar 19 2012 Alan Bartlett <ajb@elrepo.org> - 3.3.0-1
- Updated with the 3.3 source tarball.

* Tue Mar 13 2012 Alan Bartlett <ajb@elrepo.org> - 3.2.11-1
- Updated with the 3.2.11 source tarball.

* Thu Mar 01 2012 Alan Bartlett <ajb@elrepo.org> - 3.2.9-1
- Updated with the 3.2.9 source tarball.

* Tue Feb 28 2012 Alan Bartlett <ajb@elrepo.org> - 3.2.8-1
- Updated with the 3.2.8 source tarball.

* Tue Feb 21 2012 Alan Bartlett <ajb@elrepo.org> - 3.2.7-1
- Updated with the 3.2.7 source tarball.

* Tue Feb 14 2012 Alan Bartlett <ajb@elrepo.org> - 3.2.6-1
- Updated with the 3.2.6 source tarball.

* Mon Feb 06 2012 Alan Bartlett <ajb@elrepo.org> - 3.2.5-1
- Updated with the 3.2.5 source tarball.

* Sat Feb 04 2012 Alan Bartlett <ajb@elrepo.org> - 3.2.4-1
- Updated with the 3.2.4 source tarball.

* Fri Feb 03 2012 Alan Bartlett <ajb@elrepo.org> - 3.2.3-1
- Updated with the 3.2.3 source tarball.

* Fri Jan 27 2012 Alan Bartlett <ajb@elrepo.org> - 3.2.2-1
- Updated with the 3.2.2 source tarball.
- Adjustments to Conflicts and Provides [Phil Perry]

* Mon Jan 16 2012 Alan Bartlett <ajb@elrepo.org> - 3.2.1-1
- General availability.

* Mon Jan 16 2012 Alan Bartlett <ajb@elrepo.org> - 3.2.1-0.rc2
- Release candidate 2 for the version 3.2.1 package.
- CONFIG_CRYPTO_MANAGER_DISABLE_TESTS disabled [Dag Wieers][Akemi Yagi]
- CONFIG_CRYPTO_FIPS=y [Dag Wieers][Akemi Yagi]

* Fri Jan 13 2012 Alan Bartlett <ajb@elrepo.org> - 3.2.1-0.rc1
- Updated with the 3.2.1 source tarball.
- Release candidate 1 for the version 3.2.1 package.
- CONFIG_DRM_VMWGFX=m [David Lee]
