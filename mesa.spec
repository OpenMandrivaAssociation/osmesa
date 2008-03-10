%define	name			mesa
%define version			7.0.2
%define release			%mkrel 5

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

%define	dri_drivers_x86_64	"i810 i915tex i915 i965 mga mach64 r128 r200 r300 radeon savage sis unichrome tdfx"
%define	dri_drivers_ppc		"mach64 r128 r200 r300 radeon tdfx"
%define	dri_drivers_ppc64	""
%define	dri_drivers_ia64	"i810 i915 i965 mga r128 r200 radeon"
%define	dri_drivers_alpha	"mga r128 r200 radeon"
%define	dri_drivers_sparc	"ffb mach64 mga radeon savage"
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
BuildRequires:	makedepend
BuildRequires:	x11-proto-devel		>= 7.3
BuildRequires:	libdrm-devel		>= 2.3.0

BuildRequires:	libxext-devel		>= 1.0.3
BuildRequires:	libxxf86vm-devel	>= 1.0.1
BuildRequires:	libxi-devel		>= 1.1.3
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
URL:		http://www.mesa3d.org
Source0:	http://prdownloads.sourceforge.net/mesa3d/MesaLib-%{version}.tar.bz2
Source1:	http://prdownloads.sourceforge.net/mesa3d/MesaDemos-%{version}.tar.bz2
Source2:	http://prdownloads.sourceforge.net/mesa3d/MesaGLUT-%{version}.tar.bz2
Source3:	mesa-source-file-generator
Source4:	Mesa-icons.tar.bz2
Source5:	mesa-driver-install
Source6:	gl_API.xml
Source7:	EXT_framebuffer_object.xml

