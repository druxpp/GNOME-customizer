#!/usr/bin/env python3
import gi
import subprocess
import tempfile
import os
import time
import json
import threading
import subprocess
import sys
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GdkPixbuf, GLib

# ===========================
# CONFIGURAÇÃO DE CAMINHOS DE ÍCONES
# ===========================
def get_resource_path(relative_path):
    """Obtém o caminho absoluto para recursos, funciona para desenvolvimento e para o executável compilado"""
    try:
        # Para executáveis compilados com PyInstaller
        base_path = sys._MEIPASS
    except Exception:
        # Para execução normal
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

# Caminhos dos ícones (usando a função get_resource_path)
ICON_PATHS = {
    "windows10": get_resource_path("icons/windows10.png"),
    "windows11": get_resource_path("icons/windows11.png"), 
    "macos": get_resource_path("icons/macOS.png"),
    "ubuntu": get_resource_path("icons/ubuntu.png")
}

# Fallback para ícones padrão se os específicos não existirem
FALLBACK_ICONS = {
    "windows10": "windows-symbolic",
    "windows11": "windows-symbolic",
    "macos": "apple-symbolic",
    "ubuntu": "ubuntu-symbolic"
}

# Lista de extensões
extensoes = [
    "emoji-copy@felipeftn",
    "compiz-windows-effect@hermes83.github.com",
    "gsconnect@andyholmes.github.io",
    "dash-to-panel@jderose9.github.com",
    "arcmenu@arcmenu.com",
    "blur-my-shell@aunetx",
    "desktop-cube@schneegans.github.com",
    "dash2dock-lite@icedman.github.com",
    "peek-top-bar-on-fullscreen@marcinjahn.com",
    "ding@rastersoft.com",
    "tiling-assistant@ubuntu.com",
    "ubuntu-appindicators@ubuntu.com",
    "ubuntu-dock@ubuntu.com",
    "user-theme@gnome-shell-extensions.gcampax.github.com"
]

