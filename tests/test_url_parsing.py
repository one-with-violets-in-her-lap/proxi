from proxi.core.utils.url_parsing import get_origin_and_port

URLS_WITH_RESULTS = {
    "http://example.com": ("http://example.com", None),
    "https://example.com": ("https://example.com", None),
    "http://example.com/path/to/resource": (
        "http://example.com",
        None,
    ),
    "https://example.com/index.html?query=test#section": (
        "https://example.com",
        None,
    ),
    "http://username:password@example.com": (
        "http://username:password@example.com",
        None,
    ),
    "https://user123:pass456@secure.example.com/path": (
        "https://user123:pass456@secure.example.com",
        None,
    ),
    "http://example.com:8080": ("http://example.com", 8080),
    "http://localhost:3000/path": ("http://localhost", 3000),
    "https://127.0.0.1:443": ("https://127.0.0.1", 443),
    "socks5://127.0.0.1:1080": ("socks5://127.0.0.1", 1080),
    "socks5h://user:pass@proxyhost:1080": ("socks5h://user:pass@proxyhost", 1080),
    "socks4://proxy.example.com:1080": ("socks4://proxy.example.com", 1080),
}


def test_get_host_and_port():
    for url in URLS_WITH_RESULTS:
        expected_result = URLS_WITH_RESULTS[url]
        assert get_origin_and_port(url) == expected_result
