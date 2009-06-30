# (cg) Cheater...
%define Werror_cflags %nil

# (aco) Needed for the dri drivers
%define _disable_ld_no_undefined 1

%define git 0
%define relc 4
%define	name			mesa
%define version			7.5
%define rel			1

%define release			%mkrel %{rel}
%define src_type tar.bz2

%if %{relc}
%define release			%mkrel 0.rc%{relc}.%{rel}
%define vsuffix -rc%{relc}
%define src_type tar.gz
%endif

%if %{git}
%define release			%mkrel 0.git%{git}.%{rel}
%endif

%define makedepend		%{_bindir}/gccmakedep

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

# Architecture-independent Virtual provides:
%define libeglname_virt		lib%{eglname}
%define libglname_virt		lib%{glname}
%define libgluname_virt		lib%{gluname}
%define libglutname_virt	lib%{glutname}
%define libglwname_virt		lib%{glwname}

%define oldlibglname		%mklibname MesaGL 1
%define oldlibgluname		%mklibname MesaGLU 1
%define oldlibglutname		%mklibname Mesaglut 3

%define mesasrcdir		%{_prefix}/src/Mesa/
%define driver_dir		%{_libdir}/dri

%define enable_egl		0

#FIXME: (for 386/485) unset SSE, MMX and 3dnow flags
#FIXME: (for >=i586)  disable sse
#       SSE seems to have problem on some apps (gtulpas) for probing.
%define	dri_drivers_i386	"i810,i915,i965,mga,mach64,r128,r200,r300,radeon,savage,sis,unichrome,tdfx,swrast"
%define	dri_drivers_x86_64	%{dri_drivers_i386}
%define	dri_drivers_ppc		"mach64,r128,r200,r300,radeon,tdfx,swrast"
%define	dri_drivers_ppc64	""
%define	dri_drivers_ia64	"i810,i915,i965,mga,r128,r200,radeon,swrast"
%define	dri_drivers_alpha	"mga,r128,r200,radeon,swrast"
%define	dri_drivers_sparc	"ffb,mach64,mga,radeon,savage,swrast"
%define	dri_drivers		%{expand:%{dri_drivers_%{_arch}}}

Name:		%{name}
Version: 	%{version}
Release: 	%{release}
Summary:	OpenGL 2.1 compatible 3D graphics library
Group:		System/Libraries

BuildRequires:	tcl
BuildRequires:	texinfo
BuildRequires:	libxfixes-devel		>= 4.0.3
BuildRequires:	libxt-devel		>= 1.0.5
BuildRequires:	libxmu-devel		>= 1.0.3
BuildRequires:	libx11-devel		>= 1.1.3
BuildRequires:	libxdamage-devel	>= 1.1.1
BuildRequires:	libexpat-devel		>= 2.0.1
BuildRequires:	gccmakedep
BuildRequires:	x11-proto-devel		>= 7.3
BuildRequires:	libdrm-devel		>= 2.3.0

BuildRequires:	libxext-devel		>= 1.0.3
BuildRequires:	libxxf86vm-devel	>= 1.0.1
BuildRequires:	libxi-devel		>= 1.1.3

BuildRequires:	libglew-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
URL:		http://www.mesa3d.org
%if %{git}
# (ander) Current commit ref: mesa_7_3_rc3
Source0:	%{name}-%{git}.tar.bz2
%else
Source0:	http://prdownloads.sourceforge.net/mesa3d/MesaLib-%{version}%{vsuffix}.%{src_type}
Source1:	http://prdownloads.sourceforge.net/mesa3d/MesaDemos-%{version}%{vsuffix}.%{src_type}
Source2:	http://prdownloads.sourceforge.net/mesa3d/MesaGLUT-%{version}%{vsuffix}.%{src_type}
%endif
Source3:	make-git-snapshot.sh
Source4:	Mesa-icons.tar.bz2
Source5:	mesa-driver-install


# Instructions to setup your repository clone
# git://git.freedesktop.org/git/mesa/mesa
# git checkout master
# git branch -b mdv-7.3-pre20081220-redhat
# git am ../03??-*.patch
# git branch -b mdv-7.3-pre20081220-patches
# git am ../09??-*.patch

# Cherry picks
# git format-patch --start-number 100 mesa_7_5_rc3..mdv-7.5-cherry-picks
Patch100: 0100-i965-fix-memory-leak-in-context-renderbuffer-region-.patch

