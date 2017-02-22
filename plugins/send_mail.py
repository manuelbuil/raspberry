from curier_plugin import base

class SendMail(SendDriverBaseClass):

    def get_type():
        return "This is the mail driver"

    def send_message():
        return True
