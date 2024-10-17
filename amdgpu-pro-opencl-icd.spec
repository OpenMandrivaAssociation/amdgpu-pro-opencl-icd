# The version and release of the driver as specified by AMD.
%define basever 17.10
%define baserel 414273

# Names of the packages with libraries. These libraries are only used by
# the pre-built components of AMDGPU PRO, so the names do not follow the
# usual packaging conventions here.
%define libdrm %mklibname amdgpu-pro_drm
%define libgl %mklibname amdgpu-pro_gl
%define libvdpau %mklibname amdgpu-pro_vdpau
%define libopencl %mklibname amdgpu-pro_opencl
%define libvulkan %mklibname amdgpu-pro_vulkan

# Priority for the alternatives. Any number higher than 500 (the default
# priority the X11 server uses) would do.
%define priority 1016

# Specify the required version of video driver ABI provides by 
# x11-server-common.
%if %{mdvver} >= 201610
# X11 server 1.18.x
%define videodrv_major 20
%else
# X11 server 1.17.x
%define videodrv_major 19
%ifarch x86_64
%define xorg_aux_pack xorg-1.17-%{basever}.%{baserel}-x86_64
%else
%define xorg_aux_pack xorg-1.17-%{basever}.%{baserel}-i586
%endif
%endif

%ifarch x86_64
%define pkg_suffix _amd64
%define deb_libpath /usr/lib/x86_64-linux-gnu
%define optlibdir /opt/amdgpu-pro/lib/x86_64-linux-gnu
%define optlibdir32 /opt/amdgpu-pro/lib/i386-linux-gnu
%else
%define pkg_suffix _i386
%define deb_libpath /usr/lib/i386-linux-gnu
%define optlibdir /opt/amdgpu-pro/lib/i386-linux-gnu
%endif

%define optbindir /opt/amdgpu-pro/bin
%define optincludedir /opt/amdgpu-pro/include
%define optmandir /opt/amdgpu-pro/share/man
%define optxmoddir /opt/amdgpu-pro/lib/xorg/modules/

%define xorg_confdir %{_datadir}/X11/xorg.conf.d
%define udevdir /lib/udev/rules.d

%define patchopts -p1 --no-backup-if-mismatch --fuzz=0

# --------------------------------------------------------------------------

# Older package names, for obsoletes:
%define oldlibdri %mklibname amdgpu-pro_dri
%define oldlibdrm %mklibname amdgpu-pro_drm 2
%define oldlibdrm_amdgpu %mklibname amdgpu-pro_drm_amdgpu 1
%define oldlibegl %mklibname amdgpu-pro_egl 1
%define oldlibgbm %mklibname amdgpu-pro_gbm 1
%define oldlibgl %mklibname amdgpu-pro_gl 1
%define oldlibgles %mklibname amdgpu-pro_gles 2
%define oldlibkms %mklibname amdgpu-pro_kms 1
%define oldlibopencl %mklibname amdgpu-pro_opencl 1
%define olddevopencl %mklibname amdgpu-pro_opencl-devel -d
%define oldlibvdpau %mklibname amdgpu-pro_vdpau 1

# --------------------------------------------------------------------------

# Disable debug rpms.
%define _enable_debug_packages	%{nil}
%define debug_package		%{nil}

# --------------------------------------------------------------------------

# FIXME: fix the cases when immediate symbol resolution is not enough.
# For the present, fall back to the old symbol resolution rules for ld.
%define _disable_ld_now 1

# --------------------------------------------------------------------------

# Do not provide libGL.so.1 and the like. Unrelated packages should not
# pull in any AMDGPU PRO package when they just need libGL.so.1, etc.
%define __noautoprov '(.*)\\.so(.*)|devel\\(lib(.*)'

# Do not create requirements for the OpenCL libraries automatically, there
# are no such provides due to __noautoprov above.
# The respective packages should be listed in "Requires" explicitly.
# Besides that, some of the libraries packaged here require libtinfo as
# 'libtinfo.so.5(NCURSES_TINFO_5.0.19991023)(64bit)'. Our libtinfo, however,
# does not provide such versioned stuff, so let us simply require the
# library explicitly for now and see if things go well.
%define __noautoreq 'libOpenCL\\.so(.*)|.*NCURSES_TINFO_5.*'

