#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	pcre		# regular expressions support (PCRE based)
%bcond_without	static_libs	# static library
#
Summary:	Fast samples-based log normalization library
Summary(pl.UTF-8):	Szybka biblioteka do normalizowania logów oparta na próbkach
Name:		liblognorm
Version:	2.0.6
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	http://www.liblognorm.com/files/download/%{name}-%{version}.tar.gz
# Source0-md5:	9b6b6b5f76fafbc853c65aad69d5d33b
URL:		https://www.liblognorm.com/
%{?with_apidocs:BuildRequires:	sphinx-pdg}
BuildRequires:	libestr-devel
BuildRequires:	libfastjson-devel
BuildRequires:	pcre-devel
BuildRequires:	pkgconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Fast samples-based log normalization library.

%description -l pl.UTF-8
Szybka biblioteka do normalizowania logów oparta na próbkach.

%package devel
Summary:	Header files for liblognorm library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki liblognorm
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libestr-devel
Requires:	libfastjson-devel

%description devel
Header files for liblognorm library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki liblognorm.

%package static
Summary:	Static liblognorm library
Summary(pl.UTF-8):	Statyczna biblioteka liblognorm
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static liblognorm library.

%description static -l pl.UTF-8
Statyczna biblioteka liblognorm.

%package apidocs
Summary:	API documentation for liblognorm library
Summary(pl.UTF-8):	Dokumentacja API biblioteki liblognorm
Group:		Documentation
%if "%{_rpmversion}" >= "4.6"
BuildArch:	noarch
%endif

%description apidocs
API documentation for liblognorm library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki liblognorm.

%prep
%setup -q

%build
%configure \
	--includedir=%{_includedir}/liblognorm \
	%{?with_apidocs:--enable-docs} \
	--enable-regexp \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/liblognorm.la

%if %{with apidocs}
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/liblognorm/{_sources,.buildinfo,objects.inv}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README
%attr(755,root,root) %{_bindir}/lognormalizer
%attr(755,root,root) %{_libdir}/liblognorm.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblognorm.so.5

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/liblognorm.so
%{_includedir}/liblognorm
%{_pkgconfigdir}/lognorm.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/liblognorm.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_docdir}/liblognorm
%endif
