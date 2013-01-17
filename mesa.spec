# (cg) Cheater...
%define Werror_cflags %nil

# (aco) Needed for the dri drivers
%define _disable_ld_no_undefined 1

%define build_plf 0

%define git 20130111
%define git_branch 9.1
%define with_hardware 1

%define opengl_ver 3.0

%define relc	0

# bootstrap option: Build without requiring an X server
# (which in turn requires mesa to build)
%bcond_without bootstrap
%bcond_without vdpau
%bcond_with va
%bcond_without wayland
%bcond_without egl
%bcond_without opencl

%if %{relc}
%define vsuffix -rc%{relc}
%else
%define vsuffix %nil
%endif

%define osmesamajor		8
%define libosmesaname		%mklibname osmesa %{osmesamajor}
%define osmesadevel		%mklibname osmesa -d

%define eglmajor		1
%define eglname			egl
%define libeglname		%mklibname %{eglname} %{eglmajor}
%define develegl		%mklibname %{eglname} -d

%define glmajor			1
%define glname			gl
%define libglname		%mklibname %{glname} %{glmajor}
%define develgl			%mklibname %{glname} -d

%define glesv1major		1
%define glesv1name		glesv1
%define libglesv1name		%mklibname %{glesv1name}_ %{glesv1major}
%define develglesv1		%mklibname %{glesv1name} -d

%define glesv2major		2
%define glesv2name		glesv2
%define libglesv2name		%mklibname %{glesv2name}_ %{glesv2major}
%define develglesv2		%mklibname %{glesv2name} -d

%define develglesv3		%mklibname glesv3 -d

%define openvgmajor		1
%define openvgname		openvg
%define libopenvgname		%mklibname %{openvgname} %{openvgmajor}
%define developenvg		%mklibname %{openvgname} -d

%define glapimajor		0
%define glapiname		glapi
%define libglapiname		%mklibname %{glapiname} %{glapimajor}
%define develglapi		%mklibname %{glapiname} -d

%define dridrivers		%mklibname dri-drivers

%define dricoremajor		1
%define dricorename		dricore
%define libdricorename		%mklibname %{dricorename} %{dricoremajor}
%define develdricore		%mklibname %{dricorename} -d

%define gbmmajor		1
%define gbmname			gbm
%define libgbmname		%mklibname %{gbmname} %{gbmmajor}
%define develgbm		%mklibname %{gbmname} -d

%define clmajor			1
%define clname			opencl
%define libclname		%mklibname %clname %clmajor
%define develcl			%mklibname %clname -d

%define waylandeglmajor		1
%define waylandeglname		wayland-egl
%define libwaylandeglname	%mklibname %{waylandeglname} %{waylandeglmajor}
%define develwaylandegl		%mklibname %{waylandeglname} -d

%define libvadrivers		%mklibname libva-drivers

%define mesasrcdir		%{_prefix}/src/Mesa/
%define driver_dir		%{_libdir}/dri

#FIXME: (for 386/485) unset SSE, MMX and 3dnow flags
#FIXME: (for >=i586)  disable sse
#       SSE seems to have problem on some apps (gtulpas) for probing.
%define	dri_drivers_i386	"i915,i965,nouveau,r200,radeon,swrast"
%define	dri_drivers_x86_64	%{dri_drivers_i386}
%define	dri_drivers_ppc		"r200,radeon,swrast"
%define	dri_drivers_ppc64	""
%define	dri_drivers_ia64	"i915,i965,r200,radeon,swrast"
%define	dri_drivers_alpha	"r200,radeon,swrast"
%define	dri_drivers_sparc	"ffb,radeon,swrast"
%define dri_drivers_mipsel	"r200,radeon"
%define dri_drivers_arm		"swrast"
%ifarch	%{arm}
%define	dri_drivers		%{expand:%{dri_drivers_arm}}
%else
%define	dri_drivers		%{expand:%{dri_drivers_%{_arch}}}
%endif

%define short_ver 9.1

Name:		mesa
Version:	9.1.0
%if %relc
%if %git
Release:	0.rc%relc.0.%git.1
%else
Release:	0.rc%relc.1
%endif
%else
%if %git
Release:	0.%git.1
%else
Release:	1
%endif
%endif
Summary:	OpenGL 3.0 compatible 3D graphics library
Group:		System/Libraries

