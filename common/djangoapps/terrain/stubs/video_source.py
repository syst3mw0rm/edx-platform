"""
Serve HTML5 video sources for acceptance tests
"""
from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
from threading import Thread
import os

from logging import getLogger
LOGGER = getLogger(__name__)


class VideoSourceRequestHandler(SimpleHTTPRequestHandler):
    def translate_path(self, path):
        """
        Remove any extra parameters from the path.
        For example /gizmo.mp4?1397160769634
        becomes /gizmo.mp4
        """
        root_dir = self.server.config.get('root_dir', None)
        path = '{}{}'.format(root_dir, path)
        return path.split('?')[0]


class VideoSourceHttpService(HTTPServer, object):
    """
    Simple HTTP server for serving HTML5 Video sources locally for tests
    """

    def __init__(self, port_num=0):
        """
        Configure the server to listen on localhost.
        Default is to choose an arbitrary open port.
        """
        # Files are automatically served from the current directory
        # so we need to change it, start the server, then set it back.
        orig_wd = os.getcwd()

        # Set the path to root, which we will add on to with a setting
        # for root_dir when we start it up.
        os.chdir('/')

        # Set up a dict for config, which will be used to set the
        # root directory we are serving files from.
        self.config = dict()

        # Start the server in a separate thread
        address = ('0.0.0.0', port_num)
        HTTPServer.__init__(self, address, VideoSourceRequestHandler)
        server_thread = Thread(target=self.serve_forever)
        server_thread.daemon = True
        server_thread.start()

        # Reset the current working directory
        os.chdir(orig_wd)

        # Log the port we're using to help identify port conflict errors
        LOGGER.debug('Starting service on port {0}'.format(self.port))

    def shutdown(self):
        """
        Stop the server and free up the port
        """
        # First call superclass shutdown()
        HTTPServer.shutdown(self)

        # We also need to manually close the socket
        self.socket.close()

    @property
    def port(self):
        """
        Return the port that the service is listening on.
        """
        _, port = self.server_address
        return port
