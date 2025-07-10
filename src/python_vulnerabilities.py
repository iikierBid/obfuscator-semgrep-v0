#!/usr/bin/env python3
"""
ARQUIVO DE VULNERABILIDADES INTENCIONAIS EM PYTHON
Para testes e validação do Semgrep
"""

import os
import subprocess
import pickle
import hashlib
import random
import sqlite3
import requests
from urllib.parse import urlparse
import yaml
import jwt
import tempfile

# ================================
# 1. INJECTION ATTACKS
# ================================

# SQL Injection
def sql_injection_1(user_id):
    """Vulnerável: concatenação direta de string"""
    query = "SELECT * FROM users WHERE id = " + user_id
    return query

def sql_injection_2(email):
    """Vulnerável: f-string sem sanitização"""
    query = f"SELECT * FROM accounts WHERE email = '{email}'"
    return query

def sql_injection_3(name):
    """Vulnerável: % formatting"""
    query = "INSERT INTO users (name) VALUES ('%s')" % name
    return query

# Command Injection
def command_injection_1(filename):
    """Vulnerável: subprocess com shell=True"""
    cmd = f"cat {filename}"
    result = subprocess.run(cmd, shell=True, capture_output=True)
    return result.stdout

def command_injection_2(user_input):
    """Vulnerável: os.system"""
    os.system(f"ping -c 4 {user_input}")

def command_injection_3(file_path):
    """Vulnerável: subprocess.call"""
    subprocess.call(f"ls -la {file_path}", shell=True)

# LDAP Injection
def ldap_injection(username):
    """Vulnerável: construção de filtro LDAP"""
    filter_str = f"(uid={username})"
    return filter_str

# ================================
# 2. CRYPTOGRAPHY ISSUES
# ================================

# Weak Hash Algorithms
def weak_hash_md5(password):
    """Vulnerável: MD5 é criptograficamente fraco"""
    return hashlib.md5(password.encode()).hexdigest()

def weak_hash_sha1(data):
    """Vulnerável: SHA1 é criptograficamente fraco"""
    return hashlib.sha1(data.encode()).hexdigest()

# Hardcoded Secrets
SECRET_KEY = "hardcoded-secret-key-12345"  # Vulnerável
DATABASE_PASSWORD = "admin123"  # Vulnerável
API_TOKEN = "sk_live_abcdef123456789"  # Vulnerável

# Weak Random Number Generation
def weak_random():
    """Vulnerável: random não é criptograficamente seguro"""
    return random.random()

def weak_random_token():
    """Vulnerável: random para geração de tokens"""
    return str(random.randint(100000, 999999))

# ================================
# 3. DESERIALIZATION VULNERABILITIES
# ================================

# Unsafe Pickle
def unsafe_pickle_load(data):
    """Vulnerável: pickle.loads sem validação"""
    return pickle.loads(data)

def unsafe_pickle_file(filename):
    """Vulnerável: pickle.load de arquivo não confiável"""
    with open(filename, 'rb') as f:
        return pickle.load(f)

# Unsafe YAML
def unsafe_yaml_load(yaml_content):
    """Vulnerável: yaml.load sem Loader seguro"""
    return yaml.load(yaml_content)

# ================================
# 4. PATH TRAVERSAL & FILE SECURITY
# ================================

# Path Traversal
def path_traversal_1(filename):
    """Vulnerável: concatenação direta de path"""
    file_path = f"/var/www/uploads/{filename}"
    with open(file_path, 'r') as f:
        return f.read()

def path_traversal_2(user_path):
    """Vulnerável: os.path.join ainda pode ser vulnerável"""
    full_path = os.path.join("/safe/directory", user_path)
    with open(full_path, 'r') as f:
        return f.read()

# File permissions
def unsafe_file_permissions(filename):
    """Vulnerável: permissões muito abertas"""
    os.chmod(filename, 0o777)

# Temporary file race condition
def unsafe_temp_file():
    """Vulnerável: tempfile predictable"""
    temp_name = f"/tmp/temp_{random.randint(1000, 9999)}.tmp"
    with open(temp_name, 'w') as f:
        f.write("sensitive data")
    return temp_name

# ================================
# 5. AUTHENTICATION & AUTHORIZATION
# ================================

# JWT Vulnerabilities
def insecure_jwt_1():
    """Vulnerável: JWT com chave fraca"""
    payload = {"user": "admin", "role": "admin"}
    token = jwt.encode(payload, "weak-secret", algorithm="HS256")
    return token

def insecure_jwt_2():
    """Vulnerável: JWT sem verificação de algoritmo"""
    payload = {"user": "admin"}
    token = jwt.encode(payload, None, algorithm="none")
    return token

# Password Issues
def hardcoded_password_check(password):
    """Vulnerável: senha hardcoded"""
    return password == "admin123"

# ================================
# 6. INFORMATION DISCLOSURE
# ================================

# Sensitive Data in Logs
def sensitive_logging(credit_card, ssn):
    """Vulnerável: dados sensíveis em logs"""
    print(f"Processing payment for card: {credit_card}, SSN: {ssn}")

# Debug Information
def debug_info_disclosure():
    """Vulnerável: informações de debug em produção"""
    try:
        raise Exception("Database connection failed")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