# --------------------------------------------------------------------------

Summary:	AMDGPU PRO drivers provided by AMD
Name:		amdgpu-pro
Version:	%{basever}.%{baserel}
Release:	6
License:	Freeware
URL:		https://support.amd.com/en-us/kb-articles/Pages/AMDGPU-PRO-Driver-for-Linux-Release-Notes.aspx
Group:		System/Kernel and hardware
Source0:	https://www2.ati.com/drivers/linux/ubuntu/%{name}-%{basever}-%{baserel}.tar.xz
%if %{mdvver} < 201610
# ROSA releases based on rosa2014.1 have X11 server 1.17 while AMDGPU PRO
# 17.10 is build for X11 server 1.18.x for Ubuntu 16.04. So, the X11 modules
# are unlikely to work there as they are. Here are the replacements extracted
# from the packages for RHEL 7.3 that still uses X11 server 1.17.
Source1:	%{xorg_aux_pack}.tar.xz
%endif
Source100:	amdgpu-pro-opencl-icd.rpmlintrc

# Patches from ArchLinux
Patch1:		0001-disable-firmware-copy.patch
Patch2:		0002-linux-4.9-fixes.patch
Patch3:		0003-Change-seq_printf-format-for-64-bit-context.patch
Patch4:		0004-fix-warnings-for-Werror.patch

# ROSA-specific
Patch100:	0100-adapt-prebuild-to-rosa-dkms.patch

Provides:	should-restart = system

Requires:	%{name}-graphics = %{EVRD}
Requires:	%{name}-computing = %{EVRD}


%description
This package pulls in the commonly used components of AMDGPU PRO. If you are
not sure which packages to install to get AMDGPU PRO, install this one.

%files
# No files

# --------------------------------------------------------------------------

%package	computing
Summary:	OpenCL components of AMDGPU PRO
Group:		System/X11

Requires:	%{name}-core = %{EVRD}
Requires:	%{name}-clinfo = %{EVRD}
Requires:	%{name}-opencl-icd = %{EVRD}
Requires:	%{libopencl} = %{EVRD}

Obsoletes:	%{olddevopencl} < %{EVRD}

%description	computing
This package pulls in the OpenCL components of AMDGPU PRO.

%files		computing
# No files

# --------------------------------------------------------------------------

%package	graphics
Summary:	Graphics components of AMDGPU PRO
Group:		System/X11

Requires:	%{name}-core = %{EVRD}
Requires:	%{libgl} = %{EVRD}
%if %{mdvver} >= 201610
Requires:	%{libvdpau} = %{EVRD}
%endif
Requires:	%{libvulkan} = %{EVRD}
Requires:	x11-driver-video-%{name} = %{EVRD}

%description	graphics
This package pulls in the graphics components of AMDGPU PRO and instructs
the X11 server to use the AMDGPU PRO driver.

%files		graphics
%dir %{_sysconfdir}/amd
%{_sysconfdir}/amd/amdrc
%dir %{_sysconfdir}/gbm
%{_sysconfdir}/gbm/gbm.conf
%{xorg_confdir}/10-amdgpu-pro.conf

# ? Is it OK to package 10-amdgpu-pro.conf here?
# Should it be created by the appropriate graphics configuration tools
# (XFdrake and the like) instead?

# --------------------------------------------------------------------------

%ifarch %ix86

# A convenience 32-bit package. It can be used on 64-bit systems to install
# the libraries needed to run games from Steam, etc.
%package	lib32
Summary:	32-bit AMDGPU PRO libraries
Group:		System/Libraries

Requires:	%{libgl} = %{EVRD}
%if %{mdvver} >= 201610
Requires:	%{libvdpau} = %{EVRD}
%endif
Requires:	%{libvulkan} = %{EVRD}

%description	lib32
This package pulls in the 32-bit libraries needed to run 32-bit applications
using AMDGPU PRO graphics in a 64-bit system.

