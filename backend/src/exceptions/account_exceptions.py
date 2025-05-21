class AccountNotFoundError(Exception):
    "Exception used for failed account search."
    
    def __init__(self, message: str = "Could not find an account tied to this user."):
        self.message = message

    def __str__(self):
        return self.message