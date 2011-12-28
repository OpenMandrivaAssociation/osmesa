# (aco) Needed for the dri drivers
%define _disable_ld_no_undefined 1

%define build_plf 0
# freeglut should replace mesaglut soon
%define with_mesaglut 1

%define git		0
%define with_hardware 1
%define relc	0
%define release	1

%define src_type tar.bz2
%define vsuffix	%{expand:}

%if %{relc}
%define release	0.rc%{relc}.%{rel}
%define vsuffix -rc%{relc}
%define src_type tar.bz2
%endif

%if %{git}
%if %{relc}
%define release	0.rc%{relc}.2.git%{git}.%{rel}
%else
%define release	0.git%{git}.%{rel}
%endif
%endif

%define eglname			mesaegl
%define glname			mesagl
%define gluname			mesaglu
%define glutname		mesaglut
%define glwname			mesaglw
%define glesv1name		mesaglesv1
%define glesv2name		mesaglesv2
%define openvgname		mesaopenvg
%define glapiname		glapi

%define eglmajor		1
%define glmajor			1
%define glumajor		1
%define glutmajor		3
%define glwmajor		1
%define glesv1major		1
%define glesv2major		2
%define openvgmajor		1
%define glapimajor		0

%define libeglname		%mklibname %{eglname} %{eglmajor}
%define libglname		%mklibname %{glname} %{glmajor}
%define libgluname		%mklibname %{gluname} %{glumajor}
%define libglutname		%mklibname %{glutname} %{glutmajor}
%define libglwname		%mklibname %{glwname} %{glwmajor}
%define libglesv1name	%mklibname %{glesv1name}_ %{glesv1major}
%define libglesv2name	%mklibname %{glesv2name}_ %{glesv2major}
%define libopenvgname	%mklibname %{openvgname} %{openvgmajor}
%define libglapiname	%mklibname %{glapiname} %{glapimajor}

%define dridrivers		%mklibname dri-drivers

# Architecture-independent Virtual provides:
%define libeglname_virt		lib%{eglname}
%define libglname_virt		lib%{glname}
%define libgluname_virt		lib%{gluname}
%define libglutname_virt	lib%{glutname}
%define libglwname_virt		lib%{glwname}
%define libglesv1name_virt	lib%{glesv1name}
%define libglesv2name_virt	lib%{glesv2name}
%define libopenvgname_virt	lib%{openvgname}
%define libglapiname_virt	lib%{glapiname}

%define oldlibglname		%mklibname MesaGL 1
%define oldlibgluname		%mklibname MesaGLU 1
%define oldlibglutname		%mklibname Mesaglut 3

%define mesasrcdir		%{_prefix}/src/Mesa/
%define driver_dir		%{_libdir}/dri

#FIXME: (for 386/485) unset SSE, MMX and 3dnow flags
#FIXME: (for >=i586)  disable sse
#       SSE seems to have problem on some apps (gtulpas) for probing.
%define	dri_drivers_i386	"i810,i915,i965,mga,mach64,nouveau,r128,r200,r300,r600,radeon,savage,sis,unichrome,tdfx,swrast"
%define	dri_drivers_x86_64	%{dri_drivers_i386}
%define	dri_drivers_ppc		"mach64,r128,r200,r300,radeon,tdfx,swrast"
%define	dri_drivers_ppc64	""
%define	dri_drivers_ia64	"i810,i915,i965,mga,r128,r200,radeon,swrast"
%define	dri_drivers_alpha	"mga,r128,r200,radeon,swrast"
%define	dri_drivers_sparc	"ffb,mach64,mga,radeon,savage,swrast"
%define dri_drivers_mipsel	"mach64,mga,r128,r200,radeon,savage,tdfx"
%define dri_drivers_arm		"swrast"
%ifarch	%{arm}
%define	dri_drivers		%{expand:%{dri_drivers_arm}}
%else
%define	dri_drivers		%{expand:%{dri_drivers_%{_arch}}}
%endif

