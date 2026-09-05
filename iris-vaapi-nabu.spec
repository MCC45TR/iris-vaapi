Name:           iris-vaapi-nabu
Version:        0.1.0
Release:        7.alpha%{?dist}
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
# libva derives "msm" from the DRM driver when callers do not inherit the
# graphical-session environment.  Keep the canonical Iris filename and expose
# the corresponding DRM-driver alias for shells, services, and test tools.
ln -s iris_drv_video.so %{buildroot}%{_libdir}/dri/msm_drv_video.so
install -Dm0644 tools/99-iris-dmaheap.rules \
    %{buildroot}%{_prefix}/lib/udev/rules.d/99-iris-dmaheap.rules
install -Dm0644 tools/99-iris-vaapi.conf \
    %{buildroot}%{_prefix}/lib/modprobe.d/99-iris-vaapi.conf
install -Dm0644 tools/90-iris-vaapi-nabu.conf \
    %{buildroot}%{_prefix}/lib/environment.d/90-iris-vaapi-nabu.conf

%check
make check
test -s %{buildroot}%{_libdir}/dri/iris_drv_video.so
test "$(readlink %{buildroot}%{_libdir}/dri/msm_drv_video.so)" = \
    iris_drv_video.so
grep -Fxq 'options qcom_iris allow_fw_boot=1 cached_capture=1' \
    %{buildroot}%{_prefix}/lib/modprobe.d/99-iris-vaapi.conf
grep -Fxq 'LIBVA_DRIVER_NAME=iris' \
    %{buildroot}%{_prefix}/lib/environment.d/90-iris-vaapi-nabu.conf
grep -Fxq 'GST_VA_ALL_DRIVERS=1' \
    %{buildroot}%{_prefix}/lib/environment.d/90-iris-vaapi-nabu.conf
! grep -E '"/dev/video0"' src/decode.c src/iris_vaapi.c src/v4l2_dec.c

%files
%license COPYING
%doc README.md docs/
%{_libdir}/dri/iris_drv_video.so
%{_libdir}/dri/msm_drv_video.so
%{_prefix}/lib/udev/rules.d/99-iris-dmaheap.rules
%{_prefix}/lib/modprobe.d/99-iris-vaapi.conf
%{_prefix}/lib/environment.d/90-iris-vaapi-nabu.conf

%changelog
* Sat Sep 05 2026 mcc45tr <mcc45tr@gmail.com> - 0.1.0-7.alpha
- Let libva discover Iris from the MSM DRM driver in shells and services.

* Sat Sep 05 2026 mcc45tr <mcc45tr@gmail.com> - 0.1.0-6.alpha
- Resume drained V4L2 decoder sessions instead of reopening Iris per frame.
- Expose validated H.264, HEVC and VP9 decoders through GStreamer's VA plugin.

* Sat Sep 05 2026 mcc45tr <mcc45tr@gmail.com> - 0.1.0-5.alpha
- Discover the Iris decoder dynamically when camera nodes occupy /dev/video0.
- Validate the selected node by driver, card name, and M2M capabilities.

* Sat Sep 05 2026 mcc45tr <mcc45tr@gmail.com> - 0.1.0-4.alpha
- Enable the documented Iris firmware boot gate for working V4L2 sessions.
- Select the Nabu Iris VA-API driver automatically in graphical sessions.

* Tue Sep 01 2026 mcc45tr <mcc45tr@gmail.com> - 0.1.0-3.alpha
- Use stable /usr/lib paths across supported Fedora releases.

* Tue Sep 01 2026 mcc45tr <mcc45tr@gmail.com> - 0.1.0-2.alpha
- Track CFM880 revision fe8aa303 and convert the COPR package to SCM auto-build.
