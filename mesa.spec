%define	name			mesa
%define version			6.5.3
%define release			%mkrel 1
%define priority		500

%define eglname			mesaegl
%define glname			mesagl
%define gluname			mesaglu
%define glutname		mesaglut
%define glwname			mesaglw
%define eglmajor		1
%define glmajor			1
%define glumajor		1
%define glutmajor		3
%define glwmajor		1
%define libeglname              %mklibname %{eglname} %{eglmajor}
%define libglname		%mklibname %{glname} %{glmajor}
%define libgluname		%mklibname %{gluname} %{glumajor}
%define libglutname		%mklibname %{glutname} %{glutmajor}
%define libglwname		%mklibname %{glwname} %{glwmajor}

%define oldlibglname		%mklibname MesaGL 1
%define oldlibgluname		%mklibname MesaGLU 1
%define oldlibglutname		%mklibname Mesaglut 3

%define mesasrcdir		%{_prefix}/src/Mesa/
%define driver_dir		%{_libdir}/dri

%define enable_egl		0

#FIXME: (for 386/485) unset SSE, MMX and 3dnow flags
#FIXME: (for >=i586)  disable sse
#       SSE seems to have problem on some apps (gtulpas) for probing.
%define	dri_drivers_i386	"i810 i915tex i915 i965 mga mach64 r128 r200 r300 radeon savage sis unichrome tdfx"

%define	dri_drivers_x86_64	"mach64 i810 i915tex i915 i965 mga mach64 r128 r200 r300 radeon savage sis unichrome tdfx"
%define	dri_drivers_ppc		"mach64 r128 r200 r300 radeon tdfx"
%define	dri_drivers_ppc64	""
%define	dri_drivers_ia64	"i810 i915 i965 mga r128 r200 radeon"
%define	dri_drivers_alpha	"mga r128 r200 radeon"
%define	dri_drivers_sparc	"ffb mach64 mga radeon savage"
%define	dri_drivers		%{expand:%{dri_drivers_%{_arch}}}

Name:		%{name}
Version: 	%{version}
Release: 	%{release}
Summary:	OpenGL 1.4 compatible 3D graphics library
Group:		System/Libraries
BuildRequires:	tcl
BuildRequires:	texinfo
BuildRequires:	makedepend
BuildRequires:	libexpat-devel
BuildRequires:	x11-proto-devel >= 1.0.0
BuildRequires:	libx11-devel >= 1.0.0
BuildRequires:	libdrm-devel >= 2.0.1
BuildRequires:	libxext-devel >= 1.0.0
BuildRequires:	libxxf86vm-devel >= 1.0.0
BuildRequires:	libxmu-devel >= 1.0.0
BuildRequires:	libxi-devel >= 1.0.0
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
URL:		http://www.mesa3d.org
Source0:	http://prdownloads.sourceforge.net/mesa3d/MesaLib-%{version}.tar.bz2
Source1:	http://prdownloads.sourceforge.net/mesa3d/MesaDemos-%{version}.tar.bz2
Source2:	http://prdownloads.sourceforge.net/mesa3d/MesaGLUT-%{version}.tar.bz2
Source3:	mesa-source-file-generator
Source4:	Mesa-icons.tar.bz2
Source5:	mesa-driver-install

# DRI modules are not under /usr/X11R6 anymore
Patch2:		mesa-6.5.1-default_dri_dir.patch
# Install EGL header files and fixes other minor compilations problems when enabling EGL
Patch3:		mesa-egl_support.patch
# static inline functions are broken on some architetures
Patch6:		mesa-6.5-drop-static-inline.patch
# In some cases radeon may have 0 bits depth
Patch7:		mesa-radeon-0depthbits.patch
# Fix compilation on x86_64 
Patch9:		mesa-6.5-x86_64-fix-build.patch
# Fix linux-dri so it can be used for all archs (thanks Christiaan Welvaart)
Patch13:	Mesa-6.5.3-linux-dri-config.patch
# Disable some checks making Google Earth work on r300
Patch14:	mesa-6.5.1-google_earth_support.patch
# remove unfinished GLX_ARB_render_texture
Patch43:	mesa-6.5.2-no-ARB_render_texture.patch

