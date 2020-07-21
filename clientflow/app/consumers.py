from channels.consumer import SyncConsumer


class clientflowConsumer(SyncConsumer):

    def app1_message(self, message):
        # do something with message
        pass