License:	MIT
URL:		http://www.mesa3d.org
%if %{git}
# (cg) Current commit ref: origin/mesa_7_5_branch
Source0:	%{name}-%{git_branch}-%{git}.tar.xz
%else
Source0:	ftp://ftp.freedesktop.org/pub/mesa/%{version}/MesaLib-%{short_ver}%{vsuffix}.tar.bz2
%endif
Source3:	make-git-snapshot.sh
Source5:	mesa-driver-install

# Instructions to setup your repository clone
# git://git.freedesktop.org/git/mesa/mesa
# git checkout mesa_7_5_branch
# git branch mdv-cherry-picks
# git am ../02??-*.patch
# git branch mdv-redhat
# git am ../03??-*.patch
# git branch mdv-patches
# git am ../09??-*.patch

# In order to update to the branch via patches, issue this command:
# git format-patch --start-number 100 mesa_7_5_1..mesa_7_5_branch | sed 's/^0\([0-9]\+\)-/Patch\1: 0\1-/'

# Cherry picks
# git format-patch --start-number 200 mesa_7_5_branch..mdv-cherry-picks

# Mandriva & Mageia patches

# git format-patch --start-number 100 mesa_7_5_1..mesa_7_5_branch | sed 's/^0\([0-9]\+\)-/Patch\1: 0\1-/'
Patch201: 0201-revert-fix-glxinitializevisualconfigfromtags-handling.patch
Patch202: GLX_INDIRECT_RENDERING_mesa9_1.patch

BuildRequires:	flex
BuildRequires:	bison
BuildRequires:	llvm-devel >= 3.2
BuildRequires:	expat-devel >= 2.0.1
BuildRequires:	gccmakedep
BuildRequires:	makedepend
BuildRequires:	x11-proto-devel >= 7.3
BuildRequires:	libxml2-python
BuildRequires:	pkgconfig(libdrm) >= 2.4.21
BuildRequires:	pkgconfig(libudev) >= 186
BuildRequires:	pkgconfig(talloc)
BuildRequires:	pkgconfig(xfixes)	>= 4.0.3
BuildRequires:	pkgconfig(xt)		>= 1.0.5
BuildRequires:	pkgconfig(xmu)		>= 1.0.3
BuildRequires:	pkgconfig(x11)		>= 1.3.3
BuildRequires:	pkgconfig(xdamage)	>= 1.1.1
BuildRequires:	pkgconfig(xext)		>= 1.1.1
BuildRequires:	pkgconfig(xxf86vm)	>= 1.1.0
BuildRequires:	pkgconfig(xi)		>= 1.3
%if %{with opencl}
BuildRequires:	pkgconfig(libclc) clang-devel clang
%endif
%if ! %{with bootstrap}
BuildRequires:	pkgconfig(xorg-server)	>= 1.11.0
%endif
BuildRequires:	pkgconfig(xvmc)
%if %{with vdpau}
BuildRequires:	pkgconfig(vdpau)	>= 0.4.1
%endif
%if %{with va}
BuildRequires:	pkgconfig(libva)	>= 0.31.0
%endif
%if %{with wayland}
BuildRequires:	wayland-devel		>= 1.0.2
%endif

# package mesa
Requires:	%{libglname} = %{version}-%{release}

#------------------------------------------------------------------------------

%package -n	%{dridrivers}
Summary:	Mesa DRI drivers
Group:		System/Libraries
Conflicts:	%{_lib}MesaGL1 < 7.7-5
%rename %{_lib}dri-drivers-experimental

%package	xorg-drivers
Summary:	Mesa/Gallium XOrg drivers
Group:		System/X11

%package -n	%{libdricorename}
Summary:	Shared library for DRI drivers
Group:		System/Libraries

%package -n	%{libosmesaname}
Summary:	Mesa offscreen rendering library
Group:		System/Libraries

%package -n	%{osmesadevel}
Summary:	Development files for libosmesa
Group:		Development/C
Requires:	%{libosmesaname} = %{version}-%{release}
Provides:	osmesa-devel = %{version}-%{release}

%package -n	%{libvadrivers}
Summary:	Mesa libVA video acceleration drivers
Group:		System/Libraries

