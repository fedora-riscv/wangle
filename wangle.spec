# Tests are not currently passing
%bcond_with tests

Name:           wangle
Version:        2020.10.26.00
Release:        2%{?dist}
Summary:        Framework for building services in a consistent/modular/composable way

License:        ASL 2.0
URL:            https://github.com/facebook/wangle
Source0:        %{url}/releases/download/v%{version}/%{name}-v%{version}.tar.gz
Patch0:         %{url}/commit/101e328981ddc7c7c6601f9cbb7eb9b2de38ef79.patch#/%{name}-%{version}-allow_overriding_version.patch

# Folly is known not to work on big-endian CPUs
# https://bugzilla.redhat.com/show_bug.cgi?id=1892807
ExcludeArch:    s390x

BuildRequires:  cmake
BuildRequires:  gcc-c++
# Library dependencies
BuildRequires:  fizz-devel
BuildRequires:  folly-devel

%description
Wangle is a library that makes it easy to build protocols, application clients,
and application servers.

It's like Netty + Finagle smooshed together, but in C++.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup -c -p1


%build
%cmake wangle \
  -DCMAKE_INSTALL_DIR=%{_libdir}/cmake/%{name} \
  -DPACKAGE_VERSION=%{version} \
  -DSO_VERSION=%{version}
%cmake_build


%install
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


%changelog
* Wed Oct 28 2020 Michel Alexandre Salim <salimma@fedoraproject.org> - 2020.10.26.00-2
- Add ExcludeArch on s390x due to dependency on folly

* Mon Oct 26 2020 Michel Alexandre Salim <salimma@fedoraproject.org> - 2020.10.26.00-1
- Initial package
