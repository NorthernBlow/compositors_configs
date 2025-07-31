#!/usr/bin/env python3
"""
Автоматическое развертывание Hyprland конфигурации
"""

import os
import sys
import subprocess
import time
import json
from pathlib import Path
from typing import Optional

class HyprlandDeployer:
    def __init__(self):
        self.repo_root = Path(__file__).parent.parent.parent
        self.terraform_dir = self.repo_root / "automation" / "terraform"
        self.ansible_dir = self.repo_root / "automation" / "ansible"
        
    def run_command(self, cmd: list, cwd: Optional[Path] = None) -> tuple[int, str]:
        """Выполнить команду и вернуть код возврата и вывод"""
        try:
            result = subprocess.run(
                cmd, 
                cwd=cwd or Path.cwd(),
                capture_output=True,
                text=True,
                check=False
            )
            return result.returncode, result.stdout + result.stderr
        except Exception as e:
            return 1, str(e)
            
    def check_dependencies(self) -> bool:
        """Проверить наличие зависимостей"""
        deps = ["terraform", "ansible", "libvirtd"]
        missing = []
        
        for dep in deps:
            code, _ = self.run_command(["which", dep])
            if code != 0:
                missing.append(dep)
                
        if missing:
            print(f"❌ Отсутствуют зависимости: {', '.join(missing)}")
            return False
            
        print("✅ Все зависимости установлены")
        return True
        
    def terraform_init(self) -> bool:
        """Инициализация Terraform"""
        print("🔧 Инициализация Terraform...")
        code, output = self.run_command(["terraform", "init"], self.terraform_dir)
        if code != 0:
            print(f"❌ Ошибка инициализации Terraform: {output}")
            return False
        return True
        
    def terraform_apply(self) -> Optional[str]:
        """Создание VM через Terraform"""
        print("🚀 Создание виртуальной машины...")
        
        # Plan
        code, output = self.run_command(["terraform", "plan", "-out=tfplan"], self.terraform_dir)
        if code != 0:
            print(f"❌ Ошибка планирования Terraform: {output}")
            return None
            
        # Apply
        code, output = self.run_command(["terraform", "apply", "tfplan"], self.terraform_dir)
        if code != 0:
            print(f"❌ Ошибка применения Terraform: {output}")
            return None
            
        # Получить IP VM
        code, output = self.run_command(["terraform", "output", "-json"], self.terraform_dir)
        if code == 0:
            try:
                outputs = json.loads(output)
                vm_ip = outputs.get("vm_ip", {}).get("value")
                print(f"✅ VM создана с IP: {vm_ip}")
                return vm_ip
            except json.JSONDecodeError:
                pass
                
        return "192.168.100.100"  # fallback IP
        
    def wait_for_vm(self, vm_ip: str, timeout: int = 300) -> bool:
        """Ожидание готовности VM"""
        print(f"⏳ Ожидание готовности VM {vm_ip}...")
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            code, _ = self.run_command([
                "ssh", 
                "-o", "ConnectTimeout=5",
                "-o", "StrictHostKeyChecking=no",
                f"arch@{vm_ip}", 
                "echo ready"
            ])
            
            if code == 0:
                print("✅ VM готова к подключению")
                return True
                
            time.sleep(10)
            
        print("❌ Таймаут ожидания VM")
        return False
        
    def ansible_deploy(self, vm_ip: str) -> bool:
        """Развертывание конфигурации через Ansible"""
        print("🎯 Развертывание конфигурации...")
        
        # Обновить inventory с актуальным IP
        inventory_file = self.ansible_dir / "inventory.yml"
        with open(inventory_file, 'r') as f:
            inventory = f.read()
            
        inventory = inventory.replace("{{ vm_ip | default('192.168.100.100') }}", vm_ip)
        with open(inventory_file, 'w') as f:
            f.write(inventory)
            
        # Запустить playbook
        code, output = self.run_command([
            "ansible-playbook", 
            "-i", "inventory.yml",
            "playbook.yml",
            "-v"
        ], self.ansible_dir)
        
        if code != 0:
            print(f"❌ Ошибка Ansible: {output}")
            return False
            
        print("✅ Конфигурация развернута успешно")
        return True
        
    def test_deployment(self, vm_ip: str) -> bool:
        """Тестирование развертывания"""
        print("🧪 Тестирование конфигурации...")
        
        tests = [
            ("Waybar config", "ls ~/.config/waybar/style.css"),
            ("Neovim config", "ls ~/.config/nvim/init.lua"),
            ("Weather script", "python ~/.config/waybar/weather.py"),
            ("Load average script", "python ~/.config/waybar/la.py"),
        ]
        
        failed_tests = []
        for test_name, cmd in tests:
            code, output = self.run_command([
                "ssh",
                "-o", "StrictHostKeyChecking=no", 
                f"arch@{vm_ip}",
                cmd
            ])
            
            if code == 0:
                print(f"  ✅ {test_name}")
            else:
                print(f"  ❌ {test_name}: {output}")
                failed_tests.append(test_name)
                
        if failed_tests:
            print(f"❌ Провалены тесты: {', '.join(failed_tests)}")
            return False
            
        print("✅ Все тесты пройдены")
        return True
        
    def deploy(self) -> bool:
        """Полное развертывание"""
        if not self.check_dependencies():
            return False
            
        if not self.terraform_init():
            return False
            
        vm_ip = self.terraform_apply()
        if not vm_ip:
            return False
            
        if not self.wait_for_vm(vm_ip):
            return False
            
        if not self.ansible_deploy(vm_ip):
            return False
            
        if not self.test_deployment(vm_ip):
            return False
            
        print(f"🎉 Развертывание завершено успешно!")
        print(f"🖥️  Подключение: ssh arch@{vm_ip}")
        return True
        
    def destroy(self) -> bool:
        """Удаление VM"""
        print("🗑️  Удаление виртуальной машины...")
        code, output = self.run_command(["terraform", "destroy", "-auto-approve"], self.terraform_dir)
        if code != 0:
            print(f"❌ Ошибка удаления: {output}")
            return False
        print("✅ VM удалена")
        return True

def main():
    deployer = HyprlandDeployer()
    
    if len(sys.argv) > 1:
        action = sys.argv[1]
        if action == "destroy":
            deployer.destroy()
        elif action == "test":
            vm_ip = sys.argv[2] if len(sys.argv) > 2 else "192.168.100.100"
            deployer.test_deployment(vm_ip)
        else:
            print("Доступные команды: deploy, destroy, test")
    else:
        deployer.deploy()

if __name__ == "__main__":
    main()