License:	MIT
Requires:	%{libglname} = %{version}-%{release}
Provides:	hackMesa = %{version}
Obsoletes:	hackMesa <= %{version}
Provides:	Mesa = %{version}
Obsoletes:	Mesa < %{version}

%package	source
Summary:	Source files required for the Xorg 7.0 to enable glx support
Group:		Development/C
Requires:	%{libglname}-devel >= %{version}

%if %{enable_egl}
%package -n	%{libeglname}
Summary:	Files for Mesa (EGL libs)
Group:		System/Libraries

%package -n	%{libeglname}-devel
Summary:	Development files for Mesa (EGL libs)
Group:		Development/C
Requires:	%{name} = %{version}
Provides:	EGL-devel
%endif

%package -n	%{libglname}
Summary:	Files for Mesa (GL and GLX libs)
Group:		System/Libraries
Obsoletes:	%{oldlibglname} < 6.4 
Provides:	%{oldlibglname} = %{version}-%{release}

%package -n	%{libglname}-devel
Summary:	Development files for Mesa (OpenGL compatible 3D lib)
Group:		Development/C
Requires:	%{name} = %{version}
Provides:	lib%{glname}-devel = %{version}-%{release}
Provides:	%{glname}-devel = %{version}-%{release}
Provides:	GL-devel
Obsoletes:	%{oldlibglname}-devel < 6.4
Provides:	%{oldlibglname}-devel = %{version}-%{release}
Provides:	libMesaGL-devel = %{version}-%{release}
Provides:	MesaGL-devel = %{version}-%{release}

%package -n	%{libgluname}
Summary:	Files for Mesa (GLU libs)
Group:		System/Libraries
Obsoletes:	%{oldlibgluname} < 6.4
Provides:	%{oldlibgluname} = %{version}-%{release}

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

%package -n	%{libglutname}
Summary:	Files for Mesa (glut libs)
Group:		System/Libraries
Requires:	%{libgluname} = %{version}-%{release}
Provides:	Mesa-common = %{version}-%{release} hackMesa-common = %{version}
Obsoletes:	Mesa-common <= %{version} hackMesa-common <= %{version}
Obsoletes:	%{oldlibglutname} < 6.4
Provides:	%{oldlibglutname} = %{version}-%{release}

%package -n	%{libglutname}-devel
Summary:	Development files for glut libs
Group:		Development/C
Requires:	%{libglutname} = %{version}-%{release} %{libgluname}-devel = %{version}-%{release}
Provides:	lib%{glutname}-devel = %{version}-%{release} 
Provides:	%{glutname}-devel = %{version}-%{release} 
Obsoletes:	%{oldlibglutname}-devel < 6.4
Provides:	%{oldlibglutname}-devel = %{version}-%{release}
Provides:	libMesaGLUT-devel = %{version}-%{release}
Provides:	MesaGLUT-devel = %{version}-%{release}

%package -n	%{libglwname}
Summary:	Files for Mesa (glw libs)
Group:		System/Libraries
Provides:	Mesa-common = %{version}-%{release} hackMesa-common = %{version}
Obsoletes:	Mesa-common <= %{version} hackMesa-common <= %{version}

%package -n	%{libglwname}-devel
Summary:	Development files for glw libs
Group:		Development/C
Requires:	%{libglwname} = %{version}-%{release}
Provides:	lib%{glwname}-devel = %{version}-%{release} 
Provides:	%{glwname}-devel = %{version}-%{release} 

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
Requires:	%{libglutname}-devel = %{version}

%package	demos
Summary:	Demos for Mesa (OpenGL compatible 3D lib)
Group:		Graphics
Requires:	%{name} >= %{version}
Provides:	hackMesa-demos = %{version}
Obsoletes:	hackMesa-demos <= %{version}
Obsoletes: 	Mesa-demos < 6.4
Provides:	Mesa-demos = %{version}-%{release}

%description
Mesa is an OpenGL 1.4 compatible 3D graphics library.

