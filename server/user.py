class User:
    """
      Represents a user. Holds name, IP address and socket client
    """
    def __init__(self, address, client):
        self.address = address
        self.client = client
        self.name = None

    def set_name(self, name):
        """
         Sets the name of the user
        :param self:
        :param name: String
        :return:
        """
        self.name = name

    def __repr__(self):
        return "USER( %r , %r) " % (self.name , self.address)
