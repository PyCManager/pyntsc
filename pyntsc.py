#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk, os, json
import subprocess

class pyntsc:

    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", self.destroy)
        self.window.set_border_width(10)

        #### ADD Tree View block
        #self.text = self.make_text("This is a test\n")
        machine_tree = self.fetch_tree_model()
        self.treestore = gtk.TreeStore(str)
        for item_cat, item_dict in machine_tree.iteritems():
            print "adding group: {0}".format(item_cat)
            piter = self.treestore.append(None, [item_cat])
            for item_name, item_details in item_dict.iteritems():
                print "adding item: {0}".format(item_name)
                self.treestore.append(piter, [item_name])

        self.tree_scroll = gtk.ScrolledWindow()
        self.tree_scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)

        self.tree = gtk.TreeView(self.treestore)

        self.cell = gtk.CellRendererText()

        self.tvcolumn = gtk.TreeViewColumn('Connections')
        self.tvcolumn.pack_start(self.cell, True)
        self.tvcolumn.add_attribute(self.cell, 'text', 0)
        self.tvcolumn.set_sort_order(gtk.SORT_ASCENDING)
        self.tvcolumn.set_sort_column_id(0)
        self.tvcolumn.set_sort_indicator(True)

        self.tree.append_column(self.tvcolumn)
        self.tree.set_search_column(0)
        self.tree.set_reorderable(False)
        self.tree.set_enable_search(True)

        #self.tree_scroll.add_with_viewport(self.tree)
        self.tree_scroll.add(self.tree)


        ### End Tree View Block
        connection = {}
        connection['Haloween'] = {"Host": "192.168.5.46", "Port": 3389}
        connection['Appsrv'] = {"Host": "192.168.5.8", "Port": 9001}

        self.rd_Haloween = rDesktop(connection['Haloween'])
        self.rd_Appsrv = rDesktop(connection['Appsrv'])

        self.socketH = self.rd_Haloween._get_socket()
        self.socketA = self.rd_Appsrv._get_socket()

        self.notebook = self.make_notebook()

        self.hpaned = self.hpane()

        print "Socket ID: {0}".format(self.socketH.get_id())
        print "Socket ID: {0}".format(self.socketA.get_id())
        self.hproc = self.rd_Haloween._get_proc()
        self.aproc = self.rd_Appsrv._get_proc()

        self.window.show_all()
        self.rd_Haloween.start()
        self.rd_Appsrv.start()


    def fetch_tree_model(self):
        #tree = {}
        #tree['Home'] = {}
        #tree['Home']['Haloween'] = {"Host": "192.168.5.46", "Port": 3389}
        #tree['Home']['Appsrv'] = {"Host": "192.168.5.8", "Port": 9001}
        self.datafile = DataFile()
        return self.datafile.get_connections()
        #return tree

    def tree_select(self):
        print "tree element selected"

    def tree_unselect(self):
        print "tree element unselected"

    def item_select(self):
        print "item selected"

    def item_deselect(self):
        print "item unselected"

    def item_toggle(self):
        print "item toggled"

    def item_expand(self):
        print "item expanded"

    def item_collapse(self):
        print "item collapsed"

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

        hpaned.set_position(300)

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

        self.make_dir()
        if not os.path.isfile(os.path.expanduser("{0}/{1}".format(self.data_dir, self.data_file))):
            self.connections = {}
        else:
            self.rfile = open(os.path.expanduser("{0}/{1}".format(self.data_dir, self.data_file)), 'r')
            self.connections = json.loads(self.rfile.read())

    def make_dir(self):
        if not os.path.exists(os.path.expanduser(self.data_dir)):
            os.mkdir(self.data_dir, 0700)

    def write(self):
        self.make_dir()
        self.wfile = open(os.path,expanduser("{0}/{1}".format(self.data_dir, self.data_file)), 'w')
        self.wfile.write(json.dumps(self.connections))

    def update_connections(self, connections):
        self.connections = connections

    def get_connections(self):
        return self.connections



if __name__ == "__main__":
    hello = pyntsc()
    hello.main()
