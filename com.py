
from sys import exit
from socket import *
from threading import *

def_cod = 'utf-8'
TESTE = False

###########

received_msg = ''
lock = Lock()

class ClientSocket(Thread):
    def __init__(self, sock=None):
        super().__init__()

        if sock is None:
            self.sock = socket(AF_INET, SOCK_STREAM)
        else:
            self.sock = sock

        self._hdr_num = 2 # numero de cabeçalhos
        self.pHdr_len = 2 # tamanho do proto cabeçalho
        self.recv_msg = b'' # msg recebida
        self.onThread = True # indicador para desligar Thread
        self._need_read = False
        self.LENMAX = 1400

        try:
            addrsFileLines = open("addrs.txt", "r").readlines()
        except Exception as e:
            host = 'localhost'
            port = '4446'
            print(str(e) + "\nCreating a file with default host:\'" + host + "\', port:" + port)
            addrs = open("addrs.txt", "w+")
            addrs.write(host+"\n"+port)
        else:
            self.host, self.port = addrsFileLines[0][:-1], int(addrsFileLines[1]) # host e port padrôes lidos do arquivo

    def run(self):
        # Método que implementa o que a Thread roda
        while self.onThread:
            lock.acquire()
            try:
                self.recv_msg = self._receive()
            except ConnectionAbortedError:
                pass

    def defineAddrs(self):
        ans = input(
            "_______________________________\n"
            "[ENTER] - Continuar com padrão\n"
            "1 ------- Definir host e port\n"
            "2 ------- Definir host\n"
            "3 ------- Definir port\n"
            "0 ------- Sair do programa\n"
            "_______________________________\n")
        print()

        if ans == '0':
            exit(0)
        elif ans == '1':
            self.host = input("host:")
            self.port = int(input("port:"))
        elif ans == '2':
            self.host = input("host:")
        elif ans == '3':
            self.port = int(input("port:"))

        addrsFile = open("addrs.txt", "w+")
        addrsFile.write(self.host + "\n" + str(self.port))

    def connect(self, host=None, port=None):
        if host is not None:
            self.host = host
        if port is not None:
            self.port = port
        try:
            self.sock.connect((self.host, self.port))
            self.start()
            return True

        except Exception as e:
            print(e)
            return False

    def connect_pd(self):
        while not self.connect():
            ans = input(
                "_______________________________\n"
                "[ENTER] - Tentar conectar novamente\n"
                "0 - Sair do programa\n"
                "_______________________________\n")
            print()

            if ans == '0':
                exit(0)

        else:
            self.sock.send(str(self._hdr_num).encode(def_cod))

    def send(self, msg):
        ''' Método para envio de mensagens'''
        msg_cod = msg.encode(def_cod)
        HDRLEN = str(len(msg_cod)) # tamanho do cabeçalho
        prt_hdr = str(len(HDRLEN)) # tamanho do proto cabeçalho
        if len(prt_hdr) < self.pHdr_len: # caso o proto cabeçalho tenha uam quantidade de algarismos menor do que a esperada, será concatenado a quantidade de zeros necessaria na frente
            prt_hdr = '0'*(self.pHdr_len-len(prt_hdr)) + prt_hdr
        elif len(prt_hdr) > self.pHdr_len:
            raise RuntimeError("Proto Cabeçalho maior que", self.pHdr_len,"bytes")
        data = (prt_hdr + HDRLEN).encode(def_cod) + msg_cod # Dado que será efetivamente enviado = (proto cabeçalho + cabeçalho).encode + mensagem codificada
        total_len = len(data)
        totalsent = 0

        while totalsent < total_len:
            sent = self.sock.send(data[totalsent:]) # min(totalsent + self.LENMAX, total_len - totalsent)
            if sent == 0:
                raise RuntimeError("socket connection broken")

            totalsent += sent

    def _receive(self):
        ''' Método que roda na thread para receber os dados que são recebidos da rede e concatenar no self.recvBuffer'''
        hdr_len = None
        header = None
        msg = None

        while hdr_len is None:
            hdr_len = self._read_protoheader()

        if hdr_len is not None:
            if header is None:
                header = self._read_header(hdr_len)

        if header:
            if msg is None:
                msg = self._read_msg(header)
        else:
            print("Sem mensgagem para ler")

        return msg

    def _read_protoheader(self):
        hdr_len = self.sock.recv(self.pHdr_len)
        return int(hdr_len)

    def _read_header(self, hdr_len):
        hdr = self.sock.recv(hdr_len)
        # Interessante caso o cabeçalho tenha mais de um item
        # for reqhdr in ("byteorder","content-length","content-type","content-encoding",):
        #     if reqhdr not in self.jsonheader:
        #         raise ValueError(f'Missing required header "{reqhdr}".')
        return int(hdr)

    def _read_msg(self, msg_len):
        chunks = []
        bytes_recv = 0
        while bytes_recv < msg_len:
            chunk = self.sock.recv(min(self.LENMAX, msg_len - bytes_recv))
            if chunk == b'':
                raise RuntimeError("connection broken")
            chunks.append(chunk)
            bytes_recv = bytes_recv + len(chunk)
        return b''.join(chunks)

    def read(self):
        lock.release()
        i = 0
        while self.recv_msg == b'':
            if i == 1000000:
                self.close_con()
                raise RuntimeError("Demorou tempo demais para receber uma resposta")
            i += 1
        msg = self.recv_msg
        self.recv_msg = b''
        return msg.decode(def_cod)

    def pscan(self, port):
        ''' Scaner de port'''
        try:
            self.sock.connect((self.host, port))
            return True
        except Exception as e:
            return False

    def close_con(self):
        self.onThread = False
        self.sock.close()
