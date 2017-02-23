from setuptools import setup, find_packages

setup(
    name = "irrigation",
    version = "0.1",
    author = "Manuel Buil",
    author_email = "manuelbuil87@gmail.com",
    description = ("Water your plants based on weather forecast and its humidity"),
    license = "BSD",
#    include_package_data=True,
#    packages=find_packages(),
    entry_points={
        'water.curier': [
             'mail = plugins.send_mail:SendMail',
             'whatsapp = plugins.send_whatsapp:SendWhatsapp',
        ],
    },
)
