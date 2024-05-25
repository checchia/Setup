# setup

## Setup inicial do Servidor
O script executa algumas tarefas para preparar o ambiente:
- [x] Desabilita o IPv6
- [x] Cria um Banner com informações sobre o equipamento
- [x] Cria um Banner de responsabilidade sobre atos e ações (compliance)
- [x] Instala os pacotes APT utilizados por padrão pelo time de Infra/SRE
- [x] Habilita a auditoria e configura a auditoria no Sistema Operacional (vide [Audit.md](./AUDIT.md))


## TODO
- [x] Desenvolver o código Python
- [ ] Criar um Actions que irá compilar e gerar um binário
- [ ] Este Action irá gerar um pacote .deb
- [ ] Este pacote será assinado para uma instalação "limpa"
- [ ] Irá disponibilizar em um repositório APT