%package -n	%{libglname}
Summary:	Files for Mesa (GL and GLX libs)
Group:		System/Libraries
Provides:	libmesa%{glname} = %{version}-%{release}
Requires:	%{dridrivers} >= %{version}-%{release}
%if %{build_plf}
Requires:	%mklibname txc-dxtn
%endif
Obsoletes:	%{_lib}mesagl1 < %{version}-%{release}

%package -n	%{develgl}
Summary:	Development files for Mesa (OpenGL compatible 3D lib)
Group:		Development/C
Requires:	%{libglname} = %{version}-%{release}
Provides:	libmesa%{glname}-devel = %{version}-%{release}
Provides:	mesa%{glname}-devel = %{version}-%{release}
Provides:	GL-devel = %{version}-%{release}
Obsoletes:	%{_lib}mesagl1-devel < 8.0
Obsoletes:	%{_lib}gl1-devel < %{version}-%{release}

%if %{with egl}
%package -n	%{libeglname}
Summary:	Files for Mesa (EGL libs)
Group:		System/Libraries
Obsoletes:	%{_lib}mesaegl1 < 8.0

%package -n	%{develegl}
Summary:	Development files for Mesa (EGL libs)
Group:		Development/C
Requires:	%{libeglname} = %{version}-%{release}
Provides:	lib%{eglname}-devel = %{version}-%{release}
Obsoletes:	%{_lib}mesaegl1-devel < 8.0
Obsoletes:	%{_lib}egl1-devel < %{version}-%{release}
%endif

%package -n %{libglapiname}
Summary:	Files for mesa (glapi libs)
Group:		System/Libraries

%package -n %{develglapi}
Summary:	Development files for glapi libs
Group:		Development/C
Obsoletes:	%{_lib}glapi0-devel < %{version}-%{release}

%package -n	%{develdricore}
Summary:	Development files for DRI core
Group:		Development/C
Requires:	%{libdricorename} = %{version}-%{release}
Provides:	lib%{dricorename}-devel = %{version}-%{release}
Provides:	%{dricorename}-devel = %{version}-%{release}

%package -n %{libglesv1name}
Summary:	Files for Mesa (glesv1 libs)
Group:		System/Libraries
Obsoletes:	%{_lib}mesaglesv1_1 < 8.0

%package -n %{develglesv1}
Summary:	Development files for glesv1 libs
Group:		Development/C
Requires:	%{libglesv1name} = %{version}-%{release}
Provides:	lib%{glesv1name}-devel = %{version}-%{release}
Obsoletes:	%{_lib}mesaglesv1_1-devel < 8.0
Obsoletes:	%{_lib}glesv1_1-devel < %{version}-%{release}

%package -n %{libglesv2name}
Summary:	Files for Mesa (glesv2 libs)
Group:		System/Libraries
Obsoletes:	%{_lib}mesaglesv2_2 < 8.0

%package -n %{develglesv2}
Summary:	Development files for glesv2 libs
Group:		Development/C
Requires:	%{libglesv2name} = %{version}-%{release}
Provides:	lib%{glesv2name}-devel = %{version}-%{release}
Obsoletes:	%{_lib}mesaglesv2_2-devel < 8.0
Obsoletes:	%{_lib}glesv2_2-devel < %{version}-%{release}

%package -n %{develglesv3}
Summary:	Development files for glesv3 libs
Group:		Development/C

%package -n %{libopenvgname}
Summary:	Files for MESA (OpenVG libs)
Group:		System/Libraries
Obsoletes:	%{_lib}mesaopenvg1 < 8.0

%if %{with opencl}
%package -n %libclname
Summary:	OpenCL libs
Group:		System/Libraries
%endif

%if %{with vdpau}
%package -n	%{_lib}vdpau-driver-nouveau
Summary:	VDPAU plugin for nouveau driver
Group:		System/Libraries

%package -n	%{_lib}vdpau-driver-r300
Summary:	VDPAU plugin for r300 driver
Group:		System/Libraries

%package -n	%{_lib}vdpau-driver-r600
Summary:	VDPAU plugin for r600 driver
Group:		System/Libraries

%package -n	%{_lib}vdpau-driver-radeonsi
Summary:	VDPAU plugin for radeonsi driver
Group:		System/Libraries

