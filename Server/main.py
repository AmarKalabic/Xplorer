# -*- coding: utf-8 -*-

__version__ = "0.6"

__all__ = ["SimpleHTTPRequestHandler"]

import os
import posixpath
import BaseHTTPServer
import urllib
import cgi
import shutil
import mimetypes
from StringIO import StringIO
import SocketServer
import time
import sys
import unicodedata



class SimpleHTTPRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    """Simple HTTP request handler with GET and HEAD commands.

    This serves files from the current directory and any of its
    subdirectories.  It assumes that all files are plain text files
    unless they have the extension ".html" in which case it assumes
    they are HTML files.

    The GET and HEAD requests are identical except that the HEAD
    request omits the actual contents of the file.

    """

    server_version = "SimpleHTTP/" + __version__

    """def do_POST(self):
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={"REQUEST_METHOD": "POST"}
        )

        for item in form.list:
            print "%s=%s" % (item.name, item.value)"""

    def do_GET(self):
        """Serve a GET request."""
        f = self.send_head()
        if f:
            self.copyfile(f, self.wfile)
            f.close()

    def do_HEAD(self):
        """Serve a HEAD request."""
        f = self.send_head()
        if f:
            f.close()

    def send_head(self):
        """Common code for GET and HEAD commands.

        This sends the response code and MIME headers.

        Return value is either a file object (which has to be copied
        to the outputfile by the caller unless the command was HEAD,
        and must be closed by the caller under all circumstances), or
        None, in which case the caller has nothing further to do.

        """
        path_now = self.translate_path(self.path)
        path_change = (os.path.dirname(os.path.abspath(__file__)) + "/files/")
        if path_now.startswith("/home/files/"):
           pass
        else:
           os.chdir(path_change)
        path = self.translate_path(self.path) ### <---- dodan unicode() ##prikazati filename a ne path unicoded a download link googleati kako
        #path = path1.decode('ascii', 'ignore').makePath()
        #path = unicodedata.normalize('NFKD', path1).encode('ascii','ignore')
        #path2 = path1.decode("utf-8")
        #path = path2.encode("utf-8")
        #path = path2.encode("utf-8")
        ####self.send_error(500, path)
        f = None
        if os.path.isdir(path):
            for index in "index.html", "index.htm":
                index = os.path.join(path, index)
                if os.path.exists(index):
                    path = index
                    break
            else:
                return self.list_directory(path)
        ctype = self.guess_type(path)
        if ctype.startswith('text/'):
            mode = 'r'
        else:
            mode = 'rb'
        try:
            #self.send_error(405, path.encode("utf-8"))
            #self.send_error(500, path.decode("utf-8"))
            f = open(path.decode(sys.getfilesystemencoding()), mode)
            size = os.path.getsize(path)
        except IOError:
            self.send_error(404, "File not found")
            return None
        self.send_response(200)
        self.send_header("Content-type", ctype + '; charset="utf-8"') # + " charset=utf-8"
        self.send_header("Content-Length", size)
        self.end_headers()
        return f

    def list_directory(self, path):
        """Helper to produce a directory listing (absent index.html).

        Return value is either a file object, or None (indicating an
        error).  In either case, the headers are sent, making the
        interface the same as for send_head().

        """
        try:
            list = os.listdir(path)
        except os.error:
            self.send_error(404, "No permission to list directory")
            return None
        list.sort(lambda a, b: cmp(a.lower(), b.lower()))
        f = StringIO()
        f.write("<title>Directory listing for %s</title>\n" % self.path)
        f.write("<h2>Directory listing for %s</h2>\n" % self.path)
        f.write("<hr>\n<ul>\n")
        for name in list:
            fullname = os.path.join(path, name)
            displayname = linkname = name = cgi.escape(name)
            # Append / for directories or @ for symbolic links
            if os.path.isdir(fullname):
                displayname = name + "/"
                linkname = name + "/"
            if os.path.islink(fullname):
                displayname = name + "@"
                # Note: a link to a directory displays with @ and links with /
            f.write('<li><a href="%s">%s</a>\n' % (linkname, displayname))
        f.write("</ul>\n<hr>\n")
        f.seek(0)
        self.send_response(200)
        self.send_header("Content-type", 'text/html; charset="utf-8"')
        self.end_headers()
        return f

    def translate_path(self, path):
        """Translate a /-separated PATH to the local filename syntax.

        Components that mean special things to the local file system
        (e.g. drive or directory names) are ignored.  (XXX They should
        probably be diagnosed.)

        """
        try:
            path = posixpath.normpath(urllib.unquote(path))
            words = path.split('/')
            words = filter(None, words)
            path = os.getcwd()
            for word in words:
                drive, word = os.path.splitdrive(word)
                head, word = os.path.split(word)
                if word in (os.curdir, os.pardir): continue
                path = os.path.join(path, word)
            return path
        except Exception, e:
           self.send_error(403, e)
           path = posixpath.normpath(urllib.unquote(path))
           words = path.split('/')
           words = filter(None, words)
           path = os.getcwd()
           for word in words:
               drive, word = os.path.splitdrive(word)
               head, word = os.path.split(word)
               if word in (os.curdir, os.pardir): continue
               path = os.path.join(path, word)
           return path.encode("utf-8")

    def copyfile(self, source, outputfile):
        """Copy all data between two file objects.

        The SOURCE argument is a file object open for reading
        (or anything with a read() method) and the DESTINATION
        argument is a file object open for writing (or
        anything with a write() method).

        The only reason for overriding this would be to change
        the block size or perhaps to replace newlines by CRLF
        -- note however that this the default server uses this
        to copy binary data as well.

        """
        shutil.copyfileobj(source, outputfile)

    def guess_type(self, path):
        """Guess the type of a file.

        Argument is a PATH (a filename).

        Return value is a string of the form type/subtype,
        usable for a MIME Content-type header.

        The default implementation looks the file's extension
        up in the table self.extensions_map, using text/plain
        as a default; however it would be permissible (if
        slow) to look inside the data to make a better guess.

        """

        base, ext = posixpath.splitext(path)
        if self.extensions_map.has_key(ext):
            return self.extensions_map[ext]
        ext = ext.lower()
        if self.extensions_map.has_key(ext):
            return self.extensions_map[ext]
        else:
            return self.extensions_map['']

    extensions_map = mimetypes.types_map.copy()
    extensions_map.update({
        '': 'application/octet-stream', # Default
        '.py': 'text/plain',
        '.c': 'text/plain',
        '.h': 'text/plain',
        })

class ForkingHTTPServer(SocketServer.ForkingMixIn, BaseHTTPServer.HTTPServer):
    def finish_request(self, request, client_address):
        request.settimeout(30)
        # "super" can not be used because BaseServer is not created from object
        BaseHTTPServer.HTTPServer.finish_request(self, request, client_address)
        #BaseHTTPServer.test(HandlerClass, ServerClass)


def test(HandlerClass = SimpleHTTPRequestHandler, ServerClass = BaseHTTPServer.HTTPServer, server_address=("192.168.1.2", 8000)):
    """server = BaseHTTPServer.test(HandlerClass, ServerClass)
    try:
        server
    except KeyboardInterrupt:
        server.socket.close()"""
    try:
        print "Server started"
        srvr = ForkingHTTPServer(server_address, HandlerClass)
        srvr.serve_forever()  # serve_forever
    except KeyboardInterrupt:
    	print "Closing sockets..."
    	time.sleep(2)
    	print "Server is shutting down in 3"
    	time.sleep(1)
    	print "Server is shutting down in 2"
    	time.sleep(1)
    	print "Server is shutting down in 1"
    	time.sleep(1)
        srvr.socket.close()


if __name__ == '__main__':
        test()