from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Inicializa o navegador
driver = webdriver.Chrome()  # ou qualquer outro navegador suportado

# Abre a página do LinkedIn
driver.get("https://www.linkedin.com/search/results/people/?keywords=")

# Espera até que a página esteja totalmente carregada ou até 60 segundos
WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "//input[@class='search-global-typeahead__input']")))

# Solicita que o usuário insira o termo de pesquisa
termo_pesquisa = input("Digite o termo de pesquisa para o LinkedIn: ")

# Constrói a URL com o termo de pesquisa
url_linkedin = f"https://www.linkedin.com/search/results/people/?keywords={termo_pesquisa}"

# Altera a URL principal para a URL com o termo de pesquisa
driver.get(url_linkedin)

# Função para clicar no botão "Conectar"
def clicar_botao_conectar():
    botoes = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.reusable-search__entity-result-list.list-style-none button")))
    for botao in botoes:
        if botao.text.strip() == "Conectar":
            botao.click()
            print("Botão 'Conectar' clicado com sucesso!")
            return True
    return False

try:
    while True:
        # Clica no botão "Conectar"
        conectou = clicar_botao_conectar()
        
        if not conectou:
            # Se não houver mais botões "Conectar", navega para a próxima página
            try:
                # Procura pelo botão "Próxima página" e clica nele
                botao_proxima_pagina = driver.find_element(By.XPATH, "//button[@aria-label='Avançar']")
                botao_proxima_pagina.click()
                print("Navegando para a próxima página de resultados.")
                # Aguarda até que os novos resultados sejam carregados
                WebDriverWait(driver, 10).until(EC.staleness_of(botao_proxima_pagina))
            except Exception as e:
                print("Não foi possível encontrar o botão 'Próxima página' ou navegar para a próxima página:", e)
                

        # Espera até que a modal seja visível
        modal = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@data-test-modal][@role='dialog'][@tabindex='-1'][@class='artdeco-modal artdeco-modal--layer-default send-invite'][@size='medium'][@aria-labelledby='send-invite-modal']")))
        
        # Procura pelo botão "Enviar sem nota" dentro da modal
        botao_enviar_sem_nota = modal.find_element(By.XPATH, "//span[@class='artdeco-button__text'][text()='Enviar sem nota']")
        
        # Clica no botão "Enviar sem nota"
        botao_enviar_sem_nota.click()
        print("Botão 'Enviar sem nota' clicado com sucesso!")

        try:
            # Verifica se a div de confirmação está presente na página
            div_confirmacao = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@data-test-modal][@role='alertdialog'][@tabindex='-1'][@aria-describedby='dialog-desc-st3'][@class='artdeco-modal artdeco-modal--layer-confirmation '][@size='small'][@aria-labelledby='dialog-label-st3']")))
            
            # Se a div de confirmação estiver presente, clique no botão "Cancelar"
            botao_cancelar = div_confirmacao.find_element(By.XPATH, "//span[@class='artdeco-button__text'][text()='Cancelar']")
            botao_cancelar.click()
            print("Botão 'Cancelar' clicado com sucesso!")
        except:
            pass
finally:
        time.sleep(180)  
        driver.quit()
