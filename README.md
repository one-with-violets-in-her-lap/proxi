![Proxi logo](./logo.png)

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
