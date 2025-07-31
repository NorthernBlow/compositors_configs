terraform {
  required_providers {
    libvirt = {
      source = "dmacvicar/libvirt"
      version = "~> 0.7"
    }
  }
}

provider "libvirt" {
  uri = "qemu:///system"
}

# Создание виртуальной машины для тестирования
resource "libvirt_domain" "hyprland_test" {
  name   = "hyprland-test"
  memory = "4096"
  vcpu   = 4

  network_interface {
    network_name = "default"
  }

  disk {
    volume_id = libvirt_volume.hyprland_test.id
  }

  console {
    type        = "pty"
    target_port = "0"
    target_type = "serial"
  }

  graphics {
    type        = "spice"
    listen_type = "address"
    autoport    = true
  }
}

resource "libvirt_volume" "hyprland_test" {
  name   = "hyprland-test.qcow2"
  pool   = "default"
  source = "https://mirror.yandex.ru/archlinux/iso/latest/archlinux-x86_64.iso"
  format = "qcow2"
  size   = 21474836480 # 20GB
}