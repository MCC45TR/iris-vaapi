# iris-vaapi

An experimental VA-API userspace driver for the Qualcomm Iris1/Venus decoder
on Xiaomi Pad 5 (`nabu`, SM8150).

This is a fork of [CFM880/iris-vaapi](https://github.com/CFM880/iris-vaapi).
The driver is original work by ChengFangming/CFM880; the SENEMOS branch adds
Fedora packaging and COPR integration. Please retain that attribution in
derived packages and source distributions.

> The driver and kernel support are experimental. Keep a software-decoding
> fallback and do not treat a successful package build as hardware validation.

## Status

- H.264 decode through VA-API and V4L2 stateless requests
- HEVC Main/Main10 support
- VP9 Profile 0/Profile 2 support
- DMA-BUF and DRM PRIME output paths
- Optional Vulkan copy path when Vulkan development files are available
- Test programs for VA-API, V4L2, H.264, HEVC, VP9, stress, and surface fences

The matching Nabu kernel implementation is maintained in
[CFM880/nabu-iris](https://github.com/CFM880/nabu-iris). The Linux 7.2.2
SENEMOS integration combines that work with the Nabu camera overlay.

## Dependencies

Fedora development packages include a C compiler, `make`, `pkgconf-pkg-config`,
`libva-devel`, and `libdrm-devel`. Vulkan support is enabled automatically when
the Vulkan package metadata is available.

## Building and testing

```sh
make
make check
```

The driver is created as `build/iris_drv_video.so`. Additional test binaries
are placed in `build/`.

## Installing

```sh
sudo make install
```

For a temporary test without installing system-wide:

```sh
LIBVA_DRIVERS_PATH=$PWD/build LIBVA_DRIVER_NAME=iris vainfo
```

The kernel must expose a working `qcom_iris` V4L2 decoder, compatible firmware,
and the required DMA heap. The Fedora RPM installs the matching DMA-heap udev
rule and a `qcom_iris` modprobe configuration.

## Applications

Applications that support VA-API can select the driver with:

```sh
LIBVA_DRIVER_NAME=iris application-name
```

Browser and FFmpeg setup details are documented in
[`docs/video-decode-setup.en.md`](docs/video-decode-setup.en.md).

## Fedora COPR packaging

The `senemos-fedora-copr` branch contains `iris-vaapi-nabu.spec` and a `srpm`
Make target for SCM-based automatic COPR builds. The package is intentionally
named `iris-vaapi-nabu` to make its device-specific and experimental scope
clear.

## Known limitations

- This is specific to the Nabu/Iris1 integration and is not a generic Qualcomm
  VA-API implementation.
- Codec and application behavior depends on the matching kernel, firmware,
  format negotiation, and zero-copy path.
- Build success does not prove decode correctness. Validation should include
  `vainfo`, representative H.264/HEVC/VP9 samples, and sustained playback.

## License and attribution

See [LICENSE](LICENSE) and the SPDX identifiers in individual files. Original
authorship and license notices from ChengFangming/CFM880 must be preserved.
