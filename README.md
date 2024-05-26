# setup

## Setup inicial do Servidor
O script executa algumas tarefas para preparar o ambiente:
- [x] Desabilita o IPv6
- [x] Cria um Banner com informações sobre o equipamento
- [x] Cria um Banner de responsabilidade sobre atos e ações (compliance)
- [x] Habilita o UFW por padrão, liberando a porta 22
- [x] Instala os pacotes APT utilizados por padrão pelo time de Infra/SRE
- [x] Habilita a auditoria e configura a auditoria no Sistema Operacional (vide [Audit.md](./AUDIT.md))
- [x] Ajustar as configurações de IPv6 (abaixo)
- [x] Incluir checagem de pacotes para atualizar
- [x] Incluir checagem de Security Updates 
- [ ] Configurar tempo de inatividade e desconexão
- [ ] Configurar duração de senha
- [ ] configurar senha forte


## TODO
- [x] Desenvolver o código Python
- [ ] Criar um Actions que irá compilar e gerar um binário
- [ ] Este Action irá gerar um pacote .deb
- [ ] Este pacote será assinado para uma instalação "limpa"
- [ ] Irá disponibilizar em um repositório APT
- [ ] Criar conta gratuíta no Mailgun para checchia.net e para taya.sh
- [ ] Criar rotina para baixar o log de disparos de e-mail do mailgun (conta free = log retention 1 dia)

UPS

sudo nano /etc/ssh/sshd_config

PermitRootLogin no
PasswordAuthentication no
Port <custom_port>

sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow <custom_port>/tcp
sudo ufw enable


sudo apt-get install rsyslog
sudo systemctl enable rsyslog
sudo systemctl start rsyslog
