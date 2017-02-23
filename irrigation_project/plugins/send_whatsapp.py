from curier_plugin import SendDriverBaseClass 

class SendWhatsapp(SendDriverBaseClass):

    def get_type():
        return "This is the whatsapp driver"

    def send_message():
        return True