Name:		mesa
Version: 	7.11.2
Release: 	%{release}
Summary:	OpenGL 2.1 compatible 3D graphics library
Group:		System/Libraries

License:	MIT
URL:		http://www.mesa3d.org
%if %{git}
# (cg) Current commit ref: origin/mesa_7_5_branch
Source0:	%{name}-%{git}.tar.bz2
%else
Source0:	ftp://ftp.freedesktop.org/pub/mesa/%version/MesaLib-%{version}%{vsuffix}.%{src_type}
Source2:	ftp://ftp.freedesktop.org/pub/mesa/%version/MesaGLUT-%{version}%{vsuffix}.%{src_type}
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

# Patches "liberated" from Fedora:
# http://cvs.fedoraproject.org/viewvc/rpms/mesa/devel/
# git format-patch --start-number 300 mdv-cherry-picks..mdv-redhat

# Mandriva & Mageia patches
Patch900: 0900-Mips-support.patch
Patch903: 0903-Fix-NULL-pointer-dereference-in-viaXMesaWindowMoved.patch
# (anssi) fixes gwenview segfault, from git master:
Patch203: nv50-nvc0-use-screen-instead-of-context-for-flush-notifier.patch
Patch205: MesaLib-7.11.2-llvm3.0.patch

BuildRequires:	flex
BuildRequires:	bison
BuildRequires:  llvm
BuildRequires:	expat-devel		>= 2.0.1
BuildRequires:	gccmakedep
BuildRequires:	makedepend
BuildRequires:	x11-proto-devel		>= 7.3
BuildRequires:	libxml2-python
BuildRequires:	pkgconfig(libdrm)	>= 2.4.21
BuildRequires:  pkgconfig(libudev)
BuildRequires:	pkgconfig(talloc)
BuildRequires:	pkgconfig(xfixes)	>= 4.0.3
BuildRequires:	pkgconfig(xt)		>= 1.0.5
BuildRequires:	pkgconfig(xmu)		>= 1.0.3
BuildRequires:	pkgconfig(x11)		>= 1.3.3
BuildRequires:	pkgconfig(xdamage)	>= 1.1.1
BuildRequires:	pkgconfig(xext)		>= 1.1.1
BuildRequires:	pkgconfig(xxf86vm)	>= 1.1.0
BuildRequires:	pkgconfig(xi)		>= 1.3

# package mesa
Requires:	%{libglname} = %{version}-%{release}
%rename	hackMesa
%rename	Mesa

#------------------------------------------------------------------------------

%package -n	%{libglname}
Summary:	Files for Mesa (GL and GLX libs)
Group:		System/Libraries
Obsoletes:	%{oldlibglname} < 6.4
Provides:	%{oldlibglname} = %{version}-%{release}
Provides:	%{libglname_virt} = %{version}-%{release}
Requires:	%{dridrivers} >= %{version}-%{release}
%if %{build_plf}
Requires:	%mklibname txc-dxtn
%endif
# (anssi) Forces the upgrade of x11-server-common to happen before
# alternatives removal, which allows x11-server-common to grab the symlink.
Conflicts:	x11-server-common < 1.3.0.0-17

%package -n	%{dridrivers}
Summary:	Mesa DRI drivers
Group:		System/Libraries
Conflicts:	%{_lib}MesaGL1 < 7.7-5
%rename %{_lib}dri-drivers-experimental

%package -n	%{libglname}-devel
Summary:	Development files for Mesa (OpenGL compatible 3D lib)
Group:		Development/C
Requires:	%{libglname} = %{version}-%{release}
Provides:	lib%{glname}-devel = %{version}-%{release}
Provides:	%{glname}-devel = %{version}-%{release}
Provides:	GL-devel
Obsoletes:	%{oldlibglname}-devel < 6.4
Provides:	%{oldlibglname}-devel = %{version}-%{release}
Provides:	libMesaGL-devel = %{version}-%{release}
Provides:	MesaGL-devel = %{version}-%{release}
Provides:	libgl-devel

