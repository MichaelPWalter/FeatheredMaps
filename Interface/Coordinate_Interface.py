from ipyleaflet import Map, TileLayer, DrawControl

# define a function to handle the polygon creation event
def handle_draw(self, action, geo_json):
    print(geo_json['geometry']['coordinates'][0])

# create a custom tile layer with your own tile server URL
tile_layer = TileLayer(
    url='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',  # replace with your own tile server URL
    attribution='Esri'  # replace with your own attribution text
)

# create a TileLayer object with the URL of the custom tile
overlay = TileLayer(
    url='https://stamen-tiles-{s}.a.ssl.fastly.net/toner-hybrid/{z}/{x}/{y}{r}.png',
    attribution='Stamen',
    name='Topographic Map'
)

# create a map object with your custom tile layer
m = Map(center=(0, 0), zoom=2, layers=[tile_layer])

# add the overlay to the map
m.add_layer(overlay)

# create a draw control and add it to the map
dc = DrawControl()
dc.on_draw(handle_draw)
dc.polygon = {
    "shapeOptions": {
        "fillColor": "#6be5c3",
        "color": "#6be5c3",
        "fillOpacity": 0.5
    },
    "allowIntersection": False
}
dc.circle = {
    "shapeOptions": {
        "fillColor": "#efed69",
        "color": "#efed69",
        "fillOpacity": 0.7
    }
}
dc.rectangle = {
    "shapeOptions": {
        "fillColor": "#fca45d",
        "color": "#fca45d",
        "fillOpacity": 0.5
    }
}
dc.circlemarker = {}
dc.polyline = {}
m.add_control(dc)

# display the map
m