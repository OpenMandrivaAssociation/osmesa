# OSMesa was removed in Mesa 25.1.0, but is still used by
# Wine/Proton and probably a few others...

# (cg) Cheater...
%define Werror_cflags %{nil}

# (aco) Needed for the dri drivers
%define _disable_ld_no_undefined 1

# LTOing Mesa takes insane amounts of RAM :/
# So you may want to disable it for anything
# but final builds...
#define _disable_lto 1

# Mesa is used by wine and steam
%ifarch %{x86_64}
%bcond_without compat32
%else
%bcond_with compat32
%endif

# -fno-strict-aliasing is added because of numerous warnings, strict
# aliasing might generate broken code.
# (tpg) imho -g3 here is for someone who is developing graphics drivers
# or trying to pin point a specific issue. Nobody install debug symbols by default
%ifarch %{aarch64}
# In LLVM 18.0.0-rc1, O3 on aarch64 results in a build failure
%global optflags %{optflags} -O2 -fno-strict-aliasing -g1 -flto=thin
%else
%global optflags %{optflags} -O3 -fno-strict-aliasing -g1 -flto=thin
%endif
%global build_ldflags %{build_ldflags} -fno-strict-aliasing -flto=thin -Wl,--undefined-version

#define git 20240114
%define git_branch main
#define git_branch %(echo %{version} |cut -d. -f1-2)
#define relc 3

%ifarch %{riscv}
%bcond_with gcc
%else
%bcond_with gcc
%endif

%ifarch %{ix86} %{x86_64}
%bcond_without intel
%else
%bcond_with intel
%endif
# Sometimes it's necessary to disable r600 while bootstrapping
# an LLVM change (such as the r600 -> AMDGPU rename)
%bcond_without r600

%define vsuffix %{?relc:-rc%{relc}}%{!?relc:%{nil}}

%define osmesamajor 8
%define libosmesa %mklibname osmesa %{osmesamajor}
%define devosmesa %mklibname osmesa -d
%define lib32osmesa libosmesa%{osmesamajor}
%define dev32osmesa libosmesa-devel

%define devvulkan %mklibname vulkan-intel -d
%define dev32vulkan libvulkan-intel-devel

%define glesv1major 1
%define glesv1name GLESv1_CM
%define libglesv1 %mklibname %{glesv1name} %{glesv1major}
%define devglesv1 %mklibname %{glesv1name} -d
%define lib32glesv1 lib%{glesv1name}%{glesv1major}
%define dev32glesv1 lib%{glesv1name}-devel

%define glesv2major 2
%define glesv2name GLESv2
%define libglesv2 %mklibname %{glesv2name}_ %{glesv2major}
%define devglesv2 %mklibname %{glesv2name} -d
%define lib32glesv2 lib%{glesv2name}_%{glesv2major}
%define dev32glesv2 lib%{glesv2name}-devel

%define devglesv3 %mklibname glesv3 -d
%define dev32glesv3 libglesv3-devel

%define mesasrcdir %{_prefix}/src/Mesa/

%define short_ver %(if [ $(echo %{version} |cut -d. -f3) = "0" ]; then echo %{version} |cut -d. -f1-2; else echo %{version}; fi)

Summary:	OpenGL 4.6+ and ES 3.1+ compatible 3D graphics library
Name:		osmesa
Version:	25.0.4
Release:	%{?relc:0.rc%{relc}.}%{?git:0.%{git}.}1
Group:		System/Libraries
License:	MIT
Url:		https://www.mesa3d.org
%if 0%{?git:1}
%if "%{git_branch}" == "panthor" || "%{git_branch}" == "panfrost"
Source0:	https://gitlab.freedesktop.org/panfrost/mesa/-/archive/%{git}/mesa-%{git}.tar.bz2
%else
Source0:	https://gitlab.freedesktop.org/mesa/mesa/-/archive/%{git_branch}/mesa-%{git_branch}.tar.bz2#/mesa-%{git }.tar.bz2
%endif
%else
Source0:	https://mesa.freedesktop.org/archive/mesa-%{version}%{vsuffix}.tar.xz
%endif
Source100:	%{name}.rpmlintrc

