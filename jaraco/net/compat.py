"""
Some Python builds are missing essential constants, but works fine if the
constants are defined. This module restores some of those constants until
such issues can be resolved.
See http://mail.python.org/pipermail/python-list/2008-May/489377.html
and http://bugs.python.org/issue6926
and https://bugs.python.org/issue29515
"""

import sys
import platform
import socket

from jaraco.functools import call_aside


constants = dict(
    # From Python 2.5 Intel x86 Windows
    AF_APPLETALK=16,
    AF_DECnet=12,
    AF_INET=2,
    AF_INET6=23,
    AF_IPX=6,
    AF_IRDA=26,
    AF_SNA=11,
    AF_UNSPEC=0,
    AI_CANONNAME=2,
    AI_NUMERICHOST=4,
    AI_PASSIVE=1,
    EAI_AGAIN=11002,
    EAI_BADFLAGS=10022,
    EAI_FAIL=11003,
    EAI_FAMILY=10047,
    EAI_MEMORY=8,
    EAI_NODATA=11001,
    EAI_NONAME=11001,
    EAI_SERVICE=10109,
    EAI_SOCKTYPE=10044,
    EBADF=9,
    INADDR_ALLHOSTS_GROUP=-536870911,
    INADDR_ANY=0,
    INADDR_BROADCAST=-1,
    INADDR_LOOPBACK=2130706433,
    INADDR_MAX_LOCAL_GROUP=-536870657,
    INADDR_NONE=-1,
    INADDR_UNSPEC_GROUP=-536870912,
    IPPORT_RESERVED=1024,
    IPPORT_USERRESERVED=5000,
    IPPROTO_AH=51,
    IPPROTO_DSTOPTS=60,
    IPPROTO_ESP=50,
    IPPROTO_FRAGMENT=44,
    IPPROTO_GGP=3,
    IPPROTO_HOPOPTS=0,
    IPPROTO_ICMP=1,
    IPPROTO_ICMPV6=58,
    IPPROTO_IDP=22,
    IPPROTO_IGMP=2,
    IPPROTO_IP=0,
    IPPROTO_IPV4=4,
    IPPROTO_IPV6=41,
    IPPROTO_MAX=256,
    IPPROTO_ND=77,
    IPPROTO_NONE=59,
    IPPROTO_PUP=12,
    IPPROTO_RAW=255,
    IPPROTO_ROUTING=43,
    IPPROTO_TCP=6,
    IPPROTO_UDP=17,
    IPV6_HOPLIMIT=21,
    IPV6_JOIN_GROUP=12,
    IPV6_LEAVE_GROUP=13,
    IPV6_MULTICAST_HOPS=10,
    IPV6_MULTICAST_IF=9,
    IPV6_MULTICAST_LOOP=11,
    IPV6_PKTINFO=19,
    IPV6_UNICAST_HOPS=4,
    IP_ADD_MEMBERSHIP=12,
    IP_DROP_MEMBERSHIP=13,
    IP_HDRINCL=2,
    IP_MULTICAST_IF=9,
    IP_MULTICAST_LOOP=11,
    IP_MULTICAST_TTL=10,
    IP_OPTIONS=1,
    IP_TOS=3,
    IP_TTL=4,
    MSG_DONTROUTE=4,
    MSG_OOB=1,
    MSG_PEEK=2,
    NI_DGRAM=16,
    NI_MAXHOST=1025,
    NI_MAXSERV=32,
    NI_NAMEREQD=4,
    NI_NOFQDN=1,
    NI_NUMERICHOST=2,
    NI_NUMERICSERV=8,
    SHUT_RD=0,
    SHUT_RDWR=2,
    SHUT_WR=1,
    SOCK_DGRAM=2,
    SOCK_RAW=3,
    SOCK_RDM=4,
    SOCK_SEQPACKET=5,
    SOCK_STREAM=1,
    SOL_IP=0,
    SOL_SOCKET=65535,
    SOL_TCP=6,
    SOL_UDP=17,
    SOMAXCONN=2147483647,
    SO_ACCEPTCONN=2,
    SO_BROADCAST=32,
    SO_DEBUG=1,
    SO_DONTROUTE=16,
    SO_ERROR=4103,
    SO_EXCLUSIVEADDRUSE=-5,
    SO_KEEPALIVE=8,
    SO_LINGER=128,
    SO_OOBINLINE=256,
    SO_RCVBUF=4098,
    SO_RCVLOWAT=4100,
    SO_RCVTIMEO=4102,
    SO_REUSEADDR=4,
    SO_SNDBUF=4097,
    SO_SNDLOWAT=4099,
    SO_SNDTIMEO=4101,
    SO_TYPE=4104,
    SO_USELOOPBACK=64,
    SSL_ERROR_EOF=8,
    SSL_ERROR_INVALID_ERROR_CODE=9,
    SSL_ERROR_SSL=1,
    SSL_ERROR_SYSCALL=5,
    SSL_ERROR_WANT_CONNECT=7,
    SSL_ERROR_WANT_READ=2,
    SSL_ERROR_WANT_WRITE=3,
    SSL_ERROR_WANT_X509_LOOKUP=4,
    SSL_ERROR_ZERO_RETURN=6,
    TCP_NODELAY=1,
)
constants.update(
    # from Python 2.6.2 AMD64 Windows
    AF_APPLETALK=16,
    AF_DECnet=12,
    AF_INET=2,
    AF_INET6=23,
    AF_IPX=6,
    AF_IRDA=26,
    AF_SNA=11,
    AF_UNSPEC=0,
    AI_ADDRCONFIG=1024,
    AI_ALL=256,
    AI_CANONNAME=2,
    AI_NUMERICHOST=4,
    AI_NUMERICSERV=8,
    AI_PASSIVE=1,
    AI_V4MAPPED=2048,
    EAI_AGAIN=11002,
    EAI_BADFLAGS=10022,
    EAI_FAIL=11003,
    EAI_FAMILY=10047,
    EAI_MEMORY=8,
    EAI_NODATA=11001,
    EAI_NONAME=11001,
    EAI_SERVICE=10109,
    EAI_SOCKTYPE=10044,
    EBADF=9,
    INADDR_ALLHOSTS_GROUP=-536870911,
    INADDR_ANY=0,
    INADDR_BROADCAST=-1,
    INADDR_LOOPBACK=2130706433,
    INADDR_MAX_LOCAL_GROUP=-536870657,
    INADDR_NONE=-1,
    INADDR_UNSPEC_GROUP=-536870912,
    IPPORT_RESERVED=1024,
    IPPORT_USERRESERVED=5000,
    IPPROTO_ICMP=1,
    IPPROTO_IP=0,
    IPPROTO_RAW=255,
    IPPROTO_TCP=6,
    IPPROTO_UDP=17,
    IPV6_CHECKSUM=26,
    IPV6_DONTFRAG=14,
    IPV6_HOPLIMIT=21,
    IPV6_HOPOPTS=1,
    IPV6_JOIN_GROUP=12,
    IPV6_LEAVE_GROUP=13,
    IPV6_MULTICAST_HOPS=10,
    IPV6_MULTICAST_IF=9,
    IPV6_MULTICAST_LOOP=11,
    IPV6_PKTINFO=19,
    IPV6_RECVRTHDR=38,
    IPV6_RTHDR=32,
    IPV6_UNICAST_HOPS=4,
    IPV6_V6ONLY=27,
    IP_ADD_MEMBERSHIP=12,
    IP_DROP_MEMBERSHIP=13,
    IP_HDRINCL=2,
    IP_MULTICAST_IF=9,
    IP_MULTICAST_LOOP=11,
    IP_MULTICAST_TTL=10,
    IP_OPTIONS=1,
    IP_RECVDSTADDR=25,
    IP_TOS=3,
    IP_TTL=4,
    MSG_CTRUNC=512,
    MSG_DONTROUTE=4,
    MSG_OOB=1,
    MSG_PEEK=2,
    MSG_TRUNC=256,
    NI_DGRAM=16,
    NI_MAXHOST=1025,
    NI_MAXSERV=32,
    NI_NAMEREQD=4,
    NI_NOFQDN=1,
    NI_NUMERICHOST=2,
    NI_NUMERICSERV=8,
    RCVALL_MAX=3,
    RCVALL_OFF=0,
    RCVALL_ON=1,
    RCVALL_SOCKETLEVELONLY=2,
    SHUT_RD=0,
    SHUT_RDWR=2,
    SHUT_WR=1,
    SIO_RCVALL=2550136833,
    SOCK_DGRAM=2,
    SOCK_RAW=3,
    SOCK_RDM=4,
    SOCK_SEQPACKET=5,
    SOCK_STREAM=1,
    SOL_IP=0,
    SOL_SOCKET=65535,
    SOL_TCP=6,
    SOL_UDP=17,
    SOMAXCONN=2147483647,
    SO_ACCEPTCONN=2,
    SO_BROADCAST=32,
    SO_DEBUG=1,
    SO_DONTROUTE=16,
    SO_ERROR=4103,
    SO_EXCLUSIVEADDRUSE=-5,
    SO_KEEPALIVE=8,
    SO_LINGER=128,
    SO_OOBINLINE=256,
    SO_RCVBUF=4098,
    SO_RCVLOWAT=4100,
    SO_RCVTIMEO=4102,
    SO_REUSEADDR=4,
    SO_SNDBUF=4097,
    SO_SNDLOWAT=4099,
    SO_SNDTIMEO=4101,
    SO_TYPE=4104,
    SO_USELOOPBACK=64,
    SSL_ERROR_EOF=8,
    SSL_ERROR_INVALID_ERROR_CODE=9,
    SSL_ERROR_SSL=1,
    SSL_ERROR_SYSCALL=5,
    SSL_ERROR_WANT_CONNECT=7,
    SSL_ERROR_WANT_READ=2,
    SSL_ERROR_WANT_WRITE=3,
    SSL_ERROR_WANT_X509_LOOKUP=4,
    SSL_ERROR_ZERO_RETURN=6,
    TCP_MAXSEG=4,
    TCP_NODELAY=1,
)


@call_aside
def patch():
    if platform.system() != 'Windows':
        return
    if sys.version_info < (3, 8):
        return

    for item in constants.items():
        socket.__dict__.setdefault(*item)