def is_enabled(ext_id):
    """Verifica se a extensão está habilitada"""
    result = subprocess.run(
        ["gnome-extensions", "info", ext_id],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        return False
    return "State: ENABLED" in result.stdout

def disable_extension(ext_id):
    """Desabilita a extensão"""
    subprocess.run(["gnome-extensions", "disable", ext_id])

# Desabilita todas as extensões que ainda estão habilitadas
for ext in extensoes:
    if is_enabled(ext):
        print(f"Desabilitando {ext}...")
        disable_extension(ext)
    else:
        print(f"{ext} já está desabilitada.")

# Verifica se todas estão desabilitadas
todas_desabilitadas = all(not is_enabled(ext) for ext in extensoes)

if todas_desabilitadas:
    print("Todas as extensões estão desabilitadas. Executando index2.py...")
    subprocess.run([sys.executable, "index2.py"])
else:
    print("Algumas extensões não puderam ser desabilitadas.")

# ===========================
# CONSTANTES
# ===========================
EXTENSIONS = {
    "dash2dock": "dash2dock-lite@icedman.github.com",
    "panel": "dash-to-panel@jderose9.github.com",
    "arcmenu": "arcmenu@arcmenu.com",
    "ubuntu": "ubuntu-dock@ubuntu.com",
    "compiz": "compiz-windows-effect@hermes83.github.com",
    "cube": "desktop-cube@schneegans.github.com",
    "gsconnect": "gsconnect@andyholmes.github.io",
    "emoji": "emoji-copy@felipeftn",
    "tiling": "tiling-assistant@ubuntu.com",
    "appindicators": "ubuntu-appindicators@ubuntu.com",
    "blur": "blur-my-shell@aunetx"
}

# Extensões que sempre serão habilitadas (padrão para todos os modos)
ALWAYS_ENABLED_EXTENSIONS = ["compiz", "cube", "gsconnect", "emoji", "tiling", "appindicators", "blur"]

# ===========================
# PERFIS DE CONFIGURAÇÃO (ATUALIZADOS COM SUAS CONFIGURAÇÕES REAIS)
# ===========================
PROFILES = {
    "macos_normal": {
        "name": "macOS Normal",
        "icon": "macos",
        "extensions": ["dash2dock"],
        "dconf": {
            "dash2dock": """[/]
animation-bounce=0.02
animation-magnify=0.0
animation-rise=1.0
animation-spread=0.91
apps-icon-front=true
autohide-dash=true
autohide-speed=0.0
background-color=(0.0, 0.0, 0.0, 0.51666665077209473)
blur-resolution=0
border-radius=2.2
clock-icon=false
customize-label=true
customize-topbar=true
dock-padding=0.0
downloads-icon=false
edge-distance=-0.015
icon-resolution=4
icon-size=0.0
icon-spacing=0.0
items-pullout-angle=0.02
mounted-icon=true
msg-to-ext=''
open-app-animation=true
panel-mode=false
preferred-monitor=0
pressure-sense=false
pressure-sense-sensitivity=0.0
scroll-sensitivity=0.0
shrink-icons=true
topbar-background-color=(0.0, 0.0, 0.0, 0.50333333015441895)
trash-icon=true
"""
        }
    },
    "macos_extended": {
        "name": "macOS Estendido",
        "icon": "macos",
        "extensions": ["dash2dock"],
        "dconf": {
            "dash2dock": """[/]
animation-bounce=0.02
animation-magnify=0.0
animation-rise=1.0
animation-spread=0.91
apps-icon-front=true
autohide-dash=true
autohide-speed=0.0
background-color=(0.0, 0.0, 0.0, 0.51666665077209473)
blur-resolution=0
border-radius=2.2
clock-icon=false
customize-label=true
customize-topbar=true
dock-padding=0.0
downloads-icon=false
edge-distance=-0.015
icon-resolution=4
icon-size=0.0
icon-spacing=0.0
items-pullout-angle=0.02
mounted-icon=true
msg-to-ext=''
open-app-animation=true
panel-mode=true
preferred-monitor=0
pressure-sense=false
pressure-sense-sensitivity=0.0
scroll-sensitivity=0.0
shrink-icons=true
topbar-background-color=(0.0, 0.0, 0.0, 0.50333333015441895)
trash-icon=true
"""
        }
    },
    "windows11_centered": {
        "name": "Windows 11 Centralizado",
        "icon": "windows11",
        "extensions": ["panel", "arcmenu"],
        "dconf": {
            "panel": """[/]
animate-appicon-hover=true
animate-appicon-hover-animation-extent={'RIPPLE': 4, 'PLANK': 4, 'SIMPLE': 1}
appicon-margin=0
dot-position='TOP'
dot-style-focused='SQUARES'
extension-version=68
hotkeys-overlay-combo='TEMPORARILY'
panel-anchors='{"LGD-0x00000000":"MIDDLE"}'
panel-element-positions='{"LGD-0x00000000":[{"element":"showAppsButton","visible":false,"position":"stackedTL"},{"element":"activitiesButton","visible":false,"position":"stackedTL"},{"element":"leftBox","visible":true,"position":"centerMonitor"},{"element":"taskbar","visible":true,"position":"centerMonitor"},{"element":"centerBox","visible":true,"position":"stackedBR"},{"element":"rightBox","visible":true,"position":"stackedBR"},{"element":"dateMenu","visible":true,"position":"stackedBR"},{"element":"systemMenu","visible":true,"position":"stackedBR"},{"element":"desktopButton","visible":true,"position":"stackedBR"}]}'
panel-lengths='{"0":100}'
panel-positions='{}'
panel-sizes='{"0":48}'
prefs-opened=false
primary-monitor='LGD-0x00000000'
window-preview-title-position='TOP'
""",
            "arcmenu": """[/]
arc-menu-icon=71
avatar-style='Square'
button-padding=7
context-menu-items=[{'id': 'ArcMenu_Settings', 'name': 'ArcMenu Settings', 'icon': 'ArcMenu_ArcMenuIcon'}, {'id': 'ArcMenu_PanelExtensionSettings', 'name': 'Panel Extension Settings', 'icon': 'application-x-addon-symbolic'}, {'id': 'ArcMenu_Separator', 'name': 'Separator', 'icon': 'list-remove-symbolic'}, {'id': 'ArcMenu_PowerOptions', 'name': 'Power Options', 'icon': 'system-shutdown-symbolic'}, {'id': 'ArcMenu_ActivitiesOverview', 'name': 'Activities Overview', 'icon': 'view-fullscreen-symbolic'}, {'id': 'ArcMenu_ShowDesktop', 'name': 'Show Desktop', 'icon': 'computer-symbolic'}]
custom-menu-button-icon-size=26.0
disable-recently-installed-apps=false
disable-user-avatar=false
distro-icon=5
extra-categories=[(3, true), (2, true), (0, false), (1, false), (4, false)]
force-menu-location='BottomCentered'
group-apps-alphabetically-list-layouts=true
hide-overview-on-startup=false
left-panel-width=265
menu-button-appearance='Icon'
menu-button-border-radius=(true, 0)
menu-button-border-width=(false, 0)
menu-button-icon='Distro_Icon'
menu-button-position-offset=10
menu-height=600
menu-layout='Eleven'
multi-monitor=false
override-menu-theme=false
pinned-apps=[{'id': 'firefox.desktop'}, {'id': 'org.gnome.Nautilus.desktop'}, {'id': 'org.gnome.Terminal.desktop'}]
position-in-panel='Left'
prefs-visible-page=0
right-panel-width=255
search-entry-border-radius=(true, 25)
show-activities-button=false
update-notifier-project-version=66
"""
        }
    },
    "windows11_left": {
        "name": "Windows 11 Esquerda",
        "icon": "windows11",
        "extensions": ["panel", "arcmenu"],
        "dconf": {
            "panel": """[/]
animate-appicon-hover=true
animate-appicon-hover-animation-extent={'RIPPLE': 4, 'PLANK': 4, 'SIMPLE': 1}
appicon-margin=0
dot-position='TOP'
dot-style-focused='SQUARES'
extension-version=68
hotkeys-overlay-combo='TEMPORARILY'
panel-anchors='{"LGD-0x00000000":"MIDDLE"}'
panel-element-positions='{"LGD-0x00000000":[{"element":"showAppsButton","visible":false,"position":"stackedTL"},{"element":"activitiesButton","visible":false,"position":"stackedTL"},{"element":"leftBox","visible":true,"position":"stackedTL"},{"element":"taskbar","visible":true,"position":"stackedTL"},{"element":"centerBox","visible":true,"position":"stackedBR"},{"element":"rightBox","visible":true,"position":"stackedBR"},{"element":"dateMenu","visible":true,"position":"stackedBR"},{"element":"systemMenu","visible":true,"position":"stackedBR"},{'element':'desktopButton','visible':true,'position':'stackedBR'}]}'
panel-lengths='{"0":100}'
panel-positions='{}'
panel-sizes='{"0":48}'
prefs-opened=false
primary-monitor='LGD-0x00000000'
window-preview-title-position='TOP'
""",
            "arcmenu": """[/]
arc-menu-icon=71
avatar-style='Square'
button-padding=7
context-menu-items=[{'id': 'ArcMenu_Settings', 'name': 'ArcMenu Settings', 'icon': 'ArcMenu_ArcMenuIcon'}, {'id': 'ArcMenu_PanelExtensionSettings', 'name': 'Panel Extension Settings', 'icon': 'application-x-addon-symbolic'}, {'id': 'ArcMenu_Separator', 'name': 'Separator', 'icon': 'list-remove-symbolic'}, {'id': 'ArcMenu_PowerOptions', 'name': 'Power Options', 'icon': 'system-shutdown-symbolic'}, {'id': 'ArcMenu_ActivitiesOverview', 'name': 'Activities Overview', 'icon': 'view-fullscreen-symbolic'}, {'id': 'ArcMenu_ShowDesktop', 'name': 'Show Desktop', 'icon': 'computer-symbolic'}]
custom-menu-button-icon-size=26.0
disable-recently-installed-apps=false
disable-user-avatar=false
distro-icon=5
extra-categories=[(3, true), (2, true), (0, false), (1, false), (4, false)]
force-menu-location='BottomLeft'
group-apps-alphabetically-list-layouts=true
hide-overview-on-startup=false
left-panel-width=265
menu-button-appearance='Icon'
menu-button-border-radius=(true, 0)
menu-button-border-width=(false, 0)
menu-button-icon='Distro_Icon'
menu-button-position-offset=10
menu-height=600
menu-layout='Eleven'
multi-monitor=false
override-menu-theme=false
pinned-apps=[{'id': 'firefox.desktop'}, {'id': 'org.gnome.Nautilus.desktop'}, {'id': 'org.gnome.Terminal.desktop'}]
position-in-panel='Left'
prefs-visible-page=0
right-panel-width=255
search-entry-border-radius=(true, 25)
show-activities-button=false
update-notifier-project-version=66
"""
        }
    },
    "windows10": {
        "name": "Windows 10",
        "icon": "windows10",
        "extensions": ["panel", "arcmenu"],
        "dconf": {
            "panel": """[/]
animate-appicon-hover=true
animate-appicon-hover-animation-extent={'RIPPLE': 4, 'PLANK': 4, 'SIMPLE': 1}
appicon-margin=0
dot-position='TOP'
dot-style-focused='SQUARES'
extension-version=68
hotkeys-overlay-combo='TEMPORARILY'
panel-anchors='{"0":"LEFT"}'
panel-element-positions='{"0":[{"element":"showAppsButton","visible":false,"position":"stackedTL"},{"element":"activitiesButton","visible":false,"position":"stackedTL"},{"element":"leftBox","visible":true,"position":"stackedTL"},{"element":"taskbar","visible":true,"position":"stackedTL"},{"element":"centerBox","visible":true,"position":"stackedBR"},{"element":"rightBox","visible":true,"position":"stackedBR"},{"element":"dateMenu","visible":true,"position":"stackedBR"},{"element":"systemMenu","visible":true,"position":"stackedBR"},{"element":"desktopButton","visible":true,"position":"stackedBR"}]}'
panel-lengths='{"0":100}'
panel-sizes='{"0":48}'
window-preview-title-position='TOP'
""",
            "arcmenu": """[/]
arc-menu-icon=71
avatar-style='Square'
button-padding=5
context-menu-items=[{'id': 'ArcMenu_Settings', 'name': 'ArcMenu Settings', 'icon': 'ArcMenu_ArcMenuIcon'}, {'id': 'ArcMenu_PanelExtensionSettings', 'name': 'Panel Extension Settings', 'icon': 'application-x-addon-symbolic'}, {'id': 'ArcMenu_Separator', 'name': 'Separator', 'icon': 'list-remove-symbolic'}, {'id': 'ArcMenu_PowerOptions', 'name': 'Power Options', 'icon': 'system-shutdown-symbolic'}, {'id': 'ArcMenu_ActivitiesOverview', 'name': 'Activities Overview', 'icon': 'view-fullscreen-symbolic'}, {'id': 'ArcMenu_ShowDesktop', 'name': 'Show Desktop', 'icon': 'computer-symbolic'}]
custom-menu-button-icon-size=26.0
disable-recently-installed-apps=false
disable-user-avatar=false
distro-icon=5
extra-categories=[(3, true), (2, true), (0, false), (1, false), (4, false)]
force-menu-location='BottomLeft'
group-apps-alphabetically-list-layouts=true
hide-overview-on-startup=false
left-panel-width=265
menu-button-appearance='Icon'
menu-button-border-radius=(true, 0)
menu-button-border-width=(false, 0)
menu-button-icon='Distro_Icon'
menu-button-position-offset=10
menu-height=600
menu-layout='Windows'
multi-monitor=false
override-menu-theme=false
pinned-apps=[{'id': 'firefox.desktop'}, {'id': 'org.gnome.Nautilus.desktop'}, {'id': 'org.gnome.Terminal.desktop'}]
position-in-panel='Left'
prefs-visible-page=0
right-panel-width=255
search-entry-border-radius=(true, 25)
show-activities-button=false
"""
        }
    },
    "ubuntu": {
        "name": "Ubuntu Like",
        "icon": "ubuntu",
        "extensions": ["ubuntu"],
        "dconf": {}
    }
}

# Configuração padrão para emoji-copy
EMOJI_COPY_CONFIG = """[/]
always-show=false
recently-used=['👿', '👇', '😂', '❤️', '😍', '😭', '😊', '😒', '😘', '😩', '🤔']
"""

# ===========================
# FUNÇÕES AUXILIARES
# ===========================
def run_cmd(cmd, show_output=False):
    """Executa comando no terminal"""
    try:
        if show_output:
            result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
            return result.stdout.strip()
        else:
            subprocess.run(cmd, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar: {cmd}\n{e}")
        return False

def check_extension_installed(extension_id):
    """Verifica se uma extensão está instalada"""
    try:
        result = subprocess.run(
            ["gnome-extensions", "list"], 
            capture_output=True, text=True
        )
        return extension_id in result.stdout
    except:
        return False

def get_icon_pixbuf(icon_name, size=48):
    """Obtém um pixbuf para o ícone especificado"""
    try:
        icon_path = ICON_PATHS[icon_name]
        if os.path.exists(icon_path):
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(icon_path, size, size)
            return pixbuf
        else:
            # Fallback para ícones padrão do GTK
            theme = Gtk.IconTheme.get_default()
            icon_info = theme.lookup_icon(FALLBACK_ICONS[icon_name], size, 0)
            if icon_info:
                return icon_info.load_icon()
    except Exception as e:
        print(f"Erro ao carregar ícone {icon_name}: {e}")
    
    # Fallback final
    try:
        return Gtk.IconTheme.get_default().load_icon("application-x-executable", size, 0)
    except:
        # Se tudo falhar, cria um ícone vazio
        return GdkPixbuf.Pixbuf.new(GdkPixbuf.Colorspace.RGB, True, 8, size, size)

def apply_dconf_config(extension_id, config_data):
    """Aplica configuração dconf para uma extensão"""
    if not config_data:
        return True
    
    # Mapeia IDs de extensão para caminhos dconf
    dconf_paths = {
        "dash2dock": "/org/gnome/shell/extensions/dash2dock-lite/",
        "panel": "/org/gnome/shell/extensions/dash-to-panel/",
        "arcmenu": "/org/gnome/shell/extensions/arcmenu/",
        "emoji": "/org/gnome/shell/extensions/emoji-copy/"
    }
    
    if extension_id not in dconf_paths:
        return False
    
    with tempfile.NamedTemporaryFile(delete=False, mode="w") as tmp:
        tmp.write(config_data)
        tmp_path = tmp.name
    
    run_cmd(f"dconf load {dconf_paths[extension_id]} < {tmp_path}")
    os.unlink(tmp_path)
    return True

def apply_mode(profile_name, progress_callback=None):
    """Aplica um perfil de configuração"""
    profile = PROFILES[profile_name]
    
    # Desabilita todas as extensões primeiro
    if progress_callback:
        GLib.idle_add(progress_callback, "Desabilitando extensões...")
    
    for ext_id in EXTENSIONS.values():
        run_cmd(f"gnome-extensions disable {ext_id}")
    
    time.sleep(0.5)
    
    # Habilita as extensões do perfil
    if progress_callback:
        GLib.idle_add(progress_callback, "Habilitando extensões do perfil...")
    
    for ext_key in profile["extensions"]:
        ext_id = EXTENSIONS[ext_key]
        if check_extension_installed(ext_id):
            run_cmd(f"gnome-extensions enable {ext_id}")
            time.sleep(0.3)
    
    # Habilita as extensões padrão em todos os modos
    if progress_callback:
        GLib.idle_add(progress_callback, "Habilitando extensões padrão...")
    
    for ext_key in ALWAYS_ENABLED_EXTENSIONS:
        ext_id = EXTENSIONS[ext_key]
        if check_extension_installed(ext_id):
            run_cmd(f"gnome-extensions enable {ext_id}")
            time.sleep(0.3)
    
    # Aplica configurações dconf para as extensões
    if progress_callback:
        GLib.idle_add(progress_callback, "Aplicando configurações...")
    
    for ext_key, config_data in profile.get("dconf", {}).items():
        apply_dconf_config(ext_key, config_data)
    
    # Aplica configuração padrão para emoji-copy
    apply_dconf_config("emoji", EMOJI_COPY_CONFIG)
    
    # Recarrega o GNOME Shell
    if progress_callback:
        GLib.idle_add(progress_callback, "Recarregando GNOME Shell...")
    
    reload_gnome_shell()
    
    return True

def reload_gnome_shell():
    """Recarrega o GNOME Shell de forma não destrutiva"""
    run_cmd("gsettings set org.gnome.shell disable-user-extensions true")
    time.sleep(1)
    run_cmd("gsettings set org.gnome.shell disable-user-extensions false")

def create_backup():
    """Cria um backup das configurações atuais"""
    backup_data = {
        "extensions": {}
    }
    
    for ext_key, ext_id in EXTENSIONS.items():
        backup_data["extensions"][ext_key] = check_extension_installed(ext_id)
    
    backup_path = os.path.expanduser("~/.gnome_customizer_backup.json")
    with open(backup_path, 'w') as f:
        json.dump(backup_data, f)
    
    return backup_path

def restore_backup():
    """Restaura configurações do backup"""
    backup_path = os.path.expanduser("~/.gnome_customizer_backup.json")
    
    if not os.path.exists(backup_path):
        return False
    
    try:
        with open(backup_path, 'r') as f:
            backup_data = json.load(f)
        
        # Restaurar extensões
        for ext_key, is_enabled in backup_data["extensions"].items():
            ext_id = EXTENSIONS[ext_key]
            if check_extension_installed(ext_id):
                if is_enabled:
                    run_cmd(f"gnome-extensions enable {ext_id}")
                else:
                    run_cmd(f"gnome-extensions disable {ext_id}")
        
        reload_gnome_shell()
        return True
    except Exception as e:
        print(f"Erro ao restaurar backup: {e}")
        return False

# ===========================
# INTERFACE GTK
# ===========================
class LoadingScreen(Gtk.Window):
    def __init__(self, parent):
        super().__init__(title="Trocando o tema")
        self.set_decorated(False)
        self.set_modal(True)
        self.set_transient_for(parent)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_default_size(400, 200)
        
        # Fundo laranja
        orange_rgba = Gdk.RGBA()
        orange_rgba.parse("rgba(255,165,0,0.95)")
        
        self.override_background_color(Gtk.StateFlags.NORMAL, orange_rgba)
        
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        box.set_valign(Gtk.Align.CENTER)
        box.set_halign(Gtk.Align.CENTER)
        
        # Spinner
        self.spinner = Gtk.Spinner()
        self.spinner.set_size_request(64, 64)
        self.spinner.start()
        box.pack_start(self.spinner, False, False, 0)
        
        # Label
        self.label = Gtk.Label(label="Trocando o tema...")
        self.label.set_name("loading-label")
        css = b"#loading-label { font-size: 20px; color: white; font-weight: bold; }"
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(css)
        self.label.get_style_context().add_provider(css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        box.pack_start(self.label, False, False, 0)
        
        self.add(box)
        self.set_opacity(0.0)  # Inicia transparente
        
    def show_with_animation(self):
        """Mostra a tela com animação de fade in"""
        self.show_all()
        
        # Animação de fade in
        for i in range(10):
            opacity = i * 0.1
            GLib.timeout_add(i * 30, self.set_opacity, opacity)
        
    def hide_with_animation(self):
        """Esconde a tela com animação de fade out"""
        # Animação de fade out
        for i in range(10):
            opacity = 1.0 - (i * 0.1)
            GLib.timeout_add(i * 30, self.set_opacity, opacity)
        
        GLib.timeout_add(300, self.destroy)

class CustomizerWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Personalizador de Ambiente GNOME")
        self.set_border_width(15)
        self.set_default_size(700, 500)
        self.set_position(Gtk.WindowPosition.CENTER)
        
        # Configurar ícone da janela
        try:
            icon_path = get_resource_path("icon_app.png")
            if os.path.exists(icon_path):
                self.set_icon_from_file(icon_path)
            else:
                self.set_icon_name("system-settings")
        except:
            self.set_icon_name("system-settings")
        
        # Criar notebook (abas)
        self.notebook = Gtk.Notebook()
        self.add(self.notebook)
        
        # Aba de experiências
        exp_box = self.create_experiences_tab()
        self.notebook.append_page(exp_box, Gtk.Label(label="Experiências"))
        
        # Aba de utilitários
        utils_box = self.create_utils_tab()
        self.notebook.append_page(utils_box, Gtk.Label(label="Utilitários"))
        
        # Status bar
        self.statusbar = Gtk.Statusbar()
        self.statusbar.push(0, "Pronto")
        
        # Progress bar (inicialmente oculta)
        self.progressbar = Gtk.ProgressBar()
        self.progressbar.set_visible(False)
        
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        main_box.pack_start(self.notebook, True, True, 0)
        main_box.pack_start(self.progressbar, False, False, 0)
        main_box.pack_start(self.statusbar, False, False, 0)
        self.add(main_box)
        
        # Fazer backup inicial
        self.backup_path = create_backup()
        self.update_status(f"Backup criado em: {self.backup_path}")

    def create_experiences_tab(self):
        # Usar Grid para organizar em tiles
        grid = Gtk.Grid()
        grid.set_column_homogeneous(True)
        grid.set_row_homogeneous(True)
        grid.set_column_spacing(10)
        grid.set_row_spacing(10)
        grid.set_border_width(10)
        
        # Informação sobre extensões padrão
        info_label = Gtk.Label()
        info_label.set_markup("<b>Extensões sempre habilitadas:</b> Compiz, Cube, GSConnect, Emoji, Tiling, AppIndicators, Blur")
        info_label.set_halign(Gtk.Align.START)
        
        # Adicionar botões de experiências em tiles
        profiles_list = list(PROFILES.items())
        for i, (profile_key, profile_data) in enumerate(profiles_list):
            btn = self.create_tile_button(profile_data["name"], profile_data["icon"])
            btn.connect("clicked", self.on_experience_selected, profile_key)
            
            # Calcular posição na grid (2 colunas)
            row = i // 2
            col = i % 2
            grid.attach(btn, col, row, 1, 1)
        
        # Container principal
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        box.pack_start(info_label, False, False, 0)
        box.pack_start(grid, True, True, 0)
        
        return box

    def create_tile_button(self, label, icon_name):
        """Cria um botão tile com ícone e label"""
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        box.set_border_width(10)
        
        # Ícone
        try:
            pixbuf = get_icon_pixbuf(icon_name, 64)
            image = Gtk.Image.new_from_pixbuf(pixbuf)
        except:
            image = Gtk.Image.new_from_icon_name("application-x-executable", Gtk.IconSize.DIALOG)
        
        # Label
        label_widget = Gtk.Label(label=label)
        label_widget.set_max_width_chars(20)
        label_widget.set_line_wrap(True)
        label_widget.set_justify(Gtk.Justification.CENTER)
        
        box.pack_start(image, False, False, 0)
        box.pack_start(label_widget, False, False, 0)
        
        # Botão
        button = Gtk.Button()
        button.add(box)
        button.set_size_request(150, 150)
        
        return button

    def create_utils_tab(self):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        box.set_border_width(10)
        
        # Botão de backup
        btn_backup = Gtk.Button.new_with_label("Criar Backup Atual")
        btn_backup.connect("clicked", self.on_create_backup)
        box.pack_start(btn_backup, False, False, 0)
        
        # Botão de restore
        btn_restore = Gtk.Button.new_with_label("Restaurar Backup")
        btn_restore.connect("clicked", self.on_restore_backup)
        box.pack_start(btn_restore, False, False, 0)
        
        # Botão de recarregar GNOME
        btn_reload = Gtk.Button.new_with_label("Recarregar GNOME Shell")
        btn_reload.connect("clicked", self.on_reload_gnome)
        box.pack_start(btn_reload, False, False, 0)
        
        # Verificar extensões
        btn_check_ext = Gtk.Button.new_with_label("Verificar Extensões")
        btn_check_ext.connect("clicked", self.on_check_extensions)
        box.pack_start(btn_check_ext, False, False, 0)
        
        return box

    def on_experience_selected(self, widget, profile_name):
        """Aplica uma experiência em uma thread separada para não travar a UI"""
        # Mostrar tela de loading
        self.loading_screen = LoadingScreen(self)
        self.loading_screen.show_with_animation()
        
        # Aplicar mudanças após um breve delay para a animação
        GLib.timeout_add(500, self.start_experience_application, profile_name)

    def start_experience_application(self, profile_name):
        """Inicia a aplicação da experiência após a animação"""
        self.set_sensitive(False)
        self.progressbar.set_visible(True)
        self.progressbar.set_text("Preparando...")
        
        thread = threading.Thread(target=self.apply_experience_thread, args=(profile_name,))
        thread.daemon = True
        thread.start()

    def apply_experience_thread(self, profile_name):
        """Thread para aplicar experiência com feedback de progresso"""
        def progress_callback(message):
            GLib.idle_add(self.update_progress, message)
        
        # Pequeno delay para suavizar a transição
        time.sleep(0.5)
        
        success = apply_mode(profile_name, progress_callback)
        
        GLib.idle_add(self.on_experience_applied, profile_name, success)

    def update_progress(self, message):
        """Atualiza a barra de progresso (chamada da thread principal)"""
        self.progressbar.set_text(message)
        self.progressbar.pulse()
        return False

    def on_experience_applied(self, profile_name, success):
        """Callback quando a experiência é aplicada"""
        # Esconder tela de loading com animação
        if hasattr(self, 'loading_screen'):
            self.loading_screen.hide_with_animation()
        
        # Pequeno delay antes de reativar a interface
        GLib.timeout_add(500, self.finalize_experience_application, profile_name, success)

    def finalize_experience_application(self, profile_name, success):
        """Finaliza a aplicação da experiência"""
        self.set_sensitive(True)
        self.progressbar.set_visible(False)
        
        if success:
            profile = PROFILES[profile_name]
            self.show_info(
                f"Experiência {profile['name']} aplicada com sucesso!\n\n"
                f"Extensões habilitadas:\n- {', '.join(profile['extensions'])}\n- {', '.join(ALWAYS_ENABLED_EXTENSIONS)}"
            )
            self.update_status(f"Experiência {profile['name']} aplicada")
        else:
            self.show_error("Erro ao aplicar experiência. Verifique se as extensões estão instaladas.")

    def on_create_backup(self, widget):
        self.backup_path = create_backup()
        self.show_info(f"Backup criado em: {self.backup_path}")
        self.update_status("Backup criado")

    def on_restore_backup(self, widget):
        success = restore_backup()
        if success:
            self.show_info("Backup restaurado com sucesso!")
            self.update_status("Backup restaurado")
        else:
            self.show_error("Erro ao restaurar backup ou backup não encontrado")

    def on_reload_gnome(self, widget):
        self.update_status("Recarregando GNOME Shell...")
        reload_gnome_shell()
        self.show_info("GNOME Shell recarregado")
        self.update_status("GNOME Shell recarregado")

    def on_check_extensions(self, widget):
        """Verifica se as extensões necessárias estão instaladas"""
        missing_extensions = []
        
        for ext_key, ext_id in EXTENSIONS.items():
            if not check_extension_installed(ext_id):
                missing_extensions.append(ext_id)
        
        if missing_extensions:
            message = "Extensões não encontradas:\n\n" + "\n".join(missing_extensions)
            message += "\n\nInstale-as através do GNOME Extensions ou via navegador."
            self.show_error(message)
        else:
            self.show_info("Todas as extensões estão instaladas!")

    def update_status(self, message):
        self.statusbar.pop(0)
        self.statusbar.push(0, message)

    def show_info(self, message):
        dialog = Gtk.MessageDialog(
            parent=self,
            flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text=message
        )
        dialog.run()
        dialog.destroy()

    def show_error(self, message):
        dialog = Gtk.MessageDialog(
            parent=self,
            flags=0,
            message_type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.OK,
            text=message
        )
        dialog.run()
        dialog.destroy()

# ===========================
# MAIN
# ===========================
if __name__ == "__main__":
    # Verificar se estamos no GNOME
    desktop_env = os.environ.get("XDG_CURRENT_DESKTOP", "").lower()
    if "gnome" not in desktop_env:
        print("Aviso: Este script é otimizado para GNOME Desktop")
    
    win = CustomizerWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()