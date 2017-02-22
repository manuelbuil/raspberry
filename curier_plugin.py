import abc

@six.add_metaclass(abc.ABCMeta)
class SendDriverBaseClass(object):

    @abc.abstractmethod
    def get_type(self):
        ""Get driver's type.

        :returns the type of plug-in we use
        ""
        pass


    @abc.abstractmethod
    def send_message(self):
        ""Send the message to water the plants

        :returns True if everything went well
        ""
        pass