%package -n	%{libgluname}
Summary:	Files for Mesa (GLU libs)
Group:		System/Libraries
Obsoletes:	%{oldlibgluname} < 6.4
Provides:	%{oldlibgluname} = %{version}-%{release}
Provides:	%{libgluname_virt} = %{version}-%{release}

%package -n	%{libgluname}-devel
Summary:	Development files for GLU libs
Group:		Development/C
Requires:	%{libgluname} = %{version}-%{release}
Provides:	lib%{gluname}-devel = %{version}-%{release}
Provides:	%{gluname}-devel = %{version}-%{release}
Obsoletes:	%{oldlibgluname}-devel < 6.4
Provides:	%{oldlibgluname}-devel = %{version}-%{release}
Provides:	libMesaGLU-devel = %{version}-%{release}
Provides:	MesaGLU-devel = %{version}-%{release}
Provides:	libglu-devel
# pkgconfig files moved from libgl-devel:
Conflicts:	%{libglname}-devel <= 7.9-2mdv2011.0

%if %{with_mesaglut}
%package -n	%{libglutname}
Summary:	Files for Mesa (glut libs)
Group:		System/Libraries
Requires:	%{libgluname} = %{version}-%{release}
Provides:	Mesa-common = %{version}-%{release} hackMesa-common = %{version}
Obsoletes:	Mesa-common <= %{version} hackMesa-common <= %{version}
Obsoletes:	%{oldlibglutname} < 6.4
Provides:	%{oldlibglutname} = %{version}-%{release}
Provides:	%{libglutname_virt} = %{version}-%{release}

%package -n	%{libglutname}-devel
Summary:	Development files for glut libs
Group:		Development/C
Requires:	%{libglutname} = %{version}-%{release} %{libgluname}-devel = %{version}-%{release}
# (gc) /usr/lib/pkgconfig/glut.pc depends on /usr/lib/pkgconfig/{x11,xmu,xi}.pc (Requires.private) and pkg-config --list-all
# goes wild without these deps
Requires:	libx11-devel libxmu-devel libxi-devel
Provides:	lib%{glutname}-devel = %{version}-%{release}
Provides:	%{glutname}-devel = %{version}-%{release}
Obsoletes:	%{oldlibglutname}-devel < 6.4
Provides:	%{oldlibglutname}-devel = %{version}-%{release}
Provides:	libMesaGLUT-devel = %{version}-%{release}
Provides:	MesaGLUT-devel = %{version}-%{release}
Provides:	libglut-devel
# pkgconfig files moved from libgl-devel:
Conflicts:	%{libglname}-devel <= 7.9-2mdv2011.0
%endif

%package -n	%{libglwname}
Summary:	Files for Mesa (glw libs)
Group:		System/Libraries
Provides:	Mesa-common = %{version}-%{release} hackMesa-common = %{version}
Obsoletes:	Mesa-common <= %{version} hackMesa-common <= %{version}
Provides:	%{libglwname_virt} = %{version}-%{release}

%package -n	%{libglwname}-devel
Summary:	Development files for glw libs
Group:		Development/C
Requires:	%{libglwname} = %{version}-%{release}
Provides:	lib%{glwname}-devel = %{version}-%{release}
Provides:	%{glwname}-devel = %{version}-%{release}
Provides:	libglw-devel
# pkgconfig files moved from libgl-devel:
Conflicts:	%{libglname}-devel <= 7.9-2mdv2011.0

%package -n	%{libeglname}
Summary:	Files for Mesa (EGL libs)
Group:		System/Libraries
Provides:	%{libeglname_virt} = %{version}-%{release}

%package -n	%{libeglname}-devel
Summary:	Development files for Mesa (EGL libs)
Group:		Development/C
Requires:	%{libeglname} = %{version}-%{release}
Provides:	EGL-devel
Provides:	lib%{eglname}-devel
Provides:	%{eglname}-devel
Provides:	libegl-devel

