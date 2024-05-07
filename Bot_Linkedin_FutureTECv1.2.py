from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

def clicar_botao_conectar():
    try:
        botoes = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.reusable-search__entity-result-list.list-style-none button")))
        for botao in botoes:
            if botao.text.strip() == "Conectar":
                botao.click()
                print("Botão 'Conectar' clicado com sucesso!")
                return True
        return False
    except TimeoutException:
        print("Nenhum botão 'Conectar' encontrado.")
        return False

def clicar_enviar_sem_nota():
    try:
        modal = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@data-test-modal][@role='dialog'][@tabindex='-1'][@class='artdeco-modal artdeco-modal--layer-default send-invite'][@size='medium'][@aria-labelledby='send-invite-modal']")))
        botao_enviar_sem_nota = modal.find_element(By.XPATH, "//span[@class='artdeco-button__text'][text()='Enviar sem nota']")
        botao_enviar_sem_nota.click()
        print("Botão 'Enviar sem nota' clicado com sucesso!")

        try:
            div_confirmacao = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@data-test-modal][@role='alertdialog'][@tabindex='-1'][@aria-describedby='dialog-desc-st3'][@class='artdeco-modal artdeco-modal--layer-confirmation '][@size='small'][@aria-labelledby='dialog-label-st3']")))
            botao_cancelar = div_confirmacao.find_element(By.XPATH, "//span[@class='artdeco-button__text'][text()='Cancelar']")
            botao_cancelar.click()
            print("Botão 'Cancelar' clicado com sucesso!")
        except:
            pass
    except TimeoutException:
        print("Modal não encontrada. Continuando...")

# Inicializa o navegador
driver = webdriver.Chrome()  # ou qualquer outro navegador suportado
driver.implicitly_wait(10)  # Adiciona um tempo de espera implícito de 10 segundos

# Abre a página do LinkedIn
driver.get("https://www.linkedin.com/search/results/people/?keywords=")

while True:
    # Solicita que o usuário insira o termo de pesquisa
    termo_pesquisa = input("Digite o termo de pesquisa para o LinkedIn (ou 'exit' para sair): ")
    if termo_pesquisa.lower() == 'exit':
        break

    # Constrói a URL com o termo de pesquisa
    url_linkedin = f"https://www.linkedin.com/search/results/people/?keywords={termo_pesquisa}"

    # Altera a URL principal para a URL com o termo de pesquisa
    driver.get(url_linkedin)

    while True:
        # Clica no botão "Conectar"
        conectou = clicar_botao_conectar()
        
        if not conectou:
            # Se não houver mais botões "Conectar", navega para a próxima página
            try:
                botao_proxima_pagina = driver.find_element(By.XPATH, "//button[@aria-label='Avançar']")
                botao_proxima_pagina.click()
                print("Navegando para a próxima página de resultados.")
                time.sleep(2)  # Adiciona um pequeno atraso para garantir que a próxima página seja carregada completamente
            except Exception as e:
                print("Não foi possível encontrar o botão 'Próxima página' ou navegar para a próxima página:", e)
                break

        clicar_enviar_sem_nota()

# Encerrar o navegador após o término
driver.quit()
