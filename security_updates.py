#!/usr/bin/env python3
#     ____ _                   _     _         _   _ _____ _____ 
#    / ___| |__   ___  ___ ___| |__ (_) __ _  | \ | | ____|_   _|
#   | |   | '_ \ / _ \/ __/ __| '_ \| |/ _` | |  \| |  _|   | |  
#   | |___| | | |  __/ (_| (__| | | | | (_| |_| |\  | |___  | |  
#    \____|_| |_|\___|\___\___|_| |_|_|\__,_(_)_| \_|_____| |_|  
#                                                                
# 
import subprocess

def run_command(command):
    """Run a shell command and return the output."""
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    if result.returncode != 0:
        print(f"Error running command: {command}")
        print(f"Output: {result.stdout}")
        print(f"Error: {result.stderr}")
        return None
    return result.stdout

def install_packages():
    """Install the necessary packages."""
    print("Installing packages...")
    run_command("sudo apt update")
    run_command("sudo apt install -y unattended-upgrades update-notifier-common")

def configure_unattended_upgrades():
    """Configure unattended-upgrades."""
    print("Configuring unattended-upgrades...")
    unattended_upgrades_conf = "/etc/apt/apt.conf.d/50unattended-upgrades"
    
    config = """
Unattended-Upgrade::Origins-Pattern {
        "origin=Debian,codename=${distro_codename},label=Debian-Security";
        "origin=Ubuntu,codename=${distro_codename},label=Ubuntu";
        "origin=Ubuntu,codename=${distro_codename},label=Ubuntu-Security";
};

// Automatically upgrade packages from these (origin, archive) pairs
Unattended-Upgrade::Allowed-Origins {
    "${distro_id}:${distro_codename}-security";
};

// Send email to this address for problems or packages upgrades
//Unattended-Upgrade::Mail "root@localhost";

// Set this value to "true" to get emails only on errors.
//Unattended-Upgrade::MailOnlyOnError "true";

// Do automatic removal of new unused dependencies after the upgrade
Unattended-Upgrade::Remove-Unused-Dependencies "true";

// Automatically reboot *WITHOUT CONFIRMATION* if the file
// /var/run/reboot-required is found after the upgrade 
//Unattended-Upgrade::Automatic-Reboot "false";

// Automatically reboot even if users are logged in
//Unattended-Upgrade::Automatic-Reboot-WithUsers "true";
    """
    
    with open(unattended_upgrades_conf, 'w') as file:
        file.write(config)
    
def configure_periodic_updates():
    """Configure apt for periodic updates."""
    print("Configuring periodic updates...")
    auto_upgrades_conf = "/etc/apt/apt.conf.d/20auto-upgrades"
    
    config = """
APT::Periodic::Update-Package-Lists "1";
APT::Periodic::Unattended-Upgrade "1";
    """
    
    with open(auto_upgrades_conf, 'w') as file:
        file.write(config)

def main():
    install_packages()
    configure_unattended_upgrades()
    configure_periodic_updates()
    print("Configuration complete. Restarting unattended-upgrades service...")
    run_command("sudo systemctl restart unattended-upgrades")
    print("Unattended-upgrades service restarted.")
    
if __name__ == "__main__":
    main()