%package -n %{libglapiname}
Summary:        Files for mesa (glapi libs)
Group:          System/Libraries
Provides:       %{libglapiname_virt} = %{version}-%{release}

%package -n %{libglapiname}-devel
Summary:        Development files for glapi libs
Group:          Development/C
Requires:       %{libglapiname_virt} = %{version}-%{release}
Provides:       lib%{glapiname}-devel
Provides:       %{libglapiname}-devel

%package -n %{libglesv1name}
Summary:	Files for Mesa (glesv1 libs)
Group:		System/Libraries
Provides:	%{libglesv1name_virt} = %{version}-%{release}

%package -n %{libglesv1name}-devel
Summary:	Development files for glesv1 libs
Group:		Development/C
Requires:	%{libglesv1name} = %{version}-%{release}
Provides:	lib%{glesv1name}-devel
Provides:	%{glesv1name}-devel
Provides:	libglesv1-devel

%package -n %{libglesv2name}
Summary:	Files for Mesa (glesv2 libs)
Group:		System/Libraries
Provides:	%{libglesv2name_virt} = %{version}-%{release}

%package -n %{libglesv2name}-devel
Summary:	Development files for glesv2 libs
Group:		Development/C
Requires:	%{libglesv2name} = %{version}-%{release}
Provides:	lib%{glesv2name}-devel
Provides:	%{glesv2name}-devel
Provides:	libglesv2-devel

%package -n %{libopenvgname}
Summary:	Files for MESA (OpenVG libs)
Group:		System/Libraries
Provides:	%{libopenvgname_virt} = %{version}-%{release}

%package -n %{libopenvgname}-devel
Summary:	Development files vor OpenVG libs
Group:		Development/C
Requires:	%{libopenvgname} = %{version}-%{release}
Provides:	lib%{openvgname}-devel
Provides:	%{openvgname}-devel
Provides:	libopenvg-devel

%package	common-devel
Summary:	Meta package for mesa devel
Group:		Development/C
Provides:	Mesa-common-devel = %{version}-%{release}
Provides:	hackMesa-common-devel = %{version}
Obsoletes:	Mesa-common-devel < %{version}
Obsoletes:	hackMesa-common-devel < %{version}
Requires:	%{libglname}-devel = %{version}
Requires:	%{libglwname}-devel = %{version}
Requires:	%{libgluname}-devel = %{version}
%if %{with_mesaglut}
Requires:	%{libglutname}-devel = %{version}
%else
Requires:	freeglut-devel
%endif
Requires:	%{libeglname}-devel = %{version}
Requires:	%{libglesv1name}-devel = %{version}
Requires:	%{libglesv2name}-devel = %{version}

#------------------------------------------------------------------------------

%description
Mesa is an OpenGL 2.1 compatible 3D graphics library.
%if %{build_plf}

This package is in the "tainted" section because it enables some
OpenGL extentions that are covered by software patents.
%endif

%description common-devel
Mesa common metapackage devel

%description -n %{libeglname}
Mesa is an OpenGL 2.1 compatible 3D graphics library.
EGL parts.

%description -n %{libeglname}-devel
Mesa is an OpenGL 2.1 compatible 3D graphics library.
EGL development parts.

%description -n %{libglname}
Mesa is an OpenGL 2.1 compatible 3D graphics library.
GL and GLX parts.

%description -n %{dridrivers}
Mesa is an OpenGL 2.1 compatible 3D graphics library.
DRI drivers.

%description -n %{libglname}-devel
Mesa is an OpenGL 2.1 compatible 3D graphics library.

This package contains the headers needed to compile Mesa programs.

%description -n %{libgluname}
GLU is the OpenGL Utility Library.
It provides a number of functions upon the base OpenGL library to provide
higher-level drawing routines from the more primitive routines provided by
OpenGL.

%description -n %{libgluname}-devel
This package contains the headers needed to compile programs with GLU.

