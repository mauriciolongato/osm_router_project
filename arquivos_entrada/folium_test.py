import folium
import os
import SimpleHTTPServer
import SocketServer
import webbrowser

map_osm = folium.Map(location=[-23.5327531, -46.7140094])
map_osm.save('osm.html')

map_1 = folium.Map(location=[-23.5327, -46.714])
map_1.simple_marker([-23.5327, -46.714], popup='Mt. Teste I')
map_1.simple_marker([-23.5311, -46.720], popup='Timberline Teste II')
map_1.save('mthood.html')


try:
    Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
    httpd = SocketServer.TCPServer(("", 8080), Handler)
    httpd.serve_forever()
except KeyboardInterrupt:
    httpd.shutdown()
    httpd.server_close()



