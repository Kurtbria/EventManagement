import os

class PayPalClient:
    @staticmethod
    def client():
        environment = SandboxEnvironment(
            client_id=os.environ.get("PAYPAL_CLIENT_ID"),
            client_secret=os.environ.get("PAYPAL_CLIENT_SECRET")
        )
        return PayPalHttpClient(environment)
