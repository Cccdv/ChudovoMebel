from django.apps import AppConfig


class CheckoutConfig(AppConfig):
    name = 'checkout'
    verbose_name = 'Заказы'

    def ready(self):
        import checkout.signals
