PYTHON := python3
TERRAFORM_DIR := automation/terraform
ANSIBLE_DIR := automation/ansible
SCRIPTS_DIR := automation/scripts

.PHONY: help init deploy test clean destroy ssh status

help: ## Показать справку
    @echo "Доступные команды:"
    @grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

init: ## Инициализация проекта
    @echo "🔧 Инициализация..."
    cd $(TERRAFORM_DIR) && terraform init
    chmod +x $(SCRIPTS_DIR)/deploy.py

deploy: ## Развертывание полной инфраструктуры
    @echo "🚀 Запуск развертывания..."
    $(PYTHON) $(SCRIPTS_DIR)/deploy.py

test: ## Тестирование развернутой конфигурации
    @echo "🧪 Тестирование..."
    $(PYTHON) $(SCRIPTS_DIR)/deploy.py test

destroy: ## Удаление VM и очистка
    @echo "🗑️ Удаление инфраструктуры..."
    $(PYTHON) $(SCRIPTS_DIR)/deploy.py destroy

clean: ## Очистка временных файлов
    @echo "🧹 Очистка..."
    find . -name "*.pyc" -delete
    find . -name "__pycache__" -delete
    rm -f $(TERRAFORM_DIR)/tfplan
    rm -f $(TERRAFORM_DIR)/.terraform.lock.hcl

ssh: ## Подключение к VM
    @VM_IP=$$(cd $(TERRAFORM_DIR) && terraform output -raw vm_ip 2>/dev/null || echo "192.168.100.100"); \
    echo "🖥️ Подключение к $$VM_IP..."; \
    ssh -o StrictHostKeyChecking=no arch@$$VM_IP

status: ## Показать статус инфраструктуры
    @echo "📊 Статус Terraform:"
    @cd $(TERRAFORM_DIR) && terraform show -json 2>/dev/null | jq -r '.values.root_module.resources[] | select(.type == "libvirt_domain") | .values.name + ": " + (.values.network_interface[0].addresses[0] // "no IP")' || echo "VM не найдена"

logs: ## Показать логи развертывания
    @journalctl -u libvirtd --no-pager -n 50
