# Depends on fizz, which has linking issues on some platforms:
# https://bugzilla.redhat.com/show_bug.cgi?id=1893332
%ifarch i686 x86_64
%bcond_without static
%else
%bcond_with static
%endif

# Tests are not currently passing
%bcond_without tests

%global _static_builddir static_build

Name:           wangle
Version:        2021.12.20.00
Release:        %autorelease
Summary:        Framework for building services in a consistent/modular/composable way

License:        ASL 2.0
URL:            https://github.com/facebook/wangle
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
# disable failing tests, see patch for context
Patch0:         %{name}-disable_failed_tests.patch

# Folly is known not to work on big-endian CPUs
# https://bugzilla.redhat.com/show_bug.cgi?id=1892807
ExcludeArch:    s390x

BuildRequires:  cmake
BuildRequires:  gcc-c++
# Library dependencies
BuildRequires:  fizz-devel
BuildRequires:  folly-devel
%if %{with static}
BuildRequires:  fizz-static
BuildRequires:  folly-static
%endif
%if %{with tests}
BuildRequires:  gmock-devel
BuildRequires:  gtest-devel
%endif


%global _description %{expand:
Wangle is a library that makes it easy to build protocols, application clients,
and application servers.

It's like Netty + Finagle smooshed together, but in C++.}

%description %{_description}


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel %{_description}
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%if %{with static}
%package        static
Summary:        Static development libraries for %{name}
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}

%description    static %{_description}

The %{name}-static package contains static libraries for
developing applications that use %{name}.
%endif


%prep
%autosetup -p1


%build
%cmake wangle \
%if %{with tests}
  -DBUILD_TESTS=ON \
%else
  -DBUILD_TESTS=OFF \
%endif
  -DCMAKE_INSTALL_DIR=%{_libdir}/cmake/%{name} \
  -DPACKAGE_VERSION=%{version} \
  -DSO_VERSION=%{version}
%cmake_build

%if %{with static}
# static build
mkdir %{_static_builddir}
cd %{_static_builddir}
%cmake ../wangle \
  -DBUILD_SHARED_LIBS=OFF \
  -DBUILD_TESTS=OFF \
  -DCMAKE_INSTALL_DIR=%{_libdir}/cmake/%{name}-static \
  -DFIZZ_ROOT=%{_libdir}/cmake/fizz-static \
  -DFOLLY_ROOT=%{_libdir}/cmake/folly-static \
  -DPACKAGE_VERSION=%{version}
%cmake_build
%endif


%install
%if %{with static}
# static build
pushd %{_static_builddir}
%cmake_install
popd
%endif

%cmake_install

find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'


%if %{with tests}
%check
%ctest
%endif


%files
%license LICENSE
%{_libdir}/*.so.*

%files devel
%doc CONTRIBUTING.md README.md tutorial.md
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/cmake/%{name}

%if %{with static}
%files static
%{_libdir}/*.a
%{_libdir}/cmake/%{name}-static
%endif


%changelog
%autochangelog
