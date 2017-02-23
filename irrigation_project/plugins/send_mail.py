from curier_plugin import SendDriverBaseClass
import libs.gmail as gmail

class SendMail(SendDriverBaseClass):

    def get_type(self):
        return "Mail driver"

    def send_message(self, message):
        return gmail.send_mail(message)
