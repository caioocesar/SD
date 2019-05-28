import relogio

relogio.iniciar_relogio()

for i in range(1000000):
    print(relogio.get_tempo())

relogio.finalizar_relogio()