%package -n	%{_lib}vdpau-driver-softpipe
Summary:	VDPAU plugin for softpipe driver
Group:		System/Libraries
%endif

%package -n %{developenvg}
Summary:	Development files for OpenVG libs
Group:		Development/C
Requires:	%{libopenvgname} = %{version}-%{release}
Provides:	lib%{openvgname}-devel = %{version}-%{release}
Obsoletes:	%{_lib}mesaopenvg1-devel < 8.0

%if %{with opencl}
%package -n %develcl
Summary:	Development files for OpenCL libs
Group:		Development/Other
Requires:	%libclname = %version-%release
Provides:	lib%libclname-devel = %version-%release
%endif

%if %{with wayland}
%package -n %{libgbmname}
Summary:	Files for Mesa (gbm libs)
Group:		System/Libraries

%package -n %{develgbm}
Summary:	Development files for Mesa (gbm libs)
Group:		Development/C
Requires:	%{libgbmname} = %{version}-%{release}
Provides:	lib%{gbmname}-devel = %{version}-%{release}
Provides:	%{gbmname}-devel = %{version}-%{release}

%package -n %{libwaylandeglname}
Summary:	Files for Mesa (Wayland EGL libs)
Group:		System/Libraries

%package -n %{develwaylandegl}
Summary:	Development files for Mesa (Wayland EGL libs)
Group:		Development/C
Requires:	%{libwaylandeglname} = %{version}-%{release}
Provides:	lib%{waylandeglname}-devel = %{version}-%{release}
Provides:	%{waylandeglname}-devel = %{version}-%{release}
%endif

%package	common-devel
Summary:	Meta package for mesa devel
Group:		Development/C
Requires:	pkgconfig(glu)
Requires:	pkgconfig(glut)
Requires:	%{develgl} = %{version}-%{release}
Requires:	%{develegl} = %{version}-%{release}
Requires:	%{develglapi} = %{version}-%{release}
Requires:	%{develglesv1} = %{version}-%{release}
Requires:	%{develglesv2} = %{version}-%{release}

#------------------------------------------------------------------------------

%description
Mesa is an OpenGL 3.0 compatible 3D graphics library.

%if %{build_plf}
This package is in the restricted repository because it enables some
OpenGL extentions that are covered by software patents.
%endif

%description -n %{dridrivers}
Mesa is an OpenGL 3.0 compatible 3D graphics library.
DRI drivers.

%description xorg-drivers
Xorg drivers from the Mesa/Gallium project

%description -n %{libosmesaname}
Mesa offscreen rendering libraries for rendering OpenGL into
application-allocated blocks of memory.

%description -n %{osmesadevel}
This package contains the headers needed to compile programs against
the Mesa offscreen rendering library.

%description -n %{libdricorename}
Mesa is an OpenGL %{opengl_ver} compatible 3D graphics library.
DRI core part.

%description -n %{libvadrivers}
Mesa is an OpenGL 3.0 compatible 3D graphics library.
libVA drivers for video acceleration

%description common-devel
Mesa common metapackage devel

%if %{with egl}
%description -n %{libeglname}
Mesa is an OpenGL 3.0 compatible 3D graphics library.
EGL parts.

%description -n %{develegl}
Mesa is an OpenGL 3.0 compatible 3D graphics library.
EGL development parts.
%endif

%description -n %{libglname}
Mesa is an OpenGL 3.0 compatible 3D graphics library.
GL and GLX parts.

%description -n %{develgl}
Mesa is an OpenGL 3.0 compatible 3D graphics library.

This package contains the headers needed to compile Mesa programs.

%description -n %{libglapiname}
This package provides the glapi shared library used by gallium.

%description -n %{develglapi}
This package contains the headers needed to compile programs against
the glapi shared library.

%description -n %{develdricore}
Mesa is an OpenGL %{opengl_ver} compatible 3D graphics library.

This package contains the headers needed to compile DRI drivers.

%description -n %{libglesv1name}
OpenGL ES is a low-level, lightweight API for advanced embedded graphics using
well-defined subset profiles of OpenGL.

This package provides the OpenGL ES library version 1.

%description -n %{develglesv1}
This package contains the headers needed to compile OpenGL ES 1 programs.

