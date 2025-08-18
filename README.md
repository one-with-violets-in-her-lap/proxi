![Proxi logo](./readme-assets/logo.png)

# Proxi

Little utility for managing proxy preferences in Linux. It does not forcefully tunnel all your requests, but
rather tells the apps to use specified proxy. This allows a more flexible control over which apps should
use a proxy and which apps should not

Quick command line example:

```sh
# Using a proxy set by Proxi
curl ifconfig.me

# Disabling a proxy for a specific app
HTTPS_PROXY="" wget https://example.com
```

![Screenshot of the Proxi app interface showing proxy profiles named 'work',
'browsing', and 'profile 4'. The 'work' profile is active with proxy addresses listed
in HTTP, HTTPS, and SOCKS5 formats. A toggle switch indicates that proxy preferences are enabled.
Cartoon-style characters are drawn at the top right corner.](./readme-assets/screenshot.jpg)

## OS Compatibility

The app was tested with following Linux systems:

- GNOME-based distros (or systems with [gsettings](https://wiki.gentoo.org/wiki/Gsettings) support, which
  is enough)
    - Examples: Cinnamon, Ubuntu

- Distros with KDE 6
    - Examples: Manjaro KDE, Kubuntu

Other Linux systems may also work, but can require additional setup

## Installation

Install an [archive with an executable](https://github.com/one-with-violets-in-her-lap/proxi/releases/latest) and extract it:

```shell
tar -xf ./proxi.tar.gz
```

You can run it like that:

```shell
./proxi/proxi
```

To make it more convenient, add the binary to your shell PATH:

`~/.bashrc` (example):

```shell
PATH=$PATH:/mnt/1-tb-AGI1K0GIMAI/apps/proxi
```

### Integration with shell and unsupported systems

By default, the app only updates the settings of your desktop environment. But it also generates a setup script (`~/proxi_setup.sh`)
that you can use if you want to set a proxy for command line programs in your shell. To make this script
always run on shell startup, include it in your profile (e.g. `~/.bash_profile` or `~/.zshenv`):

```sh
if [[ -e ~/proxi_setup.sh ]]; then
    . ~/proxi_setup.sh
fi
```

> :eyes: You can also use this script to integrate Proxi on unsupported WM or DE by running it on startup (e.g. ~/.xsessionrc)

TODO: run from source