%define dricoremajor 1
%define dricorename dricore
%define devdricore %mklibname %{dricorename} -d
%define libdricore %mklibname %{dricorename} 9
%define dev32dricore lib%{dricorename}-devel
%define lib32dricore lib%{dricorename}9

Obsoletes:	%{libdricore} < %{EVRD}
Obsoletes:	%{devdricore} < %{EVRD}
Obsoletes:	%{name}-xorg-drivers < %{EVRD}
Obsoletes:	%{name}-xorg-drivers-radeon < %{EVRD}
Obsoletes:	%{name}-xorg-drivers-nouveau < %{EVRD}

# Without this patch, the OpenCL ICD calls into MesaOpenCL,
# which for some reason calls back into the OpenCL ICD instead
# of calling its own function by the same name.
# (Probably related to -Bsymbolic/-Bsymbolic-functions)
Patch0:		mesa-20.1.1-fix-opencl.patch
# Use llvm-config to detect llvm, since the newer method
# finds /usr/lib64/libLLVM-17.so even for 32-bit builds
Patch1:		mesa-23.1-x86_32-llvm-detection.patch
# Fix intel-vk build with clang 16 and gcc 13
#Patch2:		mesa-23.1-intel-vk-compile.patch
# find opencl-c-base.h even when crosscompiling
Patch3:		mesa-24.1-find-opencl-c-base.h.patch
Patch4:		mesa-23.3.0-rc4-panfrost-enable-gl3-by-default.patch
# Not used in the spec; this is a test case to verify patch0
# is still needed. If this code works without the patch, the
# patch can be removed. If it crashes/takes forever (infinite
# loop), the patch is still needed.
Source50:	test.c

#Patch1:		mesa-19.2.3-arm32-buildfix.patch
#Patch2:		mesa-20.3.4-glibc-2.33.patch
Patch5:		mesa-20.3.0-meson-radeon-arm-riscv-ppc.patch

Patch7:		mesa-24-llvmspirv-detection.patch
Patch8:		mesa-buildsystem-improvements.patch
Patch9:		mesa-24.0-llvmspirvlib-version-check.patch
#Patch10:	mesa-24.0.2-buildfix32.patch
###FIXME Patch11:	enable-vulkan-video-decode.patch
#Patch12:	https://gitlab.freedesktop.org/mesa/mesa/-/merge_requests/31950.patch

# Fix https://bugs.winehq.org/show_bug.cgi?id=41930
# https://gitlab.freedesktop.org/mesa/mesa/-/issues/5094
# Ported from https://gitlab.freedesktop.org/bvarner/mesa/-/tree/feature/osmesa-preserve-buffer
Patch500:	mesa-24.0-osmesa-fix-civ3.patch
# Related to the above, we should also fix
# https://gitlab.freedesktop.org/mesa/mesa/-/issues/5095

# Panthor -- https://gitlab.freedesktop.org/bbrezillon/mesa.git
# Currently no patches required

# From upstream
Patch1000:	https://gitlab.freedesktop.org/mesa/mesa/-/merge_requests/34001.patch

