from django.conf.urls import url

from channels.routing import ChannelNameRouter, ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

from rfmvp.consumers import rfmvp_WebSocketConsumer

# Consumer Imports
from clientflow.consumers import clientflowConsumer


application = ProtocolTypeRouter({

    # WebSocket handler
    "websocket": AuthMiddlewareStack(
        URLRouter([
            url(r"^ws/$", rfmvp_WebSocketConsumer),
        ])
    ),
    "channel": ChannelNameRouter({
        "clientflow": clientflowConsumer,
    })
})
