
import web
import config
import os.path

render = web.template.render(os.path.join(os.path.dirname(__file__), 'templates'), cache=config.cache)

web.template.Template.globals.update(dict(
  datestr = web.datestr,
  render = render
))
