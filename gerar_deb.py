#!/usr/bin/env python3
import os
import shutil
import subprocess
import sys
from pathlib import Path

def criar_estrutura_deb():
    # Nome do pacote e versão
    nome_pacote = "gnome-customizer"
    versao = "1.0"
    arquitetura = "all"
    
    # Diretórios de trabalho
    dir_base = f"{nome_pacote}_{versao}_{arquitetura}"
    dir_deb = Path(dir_base)
    dir_debian = dir_deb / "DEBIAN"
    dir_usr = dir_deb / "usr"
    dir_share = dir_usr / "share"
    dir_app = dir_share / "applications"
    dir_icons = dir_share / "icons" / "hicolor" / "256x256" / "apps"
    dir_bin = dir_usr / "bin"
    dir_share_gnome_customizer = dir_share / "gnome-customizer"
    
    # Limpar diretório existente
    if dir_deb.exists():
        shutil.rmtree(dir_deb)
    
    # Criar estrutura de diretórios
    dir_debian.mkdir(parents=True, exist_ok=True)
    dir_app.mkdir(parents=True, exist_ok=True)
    dir_icons.mkdir(parents=True, exist_ok=True)
    dir_bin.mkdir(parents=True, exist_ok=True)
    dir_share_gnome_customizer.mkdir(parents=True, exist_ok=True)
    
    # Criar arquivo de controle DEBIAN
    controle_content = f"""Package: {nome_pacote}
Version: {versao}
Architecture: {arquitetura}
Maintainer: Seu Nome <seu.email@exemplo.com>
Installed-Size: 1024
Depends: python3, python3-gi, gir1.2-gtk-3.0, gnome-shell-extensions
Section: utils
Priority: optional
Homepage: https://exemplo.com
Description: Personalizador de Ambiente GNOME
 Um aplicativo para personalizar a experiência do GNOME com diferentes temas
 e layouts pré-configurados como macOS, Windows 10, Windows 11 e Ubuntu.
"""
    
    with open(dir_debian / "control", "w") as f:
        f.write(controle_content)
    
    # Criar script de pós-instalação
    postinst_content = """#!/bin/bash
# Atualizar ícones e banco de dados de aplicativos
gtk-update-icon-cache -f /usr/share/icons/hicolor/
update-desktop-database /usr/share/applications/
    
# Dar permissão de execução aos scripts
chmod +x /usr/share/gnome-customizer/index.py
chmod +x /usr/bin/gnome-customizer
    
echo "Personalizador de Ambiente GNOME instalado com sucesso!"
echo "Execute com: gnome-customizer"
"""
    
    with open(dir_debian / "postinst", "w") as f:
        f.write(postinst_content)
    os.chmod(dir_debian / "postinst", 0o755)
    
    # Criar arquivo .desktop para menu de aplicativos
    desktop_content = """[Desktop Entry]
Version=1.0
Name=GNOME Customizer
Comment=Personalizador de Ambiente GNOME
Exec=gnome-customizer
Icon=gnome-customizer
Terminal=false
Type=Application
Categories=Utility;Settings;
Keywords=gnome;customizer;theme;layout;
StartupNotify=true
"""
    
    with open(dir_app / "gnome-customizer.desktop", "w") as f:
        f.write(desktop_content)
    
    # Copiar ícones (se existirem)
    icones_originais = {
        "icon_app.png": dir_icons / "gnome-customizer.png",
        "icons/macOS.png": dir_share_gnome_customizer / "icons" / "macOS.png",
        "icons/ubuntu.png": dir_share_gnome_customizer / "icons" / "ubuntu.png",
        "icons/windows10.png": dir_share_gnome_customizer / "icons" / "windows10.png",
        "icons/windows11.png": dir_share_gnome_customizer / "icons" / "windows11.png"
    }
    
    for origem, destino in icones_originais.items():
        if os.path.exists(origem):
            destino.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(origem, destino)
            print(f"Copiado: {origem} -> {destino}")
        else:
            print(f"Aviso: Arquivo não encontrado: {origem}")
    
    # Copiar o script principal
    if os.path.exists("index.py"):
        shutil.copy2("index.py", dir_share_gnome_customizer / "index.py")
        
        # Criar script de executável em /usr/bin
        bin_content = f"""#!/bin/bash
cd /usr/share/gnome-customizer
exec python3 index.py "$@"
"""
        
        with open(dir_bin / "gnome-customizer", "w") as f:
            f.write(bin_content)
        os.chmod(dir_bin / "gnome-customizer", 0o755)
    else:
        print("Erro: index.py não encontrado!")
        return False
    
    # Construir o pacote .deb
    try:
        subprocess.run(["dpkg-deb", "--build", dir_base], check=True)
        print(f"\nPacote criado com sucesso: {dir_base}.deb")
        print("\nPara instalar: sudo dpkg -i {}.deb".format(dir_base))
        print("Se houver dependências faltando: sudo apt-get install -f")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Erro ao construir pacote DEB: {e}")
        return False
    except FileNotFoundError:
        print("Erro: dpkg-deb não encontrado. Instale com: sudo apt install dpkg-dev")
        return False

def main():
    print("Criando pacote DEB para GNOME Customizer...")
    print("=" * 50)
    
    # Verificar se estamos no Linux
    if not sys.platform.startswith('linux'):
        print("Este script só pode ser executado no Linux")
        return False
    
    # Verificar se é Debian/Ubuntu
    try:
        with open('/etc/debian_version', 'r') as f:
            print("Sistema Debian/Ubuntu detectado")
    except FileNotFoundError:
        print("Aviso: Sistema não baseado em Debian. O pacote pode não funcionar corretamente.")
    
    # Criar a estrutura do DEB
    success = criar_estrutura_deb()
    
    if success:
        print("\n✅ Pacote DEB criado com sucesso!")
    else:
        print("\n❌ Falha ao criar pacote DEB")
    
    return success

if __name__ == "__main__":
    main()