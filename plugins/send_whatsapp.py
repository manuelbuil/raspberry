from curier_plugin import base

class SendWhatsapp(SendDriverBaseClass):

    def get_type():
        return "This is the whatsapp driver"

    def send_message():
        return True
