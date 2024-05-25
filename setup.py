#!/usr/bin/env python3
#     ____ _                   _     _         _   _ _____ _____ 
#    / ___| |__   ___  ___ ___| |__ (_) __ _  | \ | | ____|_   _|
#   | |   | '_ \ / _ \/ __/ __| '_ \| |/ _` | |  \| |  _|   | |  
#   | |___| | | |  __/ (_| (__| | | | | (_| |_| |\  | |___  | |  
#    \____|_| |_|\___|\___\___|_| |_|_|\__,_(_)_| \_|_____| |_|  
#                                                                
# Script para setup inicial de novos servidores Ubuntu


import os
import sys
import subprocess
import platform


# Verificar se o usuário é root
if os.geteuid() != 0:
    print("Este script precisa ser executado como root.")
    sys.exit(1)

banner_content = """#!/bin/bash
clear

# Definir cores e formatações
yellow_bold="\\033[1;33m"
red_bold="\\033[1;31m"
red_bold_blink="\\033[1;5;31m"
bold="\\033[1m"
reset="\\033[0m"

# Imprimir os caracteres em amarelo e negrito
echo -e "${yellow_bold}    ____ _                   _     _         _   _ _____ _____ "
echo -e "${yellow_bold}   / ___| |__   ___  ___ ___| |__ (_) __ _  | \\ | | ____|_   _|"
echo -e "${yellow_bold}  | |   | '_ \\ / _ \\/ __/ __| '_ \\| |/ _\\` | |  \\| |  _|   | |  "
echo -e "${yellow_bold}  | |___| | | |  __/ (_| (__| | | | | (_| |_| |\\  | |___  | |  "
echo -e "${yellow_bold}   \\____|_| |_|\\___|\\___\\___|_| |_|_|\\__,_(_)_| \\_|_____| |_|  "
echo -e "${yellow_bold} "
echo -e "${yellow_bold} "

# Exibir o último login
last_login=$(lastlog -u $USER | tail -n 1)
echo -e "${reset}${bold}Último login:${reset} $last_login"

# Exibir a data e hora atual
current_datetime=$(date)
echo -e "${bold}Data e hora atual:${reset} $current_datetime"

# Exibir o espaço livre e total na partição root
root_space=$(df -h / | awk 'NR==2 {print $4 " livre de " $2}')
echo -e "${bold}Espaço na partição root:${reset} $root_space"

# Verificar se a partição /DADOS existe e exibir o espaço livre e total
if mountpoint -q /DADOS; then
  dados_space=$(df -h /DADOS | awk 'NR==2 {print $4 " livre de " $2}')
  echo -e "${bold}Espaço na partição /DADOS:${reset} $dados_space"
else
  echo -e "${red_bold}A partição /DADOS não existe.${reset}"
fi
echo " "
echo " "
echo " "

# Mensagem sobre acesso não autorizado
echo -e "${red_bold}AVISO DE SEGURANÇA:${reset} ${bold}O acesso não autorizado a este sistema é proibido.${reset}"
echo -e "Qualquer atividade não autorizada será ${red_bold}monitorada e registrada${reset} e pode resultar em ${red_bold}processos criminais${reset}."
echo -e "Usuários que tentarem acessar o sistema sem autorização estarão sujeitos a ${bold}penalidades severas${reset} conforme as leis vigentes."

echo " "
echo " "
echo " "

# Verificar se o usuário logado é root ou possui privilégios sudoers
if [ "$EUID" -eq 0 ]; then
  echo -e "${red_bold}VOCÊ ESTÁ ACESSANDO COMO USUÁRIO PRIVILEGIADO!${reset}"
  echo -e "${red_bold_blink}\"Com grandes poderes vêm grandes responsabilidades! Não se esqueça!\"${reset}"
fi
echo " "
echo " "
echo " "
"""

file_path = "/etc/profile.d/00-banner.sh"

def disable_ipv6():
    try:
        # Abrir o arquivo de configuração do sysctl em modo de escrita
        with open('/etc/sysctl.conf', 'a') as sysctl_file:
            # Adicionar a configuração para desativar o IPv6
            sysctl_file.write('net.ipv6.conf.all.disable_ipv6 = 1\n')
            sysctl_file.write('net.ipv6.conf.default.disable_ipv6 = 1\n')
        
        # Recarregar as configurações do sysctl
        subprocess.run(['sudo', 'sysctl', '-p'], stdout=subprocess.DEVNULL)
        
        status("IPv6 desativado com sucesso!",0)
    except Exception as e:
        status(f"Erro ao desativar o IPv6: {e}",1)

def checkversion():
    if sys.version_info >= (3, 10):
        status("A versão do Python é igual ou superior à 3.10",0)
    else:
        status("A versão do Python é inferior à 3.10",1)
        sys.exit(1)

def status(mensagem, codigo):
    if codigo == 0:
        status = "\033[1;32m[OK]\033[0m"
    elif codigo == 1:
        status = "\033[1;31m[FALHA]\033[0m"
    else:
        status = "[Código inválido]"
    print(f"{mensagem.ljust(80-len(status))}{status}")

def install_packages():
    packages = ['net-tools', 'vim', 'python-is-python3', 'rsyslog', 'screen', 'auditd']
    try:
        for package in packages:
            subprocess.run(['sudo', 'apt', 'install', '-y', package], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            status(f"Pacote {package} com sucesso!",0)
    except subprocess.CalledProcessError as e:
        status(f"Erro ao instalar {package}",1)

def enable_auditd():
    try:
        subprocess.run(["sudo", "systemctl", "enable", "auditd"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        status("Habilitado o serviço auditd.",0)
    except:
        status("Erro habilitando o serviço auditd.",1)

def start_auditd():
    try:
        subprocess.run(["sudo", "systemctl", "start", "auditd"], stdout=subprocess.DEVNULL)
        status("Serviço auditd iniciado.",0)
    except:
        status("Erro iniciando o serviço auditd!",1)

def configure_audit_rules():
    audit_rules = [
        "-a always,exit -F arch=b64 -S execve",
        "-a always,exit -F arch=b32 -S execve",
        "-w /etc/passwd -p wa -k identity",
        "-w /etc/group -p wa -k identity",
        "-w /etc/shadow -p wa -k identity",
        "-w /etc/sudoers -p wa -k sudoers_changes",
        "-w /var/log/auth.log -p wa -k authentication_events"
        # Adicione outras regras conforme necessário
    ]
    with open("/etc/audit/rules.d/infra.rules", "a") as f:
        for rule in audit_rules:
            f.write(rule + "\n")
    try:
        subprocess.run(["sudo", "auditctl", "-l"], stdout=subprocess.DEVNULL)
        status("Regras de auditoria validadas",0)
    except:
        status("Erros durante validação de regras de uditoria!",1)
    try:
        subprocess.run(["sudo", "systemctl", "restart", "auditd"], stdout=subprocess.DEVNULL)
        status("Serviço auditd reiniciado.",0)
    except:
        status("Erro na reinicialização do serviço auditd!",1)

if __name__ == "__main__":
    checkversion()
    disable_ipv6()
    try:
        with open(file_path, "w") as file:
            file.write(banner_content)
        status(f"Arquivo {file_path} criado com sucesso.",0)
    except PermissionError:
        status(f"Você não tem permissões para escrever em {file_path}. Execute o script como superusuário (root) ou com permissões de escrita adequadas.",1)
    install_packages()
    enable_auditd()
    start_auditd()
    configure_audit_rules()
