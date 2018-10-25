import abc


class BaseTuvokPlugin(metaclass=abc.ABCMeta):

    def get_description(self):
        return None

    def get_name(self):
        return self.__class__.__name__

    @abc.abstractmethod
    def get_checks(self):
        pass
