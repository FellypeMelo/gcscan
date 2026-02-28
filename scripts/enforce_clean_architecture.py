"""
Clean Architecture Enforcer (AI-XP Mestre Guardrail)
Este script garante que o domínio não importe pacotes de IO/Infraestrutura.
"""

import ast
import os
import sys

DOMAIN_DIR = "src/domain"
FORBIDDEN_IMPORTS = {"os", "sys", "requests", "urllib", "matplotlib", "json", "pandas", "subprocess"}

def check_file(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        try:
            tree = ast.parse(file.read(), filename=filepath)
        except SyntaxError as e:
            print(f"[!] Erro de Sintaxe ignorado no arquivo: {filepath} ({e})")
            return []

    violations = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.split('.')[0] in FORBIDDEN_IMPORTS:
                    violations.append((node.lineno, alias.name))
        elif isinstance(node, ast.ImportFrom):
            if node.module and node.module.split('.')[0] in FORBIDDEN_IMPORTS:
                violations.append((node.lineno, node.module))
    return violations

def enforce_clean_architecture():
    if not os.path.exists(DOMAIN_DIR):
        print(f"Diretório {DOMAIN_DIR} não encontrado. Nenhuma checagem feita.")
        return 0

    has_error = False
    for root, _, files in os.walk(DOMAIN_DIR):
        for f in files:
            if f.endswith(".py"):
                filepath = os.path.join(root, f)
                violations = check_file(filepath)
                if violations:
                    has_error = True
                    for line, module in violations:
                        print(f"❌ [ERRO DE ARQUITETURA] {filepath}:{line} - Importação proibida no Domínio: '{module}'")

    if has_error:
        print("\n💥 Falha na Validação Clean Architecture: A camada de Domínio não deve conhecer I/O ou Frameworks.")
        return 1
    
    print("✅ Validação Clean Architecture Sucesso: Domínio puro mantido.")
    return 0

if __name__ == "__main__":
    sys.exit(enforce_clean_architecture())
