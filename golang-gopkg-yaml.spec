# If any of the following macros should be set otherwise,
# you can wrap any of them with the following conditions:
# - %%if 0%%{centos} == 7
# - %%if 0%%{?rhel} == 7
# - %%if 0%%{?fedora} == 23
# Or just test for particular distribution:
# - %%if 0%%{centos}
# - %%if 0%%{?rhel}
# - %%if 0%%{?fedora}
#
# Be aware, on centos, both %%rhel and %%centos are set. If you want to test
# rhel specific macros, you can use %%if 0%%{?rhel} && 0%%{?centos} == 0 condition.
# (Don't forget to replace double percentage symbol with single one in order to apply a condition)

# Generate devel rpm
%global with_devel 1
# Build project from bundled dependencies
%global with_bundled 0
# Build with debug info rpm
%global with_debug 0
# Run tests in check section
# both tests failing
%global with_check 0
# Generate unit-test rpm
%global with_unit_test 1

%if 0%{?with_debug}
%global _dwz_low_mem_die_limit 0
%else
%global debug_package   %{nil}
%endif

%global provider        github
%global provider_tld    com
%global project         go-yaml
%global repo            yaml
%global provider_prefix %{provider}.%{provider_tld}/%{project}/%{repo}
%global commit          53feefa2559fb8dfa8d81baad31be332c97d6c77
%global shortcommit     %(c=%{commit}; echo ${c:0:7})

%global import_path     gopkg.in/v2/yaml
%global import_path_sec gopkg.in/yaml.v2

%global v1_commit          1b9791953ba4027efaeb728c7355e542a203be5e
%global v1_shortcommit     %(c=%{v1_commit}; echo ${c:0:7})
%global v1_import_path     gopkg.in/v1/yaml
%global v1_import_path_sec gopkg.in/yaml.v1

%global devel_main      golang-gopkg-yaml-devel-v2

Name:           golang-gopkg-yaml
Version:        1
Release:        15%{?dist}
Summary:        Enables Go programs to comfortably encode and decode YAML values
License:        LGPLv3 with exceptions
URL:            https://%{provider_prefix}
Source0:        https://%{provider_prefix}/archive/%{commit}/yaml-%{shortcommit}.tar.gz
Source1:        https://%{provider_prefix}/archive/%{v1_commit}/yaml-%{v1_commit}.tar.gz

# e.g. el6 has ppc64 arch without gcc-go, so EA tag is required
ExclusiveArch:  %{?go_arches:%{go_arches}}%{!?go_arches:%{ix86} x86_64 aarch64 %{arm}}
# If go_compiler is not set to 1, there is no virtual provide. Use golang instead.
BuildRequires:  %{?go_compiler:compiler(go-compiler)}%{!?go_compiler:golang}
BuildRequires:  go-srpm-macros

%description
%{summary}

%if 0%{?with_devel}
%package devel
Summary:        Enables Go programs to comfortably encode and decode YAML values
BuildArch:      noarch

%if 0%{?with_check}
%endif

Provides:       golang(%{v1_import_path}) = %{version}-%{release}
Provides:       golang(%{v1_import_path_sec}) = %{version}-%{release}

%description devel
The yaml package enables Go programs to comfortably encode and decode YAML
values. It was developed within Canonical as part of the juju project, and
is based on a pure Go port of the well-known libyaml C library to parse and
generate YAML data quickly and reliably.

The yaml package is almost compatible with YAML 1.1, including support for
anchors, tags, etc. There are still a few missing bits, such as document
merging, base-60 floats (huh?), and multi-document unmarshalling. These
features are not hard to add, and will be introduced as necessary.

This package contains library source intended for
building other packages which use import path with
%{v1_import_path} prefix.

%package devel-v2
Summary:        Enables Go programs to comfortably encode and decode YAML values
BuildArch:      noarch

%if 0%{?with_check}
%endif

Provides:       golang(%{import_path}) = %{version}-%{release}
Provides:       golang(%{import_path_sec}) = %{version}-%{release}

%description devel-v2
The yaml package enables Go programs to comfortably encode and decode YAML
values. It was developed within Canonical as part of the juju project, and
is based on a pure Go port of the well-known libyaml C library to parse and
generate YAML data quickly and reliably.

The yaml package supports most of YAML 1.1 and 1.2,
including support for anchors, tags, map merging, etc.
Multi-document unmarshalling is not yet implemented, and base-60 floats
from YAML 1.1 are purposefully not supported since they're a poor design
 and are gone in YAML 1.2.

This package contains library source intended for
building other packages which use import path with
%{import_path} prefix.
%endif

%if 0%{?with_unit_test}
%package unit-test
Summary:         Unit tests for %{name} package

%if 0%{?with_check}
#Here comes all BuildRequires: PACKAGE the unit tests
#in %%check section need for running
BuildRequires:  golang(gopkg.in/check.v1)
%endif

Requires:  golang(gopkg.in/check.v1)

# test subpackage tests code from devel subpackage
Requires:        %{name}-devel = %{version}-%{release}
Requires:        %{name}-devel-v2 = %{version}-%{release}

%description unit-test
%{summary}

This package contains unit tests for project
providing packages with %{import_path} prefix.
%endif

%prep
%setup -q -n yaml-%{commit}
%setup -q -n yaml-%{v1_commit} -T -b 1

%build