# Password in URL
def password_in_url(username, password):
    """Vulnerável: senha na URL"""
    url = f"https://api.example.com/login?user={username}&pass={password}"
    return requests.get(url)

# ================================
# 7. REGEX VULNERABILITIES
# ================================

import re

# ReDoS (Regular Expression Denial of Service)
def regex_dos(input_string):
    """Vulnerável: regex com backtracking exponencial"""
    pattern = r"^(a+)+$"
    return re.match(pattern, input_string)

def regex_dos_2(email):
    """Vulnerável: regex complexo para email"""
    pattern = r"^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$"
    return re.match(pattern, email)

# ================================
# 8. XXE (XML External Entity)
# ================================

import xml.etree.ElementTree as ET

def xxe_vulnerability(xml_content):
    """Vulnerável: parsing XML sem proteção contra XXE"""
    return ET.fromstring(xml_content)

# ================================
# 9. SSRF (Server-Side Request Forgery)
# ================================

def ssrf_vulnerability(url):
    """Vulnerável: requisição sem validação de URL"""
    return requests.get(url)

def ssrf_with_user_input(user_url):
    """Vulnerável: SSRF com entrada do usuário"""
    parsed = urlparse(user_url)
    return requests.get(f"http://{parsed.netloc}/api/data")

# ================================
# 10. RACE CONDITIONS
# ================================

import threading
import time

# TOCTOU (Time-of-Check to Time-of-Use)
def toctou_vulnerability(filename):
    """Vulnerável: race condition entre check e use"""
    if os.path.exists(filename):  # Check
        time.sleep(0.1)  # Time gap
        with open(filename, 'r') as f:  # Use
            return f.read()

# ================================
# 11. BUFFER OVERFLOW SIMULATION
# ================================

def buffer_overflow_simulation(data):
    """Simulação de overflow (Python é mais seguro, mas ainda pode haver problemas)"""
    # Vulnerável: processamento de dados sem limite
    result = ""
    for i in range(len(data) * 1000000):  # Multiplicação perigosa
        result += str(i)
    return result

# ================================
# 12. DANGEROUS FUNCTIONS
# ================================

# Exec with user input
def dangerous_exec(code):
    """Vulnerável: exec com entrada do usuário"""
    exec(code)

# Eval with user input
def dangerous_eval(expression):
    """Vulnerável: eval com entrada do usuário"""
    return eval(expression)

# Import with user input
def dangerous_import(module_name):
    """Vulnerável: importação dinâmica"""
    module = __import__(module_name)
    return module

# ================================
# 13. PROTOTYPE POLLUTION (Python equivalent)
# ================================

def attribute_pollution(obj, attr_name, value):
    """Vulnerável: setattr sem validação"""
    setattr(obj, attr_name, value)

# ================================
# 14. INSECURE RANDOM
# ================================

def insecure_session_token():
    """Vulnerável: token de sessão previsível"""
    return str(random.randint(100000, 999999))

def insecure_password_reset():
    """Vulnerável: reset de senha previsível"""
    return str(random.randint(1000, 9999))

# ================================
# 15. SECURITY MISCONFIGURATIONS
# ================================

# Flask Security Issues (simulação)
def insecure_flask_config():
    """Vulnerável: configurações inseguras do Flask"""
    config = {
        'SECRET_KEY': 'development-key',  # Vulnerável
        'DEBUG': True,  # Vulnerável em produção
        'TESTING': True,  # Vulnerável em produção
    }
    return config

# ================================
# 16. MASS ASSIGNMENT
# ================================

def mass_assignment_vulnerability(user_data):
    """Vulnerável: atribuição em massa sem validação"""
    user = {}
    for key, value in user_data.items():
        user[key] = value  # Vulnerável: permite override de campos críticos
    return user

# ================================
# 17. TIMING ATTACKS
# ================================

def timing_attack_vulnerability(password):
    """Vulnerável: comparação de string que vaza informações de timing"""
    correct_password = "super_secret_password"
    return password == correct_password

# ================================
# 18. INSECURE DIRECT OBJECT REFERENCES
# ================================

def idor_vulnerability(user_id, resource_id):
    """Vulnerável: acesso direto sem verificação de autorização"""
    # Simulação de acesso a recurso sem verificar se o usuário tem permissão
    query = f"SELECT * FROM documents WHERE id = {resource_id}"
    return query

# ================================
# 19. CRYPTO IMPLEMENTATION FLAWS
# ================================

def weak_crypto_implementation():
    """Vulnerável: implementação de criptografia fraca"""
    # Usando algoritmo obsoleto
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    key = b"weak_key_16_byte"
    iv = b"weak_iv_16_bytes"
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    return cipher

if __name__ == "__main__":
    # Teste das vulnerabilidades
    print("🚨 ESTE ARQUIVO CONTÉM VULNERABILIDADES INTENCIONAIS!")
    print("⚠️  NÃO USE EM PRODUÇÃO!")
    
    # Exemplos de uso (vulneráveis)
    print(sql_injection_1("1 OR 1=1"))
    print(weak_hash_md5("password123"))
    print(command_injection_1("test.txt; rm -rf /")) 