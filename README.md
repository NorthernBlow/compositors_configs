# hyprland_config

> 🌊 My personal Hyprland configuration with automated deployment

![Hyprland](https://img.shields.io/badge/Hyprland-Dynamic%20Tiling-blue?style=flat-square&logo=wayland)
![Waybar](https://img.shields.io/badge/Waybar-Status%20Bar-green?style=flat-square&logo=linux)
![Neovim](https://img.shields.io/badge/Neovim-NvChad-brightgreen?style=flat-square&logo=neovim)
![Terraform](https://img.shields.io/badge/Terraform-IaC-7B42BC?style=flat-square&logo=terraform)
![Ansible](https://img.shields.io/badge/Ansible-Automation-EE0000?style=flat-square&logo=ansible)
![Python](https://img.shields.io/badge/Python-Scripts-3776AB?style=flat-square&logo=python)
![Arch](https://img.shields.io/badge/Arch%20Linux-1793D1?style=flat-square&logo=arch-linux)

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Window Manager** | Hyprland | Dynamic tiling Wayland compositor |
| **Status Bar** | Waybar | Customizable status bar with weather widget |
| **Editor** | Neovim + NvChad | Modern Vim-based editor configuration |
| **Infrastructure** | Terraform + LibVirt | VM provisioning for testing |
| **Automation** | Ansible | Configuration deployment |
| **Scripting** | Python | Weather widget and system monitoring |

## 🧪 Testing

The configuration includes automated testing in QEMU/KVM virtual machines:

- Creates isolated Arch Linux VM
- Deploys full Hyprland environment
- Validates all configuration files
- Provides SSH access for manual testing

## 🚀 Quick Start

```bash
# Инициализация проекта
make init

# Полное развертывание в тестовой VM
make deploy

# Тестирование конфигурации
make test

# Подключение к VM
make ssh

# Удаление тестовой инфраструктуры
make destroy
```

<img src="https://github.com/NorthernBlow/hyprland_config/blob/main/assets/northern_atlantic_ocean.jpg" alt="hyprland"  />
