class AuthStrategy:
    def authenticate(self, body):
        raise NotImplementedError("Subclasses devem implementar este método")