%files		lib32
# No files

%endif

# --------------------------------------------------------------------------

%package	core
Summary:	This package switches the GPU stack to AMDGPU PRO
Group:		System/X11

Requires:	%{libdrm} = %{EVRD}
Requires:	linux-firmware >= 20170517

%description	core
This package switches the GPU stack to AMDGPU PRO.

%files		core
%dir %{_sysconfdir}/amd
%{_sysconfdir}/amd/amdapfxx.blb
%dir %{_sysconfdir}/%{name}
%{_sysconfdir}/%{name}/ld.so.conf
%{udevdir}/91-drm_pro-modeset.rules

%posttrans	core
%{_sbindir}/update-alternatives --install \
	%{_sysconfdir}/ld.so.conf.d/GL.conf gl_conf %{_sysconfdir}/%{name}/ld.so.conf %{priority}

%{_sbindir}/update-alternatives --set gl_conf %{_sysconfdir}/%{name}/ld.so.conf

# The alternative ld.so.conf we have set above changed the paths where the
# system should look for the libraries first. Run ldconfig, just in case.
# The library packages or the meta-packages that pull them in should also
# do this for the system to know where to find libGL.so.1 and such.
/sbin/ldconfig -X

%preun	core
if [ $1 -eq 0 ]; then
	%{_sbindir}/update-alternatives --remove gl_conf %{_sysconfdir}/%{name}/ld.so.conf
fi

%postun	core
# We may have restored the original search paths for the libraries.
# Run ldconfig again to make sure the system will use them.
/sbin/ldconfig -X

# --------------------------------------------------------------------------

%package -n	dkms-%{name}
Summary:	Replacements for the in-kernel amdgpu modules
Group:		System/Kernel and hardware
Requires:	dkms
Requires(post):	dkms
Requires(preun): dkms

%description -n	dkms-%{name}
Kernel modules to manage AMD GPUs. Some of such modules, e.g., "amdgpu",
are provided by the kernel too. The modules built from this DKMS package,
may, however, have more features implemented, potentially at the cost of
stability. If the userspace components of AMDGPU PRO work OK for you with
the stock modules provided in the kernel packages, you probably do not need
this DKMS package.

