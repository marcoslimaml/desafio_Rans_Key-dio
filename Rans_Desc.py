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

# 1. Carregar a chave que foi gerada anteriormente
def load_key():
    try:
        return open("secret.key", "rb").read()
    except FileNotFoundError:
        print("Erro: A chave 'secret.key' não foi encontrada. Impossível descriptografar.")
        return None

# 2. Descriptografar arquivos em um diretório
def decrypt_files(directory):
    key = load_key()
    if not key:
        return
        
    f = Fernet(key)
    
    for file in os.listdir(directory):
        # Ignora a própria chave e a nota de resgate
        if file == "secret.key" or file == "RESGATE.txt":
            continue
            
        file_path = os.path.join(directory, file)
        
        if os.path.isfile(file_path):
            try:
                with open(file_path, "rb") as encrypted_file:
                    encrypted_data = encrypted_file.read()
                
                # Reverte a criptografia
                decrypted_data = f.decrypt(encrypted_data)
                
                with open(file_path, "wb") as decrypted_file:
                    decrypted_file.write(decrypted_data)
                
                print(f"Arquivo restaurado: {file}")
            except Exception as e:
                print(f"Falha ao descriptografar {file}: {e}")

# --- EXECUÇÃO ---
if __name__ == "__main__":
    test_dir = "./arquivos_teste" # Certifique-se de que este diretório existe
    decrypt_files(test_dir)
    print("\nProcesso de recuperação concluído.")