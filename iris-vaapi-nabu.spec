Name:           iris-vaapi-nabu
Version:        0.1.0
Release:        2.alpha%{?dist}
Summary:        Experimental VA-API driver for Qualcomm SM8150 Iris1
License:        GPL-2.0-or-later
URL:            https://github.com/CFM880/iris-vaapi
Source0:        %{name}-%{version}.tar.gz
ExclusiveArch:  aarch64

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconfig(libva)
BuildRequires:  pkgconfig(libva-drm)
BuildRequires:  pkgconfig(vulkan)
Requires:       libva
Requires:       systemd-udev

%description
The original ChengFangming/CFM880 experimental VA-API userspace driver for
the Qualcomm SM8150 Iris1 stateful V4L2 decoder used by Xiaomi Pad 5.

Upstream and original work: https://github.com/CFM880/iris-vaapi
Matching kernel work: https://github.com/CFM880/nabu-iris

%prep
%autosetup

%build
%make_build

%install
%make_install DRIVERDIR=%{_libdir}/dri
install -Dm0644 tools/99-iris-dmaheap.rules \
    %{buildroot}%{_udevrulesdir}/99-iris-dmaheap.rules
install -Dm0644 tools/99-iris-vaapi.conf \
    %{buildroot}%{_modprobedir}/99-iris-vaapi.conf

%check
make check
test -s %{buildroot}%{_libdir}/dri/iris_drv_video.so

%files
%license COPYING
%doc README.md docs/
%{_libdir}/dri/iris_drv_video.so
%{_udevrulesdir}/99-iris-dmaheap.rules
%{_modprobedir}/99-iris-vaapi.conf

%changelog
* Tue Sep 01 2026 mcc45tr <mcc45tr@gmail.com> - 0.1.0-2.alpha
- Track CFM880 revision fe8aa303 and convert the COPR package to SCM auto-build.