%description	source
Mesa is an OpenGL 1.4 compatible 3D graphics library.

Source files required by the Xorg to enable glx support.

%description common-devel
Mesa common metapackage devel

%if %{enable_egl}
%description -n	%{libeglname}
Mesa is an OpenGL 1.4 compatible 3D graphics library.
EGL parts.

%description -n	%{libeglname}-devel
Mesa is an OpenGL 1.4 compatible 3D graphics library.
EGL development parts.
%endif

%description -n	%{libglname}
Mesa is an OpenGL 1.4 compatible 3D graphics library.
GL and GLX parts.

%description -n	%{libglname}-devel
Mesa is an OpenGL 1.4 compatible 3D graphics library.

This package contains the headers needed to compile Mesa programs.

%description -n	%{libgluname}
GLU is the OpenGL Utility Library.
It provides a number of functions upon the base OpenGL library to provide
higher-level drawing routines from the more primitive routines provided by
OpenGL.

%description -n	%{libgluname}-devel
This package contains the headers needed to compile programs with GLU.

%description -n	%{libglutname}
GLUT (OpenGL Utility Toolkit) is a addon library for OpenGL programs. It
provides them utilities to define and control windows, input from the keyboard
and the mouse, drawing some geometric primitives (cubes, spheres, ...).
GLUT can even create pop-up windows.

%description -n	%{libglutname}-devel
Mesa is an OpenGL 1.4 compatible 3D graphics library.
glut parts.

This package contains the headers needed to compile Mesa programs.

%description -n	%{libglwname}
GLw adds Motif bindings to the OpenGL "canvas" (Xt/Motif/OpenGL widget code).

%description -n	%{libglwname}-devel
Mesa is an OpenGL 1.4 compatible 3D graphics library.
GLw parts.

This package contains the headers needed to compile Mesa programs.

%description	demos
Mesa is an OpenGL 1.4 compatible 3D graphics library.

This package contains some demo programs for the Mesa library.

%prep
%setup -q -n Mesa-%{version} -b1 -b2

%patch43 -p1 -b .no-ARB_render_texture
%patch2 -p1 -b .default_dri_dir

%if %{enable_egl}
%patch3 -p1 -b .egl_support
%endif

%patch6 -p0 -b .static_inline
%patch7 -p0 -b .0depth
%if "%{_lib}" != "lib"
%patch9 -p0 -b .staticinline
%endif
%patch13 -p1 -b .linux-dri-config
%patch14 -p1 -b .google_earth_r300

pushd progs/demos && {
	for i in *.c; do 
	perl -pi -e "s|\.\./images/|%{_libdir}/mesa-demos-data/|" $i ; 
	done 
	perl -pi -e "s|isosurf.dat|%{_libdir}/mesa-demos-data/isosurf.dat|" isosurf.c 
} && popd
pushd progs/xdemos && {
	for i in *.c; do 
	perl -pi -e "s|\.\./images/|%{_libdir}/mesa-demos-data/|" $i ; 
	done 
} && popd

chmod +x %{SOURCE3} %{SOURCE5}

%build
LIB_DIR=%{_lib}
INCLUDE_DIR=$RPM_BUILD_ROOT%{_includedir}
DRI_DRIVER_DIR="%{driver_dir}"
export LIB_DIR INCLUDE_DIR DRI_DRIVER_DIR

ARCH_FLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing -DNDEBUG -DDEFAULT_DRIVER_DIR=\\\"%{driver_dir}\\\""
export ARCH_FLAGS

# (tv) parallel build is broken:
make 	MKDEP=/usr/bin/makedepend \
	USING_EGL=%{enable_egl} \
	DRI_DIRS=%{dri_drivers} \
	DRI_DRIVER_SEARCH_DIR=%{driver_dir} \
	LIB_DIR=$LIB_DIR \
	linux-dri

pushd progs/demos
%make LIB_DIR=$LIB_DIR
popd
pushd progs/xdemos
%make LIB_DIR=$LIB_DIR
popd