BuildRequires:	flex
BuildRequires:	bison
BuildRequires:	libxml2-python
BuildRequires:	meson
BuildRequires:	lm_sensors-devel
BuildRequires:	cmake(LLVM)
BuildRequires:	pkgconfig(LLVMSPIRVLib)
BuildRequires:	pkgconfig(expat)
BuildRequires:	elfutils-devel
%ifarch %{ix86}
BuildRequires:	libatomic-devel
%endif
BuildRequires:	python
BuildRequires:	python%{pyver}dist(ply)
BuildRequires:	python%{pyver}dist(pyyaml)
BuildRequires:	python%{pyver}dist(mako) >= 0.8.0
%ifarch %{arm} %{armx} %{riscv}
# For etnaviv
BuildRequires:	python%{pyver}dist(pycparser)
%endif
BuildRequires:	pkgconfig(libdrm) >= 2.4.56
BuildRequires:	pkgconfig(libudev) >= 186
BuildRequires:	pkgconfig(libglvnd)
BuildRequires:	pkgconfig(libzstd)
BuildRequires:	pkgconfig(vulkan)
BuildRequires:	pkgconfig(x11) >= 1.3.3
BuildRequires:	pkgconfig(xdamage) >= 1.1.1
BuildRequires:	pkgconfig(xext) >= 1.1.1
BuildRequires:	pkgconfig(xfixes) >= 4.0.3
BuildRequires:	pkgconfig(xi) >= 1.3
BuildRequires:	pkgconfig(xmu) >= 1.0.3
BuildRequires:	pkgconfig(xproto)
BuildRequires:	pkgconfig(xt) >= 1.0.5
BuildRequires:	pkgconfig(xxf86vm) >= 1.1.0
BuildRequires:	pkgconfig(xshmfence) >= 1.1
BuildRequires:	pkgconfig(xrandr)
BuildRequires:	pkgconfig(xcb-dri3)
BuildRequires:	pkgconfig(xcb-present)
BuildRequires:	pkgconfig(xcb-keysyms)
BuildRequires:	pkgconfig(xv)
BuildRequires:	pkgconfig(valgrind)
# for libsupc++.a
BuildRequires:	stdc++-static-devel
BuildRequires:	cmake(Polly)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(libarchive)
BuildRequires:	pkgconfig(lua)
BuildRequires:	pkgconfig(libconfig)
BuildRequires:	pkgconfig(SPIRV-Tools)
BuildRequires:	pkgconfig(libunwind)
BuildRequires:	pkgconfig(wayland-client)
BuildRequires:	pkgconfig(wayland-server)
BuildRequires:	pkgconfig(wayland-protocols) >= 1.8
BuildRequires:	glslang

# package mesa
Requires:	libGL.so.1%{_arch_tag_suffix}

%if %{with compat32}
BuildRequires:	devel(libdrm)
BuildRequires:	devel(libX11)
BuildRequires:	devel(libXdamage)
BuildRequires:	devel(libXext)
BuildRequires:	devel(libXfixes)
BuildRequires:	devel(libXi)
BuildRequires:	devel(libXmu)
BuildRequires:	devel(libXt)
BuildRequires:	devel(libXxf86vm)
BuildRequires:	devel(libxshmfence)
BuildRequires:	devel(libXrandr)
BuildRequires:	devel(libxcb-dri3)
BuildRequires:	devel(libxcb-present)
BuildRequires:	devel(libXv)
BuildRequires:	devel(libxcb)
BuildRequires:	devel(libXau)
BuildRequires:	devel(libXdmcp)
BuildRequires:	devel(libsensors)
BuildRequires:	libsensors.so.5
BuildRequires:	devel(libLLVM)
BuildRequires:	devel(libclang)
BuildRequires:	devel(libzstd)
BuildRequires:	devel(libwayland-client)
BuildRequires:	devel(libwayland-server)
BuildRequires:	devel(libffi)
BuildRequires:	devel(libelf)
BuildRequires:	libunwind-nongnu-devel
BuildRequires:	devel(libz)
BuildRequires:	devel(libexpat)
BuildRequires:	devel(libOpenGL)
BuildRequires:	devel(libGLdispatch)
BuildRequires:	devel(libXrandr)
BuildRequires:	devel(libXrender)
BuildRequires:	devel(libatomic)
BuildRequires:	devel(libudev)
BuildRequires:	devel(libSPIRV-Tools-shared)
BuildRequires:	devel(libvulkan)
BuildRequires:	libLLVMSPIRVLib-devel
BuildRequires:	libLLVMSPIRVLib-static-devel
%endif

%description
Mesa is an OpenGL 4.6+ and ES 3.1+ compatible 3D graphics library.

%package -n %{libosmesa}
Summary:	Mesa offscreen rendering library
Group:		System/Libraries

%description -n %{libosmesa}
Mesa offscreen rendering libraries for rendering OpenGL into
application-allocated blocks of memory.

%package -n %{devosmesa}
Summary:	Development files for libosmesa
Group:		Development/C
Requires:	%{libosmesa} = %{EVRD}

%description -n %{devosmesa}
This package contains the headers needed to compile programs against
the Mesa offscreen rendering library.

%package -n %{libglesv1}
Summary:	Files for Mesa (glesv1 libs)
Group:		System/Libraries
Obsoletes:	%{_lib}mesaglesv1_1 < 8.0

%description -n %{libglesv1}
OpenGL ES is a low-level, lightweight API for advanced embedded graphics using
well-defined subset profiles of OpenGL.

