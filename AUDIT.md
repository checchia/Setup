# Configurações de Auditoria aplicadas

As configurações de auditoria mais comuns no auditd dependem dos requisitos específicos de segurança e conformidade de cada ambiente. No entanto, algumas configurações são amplamente utilizadas para monitorar e registrar atividades críticas do sistema. Aqui estão algumas das configurações mais comuns:

**1. Monitoramento de execução de comandos (execve):**
- Regras que monitoram a execução de comandos, como execve, ajudam a rastrear processos e programas que são iniciados no sistema. Isso pode ser crucial para detectar atividades maliciosas, como a execução de malware ou scripts não autorizados.

**2. Monitoramento de acesso a arquivos (file access):**
- Regras que monitoram o acesso a arquivos ajudam a controlar quais arquivos são acessados, modificados ou excluídos no sistema. Isso pode ajudar na detecção de tentativas de acesso não autorizado a arquivos sensíveis.

**3. Monitoramento de alterações em arquivos de configuração críticos:**
- Regras que monitoram alterações em arquivos de configuração críticos, como /etc/passwd, /etc/shadow e /etc/group, podem ajudar a detectar tentativas de comprometimento de contas de usuário ou grupos.

**4. Monitoramento de alterações em diretórios sensíveis:**
- Regras que monitoram alterações em diretórios sensíveis, como diretórios de configuração do sistema ou diretórios de aplicativos, podem ajudar a detectar alterações não autorizadas nessas áreas.

**5. Monitoramento de alterações em chaves de registro (no caso de sistemas Linux com Wine ou sistemas híbridos):**
- Em sistemas que executam aplicativos do Windows usando Wine ou sistemas híbridos, monitorar alterações nas chaves de registro pode ser importante para detectar atividades maliciosas ou não autorizadas.

**6. Monitoramento de acesso a arquivos de log:**
- Regras que monitoram o acesso a arquivos de log, como /var/log/auth.log, /var/log/syslog, entre outros, são críticas para garantir a integridade dos logs do sistema e detectar tentativas de manipulação ou exclusão de logs.

**7. Monitoramento de alterações no diretório /sbin e /bin:**
- Regras que monitoram alterações nos diretórios /sbin e /bin podem ajudar a detectar modificações nos binários do sistema, o que é importante para detectar possíveis tentativas de comprometimento do sistema.

**8. Monitoramento de acesso a portas de rede (no caso de sistemas com auditd regras de firewall):**
- Em sistemas onde as regras de firewall são gerenciadas pelo auditd, monitorar o acesso a portas de rede pode ser importante para detectar tentativas de conexão maliciosas ou não autorizadas.
