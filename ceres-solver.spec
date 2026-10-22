#
# Conditional build:
%bcond_without	apidocs		# API documentation
#
Summary:	Library for modeling and solving large, complicated optimization problems
Name:		ceres-solver
Version:	2.2.0
Release:	1
License:	BSD
Group:		Libraries
Source0:	https://github.com/ceres-solver/ceres-solver/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	b360c795a75c3e99d67a2a60f2004466
URL:		https://ceres-solver.org/
BuildRequires:	eigen3
BuildRequires:	SuiteSparse-CHOLMOD-devel
BuildRequires:	SuiteSparse-CXSparse-devel
BuildRequires:	SuiteSparse-AMD-devel
BuildRequires:	SuiteSparse-CAMD-devel
BuildRequires:	SuiteSparse-CCOLAMD-devel
BuildRequires:	SuiteSparse-COLAMD-devel
BuildRequires:	SuiteSparse-config-devel
BuildRequires:	SuiteSparse-SPQR-devel
BuildRequires:	eigen3
BuildRequires:	glog-devel
BuildRequires:	gflags-devel
BuildRequires:	abseil-cpp-devel
BuildRequires:	lapack-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Ceres Solver is an open source C++ library for modeling and solving
large, complicated optimization problems. It is a feature rich, mature
and performant library which has been used in production at Google
since 2010. Ceres Solver can solve two kinds of problems.

1. Non-linear Least Squares problems with bounds constraints.
2. General unconstrained optimization problems.

%package devel
Summary:	Header files for %{name} library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{name} library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki %{name}.

%package apidocs
Summary:	API documentation for %{name} library
Summary(pl.UTF-8):	Dokumentacja API biblioteki %{name}
Group:		Documentation
# if not arch-dependent
BuildArch:	noarch

%description apidocs
API documentation for %{name} library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki %{name}.

%prep
%setup -q

%build
mkdir -p build
cd build
%ifarch %{ix86} x32
export LDFLAGS="%{rpmldflags} -Wl,--no-keep-memory -Wl,--reduce-memory-overheads"
%endif
%cmake ../ \
	-DBUILD_DOCUMENTATION:BOOL=ON

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install -C build \
	DESTDIR=$RPM_BUILD_ROOT

# Packaged in apidocs subpackage
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/html

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md
%{_libdir}/libceres.so.*.*.*
%ghost %{_libdir}/libceres.so.4

%files devel
%defattr(644,root,root,755)
%doc CONTRIBUTING.md
%{_libdir}/libceres.so
%{_includedir}/ceres
%{_libdir}/cmake/Ceres

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc build/docs/html/*
%endif
