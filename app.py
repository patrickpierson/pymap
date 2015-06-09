import web
import folium
from pygeocoder import Geocoder

urls = (
  '/location', 'Index',
  '/map', 'Map'

)

app = web.application(urls, globals())


render = web.template.render('templates/')

class Index(object):
    def render_map(event, loc):
        loc = Geocoder.geocode(loc)
        map_1 = folium.Map(location=loc[0].coordinates, zoom_start=18)
        loc_str = str(loc[0])
        map_1.simple_marker(loc[0].coordinates, popup=loc_str)
        map_1.create_map(path='templates/map.html')

    def GET(self):
        return render.location()

    def POST(self):
        form = web.input(location="Location")
        loc = "%s" % (form.location)
        self.render_map(form.location)
        return render.index(loc = loc)

class Map(object):
    def GET(self):
        return render.map()

    #def POST(self):
        #return render.map()

if __name__ == "__main__":
    app.run()