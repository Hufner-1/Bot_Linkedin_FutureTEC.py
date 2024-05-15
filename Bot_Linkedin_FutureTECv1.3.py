from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

class LinkedInBot:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)

    def conectar(self):
        botoes = WebDriverWait(self.driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.reusable-search__entity-result-list.list-style-none button")))
        for botao in botoes:
            if botao.text.strip() == "Conectar":
                botao.click()
                print("Botão 'Conectar' clicado com sucesso!")
                return True
        return False

    def enviar_sem_nota(self):
        modal = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@data-test-modal][@role='dialog'][@tabindex='-1'][@class='artdeco-modal artdeco-modal--layer-default send-invite'][@size='medium'][@aria-labelledby='send-invite-modal']")))
        botao_enviar_sem_nota = modal.find_element(By.XPATH, "//span[@class='artdeco-button__text'][text()='Enviar sem nota']")
        botao_enviar_sem_nota.click()
        print("Botão 'Enviar sem nota' clicado com sucesso!")

    def cancelar(self):
        div_confirmacao = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@data-test-modal][@role='alertdialog'][@tabindex='-1'][@aria-describedby='dialog-desc-st3'][@class='artdeco-modal artdeco-modal--layer-confirmation '][@size='small'][@aria-labelledby='dialog-label-st3']")))
        botao_cancelar = div_confirmacao.find_element(By.XPATH, "//span[@class='artdeco-button__text'][text()='Cancelar']")
        botao_cancelar.click()
        print("Botão 'Cancelar' clicado com sucesso!")

    def navegar_para_proxima_pagina(self):
        botao_proxima_pagina = self.driver.find_element(By.XPATH, "//button[@aria-label='Avançar']")
        botao_proxima_pagina.click()
        print("Navegando para a próxima página de resultados.")
        time.sleep(2)

    def iniciar(self, termo_pesquisa):
        url_linkedin = f"https://www.linkedin.com/search/results/people/?keywords={termo_pesquisa}"
        self.driver.get(url_linkedin)

        while True:
            conectou = self.conectar()
            if not conectou:
                try:
                    self.navegar_para_proxima_pagina()
                except Exception as e:
                    print("Não foi possível encontrar o botão 'Próxima página' ou navegar para a próxima página:", e)
                    break

            try:
                self.enviar_sem_nota()
                self.cancelar()
            except TimeoutException:
                print("Modal não encontrada. Continuando...")

    def encerrar(self):
        self.driver.quit()

if __name__ == "__main__":
    bot = LinkedInBot()
    while True:
        termo_pesquisa = input("Digite o termo de pesquisa para o LinkedIn (ou 'exit' para sair): ")
        if termo_pesquisa.lower() == 'exit':
            break
        bot.iniciar(termo_pesquisa)
    bot.encerrar()
