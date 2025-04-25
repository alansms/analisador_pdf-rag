# streamlit_app.py 

import streamlit as st
import signal
import os
import time
# ... outras importações ...

# --- Correção ---
# Mova qualquer registro de sinal para o nível superior AQUI
# Execute apenas na thread principal.
# É importante verificar se isso é REALMENTE necessário, 
# pois o Streamlit já lida com SIGINT (Ctrl+C).
try:
    # Exemplo: Registrar um handler para SIGTERM (sinal de término)
    def handle_sigterm(signum, frame):
        print("Recebido SIGTERM, finalizando...")
        # Adicione sua lógica de limpeza aqui, se necessário
        st.stop() # Ou outra forma de parar o Streamlit/app

    # Registre o sinal APENAS UMA VEZ na thread principal
    # Esta linha SÓ deve ser executada na thread principal!
    signal.signal(signal.SIGTERM, handle_sigterm) 
    print("Manipulador de SIGTERM registrado.")

except ValueError as e:
     # Isso ainda pode falhar se o Streamlit executar isso fora da main thread
     # em algum cenário. Pode ser necessário mais cuidado ou evitar signals.
    print(f"AVISO: Falha ao registrar sinal (pode ser esperado em recarregamentos): {e}")
except AttributeError:
    # signal não está disponível em todas as plataformas (ex: Windows pode ter limitações)
    print("AVISO: Módulo signal ou sinais específicos não disponíveis nesta plataforma.")


# --- Restante do seu código Streamlit ---

st.title("Meu App RAG")

# Código que pode iniciar threads ou usar bibliotecas como watchdog
# NÃO COLOQUE signal.signal() dentro de funções chamadas por botões
# ou em loops que rodam em background.

def potentially_threaded_function():
    # NUNCA chame signal.signal daqui
    time.sleep(10)
    print("Thread terminou")

if st.button("Iniciar Tarefa Longa"):
    # Exemplo de como iniciar uma thread (se necessário)
    # import threading
    # thread = threading.Thread(target=potentially_threaded_function)
    # thread.start()
    st.write("Tarefa iniciada (exemplo)")

# ... resto do seu app ...