# Trabalho SD - 2019/1

## Algoritmos distribuídos

#### Objetivo:
O sistema a ser implementado consistirá de N processos iguais, identificados por um
identificador plano (número inteiro). Cada processo do sistema deve implementar o próprio relógio
local, que será atualizado através de um thread específica. Este relógio deve ser uma variável inteira
que será incrementada periodicamente pela thread com um valor fixo.
Neste cenário, os processos devem se organizar para sincronizar seus relógios. A tarefa deve
ser realizada em duas etapas. Na primeira etapa, os processos irão executar o “algoritmo do Bully”
para definir qual funcionará como coordenador. Após ser escolhido, o líder deve executar o
“algoritmo de Berkley” para sincronizar os relógios dos processos.

#### Comunicação:
Os algoritmos a serem implementados dependem do envio de mensagens UDP em multicast/
broadcast. Para a implementação, deve-se assumir os processos sempre na mesma subrede. Assim,
duas técnicas podem ser empregadas: o envio de mensagens para um endereço multicast ou o envio
de mensagens em broadcast.
A recepção de mensagens em multicast depende da configuração prévia do socket de
recepção para sua inclusão no grupo multicast. Já no caso do envio para o endereço de broadcast da
subrede depende da configuração do socket para habilitar esta função. Em C no Linux, o comando
‘setsockopts’ pode ser usado para fazer ambas as configurações. Dois exemplos estão disponíveis
nos arquivos anexos. Em outras linguagens existem interfaces semelhantes ao setsockopts, fiquem à
vontade para escolher a melhor forma.

#### Mensagens e log:
Para cada protocolo devem ser criadas mensagens específicas representando os tipos de
mensagem do algoritmo implementado. Todas as mensagens recebidas e enviadas pelos processos,
bem como eventos relevantes dos algoritmos, devem ser apresentadas na tela.

#### Detalhes de implementação:
Inicialmente os processos devem aguardar o comando para iniciar a escolha do líder. Os
processos devem ficar bloqueados esperando um Enter do usuário ou uma mensagem de outro
processo. Enquanto isso, a thread de atualização do relógio local já deve estar rodando e
incrementando o valor do relógio. Depois de escolhido, o processo líder dará início ao algoritmo de
Berkley para realizar a sincronização dos relógios locais de cada processo.
É interessante que cada processo atualize o seu relógio com incrementos diferentes ou
intervalos de tempo diferentes para que o algoritmo seja executado em um momento em que os
relógios locais possuam valores diferentes.