%description -n %{libglesv2name}
OpenGL ES is a low-level, lightweight API for advanced embedded graphics using
well-defined subset profiles of OpenGL.

This package provides the OpenGL ES library version 2.

%description -n %{develglesv2}
This package contains the headers needed to compile OpenGL ES 2 programs.

%description -n %{develglesv3}
This package contains the headers needed to compile OpenGL ES 3 programs.

%description -n %{libopenvgname}
OpenVG is a royalty-free, cross-platform API that provides a low-level hardware
acceleration interface for vector graphics libraries such as Flash and SVG.

%description -n %{developenvg}
Development files for OpenVG library.


%if %{with opencl}
%description -n %libclname
Open Computing Language (OpenCL) is a framework for writing programs that
execute across heterogeneous platforms consisting of central processing units
(CPUs), graphics processing units (GPUs), DSPs and other processors.

OpenCL includes a language (based on C99) for writing kernels (functions that
execute on OpenCL devices), plus application programming interfaces (APIs) that
are used to define and then control the platforms. OpenCL provides parallel
computing using task-based and data-based parallelism. OpenCL is an open
standard maintained by the non-profit technology consortium Khronos Group.
It has been adopted by Intel, Advanced Micro Devices, Nvidia, and ARM Holdings.

%description -n %develcl
Development files for the OpenCL library
%endif

%if %{with vdpau}
%description -n %{_lib}vdpau-driver-nouveau
This packages provides a VPDAU plugin to enable video acceleration
with the nouveau driver.

%description -n %{_lib}vdpau-driver-r300
This packages provides a VPDAU plugin to enable video acceleration
with the r300 driver.

%description -n %{_lib}vdpau-driver-r600
This packages provides a VPDAU plugin to enable video acceleration
with the r600 driver.

%description -n %{_lib}vdpau-driver-radeonsi
This packages provides a VPDAU plugin to enable video acceleration
with the radeonsi driver.

%description -n %{_lib}vdpau-driver-softpipe
This packages provides a VPDAU plugin to enable video acceleration
with the softpipe driver.
%endif

%if %{with wayland}
%description -n %{libgbmname}
Mesa is an OpenGL %{opengl_ver} compatible 3D graphics library.
GBM (Graphics Buffer Manager) parts.

%description -n %{develgbm}
Mesa is an OpenGL %{opengl_ver} compatible 3D graphics library.
GBM (Graphics Buffer Manager) development parts.

%description -n %{libwaylandeglname}
Mesa is an OpenGL %{opengl_ver} compatible 3D graphics library.
Wayland EGL platform parts.

%description -n %{develwaylandegl}
Mesa is an OpenGL %{opengl_ver} compatible 3D graphics library.
Wayland EGL platform development parts.
%endif

#------------------------------------------------------------------------------

%prep
%if %{git}
%setup -qn %{name}-%{git_branch}-%{git}
%else
%setup -qn Mesa-%{short_ver}%{vsuffix}
%endif

%apply_patches
chmod +x %{SOURCE5}

#sed -i 's/CFLAGS="$CFLAGS -Werror=implicit-function-declaration"//g' configure.ac
#sed -i 's/CFLAGS="$CFLAGS -Werror=missing-prototypes"//g' configure.ac

autoreconf -vfi

# Duplicate source tree for OSMesa, since building both versions out-of-tree
# would break build. - Anssi 12/2012
all=$(ls)
mkdir -p build-osmesa
cp -a $all build-osmesa

%build
# fix build - TODO: should this be fixed in llvm somehow, or maybe the library
# symlinks should be moved to %{_libdir}? -Anssi 08/2012
export LDFLAGS="-L%{_libdir}/llvm"

%configure2_5x	--enable-dri \
		--enable-glx \
		--with-dri-driverdir=%{driver_dir} \
		--with-dri-drivers="%{dri_drivers}" \
		--with-clang-libdir=%_prefix/lib \
%if %{with egl}
		--enable-egl \
%else
		--disable-egl \
%endif
%if %{with wayland}
		--with-egl-platforms=x11,wayland,drm \
		--enable-gbm \
		--enable-shared-glapi \
%endif
%if ! %{with bootstrap}
		--enable-xorg \
		--enable-xa \
%endif
		--enable-gles1 \
		--enable-gles2 \
		--enable-gles3 \
		--enable-openvg \