This package provides the OpenGL ES library version 1.

%package -n %{devglesv1}
Summary:	Development files for glesv1 libs
Group:		Development/C
Requires:	%{libglesv1}
Requires:	libglvnd-GLESv1_CM%{?_isa}
# For libGLESv1_CM.so symlink
Requires:	pkgconfig(libglvnd)
Obsoletes:	%{_lib}mesaglesv1_1-devel < 8.0
Obsoletes:	%{_lib}glesv1_1-devel < %{EVRD}

%description -n %{devglesv1}
This package contains the headers needed to compile OpenGL ES 1 programs.

%package -n %{libglesv2}
Summary:	Files for Mesa (glesv2 libs)
Group:		System/Libraries
Obsoletes:	%{_lib}mesaglesv2_2 < 8.0
# For libGLESv2.so symlink
Requires:	pkgconfig(libglvnd)

%description -n %{libglesv2}
OpenGL ES is a low-level, lightweight API for advanced embedded graphics using
well-defined subset profiles of OpenGL.

This package provides the OpenGL ES library version 2.

%package -n %{devglesv2}
Summary:	Development files for glesv2 libs
Group:		Development/C
Requires:	%{libglesv2}
Requires:	libglvnd-GLESv2%{?_isa}
Obsoletes:	%{_lib}mesaglesv2_2-devel < 8.0
Obsoletes:	%{_lib}glesv2_2-devel < %{EVRD}

%description -n %{devglesv2}
This package contains the headers needed to compile OpenGL ES 2 programs.

%package -n %{devglesv3}
Summary:	Development files for glesv3 libs
Group:		Development/C
# there is no pkgconfig
Provides:	glesv3-devel = %{EVRD}

%description -n %{devglesv3}
This package contains the headers needed to compile OpenGL ES 3 programs.

%if %{with compat32}
%package -n %{lib32osmesa}
Summary:	Mesa offscreen rendering library (32-bit)
Group:		System/Libraries

%description -n %{lib32osmesa}
Mesa offscreen rendering libraries for rendering OpenGL into
application-allocated blocks of memory.

%package -n %{dev32osmesa}
Summary:	Development files for libosmesa (32-bit)
Group:		Development/C
Requires:	%{lib32osmesa} = %{EVRD}
Requires:	%{devosmesa} = %{EVRD}

%description -n %{dev32osmesa}
This package contains the headers needed to compile programs against
the Mesa offscreen rendering library.
%endif

%prep
%autosetup -p1 -n mesa-%{?git:%{git_branch}}%{!?git:%{version}%{vsuffix}}

%build
%if %{with gcc}
export CC=gcc
export CXX=g++
%endif

%if %{with compat32}
cat >llvm-config <<EOF
#!/bin/sh
/usr/bin/llvm-config "\$@" |sed -e 's,lib64,lib,g'
EOF
chmod +x llvm-config
export PATH="$(pwd):${PATH}"

cat >i686.cross <<EOF
[binaries]
pkgconfig = 'pkg-config'
cmake = 'cmake'
llvm-config = '$(pwd)/llvm-config'

[host_machine]
system = 'linux'
cpu_family = 'x86'
cpu = 'i686'
endian = 'little'
EOF

export CC="%{__cc} -I%{_libdir}/clang/$(clang --version |head -n1 |cut -d' ' -f2 |cut -d. -f1)/include"
if ! %meson32 \
	-Dmicrosoft-clc=disabled \
	-Dshared-llvm=enabled \
	--cross-file=i686.cross \
	-Db_ndebug=true \
	-Dc_std=c11 \
	-Dcpp_std=c++17 \
	-Dglx=disabled \
	-Dplatforms=x11 \
	-Dvulkan-layers="" \
	-Dvulkan-drivers="" \
	-Dvulkan-beta=false \
	-Dvideo-codecs="" \
	-Dosmesa=true \
	-Dandroid-libbacktrace=disabled \
	-Dvalgrind=disabled \
	-Dglvnd=disabled \
	-Dgallium-opencl=disabled \
	-Dgallium-va=disabled \
	-Dgallium-vdpau=disabled \
	-Dgallium-xa=disabled \
	-Dgallium-nine=false \
	-Dgallium-drivers=llvmpipe \
	-Dgbm=disabled \
	-Dgles1=disabled \
	-Dgles2=enabled \
	-Degl=disabled \
	-Dglx-direct=true \
	-Dllvm=enabled \
	-Dlmsensors=enabled \
	-Dopengl=true \
	-Dshader-cache=enabled \
	-Dshared-glapi=enabled \
	-Dshared-llvm=enabled \
	-Dselinux=false \
	-Dbuild-tests=false \
	-Dintel-rt=disabled \
	-Dtools=""; then

	cat build32/meson-logs/meson-log.txt >/dev/stderr
