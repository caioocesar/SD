from sys import exit
from socket import *
from threading import *
import struct

lock = Lock()
def_cod = "utf-8"

class Comunicacao():
    def __init__(self):
        # Inicializando o socket
        self._sock_receptor = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
        self._sock_receptor.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

        self._sock_remetente = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
        self._sock_remetente.setsockopt(IPPROTO_IP, IP_MULTICAST_TTL, 1)
        self._sock_receptor.setblocking(False)

        self.mcast_group = '239.0.0.1'
        self.mcast_port = 6000
        self.mcast_addrss = (self.mcast_group, self.mcast_port)
        self.p_len = 2
        self._client_list = []

        # self._sock.setblocking(False) # Tornando o socket com o tipo de chamada não bloqueante

    def bind(self):
        try:
            self._sock_receptor.bind(('', self.mcast_port))

            mreq = struct.pack("4sl", inet_aton(self.mcast_group), INADDR_ANY)

            self._sock_receptor.setsockopt(IPPROTO_IP, IP_ADD_MEMBERSHIP, mreq)
        except Exception as e:
            print(str(e))

    def receber(self):
        global recv_msg

        if recv_msg == b'':
            self._receber()

        msg = recv_msg
        recv_msg = b''
        return msg.decode(def_cod)

    def enviar(self, msg):
        ''' Método para envio de mensagens'''
        data = self._cod_msg(msg)

        total_len = len(data)
        totalsent = 0

        while totalsent < total_len:
            sent = self._sock_remetente.sendto(data[totalsent:], self.mcast_addrss)  # min(totalsent + self.LENMAX, total_len - totalsent)
            if sent == 0:
                raise RuntimeError("enviar: socket connection broken")

            totalsent += sent

    def _receber(self):
        ''' Método que roda na thread para receber os dados que são recebidos da rede e concatenar no self.recvBuffer'''
        hdr_len = None
        header = None
        msg = None

        if hdr_len is None:
            hdr_len = self._read_protoheader()

        if hdr_len is not None:
            if header is None:
                header = self._read_header(hdr_len)

        if header:
            if msg is None:
                msg = self._read_msg(header)

        return msg

    def _read_protoheader(self):
        chunks = []
        bytes_recv = 0
        while bytes_recv < self.p_len:
            chunk = self._sock_receptor.recv(min(LENMAX, self.p_len - bytes_recv))
            if chunk == b'':
                raise RuntimeError("connection broken")
            chunks.append(chunk)
            bytes_recv = bytes_recv + len(chunk)
        return int(b''.join(chunks))

    def _read_header(self, hdr_len):
        # Interessante caso o cabeçalho tenha mais de um item
        # for reqhdr in ("byteorder","content-length","content-type","content-encoding",):
        #     if reqhdr not in self.jsonheader:
        #         raise ValueError(f'Missing required header "{reqhdr}".')
        chunks = []
        bytes_recv = 0
        while bytes_recv < hdr_len:
            chunk = self._sock_receptor.recv(min(LENMAX, hdr_len - bytes_recv))
            if chunk == b'':
                raise RuntimeError("connection broken")
            chunks.append(chunk)
            bytes_recv = bytes_recv + len(chunk)
        return int(b''.join(chunks))

    def _read_msg(self, msg_len):
        chunks = []
        bytes_recv = 0
        while bytes_recv < msg_len:
            chunk = self._sock_receptor.recv(min(LENMAX, msg_len - bytes_recv))
            if chunk == b'':
                raise RuntimeError("connection broken")
            chunks.append(chunk)
            bytes_recv = bytes_recv + len(chunk)
        return b''.join(chunks)

    def _cod_msg(self, msg):
        msg_cod = msg.encode(def_cod)
        HDRLEN = str(len(msg_cod))  # tamanho do cabeçalho
        prt_hdr = str(len(HDRLEN))  # tamanho do proto cabeçalho
        if len(prt_hdr) < self.p_len:
            # caso o proto cabeçalho tenha uma quantidade de algarismos menor do que a esperada, será concatenado a quantidade de zeros necessaria na frente
            prt_hdr = '0' * (self.p_len - len(prt_hdr)) + prt_hdr
        elif len(prt_hdr) > self.p_len:
            raise RuntimeError("Proto Cabeçalho maior que", self.p_len, "bytes")

        return (prt_hdr + HDRLEN).encode(def_cod) + msg_cod  # Dado que será efetivamente enviado = (proto cabeçalho + cabeçalho).encode + mensagem codificada