# Patches "liberated" from Fedora: 
# http://cvs.fedoraproject.org/viewvc/rpms/mesa/devel/
# git format-patch --start-number 300 mdv-7.5-cherry-picks..mdv-7.5-redhat
Patch300: 0300-RH-mesa-7.1-nukeglthread-debug-v1.1.patch
Patch301: 0301-RH-mesa-7.1-link-shared-v1.3.patch
Patch302: 0302-RH-intel-revert-vbl-v1.1.patch
Patch303: 0303-RH-mesa-7.1-disable-intel-classic-warn-v1.3.patch

# Mandriva patches
# git format-patch --start-number 900 mdv-7.5-redhat..mdv-7.5-patches
Patch900: 0900-DRI-modules-are-not-under-usr-X11R6-anymore.patch
Patch901: 0901-Fix-linux-dri-so-it-can-be-used-for-all-archs-thank.patch
Patch902: 0902-remove-unfinished-GLX_ARB_render_texture.patch
Patch903: 0903-Fix-NULL-pointer-dereference-in-viaXMesaWindowMoved.patch

License:	MIT
Requires:	%{libglname} = %{version}-%{release}
Provides:	hackMesa = %{version}
Obsoletes:	hackMesa <= %{version}
Provides:	Mesa = %{version}
Obsoletes:	Mesa < %{version}

%if %{enable_egl}
%package -n	%{libeglname}
Summary:	Files for Mesa (EGL libs)
Group:		System/Libraries
Provides:	%{libeglname_virt} = %{version}-%{release}

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
Provides:	%{libglname_virt} = %{version}-%{release}

# (anssi) Forces the upgrade of x11-server-common to happen before
# alternatives removal, which allows x11-server-common to grab the symlink.
Conflicts:	x11-server-common < 1.3.0.0-17

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
Provides:	%{libglwname_virt} = %{version}-%{release}

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
Mesa is an OpenGL 2.1 compatible 3D graphics library.

%description common-devel
Mesa common metapackage devel

%if %{enable_egl}
%description -n	%{libeglname}
Mesa is an OpenGL 2.1 compatible 3D graphics library.
EGL parts.

%description -n	%{libeglname}-devel
Mesa is an OpenGL 2.1 compatible 3D graphics library.
EGL development parts.
%endif

%description -n	%{libglname}
Mesa is an OpenGL 2.1 compatible 3D graphics library.
GL and GLX parts.

%description -n	%{libglname}-devel
Mesa is an OpenGL 2.1 compatible 3D graphics library.

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
Mesa is an OpenGL 2.1 compatible 3D graphics library.
glut parts.

This package contains the headers needed to compile Mesa programs.

%description -n	%{libglwname}
GLw adds Motif bindings to the OpenGL "canvas" (Xt/Motif/OpenGL widget code).

%description -n	%{libglwname}-devel
Mesa is an OpenGL 2.1 compatible 3D graphics library.
GLw parts.

This package contains the headers needed to compile Mesa programs.

%description	demos
Mesa is an OpenGL 2.1 compatible 3D graphics library.

This package contains some demo programs for the Mesa library.

%prep
%if %{git}
%setup -q -n mesa-%{git}
%else
%setup -q -n Mesa-%{version}%{vsuffix} -b1 -b2
%endif

%apply_patches

%if %{enable_egl}
# (cg) Need to fix this post 7.4.1 - patch not yet migrated
#patch1001 -p1
%endif

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

chmod +x %{SOURCE5}

%build
LIB_DIR=%{_lib}
INCLUDE_DIR=$RPM_BUILD_ROOT%{_includedir}
DRI_DRIVER_DIR="%{driver_dir}"
export LIB_DIR INCLUDE_DIR DRI_DRIVER_DIR

# (blino) strict aliasing is known to break some Mesa code
#   https://bugs.freedesktop.org/show_bug.cgi?id=6046
#   https://bugs.freedesktop.org/show_bug.cgi?id=9456
# (blino) tree VRP in gcc-4.2.1 triggers misrendering in Blender,
#         and hard lock with compiz (in r300_state.c)
#   https://bugs.freedesktop.org/show_bug.cgi?id=11380
#   http://gcc.gnu.org/bugzilla/show_bug.cgi?id=32544
# (tv) -O1 fixe some freeze on r200 (http://bugs.freedesktop.org/show_bug.cgi?id=10224)
ARCH_FLAGS="$RPM_OPT_FLAGS -O1 -fno-strict-aliasing -fno-tree-vrp"
export ARCH_FLAGS

