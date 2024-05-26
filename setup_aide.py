#!/usr/bin/env python3
#     ____ _                   _     _         _   _ _____ _____ 
#    / ___| |__   ___  ___ ___| |__ (_) __ _  | \ | | ____|_   _|
#   | |   | '_ \ / _ \/ __/ __| '_ \| |/ _` | |  \| |  _|   | |  
#   | |___| | | |  __/ (_| (__| | | | | (_| |_| |\  | |___  | |  
#    \____|_| |_|\___|\___\___|_| |_|_|\__,_(_)_| \_|_____| |_|  
#                                                                
# 
import os
import subprocess

# Função para executar comandos shell
def run_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return stdout, stderr, process.returncode

# Instalar o AIDE
print("Instalando o AIDE...")
stdout, stderr, returncode = run_command("sudo apt-get install -y aide")
if returncode != 0:
    print(f"Erro ao instalar o AIDE: {stderr.decode()}")
    exit(1)
print(stdout.decode())

# Inicializar a base de dados do AIDE
print("Inicializando a base de dados do AIDE...")
stdout, stderr, returncode = run_command("sudo aideinit -y")
if returncode != 0:
    print(f"Erro ao inicializar a base de dados do AIDE: {stderr.decode()}")
    exit(1)
print(stdout.decode())

# Renomear a base de dados gerada
print("Renomeando a base de dados do AIDE...")
stdout, stderr, returncode = run_command("sudo mv /var/lib/aide/aide.db.new /var/lib/aide/aide.db")
if returncode != 0:
    print(f"Erro ao renomear a base de dados do AIDE: {stderr.decode()}")
    exit(1)
print(stdout.decode())

# Configurar o arquivo aide.conf
aide_conf_content = """
# Configuração do AIDE

# Definindo regras
Rule = p+i+n+u+g+s+m+c+acl+xattrs+sha512

# Aplicando regras
/boot   Rule
/bin    Rule
/sbin   Rule
/lib    Rule
/lib64  Rule
/usr    Rule
/etc    Rule
/var/log    Rule
/home   Rule
/etc/ssh    Rule
/etc/passwd Rule
/etc/group  Rule
/etc/shadow Rule
/usr/local/bin  Rule
"""

print("Configurando o arquivo /etc/aide/aide.conf...")
with open('/etc/aide/aide.conf', 'w') as f:
    f.write(aide_conf_content)

# Criar o script cron diário para verificar o AIDE
cron_script_content = """#!/bin/sh
/usr/bin/aide.wrapper --config /etc/aide/aide.conf --check | mail -s "AIDE Integrity Check" daniel.checchia@gmail.com
"""

cron_script_path = "/etc/cron.daily/aide"
print(f"Criando o script cron diário em {cron_script_path}...")
with open(cron_script_path, 'w') as f:
    f.write(cron_script_content)

# Tornar o script cron executável
print(f"Tornando o script cron {cron_script_path} executável...")
stdout, stderr, returncode = run_command(f"sudo chmod +x {cron_script_path}")
if returncode != 0:
    print(f"Erro ao tornar o script cron executável: {stderr.decode()}")
    exit(1)
print(stdout.decode())

# Atualizar a base de dados do AIDE após verificar a configuração inicial
print("Atualizando a base de dados do AIDE...")
stdout, stderr, returncode = run_command("sudo aide.wrapper --update && sudo mv /var/lib/aide/aide.db.new /var/lib/aide/aide.db")
if returncode != 0:
    print(f"Erro ao atualizar a base de dados do AIDE: {stderr.decode()}")
    exit(1)
print(stdout.decode())

print("Configuração do AIDE concluída com sucesso.")