fi
unset CC

%ninja_build -C build32/
rm llvm-config
%endif

%if %{cross_compiling}
# We need to use a HOST compatible llvm-config... While technically wrong-ish,
# target llvm-config is for the target architecture...
cat >llvm-config <<EOF
#!/bin/sh
%{_bindir}/llvm-config "\$@" |sed -e 's,-I/usr/include ,,;s,-isystem/usr/include ,,;s,-L/usr/lib64 ,,'
EOF
chmod +x llvm-config
cp %{_datadir}/meson/toolchains/%{_target_platform}.cross cross.cross
sed -i -e "/binaries/allvm-config = '$(pwd)/llvm-config'" cross.cross
%endif

if ! %meson \
%if %{cross_compiling}
	--cross-file=cross.cross \
	-Dvalgrind=disabled \
%endif
	-Dmicrosoft-clc=disabled \
	-Dshared-llvm=enabled \
	-Db_ndebug=true \
	-Dc_std=c11 \
	-Dcpp_std=c++17 \
	-Dandroid-libbacktrace=disabled \
	-Dgallium-drivers=llvmpipe \
	-Dvulkan-drivers="" \
%ifarch %{x86_64}
	-Dintel-clc=enabled \
%endif
	-Dgallium-opencl=disabled \
	-Dgallium-rusticl=false \
	-Dgallium-extra-hud=false \
	-Dgallium-va=disabled \
	-Dgallium-vdpau=disabled \
	-Dgallium-xa=disabled \
	-Dgallium-nine=false \
	-Dglx=disabled \
	-Dplatforms=x11 \
	-Dvulkan-layers="" \
	-Dvulkan-beta=false \
	-Dvideo-codecs="" \
	-Degl=disabled \
	-Dosmesa=true \
	-Dglvnd=disabled \
	-Dgbm=disabled \
	-Dgles1=disabled \
	-Dgles2=enabled \
	-Dglx-direct=true \
	-Dllvm=enabled \
	-Dlmsensors=enabled \
	-Dopengl=true \
	-Dshader-cache=enabled \
	-Dshared-glapi=enabled \
	-Dshared-llvm=enabled \
	-Dselinux=false \
	-Dbuild-tests=false \
%ifarch %{x86_64}
	-Dintel-rt=enabled \
%else
	-Dintel-rt=disabled \
%endif
	-Dtools=""; then

	cat build/meson-logs/meson-log.txt >/dev/stderr
fi

%ninja_build -C build/

%install
%if %{with compat32}
%ninja_install -C build32/
%endif
%ninja_install -C build/

# We get those from libglvnd and mesa
rm -rf	%{buildroot}%{_includedir}/GL/gl.h \
	%{buildroot}%{_includedir}/GL/glcorearb.h \
	%{buildroot}%{_includedir}/GL/glext.h \
	%{buildroot}%{_includedir}/GLES2 \
	%{buildroot}%{_includedir}/GLES3 \
	%{buildroot}%{_includedir}/KHR \
	%{buildroot}%{_datadir}/drirc.d

%files -n %{libosmesa}
%{_libdir}/libOSMesa.so.%{osmesamajor}*

%files -n %{devosmesa}
%{_includedir}/GL/osmesa.h
%{_libdir}/libOSMesa.so
%{_libdir}/pkgconfig/osmesa.pc

%if %{with compat32}
%files -n %{lib32osmesa}
%{_prefix}/lib/libOSMesa.so.%{osmesamajor}*

%files -n %{dev32osmesa}
%{_prefix}/lib/libOSMesa.so
%{_prefix}/lib/pkgconfig/osmesa.pc
%endif
