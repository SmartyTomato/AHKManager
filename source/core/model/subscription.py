class Subscription(object):

    def __init__(self):
        self.subscriptions: [] = []

    def subscribe(self, method):
        self.subscriptions.append(method)

    def on_subscription_changed(self):
        i = 0
        while i < len(self.subscriptions):
            method = self.subscriptions[i]
            try:
                method()
                i += 1
            except Exception as error:
                del self.subscriptions[i]
                print(error)
