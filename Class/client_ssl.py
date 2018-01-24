import socket
import ssl


"""
接受 query
接受 post
"""


def get(url):
    """
    https://movie.douban.com/top250
    p = https
    u = movie.douban.com/top250
    """
    # p, u = url.split('://')
    u = url.split('://')[1]
    i = u.find('/')
    host = u[:i]
    path = u[i:]

    port = 2000
    # port = 443
    # s = ssl.wrap_socket(socket.socket())
    s = socket.socket()

    s.connect((host, port))

    request = 'GET {} HTTP/1.1\r\nhost:{}\r\nGua: 好\r\n\r\nname=gua'.format(path, host)
    encoding = 'utf-8'
    s.send(request.encode(encoding))

    response = b''
    buffer_size = 1024
    while True:
        r = s.recv(buffer_size)
        response += r
        if len(r) < buffer_size:
            break
    return response.decode(encoding)


def main():
    # url = 'https://movie.douban.com/top250'
    url = 'http://localhost/gua'
    r = get(url)
    print(r)


if __name__ == '__main__':
    main()
