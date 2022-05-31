import urllib.request
import socket


def get_external_ip(host: str = '', ipv6_flag: bool = False) -> str:
    """ Return external IP. By default use https://api.ipify.org
        If no IPv6 address, service returning IPv4. With any exception return empty string

    :param host: string with name service to return ip
    :param ipv6_flag: if True - use https://api64.ipify.org.
    :return: String with external IP or empty string if any exception rised
    """
    if not host:
        host = 'https://api64.ipify.org' if ipv6_flag else 'https://api.ipify.org'
    try:
        result = urllib.request.urlopen(host).read().decode('utf8')
    except Exception:
        result = ''
    return result


def get_internal_ip() -> str:
    """ Return internal IP

    :return: String with internal IP
    """
    return socket.gethostbyname(socket.gethostname())


if __name__ == '__main__':
    print(f"External IPv4: {get_external_ip()}")
    print(f"External IPv6: {get_external_ip(ipv6_flag=True)}")
    print(f"Internal IP: {get_internal_ip()}")
