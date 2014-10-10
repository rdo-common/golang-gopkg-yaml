%global debug_package   %{nil}
%global commit          1b9791953ba4027efaeb728c7355e542a203be5e
%global shortcommit     %(c=%{commit}; echo ${c:0:7})
%global import_path     gopkg.in/v1/yaml
%global import_path_sec gopkg.in/yaml.v1

Name:           golang-gopkg-yaml
Version:        1
Release:        4%{?dist}
Summary:        Enables Go programs to comfortably encode and decode YAML values
License:        LGPLv3 with exceptions
URL:            http://%{import_path}
Source0:        https://github.com/go-yaml/yaml/archive/%{commit}/yaml-%{commit}.tar.gz
BuildArch:      noarch

%description
%{summary}

%package devel
BuildRequires:  golang >= 1.2.1-3
BuildRequires:  golang(gopkg.in/check.v1)
Requires:       golang >= 1.2.1-3
Summary:        Enables Go programs to comfortably encode and decode YAML values
Provides:       golang(%{import_path}) = %{version}-%{release}
Provides:       golang(%{import_path_sec}) = %{version}-%{release}

%description devel
%{summary}

The yaml package enables Go programs to comfortably encode and decode YAML
values. It was developed within Canonical as part of the juju project, and
is based on a pure Go port of the well-known libyaml C library to parse and
generate YAML data quickly and reliably.

The yaml package is almost compatible with YAML 1.1, including support for
anchors, tags, etc. There are still a few missing bits, such as document
merging, base-60 floats (huh?), and multi-document unmarshalling. These
features are not hard to add, and will be introduced as necessary.

%prep
%setup -n yaml-%{commit} -q

%build

%install
install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
cp -pav *.go %{buildroot}/%{gopath}/src/%{import_path}/
install -d -p %{buildroot}/%{gopath}/src/%{import_path_sec}/
cp -pav *.go %{buildroot}/%{gopath}/src/%{import_path_sec}/

%check
GOPATH=%{buildroot}%{gopath}:%{gopath} go test %{import_path_sec}

%files devel
%doc LICENSE LICENSE.libyaml README.md
%dir %{gopath}/src/gopkg.in
%dir %{gopath}/src/gopkg.in/v1
%dir %{gopath}/src/%{import_path}
%dir %{gopath}/src/%{import_path_sec}
%{gopath}/src/%{import_path}/*.go
%{gopath}/src/%{import_path_sec}/*.go

%changelog
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
