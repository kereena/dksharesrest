import web

web.webapi.internalerror = web.debugerror

middleware = [web.reloader]

cache = False
