Summary:	General-purpose scalable concurrent malloc implementation
Name:		jemalloc
Version:	2.2.3
Release:	2
License:	BSD
Group:		Libraries
URL:		http://www.canonware.com/jemalloc/
Source0:	http://www.canonware.com/download/jemalloc/%{name}-%{version}.tar.bz2
# Source0-md5:	9da87786f2cb399913daa01f95ad6b91
# Remove pprof, as it already exists in google-perftools
Patch0:		no_pprof.patch
BuildRequires:	/usr/bin/xsltproc
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
General-purpose scalable concurrent malloc(3) implementation. This
distribution is the stand-alone "portable" implementation of jemalloc.

%package devel
Summary:	Development files for jemalloc
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains libraries and header files for developing
applications that use jemalloc library.

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
mv $RPM_BUILD_ROOT%{_libdir}/libjemalloc.so.{?,%{version}}
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
%doc COPYING README VERSION
%doc doc/jemalloc.html
%attr(755,root,root) %{_libdir}/libjemalloc.so.*.*.*
%ghost %{_libdir}/libjemalloc.so.1

%files devel
%defattr(644,root,root,755)
%{_includedir}/jemalloc
%{_libdir}/libjemalloc.so
%{_mandir}/man3/jemalloc.3*

%files static
%defattr(644,root,root,755)
%{_libdir}/libjemalloc.a
%{_libdir}/libjemalloc_pic.a