# git format-patch mesa_7_0_2..origin/mesa_7_0_branch
Patch1:   0001-add-glw.pc.in-to-tarball-list-remove-from-DEPEND_FI.patch
Patch2:   0002-remove-dependency-on-libGLU.patch
Patch3:   0003-DRI-memory-manager-info-fixes-dangling-link.patch
Patch4:   0004-add-pointer-to-Gallium3D-info.patch
Patch5:   0005-fix-bogus-assumption-if-ddx-has-set-up-surface-reg-f.patch
Patch6:   0006-fix-position-invariant-vertex-programs-for-sw-tnl.patch
Patch7:   0007-added-gl_dispatch_stub_772.patch
Patch8:   0008-fix-out-of-bounds-array-index-ix-1.patch
Patch9:   0009-fix-some-texture-format-assertions-etc.patch
Patch10:  0010-clamp-lambda-to-Min-MaxLod.patch
Patch11:  0011-Rename-glut_fbc.c-glut_fcb.c-cb-callback.patch
Patch12:  0012-Obsolete.patch
Patch13:  0013-bring-over-Fortran-fixes-from-master.patch
Patch14:  0014-Initial-7.0.3-relnotes.patch
Patch15:  0015-fix-z-buffer-read-write-issue-with-rv100-like-chips.patch
Patch16:  0016-Recompute-ctx-Point._Size-if-GL_POINT_SIZE_MIN-MAX.patch
Patch17:  0017-Bump-version-numbers-to-7.0.3-for-next-release.patch
Patch18:  0018-need-to-check-border-width-in-sample_linear_2d-f.patch
Patch19:  0019-Fix-parsing-of-gl_FrontLightModelProduct.sceneColor.patch
Patch20:  0020-fix-a-few-GLSL-bugs.patch
Patch21:  0021-Consolidate-texture-fetch-code-and-use-partial-deriv.patch
Patch22:  0022-i915tex-Actually-wait-for-previous-commands-to-comp.patch
Patch23:  0023-i915tex-Some-additional-blit-fixes-and-assertions.patch
Patch24:  0024-i915tex-Catch-cases-where-not-all-state-is-emitted.patch
Patch25:  0025-i915tex-Fix-some-minor-batchbuffer-errors.patch
Patch26:  0026-improve-24-bit-Z-to-32-bit-Z-conversion.patch
Patch27:  0027-set-fp-UsesKill-when-emitting-OPCODE_KIL.patch
Patch28:  0028-document-GLSL-float-f-F-suffix-bug.patch
Patch29:  0029-minor-additions-to-avoid-FAQs.patch
Patch30:  0030-use-DEFAULT_SOFTWARE_DEPTH_BITS.patch
Patch31:  0031-r200-Fix-texture-format-regression-on-big-endian-sy.patch
Patch32:  0032-make-sure-state-token-values-are-fully-initialized.patch
Patch33:  0033-Move-_mesa_load_tracked_matrices-from-TNL-module-t.patch
Patch34:  0034-cleanups-comments.patch
Patch35:  0035-New-ctx-Driver.Map-UnmapTexture-functions-for-acc.patch
Patch36:  0036-i965-use-uncompressed-instruction-to-ensure-only.patch
#Patch37:  0037-better-front-plane-clip-test.patch
Patch38:  0038-fix-broken-two-sided-stencil.patch
Patch39:  0039-fix-build-remove-ctx-_Facing-assignment.patch
Patch40:  0040-i915tex-Fix-up-state-changes-for-i8xx.patch
Patch41:  0041-added-missing-quote-char.patch
Patch42:  0042-fix-two-sided-stencil.patch
#Patch43:  0043-Fix-the-library-name-in-glw.pc.patch
Patch44:  0044-fix-DD_TRI_LIGHT_TWOSIDE-bug-13368.patch
Patch45:  0045-fix-two-side-lighting-bug-crash.patch
Patch46:  0046-Use-Bsymbolic-for-linking-all-shared-objects.patch
Patch47:  0047-Fix-gl_FrontFacing-compilation-problem.patch
Patch48:  0048-fix-span-facing-computation-and-gl_FrontFacing-init.patch
Patch49:  0049-fix-gl_FrontFacing.patch
Patch50:  0050-configs-Fix-linking-with-static-libGL-and-as-need.patch
Patch51:  0051-fix-polygon-cull-regression.patch
Patch52:  0052-i915tex-Fix-issues-with-glDrawBuffer-GL_NONE.patch
Patch53:  0053-fix-NEED_SECONDARY_COLOR-for-vert-frag-progs.patch
Patch54:  0054-simplify-update-two-side-lighting-test-follow-on-to.patch
Patch55:  0055-Remove-I-TOP-src-mesa-transform.patch
Patch56:  0056-i965-restore-the-flag-after-building-the-subroutine.patch
Patch57:  0057-i965-allocate-GRF-registers-before-building-subrout.patch
Patch58:  0058-return-correct-size-from-glGetActiveUniform-bug-137.patch
Patch59:  0059-glGetActiveUniform-fix.patch
Patch60:  0060-fix-GL_LINE_LOOP-with-drivers-using-own-render-pipel.patch
Patch61:  0061-add-missing-double-quote-bug-13878.patch
Patch62:  0062-add-Get-info-for-MAX_3D_TEXTURE_SIZE-for-bug-1381.patch
Patch63:  0063-added-get-info-for-framebuffer-object-tokens.patch
Patch64:  0064-Fix-several-bugs-relating-to-uniforms-and-attributes.patch
Patch65:  0065-More-fixes-to-shader_api.patch
Patch66:  0066-Add-a-test-program-to-test-for-assorted-bugs-in-shad.patch
Patch67:  0067-Make-use-of-count-in-_mesa_uniform_matrix.patch
#Patch68:  0068-Convert-to-0-1-when-setting-boolean-uniforms.patch
Patch69:  0069-fix-GLSL-uniform-attrib-bugs-13753.patch
Patch70:  0070-additional-GL_COLOR_ATTACHMENTx_EXT-cases-bug-13767.patch
Patch71:  0071-fix-vbo-display-list-memleak-upon-context-destructio.patch
Patch72:  0072-additional-GL_COLOR_ATTACHMENTx_EXT-cases-bug-13767.patch
Patch73:  0073-additional-stub-functions.patch
Patch75:  0075-fix-3d-proxy-texture-depth-bug.patch
Patch74:  0074-fix-depth-1-typo-in-glTexImage3D-proxy-code.patch
Patch76:  0076-i915tex-Centralize-mipmap-pitch-computations.patch
Patch77:  0077-i965-Fix-unresolved-symbol-intel_miptree_pitch_alig.patch
Patch78:  0078-i965-Fix-byte-vs.-pixel-unit-mixup-for-aligned-text.patch
Patch79:  0079-prep-for-7.0.3-release.patch
Patch80:  0080-define-M_PI-if-needed.patch
Patch81:  0081-remove-unused-var.patch
Patch82:  0082-Don-t-build-yuvrect_client-by-default.patch
Patch83:  0083-fix-pc-vs.-gc-ps-usage-bug-14197.patch
Patch84:  0084-fix-GLX-vertex-array-bug-14197.patch
Patch85:  0085-glxinfo-Fix-multisample-visual-reporting.patch
#Patch86:  0086-Assorted-patches-for-miniglx-linux-solo-Gavin-Li-c.patch
Patch87:  0087-i965-re-define-the-type-of-reg.loopcount.patch
Patch88:  0088-i965-valid-message-length-includes-message-header.patch
Patch89:  0089-fix-some-pbo-path-problems.patch
Patch90:  0090-pull-some-more-fixes-for-pbo-access-from-trunk.patch
Patch91:  0091-R300-RV410-SE-chips-have-half-the-pipes-of-regular.patch
Patch92:  0092-Add-new-RV380-pci-id.patch
Patch93:  0093-check-if-fb-Delete-is-null-bugs-13507-14293.patch
Patch94:  0094-fix-bugs-13507-14293.patch
Patch95:  0095-fix-w-component-of-glsl-vec4-asin.patch
Patch96:  0096-regenerate-glsl-library-functions.patch
Patch97:  0097-965-Fix-memory-leak-when-deleting-buffers-with-bac.patch
Patch98:  0098-Fix-bug-9871-enable-user-defined-clip-planes-for-R3.patch
Patch99:  0099-fix-bug-9871.patch
Patch100: 0100-added-altopts-to-allow-overriding-all-other-opts.patch
Patch101: 0101-_mesa_swizzle_ubyt_image-Don-t-use-single-swizzle_c.patch
Patch103: 0103-fix-bug-with-generated-fragment-programs-if-vertex-s.patch
Patch104: 0104-Fix-glBindTexture-crash-bug-14514.patch
Patch105: 0105-Fix-potential-glDrawPixels-GL_DEPTH_COMPONENT-crash.patch
Patch106: 0106-i965-new-integrated-graphics-chipset-support.patch
Patch107: 0107-Apple-Pulled-in-changes-from-Apple-s-patchset-to-al.patch
Patch108: 0108-Added-size-name-Get-mode-get-lines-for-point.patch
Patch109: 0109-Fix-glBegin-time-test-for-invalid-programs-shaders.patch
Patch110: 0110-raise-GL_INVALID_OPERATION-if-glProgramString-compil.patch
Patch111: 0111-Fix-point-rasterization-regression-caused-by-commit.patch
Patch112: 0112-latest-bug-fixes.patch
Patch113: 0113-prep-for-7.0.3-rc-2.patch
Patch114: 0114-bump-libGL.so-version-number.patch
Patch115: 0115-Replace-glut_fbc.c-with-glut_fcb.c-cb-callback.patch
Patch116: 0116-Don-t-Swap-buffer-if-a-DRIDrawable-is-entirely-obscu.patch
Patch117: 0117-state.depth.range-alpha-value-should-be-1-not-0-bu.patch
Patch118: 0118-fix-__builtin_expect-definition-test-for-IBM-XLC.patch
Patch119: 0119-init-vertex-weight-attrib-to-1-0-0-0.patch
Patch120: 0120-Set-normalized-flag-for-GLubyte-arrays-in-_mesa_Vert.patch
Patch121: 0121-fix-parsing-of-state.texenv.color-bug-14931.patch