%if %{with opencl}
		--enable-opencl \
%endif
		--enable-gallium-egl \
		--enable-gallium-g3dvl \
		--enable-xvmc \
%if %{with vdpau}
		--enable-vdpau \
%else		
		--disable-vdpau \
%endif
%if %{with va}
		--enable-va \
%else
		--disable-va \
%endif
%if %{with_hardware}
		--with-gallium-drivers=r300,r600,radeonsi,nouveau,swrast \
		--enable-gallium-llvm \
		--enable-r600-llvm-compiler \
%else
		--disable-gallium-llvm \
		--with-gallium-drivers=swrast \
%endif
%if %{build_plf}
		--enable-texture-float  \
%endif
		# end of configure options


# Build OSMesa separately, since we want to build OSMesa without shared-glapi,
# since doing that causes OSMesa to miss the OpenGL symbols.
# See e.g. https://bugs.launchpad.net/ubuntu/+source/mesa/+bug/1066599
# -Anssi 12/2012

pushd build-osmesa
%configure2_5x \
		--enable-osmesa \
		--disable-dri \
		--disable-glx \
		--disable-egl \
		--disable-shared-glapi \
		--without-gallium-drivers
popd

%make
%make -C build-osmesa

%install
%makeinstall_std -C build-osmesa
%makeinstall_std

# FIXME: strip will likely break the hardlink
# (blino) hardlink libGL files in %{_libdir}/mesa
# to prevent proprietary driver installers from removing them
mkdir -p $RPM_BUILD_ROOT%{_libdir}/mesa
pushd $RPM_BUILD_ROOT%{_libdir}/mesa
for l in ../libGL.so.*; do cp -a $l .; done
popd

%ifarch %{x86_64}
mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib/dri
%endif

# .so files are not needed by vdpau
rm -f %{buildroot}%{_libdir}/vdpau/libvdpau_*.so

# .la files are not needed by mesa
find %{buildroot} -name '*.la' -exec rm {} \;

# use swrastg if built (Anssi 12/2011)
[ -e %{buildroot}%{_libdir}/dri/swrastg_dri.so ] && mv %{buildroot}%{_libdir}/dri/swrast{g,}_dri.so

#------------------------------------------------------------------------------


%files
%doc docs/COPYING docs/README.*
%ifnarch %{arm}
%config(noreplace) %{_sysconfdir}/drirc
%endif