%if %{with_mesaglut}
%description -n %{libglutname}
GLUT (OpenGL Utility Toolkit) is a addon library for OpenGL programs. It
provides them utilities to define and control windows, input from the keyboard
and the mouse, drawing some geometric primitives (cubes, spheres, ...).
GLUT can even create pop-up windows.

%description -n %{libglutname}-devel
Mesa is an OpenGL 2.1 compatible 3D graphics library.
glut parts.

This package contains the headers needed to compile Mesa programs.
%endif

%description -n %{libglwname}
GLw adds Motif bindings to the OpenGL "canvas" (Xt/Motif/OpenGL widget code).

%description -n %{libglwname}-devel
Mesa is an OpenGL 2.1 compatible 3D graphics library.
GLw parts.

This package contains the headers needed to compile Mesa programs.

%description -n %{libglapiname}
This packages provides the glapi shared library used by gallium.

%description -n %{libglapiname}-devel
This package contains the headers needed to compile programes against
glapi shared library.

%description -n %{libglesv1name}
OpenGL ES is a low-level, lightweight API for advanced embedded graphics using
well-defined subset profiles of OpenGL.

This package provides the OpenGL ES library version 1.

%description -n %{libglesv1name}-devel
This package contains the headers needed to compile OpenGL ES 1 programs.

%description -n %{libglesv2name}
OpenGL ES is a low-level, lightweight API for advanced embedded graphics using
well-defined subset profiles of OpenGL.

This package provides the OpenGL ES library version 2.

%description -n %{libglesv2name}-devel
This package contains the headers needed to compile OpenGL ES 2 programs.

%description -n %{libopenvgname}
OpenVG is a royalty-free, cross-platform API that provides a low-level hardware
acceleration interface for vector graphics libraries such as Flash and SVG.

%description -n %{libopenvgname}-devel
Development files for OpenVG library.

#------------------------------------------------------------------------------

%prep
%if %{git}
%setup -q -n mesa-%{git}
%else
%setup -q -n Mesa-%{version}%{vsuffix} -b2
%endif

%apply_patches
chmod +x %{SOURCE5}

%build
#%if %{git}
#./autogen.sh -v
#%endif

# need autoreconf since nouveau-updates patches configure.ac
autoreconf
%configure2_5x \
	--with-driver=dri \
	--with-dri-driverdir=%{driver_dir} \
	--with-dri-drivers="%{dri_drivers}" \
	--with-state-trackers=dri \
	--enable-shared-dricore \
	--enable-gallium-nouveau \
	--enable-egl \
	--enable-gles1 \
	--enable-gles2 \
	--enable-openvg \
	 --enable-gallium-egl \
%if %{with_hardware}
	--with-gallium-drivers=r300,r600,nouveau,swrast \
   	--enable-gallium-llvm \
%else
   	--disable-gallium-llvm \
   	--with-gallium-drivers=swrast \
%endif
%if %{build_plf}
   	--enable-texture-float \
%endif
%if %{with_mesaglut}
	--enable-glut
%else
	--disable-glut
%endif

%make

%install
rm -rf %{buildroot}
%makeinstall_std

# (blino) hardlink libGL files in %{_libdir}/mesa
# to prevent proprietary driver installers from removing them
mkdir -p %{buildroot}%{_libdir}/mesa
pushd %{buildroot}%{_libdir}/mesa
for l in ../libGL.so.*; do cp -a $l .; done
popd

%ifarch %{x86_64}
mkdir -p %{buildroot}%{_prefix}/lib/dri
%endif

%if !%{with_mesaglut}
rm -f %{buildroot}/%{_includedir}/GL/glut.h
rm -f %{buildroot}/%{_includedir}/GL/glutf90.h
%endif

# use swrastg if built (Anssi 12/2011)
[ -e %{buildroot}%{_libdir}/dri/swrastg_dri.so ] && mv %{buildroot}%{_libdir}/dri/swrast{g,}_dri.so

#------------------------------------------------------------------------------

