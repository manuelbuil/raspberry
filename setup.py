from setuptools import setup

setup(
    name = "My watering project",
    version = "0.1",
    author = "Manuel Buil",
    author_email = "manuelbuil87@gmail.com",
    description = ("Water your plants based on weather forecast and its humidity"),
    license = "BSD",
    entry_points={
        'watering.curier': [
             'mail = plugins.send_mail:SendMail',
             'whatsapp = plugins.send_whatsapp:SendWhatsapp',
        ],
    },
)
