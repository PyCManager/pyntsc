#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk, os, json
import subprocess

class pyntsc:

    def __init__(self):
        self.connection = {}
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", self.destroy)
        self.window.set_border_width(10)
        gtk.Window.set_geometry_hints(self.window, min_width=650, min_height=400, max_width=-1, max_height=-1, base_width=650, base_height=400)

        self.make_treeview()

        connection = self.fetch_tree_model()

        #self.rd_Haloween = rDesktop(connection['Home']['Snow'])
        #self.rd_Appsrv = rDesktop(connection['Home']['AppServer'])

        #self.socketH = self.rd_Haloween._get_socket()
        #self.socketA = self.rd_Appsrv._get_socket()

        self.notebook = self.make_notebook()

        self.hpaned = self.hpane()

        #print "Socket ID: {0}".format(self.socketH.get_id())
        #print "Socket ID: {0}".format(self.socketA.get_id())
        #self.hproc = self.rd_Haloween._get_proc()
        #self.aproc = self.rd_Appsrv._get_proc()

        self.window.show_all()
        #self.rd_Haloween.start()
        #self.rd_Appsrv.start()

    def make_treeview(self):
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
        self.tree.connect('button-press-event', self.treeview_button_press)

        self.tree_scroll.add(self.tree)

    def treeview_button_press(self, treeview, event):
        print "x, y: {0},{1}".format(str(event.x), str(event.y))
        treeselection = self.tree.get_selection()
        (model, iter) = treeselection.get_selected()
        name_of_connection = self.treestore.get_value(iter, 0)

        print "event.button: {0}, event.type: {1}".format(event.button, event.type)
        print "{0}".format(gtk.gdk._2BUTTON_PRESS)

        if event.button == 3:
            try:
                path, col, cellx, celly = treeview.get_path_at_pos(int(event.x), int(event.y))
            except TypeError:
                print "No associated item with click"
                self.popup()
                return True
            self.popup(name_of_connection)
        elif event.button == 1 and event.type == gtk.gdk._2BUTTON_PRESS:
            print "connecting to: {0}".format(name_of_connection)
            self.connection[name_of_connection] = rDesktop(self.get_machine_data(name_of_connection))
            appSocket = self.connection[name_of_connection]._get_socket()
            #hey lets crank up a stupid object just to display some text in a tab here
            tab_label = gtk.Label(name_of_connection)
            tab_label.connect('button-press-event', self.connection[name_of_connection].focus)
            tab = self.notebook.append_page(appSocket, tab_label)
            self.connection[name_of_connection].start()
            appSocket.show()
            self.connection[name_of_connection].focus()

    def get_machine_data(self, name):
        tree_model = self.fetch_tree_model()
        if name is not None:
            for cat in tree_model:
                for item in tree_model[cat]:
                    if name == item:
                        return tree_model[cat][item]

    def popup(self, name=None):
        #determine if name is a category or item
        tree_model = self.fetch_tree_model()
        if name is not None:
            for cat in tree_model:
                if name == cat:
                    self.cat_popup(name)
                    break
                for item in tree_model[cat]:
                    if name == item:
                        self.item_popup(name)
                        break
        else:
            self.cat_popup(None)

    def cat_popup(self, name):
        if name is None:
            print "new Cat Popup"
        else:
            print "in Cat Popup"

    def item_popup(self, name):
        print "in item popup"


    def fetch_tree_model(self):
        self.datafile = DataFile()
        return self.datafile.get_connections()

    def __del__(self):
        print "rdesktops terminated"

    def make_notebook(self):
        notebook = gtk.Notebook()
        notebook.set_tab_pos(gtk.POS_TOP)

        return notebook

    def hpane(self):
        hpaned = gtk.HPaned()
        self.window.add(hpaned)

        hpaned.add1(self.tree_scroll)
        hpaned.add2(self.notebook)

        hpaned.set_position(150)

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
            self.socket.connect('button-press-event', self.focus)
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

    def focus(self):
        print "calling focus to socket"
        self.socket.grab_focus()
        self.socket.child_focus(gtk.DIR_TAB_FORWARD)

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
