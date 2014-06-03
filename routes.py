from handlers.index import IndexHandler
from handlers.login import LoginHandler
from handlers.mark import MarkHandler

routes = [
    (r'/', IndexHandler),
    (r'/\$login', LoginHandler),
    (r'/(\w{1,64})/', MarkHandler),
]
