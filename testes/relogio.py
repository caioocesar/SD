import time
from threading import *

TESTE = False
_tempo = 0
_on = False
_print_lock = Lock()

def _rodar_relogio():
    global _tempo
    global _on

    print_test(str(_on))
    while _on:
        _tempo += 1
        print_test("Tempo incrementado em 1, tempo = " + str(_tempo))
        time.sleep(1)


def iniciar_relogio():
    global _on

    _on = True
    t = Thread(target=_rodar_relogio)
    t.daemon = True
    t.start()
    print_test("Thread iniciada com sucesso")

def get_tempo():
    return _tempo

def finalizar_relogio():
    global _on
    _on = False
    print_test("Thread finalizada")

def print_test(s):
    if TESTE:
        _print_lock.acquire()
        print("[TESTE]", s)
        _print_lock.release()
