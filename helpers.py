import os
import time
from datetime import datetime
from typing import Optional

from cleantext import clean
from selenium import webdriver
from selenium.common import (
    NoSuchElementException,
    StaleElementReferenceException
)
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webelement import WebElement

from global_variables import (
    MENU,
    TEXT_BOX_XPATH,
    NORMAL_SEND_BUTTON_XPATH,
    NOTIFICATIONS_XPATH,
    NOTIFICATION_SPAN_CLASS,
    CASH_MESSAGES,
    WHATSAPP_URL,
    CONTACT_NAME_XPATH,
    ATTACHMENT_ICON_XPATH,
    ATTACHMENT_IMAGE_INPUT_XPATH,
    MEDIA_SEND_BUTTON_XPATH,
    INVALID_OPTION_MSG,
    DEFAULT_WELLCOME_MESSAGE,
    MENU_MEDIA_PATH,
)


class WhatsAppBotAuxTools:
    dir_path = os.getcwd()

    def __init__(self):
        self.chrome = Service(executable_path=f"{self.dir_path}/chrome_driver/chromedriver")
        self.options = Options()
        # self.options.add_argument('--headless')  # TODO: Check why this option is not working with Chrome
        self.options.add_argument(r"user-data-dir=" + self.dir_path + "\profile\wpp")
        self.driver = webdriver.Chrome(service=self.chrome, options=self.options)

    def open_whatsapp(self, implicitly_wait: int = 15):
        self.driver.get(WHATSAPP_URL)
        self.driver.implicitly_wait(implicitly_wait)

    def check_last_contact_choice(self, contact_name, get_last_received: bool = True) -> Optional[str]:
        last_metadata = "last_message_received" if get_last_received else "last_message_sent"
        last_message_metadata = self.get_last_messages().get(last_metadata)
        last_message_received = last_message_metadata.get("message")
        is_first_message_cached = None
        is_new_message = None
        try:
            last_message_received_id = last_message_metadata.get("message_id")
            if last_message_received:
                is_first_message_cached, is_new_message = self.cash_message(
                    message=last_message_received,
                    contact_name=contact_name,
                    message_id=last_message_received_id
                )
                if not is_first_message_cached and is_new_message:
                    option = int(last_message_received)
                    menu_item = MENU.get(option)

                    return menu_item, is_first_message_cached

                return None, is_first_message_cached

            return None, None

        except (TypeError, ValueError):
            if is_first_message_cached:
                return None, is_first_message_cached
            elif not is_first_message_cached and is_new_message:
                self.send_text_message(message=INVALID_OPTION_MSG)
            return None, is_first_message_cached

    def wellcome_message(self, message: str = None, contact_name: str = None):
        self.send_text_message(
            message=message or DEFAULT_WELLCOME_MESSAGE % contact_name
        )
        self.send_media_message(
            media_path=MENU_MEDIA_PATH
        )

    def send_message(self, is_media: bool = False):
        sender = self.driver.find_element(
            By.XPATH, NORMAL_SEND_BUTTON_XPATH if not is_media else MEDIA_SEND_BUTTON_XPATH
        )
        sender.click()

    def send_text_message(self, message: str, wait_time=None):
        time.sleep(wait_time) if wait_time else None
        text_box = self.driver.find_element(
            By.XPATH, TEXT_BOX_XPATH
        )
        text_box.click()
        text_box.send_keys(message)
        self.send_message()

    def send_media_message(self, media_path, wait_to_upload: float = 1):
        attachment_icon = self.driver.find_element(
            By.XPATH,
            ATTACHMENT_ICON_XPATH
        )
        attachment_icon.click()
        time.sleep(wait_to_upload)
        image_input = self.driver.find_element(
            By.XPATH, ATTACHMENT_IMAGE_INPUT_XPATH
        )
        image_input.send_keys(
            media_path
        )
        time.sleep(wait_to_upload)
        self.send_message(is_media=True)

    def get_contact(self, contact_xpath) -> tuple[WebElement, str]:
        """Returns the contact WebElement and the contact name"""
        contact = self.driver.find_element(By.XPATH, contact_xpath)
        contact_name_xpath = CONTACT_NAME_XPATH % contact_xpath
        contact_name_el = contact.find_element(By.XPATH, contact_name_xpath)
        return contact, self.format_name(contact_name_el.text)

    @staticmethod
    def get_notifications(contact: WebElement, contact_xpath: str) -> Optional[WebElement]:
        notifications_xpath = NOTIFICATIONS_XPATH % contact_xpath
        try:
            contact_notifications_div = contact.find_element(By.XPATH, notifications_xpath)
            return contact_notifications_div.find_element(By.CLASS_NAME, NOTIFICATION_SPAN_CLASS)
        except (NoSuchElementException, StaleElementReferenceException):
            return None

    def get_last_messages(self) -> dict:
        return {
            "last_message_received": self.get_last_message(),
            "last_message_sent": self.get_last_message(get_message_in=False),
        }

    def get_last_message(self, get_message_in=True) -> dict:
        last_message = None
        is_audio_or_video = False
        class_name = 'message-in' if get_message_in else 'message-out'
        messages = self.driver.find_elements(By.CLASS_NAME, class_name)
        message_id = None
        if messages:
            last_position_message = messages[-1]
            parent = last_position_message.find_element(By.XPATH, '..')
            message_id = parent.get_attribute("data-id")
            try:
                last_message = last_position_message.find_element(By.CLASS_NAME, 'selectable-text')
            except NoSuchElementException:
                is_audio_message = last_position_message.find_element(By.TAG_NAME, 'button')
                if is_audio_message:
                    is_audio_or_video = True

        return {
            "message": last_message.text if last_message else last_message,
            "is_audio_or_video": is_audio_or_video,
            "message_id": message_id
        }

    @staticmethod
    def format_name(full_name: str) -> str:
        """Remove emojis and uppercase the first letter"""
        full_name_cleaned = clean(full_name, no_emoji=True)
        name_parts = full_name_cleaned.split(' ')
        capitalized_names = [
            name.capitalize() for name
            in name_parts
        ]
        return ' '.join(capitalized_names)

    @staticmethod
    def get_contact_data_from_cash(contact_name: str) -> dict:
        return CASH_MESSAGES.get(contact_name)

    def update_chash_messages(self, message: str, contact_name: str, message_id: str) -> dict:
        CASH_MESSAGES.update(
            {
                contact_name: {
                    "message_id": message_id,
                    "message": message.lower(),
                    "timestamp": datetime.now()
                },

            }
        )
        return self.get_contact_data_from_cash(contact_name)

    def cash_message(self, message: str, contact_name: str, message_id: str) -> tuple[bool, bool]:
        """
        :return: (is_first_cache, is_new_message)
        """
        contact_last_cash = self.get_contact_data_from_cash(contact_name)
        if not contact_last_cash:
            self.update_chash_messages(message, contact_name, message_id)
            return True, True
        stored_message = contact_last_cash.get("message")
        if message.lower() != stored_message:
            self.update_chash_messages(message, contact_name, message_id)
            return False, True

        return False, False
