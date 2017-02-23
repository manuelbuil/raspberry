from curier_plugin import SendDriverBaseClass 

class SendWhatsapp(SendDriverBaseClass):

    def get_type(self):
        return "Whatsapp driver"

    def send_message(self, message):
        return True
