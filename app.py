import web
import folium
from cStringIO import StringIO
import image
import urllib
from pygeocoder import Geocoder
from PIL import Image



urls = (
  '/location', 'Index',
  '/map', 'Map',
  '/images/(.*)', 'ImageDisplay',
  '/submit', 'Submit'
)

app = web.application(urls, globals())

render = web.template.render('templates/')

class Index(object):
    def render_map(event, loc):
        loc = Geocoder.geocode(loc)
        current_loc = str(loc[0].coordinates)
        lat, lng = map(float, current_loc.strip('()').split(','))
        #map_1 = folium.Map(location=loc[0].coordinates, zoom_start=18)
        loc_str = str(loc[0])
        #map_1.simple_marker(loc[0].coordinates, popup=loc_str)
        #map_1.create_map(path='templates/map.html')
        url = "http://maps.googleapis.com/maps/api/staticmap?center=" + str(lat) + "," + str(lng) + "&maptype=hybrid&zoom=17&&size=800x600&markers=color:blue%7C" + str(lat) + "," + str(lng)
        buffer = StringIO(urllib.urlopen(url).read())
        output = Image.open(buffer)
        output.save('map.png')
        #map_image = image.open(buffer)
        #return buffer


    def GET(self):
        return render.location()

    def POST(self):
        form = web.input(location="Location")
        loc = "%s" % (form.location)
        map_image = self.render_map(form.location)
        #return map_image
        return render.index(loc = loc)

class Map(object):
    def GET(self):
        return render.map()

class Submit(object):
    def POST(self):
        print "submitting!!!"
        return render.submit()

class ImageDisplay(object):
   def GET(self,fileName):
      imageBinary = open(fileName,'rb').read()
      return imageBinary



if __name__ == "__main__":
    app.run()