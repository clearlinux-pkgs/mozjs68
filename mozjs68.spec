#
# Inspired by the Arch Linux equivalent package.....
#
Name     : mozjs68
Version  : 68.12.0
Release  : 5
Source0  : https://archive.mozilla.org/pub/firefox/releases/68.12.0esr/source/firefox-68.12.0esr.source.tar.xz
Group    : Development/Tools
License  : Apache-2.0 BSD-2-Clause BSD-3-Clause BSD-3-Clause-Clear GPL-2.0 LGPL-2.0 LGPL-2.1 MIT MPL-2.0-no-copyleft-exception
Requires: mozjs68-bin
Requires: mozjs68-lib
Requires: psutil
Requires: pyOpenSSL
Requires: pyasn1
Requires: wheel
BuildRequires : icu4c-dev
BuildRequires : nspr-dev
BuildRequires : pbr
BuildRequires : pip
BuildRequires : pkgconfig(libffi)
BuildRequires : pkgconfig(x11)
BuildRequires : psutil
BuildRequires : python-core
BuildRequires : python-dev
BuildRequires : python3-dev
BuildRequires : setuptools
BuildRequires : zlib-dev
BuildRequires : autoconf213
BuildRequires : readline-dev
BuildRequires : ncurses-dev
BuildRequires : psutil
BuildRequires : rustc
BuildRequires : llvm-dev
Summary: mozjs

Patch1: fix-soname.patch
Patch2: copy-headers.patch
Patch3: init_patch.patch
Patch4: emitter.patch
Patch5: emitter_test.patch
Patch6: spidermonkey_checks_disable.patch

# Suppress stripping binaries
%define __strip /bin/true
%define debug_package %{nil}

%description
JavaScript interpreter and libraries - Version 68

%package bin
Summary: bin components for the mozjs68 package.
Group: Binaries

%description bin
bin components for the mozjs68 package.


%package dev
Summary: dev components for the mozjs68 package.
Group: Development
Requires: mozjs68-lib
Requires: mozjs68-bin
Provides: mozjs68-devel

%description dev
dev components for the mozjs68 package.


%package lib
Summary: lib components for the mozjs68 package.
Group: Libraries

%description lib
lib components for the mozjs68 package.


%prep
%setup -q -n firefox-68.12.0

%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

# use system zlib for perf
rm -rf ../../modules/zlib


%build
export http_proxy=http://127.0.0.1:9/
export https_proxy=http://127.0.0.1:9/
export no_proxy=localhost,127.0.0.1,0.0.0.0
export LANG=C
export SOURCE_DATE_EPOCH=1501084420
export CFLAGS="-Os -falign-functions=4 -fno-semantic-interposition -fassociative-math -fno-signed-zeros "
export FCFLAGS="-O3 -falign-functions=32 -fno-semantic-interposition "
export FFLAGS="$CFLAGS -O3 -falign-functions=32 -fno-semantic-interposition "
export CXXFLAGS="-Os -falign-functions=4 -fno-semantic-interposition -fassociative-math -fno-signed-zeros"
export AUTOCONF="/usr/bin/autoconf213"
CFLAGS+=' -fno-delete-null-pointer-checks -fno-strict-aliasing -fno-tree-vrp '
CXXFLAGS+=' -fno-delete-null-pointer-checks -fno-strict-aliasing -fno-tree-vrp '
export CC=gcc CXX=g++ PYTHON=/usr/bin/python2

pushd js/src

autoconf213
%configure --disable-static --with-x \
    --prefix=/usr \
    --disable-debug \
    --enable-debug-symbols \
    --disable-strip \
    --disable-jemalloc \
    --enable-optimize="-O3" \
    --enable-posix-nspr-emulation \
    --enable-readline \
    --enable-release \
    --enable-shared-js \
    --enable-tests \
    --with-intl-api \
    --with-system-zlib \
    --program-suffix=68 \
    --without-system-icu

make V=1  %{?_smp_mflags}
popd


%install
export SOURCE_DATE_EPOCH=1501084420
rm -rf %{buildroot}
pushd js/src
%make_install
popd
rm %{buildroot}/usr/lib64/*.ajs

cp %{buildroot}/usr/lib64/libmozjs-68.so %{buildroot}/usr/lib64/libmozjs-68.so.0
#find %{buildroot}/usr/{lib/pkgconfig,include} -type f -exec chmod -c a-x {} +
## make_install_append content
#mv %{buildroot}/usr/lib64/pkgconfig/js.pc %{buildroot}/usr/lib64/pkgconfig/mozjs-60.pc
## make_install_append end

%files
%defattr(-,root,root,-)
#/usr/lib64/libjs_static.ajs

%files bin
%defattr(-,root,root,-)
/usr/bin/js68
/usr/bin/js68-config

%files dev
%defattr(-,root,root,-)
/usr/include/mozjs-68/
/usr/lib64/pkgconfig/mozjs-68.pc

%files lib
%defattr(-,root,root,-)
/usr/lib64/libmozjs-68.so
/usr/lib64/libmozjs-68.so.0