# DRI modules are not under /usr/X11R6 anymore
Patch1000:	mesa-6.5.1-default_dri_dir.patch
# Install EGL header files and fixes other minor compilations problems when enabling EGL
Patch1001:	mesa-egl_support.patch
# Fix linux-dri so it can be used for all archs (thanks Christiaan Welvaart)
Patch1002:	Mesa-7.0-linux-dri-config.patch
# remove unfinished GLX_ARB_render_texture
Patch1003:	mesa-6.5.2-no-ARB_render_texture.patch
# reported as upstream bug 12097
Patch1004:	mesa-7.0.1-via_null_deref2.patch
# (tv) fix build:
Patch1005:	mesa-7.0.2-build-config.patch 

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
Mesa is an OpenGL 2.1 compatible 3D graphics library.

%description	source
Mesa is an OpenGL 2.1 compatible 3D graphics library.

Source files required by the Xorg to enable glx support.

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
%setup -q -n Mesa-%{version} -b1 -b2

cp -f %{SOURCE6} %{SOURCE7} src/mesa/glapi

%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1
%patch21 -p1
%patch22 -p1
%patch23 -p1
%patch24 -p1
%patch25 -p1
%patch26 -p1
%patch27 -p1
%patch28 -p1
%patch29 -p1
%patch30 -p1
%patch31 -p1
%patch32 -p1
%patch33 -p1
%patch34 -p1
%patch35 -p1
%patch36 -p1
#%patch37 -p1
%patch38 -p1
%patch39 -p1
%patch40 -p1
%patch41 -p1
%patch42 -p1
#%patch43 -p1
%patch44 -p1
%patch45 -p1
%patch46 -p1
%patch47 -p1
%patch48 -p1
%patch49 -p1
%patch50 -p1
%patch51 -p1
%patch52 -p1
%patch53 -p1
%patch54 -p1
%patch55 -p1
%patch56 -p1
%patch57 -p1
%patch58 -p1
%patch59 -p1
%patch60 -p1
%patch61 -p1
%patch62 -p1
%patch63 -p1
%patch64 -p1
%patch65 -p1
%patch67 -p1
#%patch68 -p1
%patch69 -p1
%patch70 -p1
%patch71 -p1
%patch72 -p1
%patch73 -p1
%patch74 -p1
%patch75 -p1
%patch76 -p1
%patch77 -p1
%patch78 -p1
%patch79 -p1
%patch80 -p1
%patch81 -p1
%patch82 -p1
%patch83 -p1
%patch84 -p1
%patch85 -p1
#%patch86 -p1
%patch87 -p1
%patch88 -p1
%patch89 -p1
%patch90 -p1
%patch91 -p1
%patch92 -p1
%patch93 -p1
%patch94 -p1
%patch95 -p1
%patch96 -p1
%patch97 -p1
%patch98 -p1
%patch99 -p1
%patch100 -p1
%patch101 -p1
%patch103 -p1
%patch104 -p1
%patch105 -p1
%patch106 -p1
%patch107 -p1
%patch108 -p1
%patch109 -p1
%patch110 -p1
%patch111 -p1
%patch112 -p1
%patch113 -p1
%patch114 -p1
%patch115 -p1
%patch116 -p1
%patch117 -p1
%patch118 -p1
%patch119 -p1
%patch120 -p1
%patch121 -p1