%files
%doc docs/COPYING docs/README.*

%files -n %{dridrivers}
%ifnarch ppc64
%dir %{_libdir}/dri
%{_libdir}/dri/libdricore.so
%{_libdir}/dri/libglsl.so
%{_libdir}/dri/*_dri.so
%endif

%files -n %{libglname}
%{_libdir}/libGL.so.*
%dir %{_libdir}/mesa
%{_libdir}/mesa/libGL.so.%{glmajor}*

%files -n %{libgluname}
%{_libdir}/libGLU.so.%{glumajor}*

%if %{with_mesaglut}
%files -n %{libglutname}
%doc docs/COPYING
%{_libdir}/libglut.so.%{glutmajor}*
%endif

%files -n %{libglwname}
%{_libdir}/libGLw.so.%{glwmajor}*

%files -n %{libeglname}
%{_libdir}/libEGL.so.%{eglmajor}*
%dir %{_libdir}/egl
%{_libdir}/egl/st_GL.so
%{_libdir}/egl/egl_gallium.so

%files -n %{libglapiname}
%{_libdir}/libglapi.so.%{glapimajor}*

%files -n %{libglesv1name}
%{_libdir}/libGLESv1_CM.so.%{glesv1major}*

%files -n %{libglesv2name}
%{_libdir}/libGLESv2.so.%{glesv2major}*

%files -n %{libopenvgname}
%{_libdir}/libOpenVG.so.%{openvgmajor}*

%files -n %{libglname}-devel
%{_includedir}/GL/gl.h
%{_includedir}/GL/glext.h
%{_includedir}/GL/gl_mangle.h
%{_includedir}/GL/osmesa.h
%{_includedir}/GL/wglext.h
%{_includedir}/GL/glx.h
%{_includedir}/GL/glxext.h
%{_includedir}/GL/glx_mangle.h
%{_libdir}/libGL.so
%{_libdir}/pkgconfig/gl.pc
%{_libdir}/pkgconfig/dri.pc

#FIXME: check those headers
%{_includedir}/GL/glfbdev.h
%{_includedir}/GL/vms_x_fix.h
%{_includedir}/GL/wmesa.h
%dir %{_includedir}/GL/internal
%{_includedir}/GL/internal/dri_interface.h

%files -n %{libgluname}-devel
%{_includedir}/GL/glu.h
%{_includedir}/GL/glu_mangle.h
%{_includedir}/GL/mesa_wgl.h
%{_libdir}/libGLU.so
%{_libdir}/pkgconfig/glu.pc

%if %{with_mesaglut}
%files -n %{libglutname}-devel
%{_includedir}/GL/glut.h
%{_includedir}/GL/glutf90.h
%{_libdir}/libglut.so
%{_libdir}/pkgconfig/glut.pc
%endif

%files common-devel
# meta devel pkg

%files -n %{libglwname}-devel
%{_includedir}/GL/GLwDrawA.h
%{_includedir}/GL/GLwDrawAP.h
%{_includedir}/GL/GLwMDrawA.h
%{_includedir}/GL/GLwMDrawAP.h
%{_libdir}/libGLw.so
%{_libdir}/pkgconfig/glw.pc

%files -n %{libeglname}-devel
%{_includedir}/EGL
%{_includedir}/KHR
%{_libdir}/libEGL.so
%{_libdir}/pkgconfig/egl.pc

%files -n %{libglapiname}-devel
%{_libdir}/libglapi.so

%files -n %{libglesv1name}-devel
%{_includedir}/GLES
%{_libdir}/libGLESv1_CM.so
%{_libdir}/pkgconfig/glesv1_cm.pc

%files -n %{libglesv2name}-devel
%{_includedir}/GLES2
%{_libdir}/libGLESv2.so
%{_libdir}/pkgconfig/glesv2.pc

%files -n %{libopenvgname}-devel
%{_includedir}/VG
%{_libdir}/libOpenVG.so
%{_libdir}/pkgconfig/vg.pc

