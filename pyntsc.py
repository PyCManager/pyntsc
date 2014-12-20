#!/usr/bin/env python

# example helloworld.py

import pygtk
pygtk.require('2.0')
import gtk
import subprocess

class pyntsc:

    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", self.destroy)
        self.window.set_border_width(10)

        self.text = self.make_text("This is a test\n")
        self.text2 = self.make_text("This is a second test\n")

        self.socketH = gtk.Socket()
        self.socketA = gtk.Socket()
        self.notebook = self.make_notebook()

        self.hpaned = self.hpane()

        self.text.show()
        self.socketA.show()
        self.socketH.show()

        print "Socket ID: {0}".format(self.socketH.get_id())
        print "Socket ID: {0}".format(self.socketA.get_id())
        self.hproc = self.rdesktop(self.socketH.get_id(), "Haloween")
        self.aproc = self.rdesktop(self.socketA.get_id(), "Appsrv")

        self.notebook.show()
        self.hpaned.show()
        self.window.show()

    def __del__(self):
        self.hproc.terminate()
        self.aproc.terminate()
        print "rdesktops terminated"

    def make_notebook(self):
        notebook = gtk.Notebook()
        notebook.set_tab_pos(gtk.POS_TOP)
        notebook.append_page(self.socketA, None)
        notebook.append_page(self.socketH, None)

        return notebook

    def make_text(self, string):
        text = gtk.TextView()
        buffer = text.get_buffer()
        iter = buffer.get_iter_at_offset(0)
        buffer.insert(iter, string)

        return text

    def hpane(self):
        hpaned = gtk.HPaned()
        self.window.add(hpaned)

        hpaned.add1(self.text)
        hpaned.add2(self.notebook)

        return hpaned

    def delete_event(self, widget, event, data=None):
        print "delete event occurred"

        return False

    def destroy(self, widget, data=None):
        print "destroy signal occurred"
        gtk.main_quit()

    def main(self):
        gtk.main()

    def rdesktop(self, socket_id, server):
        connection = {}
        connection['Haloween'] = {"Host": "192.168.5.36", "Port": 3389}
        connection['Appsrv'] = {"Host": "192.168.5.8", "Port": 9001}
        rdesktop_exe = "/usr/bin/rdesktop"

        proc = subprocess.Popen([
            rdesktop_exe,
            "-X {0}".format(socket_id),
            "{0}:{1}".format(connection[server]['Host'], connection[server]['Port'])
        ])
        return proc

class rdesktop(object):
    def __init__(self, connection):
        self.host = connection['Host']
        self.port = connection['Port']
        self.username = connection['Username']
        self.password = connection['Password']
        self.domain = connection['Domain']
        self.GeoX = connection['GeoX']
        self.GeoY = connection['GeoY']

    def run(self):
        subprocess.Popen([rdesktop_exe, "-X {0}".format(socket_id), connection['Host']])

if __name__ == "__main__":
    hello = pyntsc()
    hello.main()