%patch1003 -p1 -b .no-ARB_render_texture
%patch1000 -p1 -b .default_dri_dir

%if %{enable_egl}
%patch1001 -p1 -b .egl_support
%endif

%patch1002 -p1 -b .linux-dri-config
%patch1004 -p1 -b .via_null_deref2
%patch1005 -p1 -b .fix_build

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
ARCH_FLAGS="$RPM_OPT_FLAGS -O1 -fno-strict-aliasing -fno-tree-vrp -DNDEBUG -DDEFAULT_DRIVER_DIR=\\\"%{driver_dir}\\\""
export ARCH_FLAGS

%make 	MKDEP=/usr/bin/makedepend \
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

mkdir -p %{buildroot}/%{_bindir}
for demo in `find progs/demos -type f -perm /a+x` `find progs/xdemos -type f -perm /a+x`; do
    cp -v $demo %{buildroot}/%{_bindir}
done
# (fg) So that demos at least work :)
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

# generate mesa source files
chmod +x %{SOURCE3}
%{SOURCE3} $RPM_BUILD_ROOT %{mesasrcdir}


%clean
rm -fr $RPM_BUILD_ROOT

%if %{enable_egl}
%post -n %{libeglname} -p /sbin/ldconfig
%postun -n %{libeglname} -p /sbin/ldconfig
%endif

%post -n %{libglname} -p /sbin/ldconfig

%postun -n %{libglname} -p /sbin/ldconfig

%post -n %{libgluname} -p /sbin/ldconfig 

%postun -n %{libgluname} -p /sbin/ldconfig

%post -n %{libglutname} -p /sbin/ldconfig 

%postun -n %{libglutname} -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc docs/COPYING docs/README.*

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
%_libdir/pkgconfig/*.pc

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

