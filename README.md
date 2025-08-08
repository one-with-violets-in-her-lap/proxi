![Proxi logo](./readme-assets/logo.png)

# Proxi

Little utility for managing proxy preferences. It does not forcefully tunnel all your requests, but
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
Cartoon-style characters are drawn at the top right corner.](./readme-assets/logo.png)

