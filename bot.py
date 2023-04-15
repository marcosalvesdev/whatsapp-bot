import os

from selenium.common import (
    NoSuchElementException,
    StaleElementReferenceException
)

from global_variables import (
    CONTACT_XPATH,
)
from helpers import WhatsAppBotAuxTools


class WhatsAppBot(WhatsAppBotAuxTools):

    def start(self):
        self.open_whatsapp()

        contacts_xpath = [
            CONTACT_XPATH % index for index in range(1, 18)
        ]
        count_first_cash = len(contacts_xpath)

        self.driver.implicitly_wait(0.0)

        while True:
            for contact_xpath in contacts_xpath:
                try:
                    contact, contact_name = self.get_contact(contact_xpath)
                    if count_first_cash > 0:
                        contact.click()
                        count_first_cash -= 1
                    contact_notifications = self.get_notifications(contact=contact, contact_xpath=contact_xpath)
                    if contact_notifications:
                        contact.click()
                    item, is_first_cache = self.check_last_contact_choice(contact_name)
                    if contact_notifications and is_first_cache:
                        self.wellcome_message()
                        continue
                    if item:
                        if not contact.is_selected():
                            contact.click()
                        self.send_text_message(
                            message=f"Você selecionou o item {item}"
                        )
                except (NoSuchElementException, StaleElementReferenceException):
                    continue


if __name__ == '__main__':
    whatsapp_bot = WhatsAppBot()
    whatsapp_bot.start()