%install
LIB_DIR=%{_lib}
INCLUDE_DIR=$RPM_BUILD_ROOT%{_includedir}
DRI_DRIVER_DIR="%{_libdir}/dri"
export LIB_DIR INCLUDE_DIR DRI_DRIVER_DIR DRIMODULE_SRCDIR DRIMODULE_DESTDIR

rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_libdir}/mesa-demos-data
mkdir -p $RPM_BUILD_ROOT%{_includedir}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}
make INSTALL_DIR=/$RPM_BUILD_ROOT%{_prefix} \
     DRI_DRIVER_INSTALL_DIR=$RPM_BUILD_ROOT$DRI_DRIVER_DIR \
     MKDEP=%{_bindir}/makedepend \
     USING_EGL=%{enable_egl} \
     DRI_DIRS=%{dri_drivers} \
     LIB_DIR=$LIB_DIR \
     install

mkdir -p $RPM_BUILD_ROOT%{_bindir}
for i in bounce clearspd drawpix engine gamma gears glinfo glutfx isosurf morph3d \
         multiarb paltex pointblast reflect renormal \
         spectex stex3d tessdemo texcyl texobj trispd winpos; do
  cp -v progs/demos/$i $RPM_BUILD_ROOT%{_bindir}
done

for i in glthreads glxdemo glxgears glxgears_fbconfig glxcontexts glxheads \
        glxinfo glxpixmap glxpbdemo glxswapcontrol manywin offset overlay \
        pbinfo pbdemo wincopy xfont xrotfontdemo yuvrect_client; do
  cp -v progs/xdemos/$i $RPM_BUILD_ROOT%{_bindir} 
done

