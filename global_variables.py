import os

NOTIFICATION_SPAN_CLASS = 'l7jjieqr'
NOTIFICATIONS_XPATH = f"%s/div/div/div/div[2]/div[2]/div[2]"
CONTACT_XPATH = '//*[@id="pane-side"]/div[2]/div/div[1]/div[%s]'
CONTACT_NAME_XPATH = "%s/div/div/div/div[2]/div[1]/div[1]/span"
TEXT_BOX_XPATH = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]'

FOOTER_XPATH = '//*[@id="main"]/footer/div[1]'
ATTACHMENTS_XPATH = f'{FOOTER_XPATH}/div/span[2]/div/div[1]/div[2]/div/span/div/div'
NORMAL_SEND_BUTTON_XPATH = f'{FOOTER_XPATH}/div/span[2]/div/div[2]/div[2]'
MEDIA_SEND_BUTTON_XPATH = '//*[@id="app"]/div/div/div[3]/div[2]/span/div/span/div/div/div[2]/div/div[2]/div[2]'
ATTACHMENT_ICON_XPATH = f'{FOOTER_XPATH}/div/span[2]/div/div[1]/div[2]/div/div'
ATTACHMENT_IMAGE_INPUT_XPATH = f'{FOOTER_XPATH}/div/span[2]/div/div[1]/div[2]/div/span/div/div/ul/li[1]/button/input'

WHATSAPP_URL = "https://web.whatsapp.com/"

INVALID_OPTION_MSG = "Opção inválida. Por favor, informe apenas o numero de identificação de itens do cardápio."
DEFAULT_WELLCOME_MESSAGE = """Olá, %s! Seja muito bem-vinda!\n
                           Sou seu atendente virtual e vou te auxiliar no seu pedido!\n
                           Confira o nosso cardápio do dia!"""

CASH_MESSAGES = dict()


MENU_MEDIA_PATH = os.getcwd() + "/medias/menu.jpeg"
MENU = {
    0: "Encerrar o antendimento.",
    1: "Água",
    2: "Refigerante",
    3: "Pastel",
    4: "Pizza",
    5: "Batata-frita",
    6: "Hamburger",
    8: "Café",
    7: "Falar com um atendente humano.",
}