%files -n	dkms-%{name}
%dir /usr/src/%{name}-%{version}-%{release}
/usr/src/%{name}-%{version}-%{release}/*
%dir %{_sysconfdir}/modprobe.d
%{_sysconfdir}/modprobe.d/blacklist-radeon.conf
%{_datadir}/dkms/modules_to_force_install/amdgpu-pro
/usr/lib/dracut/dracut.conf.d/10-amdgpu-pro.conf
%{_sysconfdir}/depmod.d/10-amdgpu-pro.conf

%post -n	dkms-%{name}
/usr/sbin/dkms --rpm_safe_upgrade add -m %{name} -v %{version}-%{release}

# Build and install the driver for all available kernels that have devel
# files, no matter how these kernels were installed (from RPMs or manually).
# Do not fail the installation of the package if the build fails for some
# kernels, this may happen during testing, etc.
for kk in /lib/modules/*; do
	kk=$(echo $kk | sed 's/^\/lib\/modules\///');
	if test -d "/lib/modules/$kk/build"; then
		/usr/sbin/dkms --rpm_safe_upgrade build -m %{name} -v %{version}-%{release} -k $kk &&
		/usr/sbin/dkms --rpm_safe_upgrade install -m %{name} -v %{version}-%{release} -k $kk || true
	else
		echo "WARNING: No development files for kernel \"$kk\"" > /dev/stderr;
	fi;
done

# It is unclear why, but it seems that dkms does not always call depmod
# when needed.
# Do it explicitly.
/sbin/depmod -a

%preun -n	dkms-%{name}
/usr/sbin/dkms --rpm_safe_upgrade remove -m %{name} -v %{version}-%{release} --all || true

%postun
# Same as in _post, just in case.
/sbin/depmod -a

# --------------------------------------------------------------------------

%package -n	%{libdrm}
Summary:	Userspace interface to kernel DRM services
Group:		System/Libraries

Obsoletes:	%{oldlibdrm} < %{EVRD}
Obsoletes:	%{oldlibdrm_amdgpu} < %{EVRD}
Obsoletes:	%{oldlibkms} < %{EVRD}
Obsoletes:	%{name}-libdrm-tools


%description -n	%{libdrm}
Userspace interface to kernel DRM services.

%files -n	%{libdrm}
%dir %{optlibdir}
%{optlibdir}/libdrm*.so*
%{optlibdir}/libkms.so*
%dir %{optbindir}
%{optbindir}/amdgpu_test
%{optbindir}/kms-steal-crtc
%{optbindir}/kms-universal-planes
%{optbindir}/kmstest
%{optbindir}/modeprint
%{optbindir}/modetest
%{optbindir}/proptest
%{optbindir}/vbltest

%post -n	%{libdrm}
# The core package installs ld.so.conf with the non-standard library paths.
# Make sure the linker knows about that.
/sbin/ldconfig -X

%postun -n	%{libdrm}
/sbin/ldconfig -X

# --------------------------------------------------------------------------

%package -n	%{libgl}
Summary:	OpenGL-related runtime libraries
Group:		System/Libraries
Requires:	%{libdrm} = %{EVRD}

Obsoletes:	%{oldlibdri} < %{EVRD}
Obsoletes:	%{oldlibegl} < %{EVRD}
Obsoletes:	%{oldlibgbm} < %{EVRD}
Obsoletes:	%{oldlibgl} < %{EVRD}
Obsoletes:	%{oldlibgles} < %{EVRD}

%description -n	%{libgl}
OpenGL-related runtime libraries.

%files -n	%{libgl}
%{deb_libpath}/dri
%{_libdir}/dri/amdgpu_dri.so
%{optlibdir}/libGL.so*
%{optlibdir}/libEGL.so*
%{optlibdir}/libGLESv2.so*
%{optlibdir}/libgbm.so*
%dir %{optlibdir}/gbm
%{optlibdir}/gbm/*.so

%post -n	%{libgl}
# See the notes for libdrm above.
/sbin/ldconfig -X

%postun -n	%{libgl}
/sbin/ldconfig -X

# --------------------------------------------------------------------------

%if %{mdvver} >= 201610

# vdpau libraries packaged here also require version GLIBCXX_3.4.21 from
# libstdc++.so.6 which is provided in rosa2016.1 and newer but not in
# rosa2014.1.

%package -n	%{libvdpau}
Summary:	AMDGPU Pro VDPAU driver
Group:		System/X11
Requires:	%{libdrm} = %{EVRD}
Requires:	%{libgl} = %{EVRD}
# See the note about libtinfo above.
Requires:	%{_lib}tinfo5

Obsoletes:	%{oldlibvdpau} < %{EVRD}


%description -n	%{libvdpau}
AMDGPU Pro VDPAU driver.

%files -n	%{libvdpau}
%dir %{optlibdir}/vdpau
%{optlibdir}/vdpau/libvdpau_amdgpu.so*
%dir %{optlibdir}/dri
%{optlibdir}/dri/radeonsi_drv_video.so
%{_libdir}/vdpau/libvdpau_amdgpu.so*

%endif

# --------------------------------------------------------------------------

%package -n	%{libvulkan}
Summary:	AMDGPU PRO Vulkan driver
Group:		System/X11

Requires:	%{name}-core = %{EVRD}
Requires:	vulkan
Provides:	%{name}-vulkan-driver = %{EVRD}

%description -n	%{libvulkan}
AMDGPU PRO Vulkan driver.

%files -n	%{libvulkan}
%dir %{_sysconfdir}/vulkan/icd.d
%{_sysconfdir}/vulkan/icd.d/amd_icd*.json
%{optlibdir}/amdvlk*.so

# --------------------------------------------------------------------------

%package -n	%{libopencl}
Summary:	AMD OpenCL ICD Loader library
Group:		System/Libraries
Requires:	%{name}-core

Obsoletes:	%{oldlibopencl} < %{EVRD}

%description -n	%{libopencl}
AMD OpenCL ICD Loader library.

%files -n	%{libopencl}
%{optlibdir}/libOpenCL.so*

%post -n	%{libopencl}
# See the notes for libdrm above.
/sbin/ldconfig -X

%postun -n	%{libopencl}
/sbin/ldconfig -X

# --------------------------------------------------------------------------

%package	opencl-icd
Summary:	Non-free AMD OpenCL ICD Loaders
Group:		System/X11

%description	opencl-icd
Non-free AMD OpenCL ICD Loaders.

%files		opencl-icd
%{_sysconfdir}/OpenCL/vendors/*.icd
%{optlibdir}/libamdocl*.so*

# --------------------------------------------------------------------------

%package	clinfo
Summary:	AMD OpenCL info utility
Group:		System/X11

Requires:	%{libopencl} = %{EVRD}
Requires:	%{name}-opencl-icd = %{EVRD}

%description	clinfo
AMD OpenCL info utility.

%files		clinfo
%{optbindir}/clinfo

# --------------------------------------------------------------------------

%package -n	x11-driver-video-%{name}
Summary:	AMDGPU PRO X11 driver
Group:		System/X11

Requires:	%{name}-core = %{EVRD}
Requires:	%{libdrm} = %{EVRD}
Requires:	%{libgl} = %{EVRD}
Requires:	xserver-abi(videodrv-%{videodrv_major})
# See the note about libtinfo above.
Requires:	%{_lib}tinfo5

Conflicts:	x11-driver-video-fglrx

# Now that AMDGPU PRO keeps its X11 modules in /opt tree, the conflict with
# the opensource driver might be unnecessary, they might be able to
# coexist.
#Conflicts:	x11-driver-video-amdgpu

%description -n	x11-driver-video-%{name}
This package contains the AMDGPU PRO X11 driver.

%files -n 	x11-driver-video-%{name}
%dir %{optxmoddir}
%{optxmoddir}/libglamoregl.so
%dir %{optxmoddir}/drivers
%{optxmoddir}/drivers/*_drv.so
%dir %{optxmoddir}/extensions
%{optxmoddir}/extensions/libglx.so
%dir %{optmandir}/man4
%{optmandir}/man4/*
%{optbindir}/amdgpu-pro-px
# libomx_mesa.so needs 'libstdc++.so.6(GLIBCXX_3.4.21)(64bit)' which is
# provided in rosa2016.1 and newer but not in rosa2014.1
%if %{mdvver} >= 201610
%dir %{optlibdir}/libomxil-bellagio0
%{optlibdir}/libomxil-bellagio0/libomx_mesa.so
%dir %{optlibdir}/gstreamer-1.0
%{optlibdir}/gstreamer-1.0/libgstomx.so
%dir %{_sysconfdir}/xdg
%{_sysconfdir}/xdg/gstomx.conf
%endif
# --------------------------------------------------------------------------

%prep
%if %{mdvver} >= 201610
%setup -qn %{name}-%{basever}-%{baserel}
%else
%setup -qn %{name}-%{basever}-%{baserel} -a 1
%endif

%build

%install

for pkg in *%{pkg_suffix}.deb *_all.deb; do
# Unpack all packages except the ones with development files.
	echo "${pkg}" | grep -qF -- '-dev_' && continue
	ar x ${pkg} && tar -C "%{buildroot}" -xf data.tar.xz
	if test ${?} -ne 0; then
		echo "ERROR: failed to unpack ${pkg}."
		exit 1
	fi
	rm -f data.tar.xz control.tar.* debian-binary
done

# Remove Debian-specific doc files.
rm -rf %{buildroot}%{_datadir}/doc

install -d -m 755 %{buildroot}%{_libdir}
mv %{buildroot}%{deb_libpath}/* %{buildroot}%{_libdir}/
rm -r %{buildroot}%{deb_libpath}/

# Some libraries from these packages (libglx.so?) may have the path to
# the DRI driver hard-coded, hence this ugly hack.
install -d -m 755 %{buildroot}%{deb_libpath}
ln -s %{_libdir}/dri %{buildroot}%{deb_libpath}/dri

# ld.so.conf
install -d -m 755 %{buildroot}%{_sysconfdir}/%{name}
echo "%{optlibdir}" >> %{buildroot}%{_sysconfdir}/%{name}/ld.so.conf
%ifarch x86_64
echo "%{optlibdir32}" >> %{buildroot}%{_sysconfdir}/%{name}/ld.so.conf
%endif

# Fixup X11 module path.
sed -ri "s,/usr/lib/xorg/modules,%{_libdir}/xorg/modules,g" %{buildroot}%{_datadir}/X11/xorg.conf.d/10-amdgpu-pro.conf

%if %{mdvver} >= 201610
# Fixup library path.
sed -ri "s,/usr/lib,%{_libdir},g" %{buildroot}%{_sysconfdir}/xdg/gstomx.conf

# Is this really needed? ArchLinux does it, not sure why.
install -d -m 755 %{buildroot}%{_libdir}/vdpau/
ln -s %{optlibdir}/vdpau/libvdpau_amdgpu.so.1.0.0 %{buildroot}%{_libdir}/vdpau/
ln -s %{optlibdir}/vdpau/libvdpau_amdgpu.so.1 %{buildroot}%{_libdir}/vdpau/
ln -s %{optlibdir}/vdpau/libvdpau_amdgpu.so %{buildroot}%{_libdir}/vdpau/

%else
# See the comments for x11-driver-video-amdgpu-pro and vdpau packages.
rm -f %{buildroot}%{_sysconfdir}/xdg/gstomx.conf
rm -rf %{buildroot}%{optlibdir}/libomxil-bellagio0
rm -rf %{buildroot}%{optlibdir}/gstreamer-1.0

rm -rf %{buildroot}%{optlibdir}/vdpau
rm -f %{buildroot}%{optlibdir}/dri/radeonsi_drv_video.so
rm -r %{buildroot}%{optlibdir}/dri
%endif

%if %{mdvver} < 201610
# Replace X11 modules with the ones built for the needed version of X11 server.
rm -rf %{buildroot}%{optxmoddir}/*
mv %{xorg_aux_pack}/modules/* %{buildroot}%{optxmoddir}/
%endif

# Needed for DKMS to operate.
mv %{buildroot}/usr/src/%{name}-%{basever}-%{baserel} %{buildroot}/usr/src/%{name}-%{version}-%{release}

# Apply patches to the sources of the kernel module, etc.
# We do not use %%patchN here because that may leave backup files which
# are not needed in the package.
pushd %{buildroot}/usr/src/%{name}-%{version}-%{release}
patch %{patchopts} < %{PATCH1}
patch %{patchopts} < %{PATCH2}
patch %{patchopts} < %{PATCH3}
patch %{patchopts} < %{PATCH4}

patch %{patchopts} < %{PATCH100}
sed -ri "s,@SOURCEDIR@,/usr/src/%{name}-%{version}-%{release},g" pre-build.sh
sed -ri "s,@BUILDDIR@,/var/lib/dkms/%{name}/%{version}-%{release}/build,g" pre-build.sh
popd

# Make sure dracut does not include the stock amdgpu kernel modules into
# initrd, that could cause problems for AMDGPU PRO.
install -d -m 755 %{buildroot}/usr/lib/dracut/dracut.conf.d/
echo "omit_drivers+=\" amdgpu amdkfd \"" > %{buildroot}/usr/lib/dracut/dracut.conf.d/10-amdgpu-pro.conf

# Make sure depmod searches /updates for the drivers first, thus giving
# priority to the kernel modules from AMDGPU PRO packages. It probably
# should do that by default but it is not always the case at the moment.
install -d -m 755 %{buildroot}%{_sysconfdir}/depmod.d/
echo "search updates built-in" > %{buildroot}%{_sysconfdir}/depmod.d/10-amdgpu-pro.conf

%changelog

* Wed Aug 23 2017 Evgenii Shatokhin <eugene.shatokhin@rosalab.ru> 17.10.414273-6
- (9a141b2) Release up


