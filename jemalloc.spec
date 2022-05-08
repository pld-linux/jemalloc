Summary:	General-purpose scalable concurrent malloc implementation
Summary(pl.UTF-8):	Ogólnego przeznaczenia, skalowalna, współbieżna implementacja funkcji malloc
Name:		jemalloc
Version:	5.3.0
Release:	1
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/jemalloc/jemalloc/releases
Source0:	https://github.com/jemalloc/jemalloc/releases/download/%{version}/%{name}-%{version}.tar.bz2
# Source0-md5:	09a8328574dab22a7df848eae6dbbf53
URL:		http://jemalloc.net/
BuildRequires:	libxslt-progs
BuildRequires:	sed >= 4.0
# list from include/jemalloc/internal/jemalloc_internal.h.in
# https://github.com/jemalloc/jemalloc/blob/3.6.0/include/jemalloc/internal/jemalloc_internal.h.in#L239
ExclusiveArch:	%{ix86} %{x8664} x32 alpha %{arm} aarch64 hppa ia64 le32 mips or1k ppc riscv s390 s390x sh4 sparcv9 sparc64 tile
# broken for us
# alpha: Missing implementation for 64-bit atomic operations"
# alpha: Missing implementation for 32-bit atomic operations"
ExcludeArch:	alpha
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
General-purpose scalable concurrent malloc(3) implementation. This
distribution is the stand-alone "portable" implementation of jemalloc.

%description -l pl.UTF-8
Ogólnego przeznaczenia, skalowalna, współbieżna implementacja funkcji
malloc(3). Ten pakiet zawiera samodzielną "przenośną" implementację
jemalloc.

%package devel
Summary:	Development files for jemalloc
Summary(pl.UTF-8):	Pliki programistyczne biblioteki jemalloc
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains the header files for developing applications
that use jemalloc library.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe do tworzenia aplikacji
wykorzystujących bibliotekę jemalloc.

%package static
Summary:	Static jemalloc library
Summary(pl.UTF-8):	Statyczna biblioteka jemalloc
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static jemalloc library.

%description static -l pl.UTF-8
Statyczna biblioteka jemalloc.

%prep
%setup -q

# This is truncated during build. Seems interesting to save.
cp -p VERSION version

%{__sed} -i '1s, /usr/bin/env perl,%{__perl},' bin/jeprof.in

%build
# enable GNU+C99 standard (C99 for restrict keyword, GNU for asm)
CFLAGS="%{rpmcflags} -std=gnu99"
%configure \
	--with-jemalloc-prefix=je_

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# restore
cp -pf version VERSION

# soname improperly made, use fake main name (just use our current version)
%{__mv} $RPM_BUILD_ROOT%{_libdir}/libjemalloc.so.{2,%{version}}
ln -s $(basename $RPM_BUILD_ROOT%{_libdir}/libjemalloc.so.*.*.*) \
	$RPM_BUILD_ROOT%{_libdir}/libjemalloc.so.2

# Install this with doc macro instead
%{__rm} $RPM_BUILD_ROOT%{_docdir}/%{name}/jemalloc.html

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING README VERSION doc/jemalloc.html
%attr(755,root,root) %{_bindir}/jemalloc.sh
%attr(755,root,root) %{_libdir}/libjemalloc.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libjemalloc.so.2

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/jemalloc-config
%attr(755,root,root) %{_bindir}/jeprof
%attr(755,root,root) %{_libdir}/libjemalloc.so
%{_includedir}/jemalloc
%{_pkgconfigdir}/jemalloc.pc
%{_mandir}/man3/jemalloc.3*

%files static
%defattr(644,root,root,755)
%{_libdir}/libjemalloc.a
%{_libdir}/libjemalloc_pic.a
