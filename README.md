# TR2_UDP
TR2 UDP + Go back N + RDT Over UDP

Nesta tarefa vamos utilizar os conceitos vistos até aqui na Camada de Transporte e desenvolver um programa que permita o envio de dados em pipiline. Para tal, vamos utilizar como base os exemplos na pasta "Python Examples".

Sua tarefa consiste em adicionar ao protocolo UDP as seguintes características: 
1) Garantir a entrega confiável e em ordem dos dados
2) Controle de fluxo
3) Pipeline (não deve ser stop-and-wait)

Estes itens devem ser implementados na camada de aplicação do seu programa. Certifique que vc leu e entendeu estes conceitos antes de implementá-los

O seu trabalho deve incluir:

a) um texto (PDF) com informações de como estas questões foram resolvidas (tratadas pelo seu programa). 
b) exemplos de execução onde há perda de dados, onde há dados corrompidos, e de pipeline. 
c) incluir informações de desempenho (relatório) do seu programa em termos de vazão (qual o volume máximo que seu programa consegue obter em um enlace sem perda e sem erros de transmissão). 
