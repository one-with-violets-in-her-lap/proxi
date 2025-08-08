import urllib.parse


def get_origin_and_port(url: str):
    parsed_url = urllib.parse.urlparse(url)

    host = f"{parsed_url.scheme}://"

    if parsed_url.username is not None and parsed_url.password is not None:
        host += f"{parsed_url.username}:{parsed_url.password}@"

    host += f"{parsed_url.hostname}"

    return (host, parsed_url.port)
