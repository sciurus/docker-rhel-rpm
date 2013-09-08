This repository contains the files needed to build RPMs for the dependencies of [Docker](http://docker.io) on Red Hat Enterprise Linux 6 and derivatives like CentOS and Scientific Linux. The kernel spec file is based on the [kernel-ml](http://elrepo.org/tiki/kernel-ml) package from ELRepo but adds [aufs](http://aufs.sourceforge.net/) support. The lxc spec file is copied from [Fedora](https://admin.fedoraproject.org/pkgdb/acls/name/lxc).

Before building the packages, be sure to install [fedora-packager](https://dl.fedoraproject.org/pub/epel/6/x86_64/repoview/fedora-packager.html) and add yourself to the _mock_ group.

You can build the packages with the following commands. Note that building the kernel can take a long time, maybe even hours. If you want to build these for Fedora instead of RHEL, when running mock you should replace epel-6-x86\_64 with fedora-19-x86\_64. Also, you can skip building the lxc rpm because it already exists in Fedora's repository.

    # build docker rpm
    spectool -g -C docker docker/docker.spec 
    mock -r epel-6-x86_64 --buildsrpm --spec docker/docker.spec --sources docker --resultdir output
    mock -r epel-6-x86_64 --rebuild --resultdir output output/docker-0.5.3-1.el6.src.rpm 

    # build lxc rpm
    spectool -g -C lxc lxc/lxc.spec
    mock -r epel-6-x86_64 --buildsrpm --spec lxc/lxc.spec --sources lxc --resultdir output
    mock -r epel-6-x86_64 --rebuild --resultdir output output/lxc-0.8.0-3.el6.src.rpm

    # build kernel rpm
    spectool -g -C kernel-ml-aufs kernel-ml-aufs/kernel-ml-aufs-3.10.spec
    git archive --remote git://git.code.sf.net/p/aufs/aufs3-standalone aufs3.10 > kernel-ml-aufs/aufs3-standalone.tar
    mock -r epel-6-x86_64 --buildsrpm --spec kernel-ml-aufs/kernel-ml-aufs-3.10.spec --sources kernel-ml-aufs --resultdir output
    mock -r epel-6-x86_64 --rebuild --resultdir output output/kernel-ml-aufs-3.10.5-3.el6.src.rpm

The resulting RPMs will be placed in a directory named _output_. You can install them with

    cd output
    yum localinstall --nogpgcheck kernel-ml-aufs-3.10.5-3.el6.x86_64.rpm lxc-0.8.0-3.el6.x86_64.rpm lxc-libs-0.8.0-3.el6.x86_64.rpm docker-0.5.3-1.el6.x86_64.rpm

In order to use docker, you'll need to configure the cgroup filesystem and reboot into your new kernel. Add the line 

    none                    /sys/fs/cgroup          cgroup  defaults        0 0

to _/etc/fstab_. Reboot and choose the 3.10 kernel from your GRUB menu (or edit _/boot/grub/grub.conf_ and change your default kernel).

The docker daemon should have started automatically; this can be controlled by via [initctl](http://upstart.ubuntu.com/cookbook/#initctl). To give a non-root user permission to use docker, add them to the _docker_ group.