%install
# source codes for building projects
%if 0%{?with_devel}
install -d -p %{buildroot}/%{gopath}/src/%{v1_import_path}/
install -d -p %{buildroot}/%{gopath}/src/%{v1_import_path_sec}/
# find all *.go but no *_test.go files and generate devel.file-list
for file in $(find . -iname "*.go" \! -iname "*_test.go") ; do
    install -d -p %{buildroot}/%{gopath}/src/%{v1_import_path}/$(dirname $file)
    cp -pav $file %{buildroot}/%{gopath}/src/%{v1_import_path}/$file
    echo "%%{gopath}/src/%%{v1_import_path}/$file" >> v1_devel.file-list
    install -d -p %{buildroot}/%{gopath}/src/%{v1_import_path_sec}/$(dirname $file)
    cp -pav $file %{buildroot}/%{gopath}/src/%{v1_import_path_sec}/$file
    echo "%%{gopath}/src/%%{v1_import_path_sec}/$file" >> v1_devel.file-list
done
pushd ../yaml-%{commit}
install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
install -d -p %{buildroot}/%{gopath}/src/%{import_path_sec}/
# find all *.go but no *_test.go files and generate devel.file-list
for file in $(find . -iname "*.go" \! -iname "*_test.go") ; do
    install -d -p %{buildroot}/%{gopath}/src/%{import_path}/$(dirname $file)
    cp -pav $file %{buildroot}/%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> ../yaml-%{v1_commit}/devel.file-list
    install -d -p %{buildroot}/%{gopath}/src/%{import_path_sec}/$(dirname $file)
    cp -pav $file %{buildroot}/%{gopath}/src/%{import_path_sec}/$file
    echo "%%{gopath}/src/%%{import_path_sec}/$file" >> ../yaml-%{v1_commit}/devel.file-list
done
popd
%endif

# testing files for this project
%if 0%{?with_unit_test}
install -d -p %{buildroot}/%{gopath}/src/%{v1_import_path}/
install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
# find all *_test.go files and generate unit-test.file-list
for file in $(find . -iname "*_test.go"); do
    install -d -p %{buildroot}/%{gopath}/src/%{v1_import_path}/$(dirname $file)
    cp -pav $file %{buildroot}/%{gopath}/src/%{v1_import_path}/$file
    echo "%%{gopath}/src/%%{v1_import_path}/$file" >> unit-test.file-list
done
pushd ../yaml-%{commit}
for file in $(find . -iname "*_test.go"); do
    install -d -p %{buildroot}/%{gopath}/src/%{import_path}/$(dirname $file)
    cp -pav $file %{buildroot}/%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> ../yaml-%{v1_commit}/unit-test.file-list
done
popd
%endif

%check
%if 0%{?with_check} && 0%{?with_unit_test} && 0%{?with_devel}
export GOPATH=%{buildroot}/%{gopath}:%{gopath}

%if ! 0%{?gotest:1}
%global gotest go test
%endif

%gotest %{import_path}
pushd ../yaml-%{v1_commit}
%gotest %{v1_import_path}
popd
%endif

#define license tag if not already defined
%{!?_licensedir:%global license %doc}

%if 0%{?with_devel}
%files devel -f v1_devel.file-list
%license LICENSE LICENSE.libyaml
%doc README.md
%dir %{gopath}/src/gopkg.in/v1
%dir %{gopath}/src/%{v1_import_path}
%dir %{gopath}/src/%{v1_import_path_sec}

%files devel-v2 -f devel.file-list
%license LICENSE LICENSE.libyaml
%doc README.md
%dir %{gopath}/src/gopkg.in/v2
%dir %{gopath}/src/%{import_path}
%dir %{gopath}/src/%{import_path_sec}
%endif

%if 0%{?with_unit_test}
%files unit-test -f unit-test.file-list
%license LICENSE LICENSE.libyaml
%doc README.md
%endif

%changelog
* Fri Dec 16 2016 Jan Chaloupka <jchaloup@redhat.com> - 1-15
- Polish the spec file
  related: #1250524

* Thu Aug 25 2016 jchaloup <jchaloup@redhat.com> - 1-14
- Enable devel and unit-test for epel7
  related: #1250524

* Thu Jul 21 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1-13
- https://fedoraproject.org/wiki/Changes/golang1.7

* Sun May 15 2016 jchaloup <jchaloup@redhat.com> - 1-12
- Bump to upstream 53feefa2559fb8dfa8d81baad31be332c97d6c77
  related: #1250524

* Sat Mar 05 2016 jchaloup <jchaloup@redhat.com> - 1-11
- Bump to upstream bef53efd0c76e49e6de55ead051f886bea7e9420
  related: #1250524

* Mon Feb 22 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1-10
- https://fedoraproject.org/wiki/Changes/golang1.6

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Aug 20 2015 jchaloup <jchaloup@redhat.com> - 1-8
- Choose the correct architecture
- Update unit-test subpackage
  related: #1250524

* Thu Aug 20 2015 jchaloup <jchaloup@redhat.com> - 1-7
- Update spec file to spec-2.0
  resolves: #1250524

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Dec 10 2014 jchaloup <jchaloup@redhat.com> - 1-5
- Update to gopkg.in/check.v2 but still provide gopkg.in/check.v1
  related: #1141875

* Fri Oct 10 2014 jchaloup <jchaloup@redhat.com> - 1-4
- Adding go test and deps on gopkg.in/check.v1
- Adding another Provides

* Mon Sep 15 2014 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1-3
- Resolves: rhbz#1141875 - newpackage
- no debug_package
- preserve timestamps
- do not redefine gopath

* Thu Aug 07 2014 Adam Miller <maxamillion@fedoraproject.org> - 1-2
- Fix import_path

* Tue Aug 05 2014 Adam Miller <maxamillion@fedoraproject.org> - 1-1
- First package for Fedora