%files -n %{dridrivers}
%doc docs/COPYING
%ifnarch ppc64
%dir %{_libdir}/dri
# (blino) new mesa 8.1 build system seems to use a static libglsl
#%{_libdir}/dri/libglsl.so
%{_libdir}/dri/*_dri.so
%{_libdir}/libXvMCnouveau.so.*
%{_libdir}/libXvMCr300.so.*
%{_libdir}/libXvMCr600.so.*
%{_libdir}/libXvMCsoftpipe.so.*
%dir %_libdir/gallium-pipe
%_libdir/gallium-pipe/pipe_nouveau.so
%_libdir/gallium-pipe/pipe_r300.so
%_libdir/gallium-pipe/pipe_r600.so
%_libdir/gallium-pipe/pipe_radeonsi.so
%_libdir/gallium-pipe/pipe_swrast.so
%_libdir/libllvmradeon9.1.0.so
%endif

%if ! %{with bootstrap}
%files xorg-drivers
%_libdir/xorg/modules/drivers/*.so
%endif

%files -n %{libdricorename}
%{_libdir}/libdricore%{version}.so.%{dricoremajor}
%{_libdir}/libdricore%{version}.so.%{dricoremajor}.*

%files -n %{libosmesaname}
%{_libdir}/libOSMesa.so.%{osmesamajor}*

%files -n %{osmesadevel}
%dir %{_includedir}/GL
%{_includedir}/GL/osmesa.h
%{_libdir}/libOSMesa.so
%{_libdir}/pkgconfig/osmesa.pc

%if %{with va}
%files -n %{libvadrivers}
%{_libdir}/va/lib*.so*
%endif

%files -n %{libglname}
%{_libdir}/libGL.so.*
%dir %{_libdir}/mesa
%{_libdir}/mesa/libGL.so.%{glmajor}*

%if %{with egl}
%files -n %{libeglname}
%doc docs/COPYING
%{_libdir}/libEGL.so.%{eglmajor}*
%dir %{_libdir}/egl
%if !%{with wayland}
# st_GL, built only when shared glapi is not enabled
%{_libdir}/egl/st_GL.so
%endif
%{_libdir}/egl/egl_gallium.so
%endif

%files -n %{libglapiname}
%{_libdir}/libglapi.so.%{glapimajor}*

%files -n %{libglesv1name}
%{_libdir}/libGLESv1_CM.so.%{glesv1major}*

%files -n %{libglesv2name}
%{_libdir}/libGLESv2.so.%{glesv2major}*

%files -n %{libopenvgname}
%{_libdir}/libOpenVG.so.%{openvgmajor}*

%if %{with opencl}
%files -n %libclname
%_libdir/libOpenCL.so.%{clmajor}*
%endif

%if %{with wayland}
%files -n %{libgbmname}
%{_libdir}/libgbm.so.%{gbmmajor}
%{_libdir}/libgbm.so.%{gbmmajor}.*
%{_libdir}/gbm/gbm_*.so

%files -n %{libwaylandeglname}
%{_libdir}/libwayland-egl.so.%{waylandeglmajor}
%{_libdir}/libwayland-egl.so.%{waylandeglmajor}.*
%endif

%files -n %{develgl}
%doc docs/COPYING
%dir %{_includedir}/GL
%{_includedir}/GL/gl.h
%{_includedir}/GL/glext.h
%{_includedir}/GL/gl_mangle.h
%{_includedir}/GL/wglext.h
%{_includedir}/GL/glx.h
%{_includedir}/GL/glxext.h
%{_includedir}/GL/glx_mangle.h
%{_libdir}/libGL.so
%{_libdir}/libXvMC*.so
%{_libdir}/pkgconfig/gl.pc
%{_libdir}/pkgconfig/dri.pc

#FIXME: check those headers
%{_includedir}/GL/wmesa.h
%dir %{_includedir}/GL/internal
%{_includedir}/GL/internal/dri_interface.h
#% _includedir/xa_*.h


%files common-devel
# meta devel pkg

%if %{with egl}
%files -n %{develegl}
%{_includedir}/EGL
%{_includedir}/KHR
%{_libdir}/libEGL.so
%{_libdir}/pkgconfig/egl.pc
%endif

%files -n %{develglapi}
%{_libdir}/libglapi.so

%files -n %{develdricore}
%{_libdir}/libdricore%{version}.so

#vdpau enblaed
%if %{with vdpau}
%files -n %{_lib}vdpau-driver-nouveau
%{_libdir}/vdpau/libvdpau_nouveau.so.*

%files -n %{_lib}vdpau-driver-r300
%{_libdir}/vdpau/libvdpau_r300.so.*

%files -n %{_lib}vdpau-driver-r600
%{_libdir}/vdpau/libvdpau_r600.so.*

%files -n %{_lib}vdpau-driver-radeonsi
%{_libdir}/vdpau/libvdpau_radeonsi.so.*

%files -n %{_lib}vdpau-driver-softpipe
%{_libdir}/vdpau/libvdpau_softpipe.so.*
%endif

%files -n %{develglesv1}
%{_includedir}/GLES
%{_libdir}/libGLESv1_CM.so
%{_libdir}/pkgconfig/glesv1_cm.pc

%files -n %{develglesv2}
%{_includedir}/GLES2
%{_libdir}/libGLESv2.so
%{_libdir}/pkgconfig/glesv2.pc

%files -n %{develglesv3}
%{_includedir}/GLES3

%files -n %{developenvg}
%{_includedir}/VG
%{_libdir}/libOpenVG.so
%{_libdir}/pkgconfig/vg.pc

%if %{with opencl}
%files -n %develcl
%_includedir/CL
%_libdir/libOpenCL.so
%endif

%if %{with wayland}
%files -n %{develgbm}
%{_includedir}/gbm.h
%{_libdir}/libgbm.so
%{_libdir}/pkgconfig/gbm.pc

%files -n %{develwaylandegl}
%{_libdir}/libwayland-egl.so
%{_libdir}/pkgconfig/wayland-egl.pc
%endif
