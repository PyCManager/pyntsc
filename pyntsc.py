#!/usr/bin/env python

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

        #### ADD Tree View block
        #self.text = self.make_text("This is a test\n")
        self.tree_scroll = gtk.GtkScrolledWindow()
        tree = gtk.GtkTree()
        tree.connect("select_child", self.db_select_child, tree)
        tree.connect("unselect_child", self.cb_unselect_child, tree)
        tree.connect("selection_changed", self.cb_selection_changed)
        self.tree_scroll.add_with_viewport(tree)
        tree.show()
        itemnames = ["Haloween", "Appsrv", "Datasrv", "Websrv", "Buttsrv"]
        for i in itemnames:
            item = gtk.GtkTreeItem(itemnames[i])
            item.connect("select", self.cb_itemsignal, "select")
            item.connect("deselect", self.cb_itemsignal, "deselect")
            item.connect("toggle", self.cb_itemsignal, "toggle")
            item.connect("expand", selb.cb_itemsignal, "expand")
            item.connect("collapse", self.cb_itemsignal, "collapse")

            tree.append(item)
            item.show()

        ### End Tree View Block
        connection = {}
        connection['Haloween'] = {"Host": "192.168.5.36", "Port": 3389}
        connection['Appsrv'] = {"Host": "192.168.5.8", "Port": 9001}

        self.rd_Haloween = rDesktop(connection['Haloween'])
        self.rd_Appsrv = rDesktop(connection['Appsrv'])

        self.socketH = self.rd_Haloween._get_socket()
        self.socketA = self.rd_Appsrv._get_socket()

        self.notebook = self.make_notebook()

        self.hpaned = self.hpane()

        #self.text.show()
        self.tree_scroll.show()
        self.socketA.show()
        self.socketH.show()

        print "Socket ID: {0}".format(self.socketH.get_id())
        print "Socket ID: {0}".format(self.socketA.get_id())
        self.hproc = self.rd_Haloween._get_proc()
        self.aproc = self.rd_Appsrv._get_proc()

        self.rd_Haloween.start()
        self.rd_Appsrv.start()

        self.notebook.show()
        self.hpaned.show()
        self.window.show()

    def __del__(self):
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

        #hpaned.add1(self.text)
        hpaned.add1(self.tree_scroll)
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


class rDesktop(object):
    def __init__(self, connection):
        self.rdesktop_exe = "/usr/bin/rdesktop"
        self.host = connection['Host']
        self.port = connection['Port']
        #self.username = connection['Username']
        #self.password = connection['Password']
        #self.domain = connection['Domain']
        #self.GeoX = connection['GeoX']
        #self.GeoY = connection['GeoY']
        self.socket = False
        self.process = False

    def _get_socket(self):
        if not self.socket:
            self.socket = gtk.Socket()
        return self.socket

    def _get_proc(self):
        return self.process

    def start(self):
        socket = self._get_socket()
        self.process = subprocess.Popen([
            self.rdesktop_exe,
            "-X {0}".format(socket.get_id()),
            "{host}:{port}".format(host=self.host, port=self.port)
            ])
        socket.child_focus(gtk.DIR_TAB_FORWARD)

    def __del__(self):
        self.process.terminate()


class DataFile(object):
    def __init__(self):
        self.data_dir = "~/.pyntsc"
        self.data_file = "connections.json"



if __name__ == "__main__":
    hello = pyntsc()
    hello.main()