# (fg) So that demos at least work :)
cp -v progs/images/*rgb progs/demos/isosurf.dat $RPM_BUILD_ROOT%{_libdir}/mesa-demos-data

# (blino) hardlink libGL files in %{_libdir}/mesa
# to prevent proprietary driver installers from removing them
mkdir -p $RPM_BUILD_ROOT%{_libdir}/mesa
pushd $RPM_BUILD_ROOT%{_libdir}/mesa
for l in ../libGL.so.*; do cp -a $l .; done
popd

# (gb) use update-alternatives to manage several GL libraries/drivers
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d/GL/
cat > $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d/GL/%{libglname}.conf << EOF
# This file is knowingly empty since %{_libdir} is a standard search path
EOF
touch $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d/GL.conf

# icons for three demos examples [we lack a frontend
# to launch the demos obviously]
install -m 755 -d $RPM_BUILD_ROOT%{_miconsdir}
install -m 755 -d $RPM_BUILD_ROOT%{_iconsdir}
install -m 755 -d $RPM_BUILD_ROOT%{_liconsdir}
tar jxvf %{SOURCE4} -C $RPM_BUILD_ROOT%{_iconsdir}

# clean any .la file with still reference to tmppath.
perl -pi -e "s|\S+$RPM_BUILD_DIR\S*||g" $RPM_BUILD_ROOT/%{_libdir}/*.la

# generate mesa source files
%{SOURCE3} $RPM_BUILD_ROOT %{mesasrcdir}


%clean
rm -fr $RPM_BUILD_ROOT

%if %{enable_egl}
%post -n %{libeglname} -p /sbin/ldconfig
%postun -n %{libeglname} -p /sbin/ldconfig
%endif

%post -n %{libglname}
/usr/sbin/update-alternatives --install %{_sysconfdir}/ld.so.conf.d/GL.conf gl_conf %{_sysconfdir}/ld.so.conf.d/GL/%{libglname}.conf %{priority}
if [ ! -L %{_sysconfdir}/ld.so.conf.d/GL.conf ]; then
  /usr/sbin/update-alternatives --auto gl_conf
fi
/sbin/ldconfig

%postun -n %{libglname}
if [ ! -f %{_sysconfdir}/ld.so.conf.d/GL/%{libglname}.conf ]; then
  /usr/sbin/update-alternatives --remove gl_conf %{_sysconfdir}/ld.so.conf.d/GL/%{libglname}.conf
fi
/sbin/ldconfig

%post -n %{libgluname} -p /sbin/ldconfig 

%postun -n %{libgluname} -p /sbin/ldconfig

%post -n %{libglutname} -p /sbin/ldconfig 

%postun -n %{libglutname} -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc docs/COPYING docs/README.*
%doc docs/RELNOTES-3* docs/RELNOTES-4.* 

%files source -f mesa-source-rpm-filelist.lst
%defattr(-,root,root)
%doc docs/COPYING

%if %{enable_egl}
%files -n %{libeglname}
%defattr(-,root,root)
%{_libdir}/libegl.so.1*
%{_libdir}/libegldri.so.1*

%files -n %{libeglname}-devel
%defattr(-,root,root)
%{_libdir}/libegl.so
%{_libdir}/libegldri.so
%{_includedir}/gles/egl*.h
%endif

%files -n %{libglname}
%defattr(-,root,root)
%doc docs/COPYING
%ghost %{_sysconfdir}/ld.so.conf.d/GL.conf
%config %{_sysconfdir}/ld.so.conf.d/GL/%{libglname}.conf
%{_libdir}/libGL.so.*
%dir %{_libdir}/mesa
%{_libdir}/mesa/libGL.so.*
%ifnarch ppc64
%dir %{_libdir}/dri
%{_libdir}/dri/*
%endif
%ifarch %{ix86}
#%{_libdir}/modules/*
%endif

%files -n %{libglname}-devel
%defattr(-,root,root)
%doc docs/COPYING
%{_includedir}/GL/gl.h
%{_includedir}/GL/glext.h
%{_includedir}/GL/gl_mangle.h
%{_includedir}/GL/osmesa.h
%ifnarch ia64 alpha
%{_includedir}/GL/svgamesa.h
%endif
%{_includedir}/GL/glx.h
%{_includedir}/GL/glxext.h
%{_includedir}/GL/glx_mangle.h
%{_includedir}/GL/xmesa.h
%{_includedir}/GL/xmesa_x.h
%{_includedir}/GL/xmesa_xf86.h
%{_libdir}/libGL.so

#FIXME: check those headers
%{_includedir}/GL/mglmesa.h
%{_includedir}/GL/amesa.h
%{_includedir}/GL/dmesa.h
%{_includedir}/GL/fxmesa.h
%{_includedir}/GL/ggimesa.h
%{_includedir}/GL/glfbdev.h
%{_includedir}/GL/uglglutshapes.h
%{_includedir}/GL/uglmesa.h
%{_includedir}/GL/vms_x_fix.h
%{_includedir}/GL/wmesa.h

%files -n %{libgluname}
%defattr(-,root,root)
%doc docs/COPYING
%{_libdir}/libGLU.so.*

%files -n %{libglutname}
%defattr(-,root,root)
%doc docs/COPYING
%{_libdir}/libglut.so.*

%files -n %{libglwname}
%defattr(-,root,root)
%doc docs/COPYING
%{_libdir}/libGLw.so.*


%files -n %{libgluname}-devel
%defattr(-,root,root)
%doc docs/COPYING
%{_includedir}/GL/glu.h
%{_includedir}/GL/glu_mangle.h
%{_includedir}/GL/mesa_wgl.h
%{_libdir}/libGLU.so

%files -n %{libglutname}-devel
%defattr(-,root,root)
%doc docs/COPYING
%{_includedir}/GL/glut.h
%{_includedir}/GL/glutf90.h
%{_libdir}/libglut.so

%files common-devel
%defattr(-,root,root)

%files -n %{libglwname}-devel
%defattr(-,root,root)
%doc docs/COPYING
%{_includedir}/GL/GLwDrawA.h
%{_includedir}/GL/GLwDrawAP.h
%{_includedir}/GL/GLwMDrawA.h
%{_includedir}/GL/GLwMDrawAP.h
%{_libdir}/libGLw.so

%files demos
%defattr(-,root,root)
%doc docs/COPYING
%{_bindir}/*
%dir %{_libdir}/mesa-demos-data
%{_libdir}/mesa-demos-data/*
%{_miconsdir}/*demos*.png
%{_iconsdir}/*demos*.png
%{_liconsdir}/*demos*.png



