#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk, os, json
import subprocess

class pyntsc:

    def __init__(self):
        self.connection = {}
        self.datafile = DataFile()
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", self.destroy)
        self.window.set_border_width(10)
        gtk.Window.set_geometry_hints(self.window, min_width=650, min_height=400, max_width=-1, max_height=-1, base_width=650, base_height=400)

        self.make_treeview()

        self.notebook = self.make_notebook()

        self.hpaned = self.hpane()

        self.window.show_all()

    def make_treeview(self):
        machine_tree = self.datafile.get_connections()
        self.treestore = gtk.TreeStore(str)
        for item_cat, item_dict in machine_tree.iteritems():
            print "adding group: {0}".format(item_cat)
            piter = self.treestore.append(None, [item_cat])
            for item_name, item_details in item_dict['Items'].iteritems():
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
        pthinfo = treeview.get_path_at_pos(int(event.x), int(event.y))
        if pthinfo is not None:
            path, col, cellx, celly = pthinfo
            treeview.grab_focus()
            treeview.set_cursor(path, col, 0)
        treeselection = self.tree.get_selection()
        (model, iter) = treeselection.get_selected()
        print "iter is: {0}".format(iter)
        if iter is not None:
            name_of_connection = self.treestore.get_value(iter, 0)
        else:
            name_of_connection = None

        print "event.button: {0}, event.type: {1}".format(event.button, event.type)
        print "{0}".format(gtk.gdk._2BUTTON_PRESS)

        if event.button == 3:
            self.right_click_menu(event, name_of_connection)
        elif event.button == 1 and event.type == gtk.gdk._2BUTTON_PRESS:
            print "connecting to: {0}".format(name_of_connection)
            self.connection[name_of_connection] = rDesktop(self.datafile.get_connection_data(name_of_connection))
            app_socket = self.connection[name_of_connection]._get_socket()
            tab_label = gtk.Label(name_of_connection)
            tab_label.connect('button-press-event', self.connection[name_of_connection].focus)
            tab = self.notebook.append_page(app_socket, tab_label)
            self.connection[name_of_connection].start()
            app_socket.show()
            self.connection[name_of_connection].focus()

    def right_click_menu(self, event, name):
        print "Showing right_click_menu"
        menu = gtk.Menu()
        edit_menu_item = gtk.MenuItem("Edit Item")
        edit_menu_item.connect("activate", self.edit_window, name)
        add_menu_item = gtk.MenuItem("Add Item")
        add_menu_item.connect("activate", self.edit_window, None)
        if name is not None:
            menu.append(edit_menu_item)
            edit_menu_item.show()
        menu.append(add_menu_item)
        add_menu_item.show()
        menu.popup(None, None, None, event.button, event.time)

    def edit_window(self, object, name):
        #print "Name, Something_else: {0}, {1}".format(name, something_else)
        if name is None:
            window_name = "Add Connection"
            add = True
        else:
            window_name = "Edit Connection {0}".format(name)

        data = self.datafile.get_connection_data(name)
        print "data: {0}".format(data)

        #create Window
        edit_window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        #edit_window.connect("delete_event", edit_window.delete_event)
        edit_window.connect("destroy", edit_window.destroy)
        edit_window.set_border_width(10)
        edit_window.set_position(gtk.WIN_POS_CENTER)
        edit_window.label = gtk.Label(window_name)
        edit_window.set_size_request(472, 313)

        #Create structure
        #fixed = gtk.Fixed()
        #fixed.put(label, 60, 40)
        table = gtk.Table(9, 3)

        category_label = gtk.Label("Category:")
        category_combo = gtk.combo_box_entry_new_text()
        cats = self.datafile.get_categories()
        for cat in cats:
            category_combo.append_text(cat)

        cat_add = gtk.Button("Add")
        cat_edit = gtk.Button("Edit")

        cat_separator = gtk.HSeparator()

        name_label = gtk.Label("Connection Name:")
        name_label.set_justify(gtk.JUSTIFY_RIGHT)
        name_entry = gtk.Entry()
        name_entry.add_events(gtk.gdk.KEY_RELEASE_MASK)
        name_entry.set_text(data['Name'])

        hostname_label = gtk.Label("Hostname:")
        hostname_label.set_justify(gtk.JUSTIFY_RIGHT)
        hostname_entry = gtk.Entry()
        hostname_entry.add_events(gtk.gdk.KEY_RELEASE_MASK)
        hostname_entry.set_text(str(data['Host']))

        port_label = gtk.Label("Port:")
        port_label.set_justify(gtk.JUSTIFY_RIGHT)
        port_entry = gtk.Entry()
        port_entry.add_events(gtk.gdk.KEY_RELEASE_MASK)
        port_entry.set_text(str(data['Port']))

        geometry_label = gtk.Label("Geometry W/H:")
        geometry_label.set_justify(gtk.JUSTIFY_RIGHT)
        geometry_X_entry = gtk.Entry()
        geometry_X_entry.add_events(gtk.gdk.KEY_RELEASE_MASK)
        geometry_X_entry.set_text(str(data['GeoX']))
        geometry_Y_entry = gtk.Entry()
        geometry_Y_entry.add_events(gtk.gdk.KEY_RELEASE_MASK)
        geometry_Y_entry.set_text(str(data['GeoY']))

        def kill_window(thing):
            edit_window.destroy()

        button_separator = gtk.HSeparator()
        delete_button = gtk.Button("Delete")
        ok_button = gtk.Button("Ok")
        cancel_button = gtk.Button("Cancel")
        cancel_button.connect("released", kill_window)

        table.attach(category_label, 0, 1, 0, 1)
        table.attach(category_combo, 1, 3, 0, 1)
        table.attach(cat_add, 1, 2, 1, 2)
        table.attach(cat_edit, 2, 3, 1, 2)
        table.attach(cat_separator, 0, 3, 2, 3)
        table.attach(name_label, 0, 1, 3, 4)
        table.attach(name_entry, 1, 3, 3, 4)
        table.attach(hostname_label, 0, 1, 4, 5)
        table.attach(hostname_entry, 1, 3, 4, 5)
        table.attach(port_label, 0, 1, 5, 6)
        table.attach(port_entry, 1, 3, 5, 6)
        table.attach(geometry_label, 0, 1, 6, 7)
        table.attach(geometry_X_entry, 1, 2, 6, 7)
        table.attach(geometry_Y_entry, 2, 3, 6, 7)
        table.attach(button_separator, 0, 1, 7, 8)
        table.attach(delete_button, 0, 1, 8, 9)
        table.attach(ok_button, 1, 2, 8, 9)
        table.attach(cancel_button, 2, 3, 8, 9)

        edit_window.add(table)

        edit_window.show_all()

    def cat_edit_window(self):
        cat_window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        cat_window.connect("destroy", cat_window.destroy)
        cat_window.set_border_width(10)
        cat_window.set_position(gtk.WIN_POS_CENTER)
        cat_window.label = gtk.Label("Edit Category")
        cat_window.set_size_request(472, 313)

        table = gtk.Table(5, 3)

        category_name_label = gtk.Label("Category Name:")
        category_name_entry = gtk.Entry()
        category_name_entry.add_events(gtk.gdk.KEY_RELEASE_MASK)

        username_label = gtk.Label("Username:")
        username_entry = gtk.Entry()
        username_entry.add_events(gtk.gdk.KEY_RELEASE_MASK)

        password_label = gtk.Label("Password:")
        password_entry = gtk.Entry()
        password_entry.add_events(gtk.gdk.KEY_RELEASE_MASK)
        password_entry.set_visibility(False)

        domain_label = gtk.Label("Domain:")
        domain_entry = gtk.Entry()
        domain_entry.add_events(gtk.gdk.KEY_RELEASE_MASK)

        delete_button = gtk.Button("Delete")
        ok_button = gtk.Button("Ok")
        cancel_button = gtk.Button("Cancel")

        table.attach(category_name_label, 0, 1, 0, 1)
        table.attach(category_name_entry, 1, 3, 0, 1)
        table.attach(username_label, 0, 1, 1, 2)
        table.attach(username_entry, 1, 3, 1, 2)
        table.attach(password_label, 0, 1, 2, 3)
        table.attach(password_entry, 1, 3, 2, 3)
        table.attach(domain_label, 0, 1, 3, 4)
        table.attach(domain_entry, 1, 3, 3, 4)
        table.attach(delete_button, 0, 1, 4, 5)
        table.attach(ok_button, 1, 2, 4, 5)
        table.attach(cancel_button, 2, 3, 4, 5)

        cat_window.add(table)
        cat_window.show_all()

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
        self.socket.set_can_focus(True);
        #self.socket.grab_focus()
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
            os.mkdir(os.path.expanduser(self.data_dir), 0700)

    def write(self):
        self.make_dir()
        self.wfile = open(os.path,expanduser("{0}/{1}".format(self.data_dir, self.data_file)), 'w')
        self.wfile.write(json.dumps(self.connections))

    def update_connections(self, connections):
        self.connections = connections

    def get_connections(self):
        return self.connections

    def get_connection_data(self, name):
        print "get_connection_data is looking for: {0}".format(name)
        tree_model = self.get_connections()
        if name is not None:
            for cat in tree_model:
                for item in tree_model[cat]['Items']:
                    if name == item:
                        entry = tree_model[cat]['Items'][item]
                        entry['Parent'] = cat
                        entry['Name'] = item
                        return entry

    def get_categories(self):
        tree_model = self.get_connections()
        cats = tree_model.keys()
        print "get_categories returning: {0}".format(cats)
        return cats


if __name__ == "__main__":
    hello = pyntsc()
    hello.main()
