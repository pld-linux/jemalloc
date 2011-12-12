Summary:	General-purpose scalable concurrent malloc implementation
Summary(pl.UTF-8):	Ogólnego przeznaczenia, skalowalna, współbieżna implementacja funkcji malloc
Name:		jemalloc
Version:	2.2.5
Release:	2
License:	BSD
Group:		Libraries
Source0:	http://www.canonware.com/download/jemalloc/%{name}-%{version}.tar.bz2
# Source0-md5:	a5c4332705ed0e3fff1ac73cfe975640
# Remove pprof, as it already exists in google-perftools
Patch0:		no_pprof.patch
URL:		http://www.canonware.com/jemalloc/
BuildRequires:	libxslt-progs
# list from include/jemalloc/internal/jemalloc_internal.h.in
ExclusiveArch:	%{ix86} %{x8664} alpha arm mips s390 sparc64
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
%patch0 -p0

# This is truncated during build. Seems interesting to save.
cp -p VERSION version

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# restore
cp -pf version VERSION

# soname improperly made, use fake main name (just use our current version)
mv $RPM_BUILD_ROOT%{_libdir}/libjemalloc.so.{1,%{version}}
ln -s $(basename $RPM_BUILD_ROOT%{_libdir}/libjemalloc.so.*.*.*) \
	$RPM_BUILD_ROOT%{_libdir}/libjemalloc.so.1

# Install this with doc macro instead
%{__rm} $RPM_BUILD_ROOT%{_docdir}/%{name}/jemalloc.html

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING README VERSION doc/jemalloc.html
%attr(755,root,root) %{_libdir}/libjemalloc.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libjemalloc.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libjemalloc.so
%{_includedir}/jemalloc
%{_mandir}/man3/jemalloc.3*

%files static
%defattr(644,root,root,755)
%{_libdir}/libjemalloc.a
%{_libdir}/libjemalloc_pic.a