%configure2_5x	--with-driver=dri \
		--with-dri-driverdir=%{driver_dir} \
		--with-dri-drivers="%{dri_drivers}" \
		--disable-gallium \
%if %{enable_egl}
		--enable-egl \
%else
		--disable-egl \
%endif
		--with-demos

%make

%install
make DESTDIR=$RPM_BUILD_ROOT install

# (cg) Needed for the link-shared patch
install -m 0755 -t $RPM_BUILD_ROOT%{_libdir} %{_lib}/libdricore.so >& /dev/null

mkdir -p $RPM_BUILD_ROOT%{_bindir}
for demo in `find progs/demos -type f -perm /a+x` `find progs/xdemos -type f -perm /a+x`; do
    cp -v $demo %{buildroot}/%{_bindir}
done

# (fg) So that demos at least work :)
mkdir -p $RPM_BUILD_ROOT%{_libdir}/mesa-demos-data
cp -v progs/images/*rgb progs/demos/isosurf.dat %{buildroot}/%{_libdir}/mesa-demos-data


# (blino) hardlink libGL files in %{_libdir}/mesa
# to prevent proprietary driver installers from removing them
mkdir -p $RPM_BUILD_ROOT%{_libdir}/mesa
pushd $RPM_BUILD_ROOT%{_libdir}/mesa
for l in ../libGL.so.*; do cp -a $l .; done
popd

# icons for three demos examples [we lack a frontend
# to launch the demos obviously]
install -m 755 -d $RPM_BUILD_ROOT%{_miconsdir}
install -m 755 -d $RPM_BUILD_ROOT%{_iconsdir}
install -m 755 -d $RPM_BUILD_ROOT%{_liconsdir}
tar jxvf %{SOURCE4} -C $RPM_BUILD_ROOT%{_iconsdir}

# clean any .la file with still reference to tmppath.
perl -pi -e "s|\S+$RPM_BUILD_DIR\S*||g" $RPM_BUILD_ROOT/%{_libdir}/*.la

%ifarch %{x86_64}
mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib/dri
%endif


%clean
rm -fr $RPM_BUILD_ROOT

%if %{enable_egl}
%if %mdkversion < 200900
%post -n %{libeglname} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{libeglname} -p /sbin/ldconfig
%endif
%endif

%if %mdkversion < 200900
%post -n %{libglname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libglname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%post -n %{libgluname} -p /sbin/ldconfig 
%endif

%if %mdkversion < 200900
%postun -n %{libgluname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%post -n %{libglutname} -p /sbin/ldconfig 
%endif

%if %mdkversion < 200900
%postun -n %{libglutname} -p /sbin/ldconfig
%endif

%files
%defattr(-,root,root)
%doc docs/COPYING docs/README.*

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
%{_libdir}/libGL.so.*
%dir %{_libdir}/mesa
%{_libdir}/mesa/libGL.so.*
%ifnarch ppc64
%dir %{_libdir}/dri
%{_libdir}/dri/*
%{_libdir}/libdricore.so
%endif
%ifarch %{x86_64}
%{_prefix}/lib/dri
%endif

%files -n %{libglname}-devel
%defattr(-,root,root)
%doc docs/COPYING
%{_includedir}/GL/gl.h
%{_includedir}/GL/glext.h
%{_includedir}/GL/gl_mangle.h
%{_includedir}/GL/osmesa.h
%{_includedir}/GL/wglext.h
%ifnarch ia64 alpha
%{_includedir}/GL/svgamesa.h
%endif
%{_includedir}/GL/glx.h
%{_includedir}/GL/glxext.h
%{_includedir}/GL/glx_mangle.h
%{_libdir}/libGL.so
%_libdir/pkgconfig/*.pc

#FIXME: check those headers
%{_includedir}/GL/mglmesa.h
%{_includedir}/GL/dmesa.h
%{_includedir}/GL/ggimesa.h
%{_includedir}/GL/glfbdev.h
%{_includedir}/GL/vms_x_fix.h
%{_includedir}/GL/wmesa.h
%dir %{_includedir}/GL/internal
%{_includedir}/GL/internal/dri_interface.h

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

