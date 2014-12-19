#!/usr/bin/env python

# example helloworld.py

import pygtk
pygtk.require('2.0')
import gtk

class pyntsc:

    def __init__(self):
        # create a new window
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)

        # When the window is given the "delete_event" signal (this is given
        # by the window manager, usually by the "close" option, or on the
        # titlebar), we ask it to call the delete_event () function
        # as defined above. The data passed to the callback
        # function is NULL and is ignored in the callback function.
        self.window.connect("delete_event", self.delete_event)

        # Here we connect the "destroy" event to a signal handler.
        # This event occurs when we call gtk_widget_destroy() on the window,
        # or if we return FALSE in the "delete_event" callback.
        self.window.connect("destroy", self.destroy)

        # Sets the border width of the window.
        self.window.set_border_width(10)

        #create pane to seperate work area from navigation
        self.hpaned = gtk.HPaned()
        self.window.add(self.hpaned)

        # Creates a new button with the label "Hello World".
        self.button = gtk.Button("Hello World")

        # When the button receives the "clicked" signal, it will call the
        # function hello() passing it None as its argument.  The hello()
        # function is defined above.
        self.button.connect("clicked", self.hello, None)

        # This will cause the window to be destroyed by calling
        # gtk_widget_destroy(window) when "clicked".  Again, the destroy
        # signal could come from here, or the window manager.
        self.button.connect_object("clicked", gtk.Widget.destroy, self.window)

        #self.text = self.create_text()
        self.text = gtk.TextView()
        buffer = self.text.get_buffer()
        iter = buffer.get_iter_at_offset(0)
        buffer.insert(iter, "This is a test\n")
        self.hpaned.add1(self.text)
        self.text.show()

        self.vpaned = gtk.VPaned()

        self.text2 = gtk.TextView()
        buffer2 = self.text2.get_buffer()
        iter2 = buffer2.get_iter_at_offset(0)
        buffer2.insert(iter2, "This is a second test\n")
        self.vpaned.add1(self.text2)
        self.text2.show()

        # This packs the button into the window (a GTK container).
        #self.window.add(self.button)
        self.hpaned.add2(self.vpaned)
        self.vpaned.add2(self.button)

        self.button.show()
        self.hpaned.show()
        self.vpaned.show()
        self.window.show()

    def hello(self, widget, data=None):
        print "Hello World"

    def delete_event(self, widget, event, data=None):
        # If you return FALSE in the "delete_event" signal handler,
        # GTK will emit the "destroy" signal. Returning TRUE means
        # you don't want the window to be destroyed.
        # This is useful for popping up 'are you sure you want to quit?'
        # type dialogs.
        print "delete event occurred"

        # Change FALSE to TRUE and the main window will not be destroyed
        # with a "delete_event".
        return False

    def destroy(self, widget, data=None):
        print "destroy signal occurred"
        gtk.main_quit()

    def main(self):
        # All PyGTK applications must have a gtk.main(). Control ends here
        # and waits for an event to occur (like a key press or mouse event).
        gtk.main()

    def create_text(self):
        view = gtk.TextView()
        buffer = view.get_buffer()
        scrolled_window = gtk.ScrolledWindow()
        scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrolled_window.add(view)
        scrolled_window.show_all()
        return scrolled_window

if __name__ == "__main__":
    hello = pyntsc()
    hello.main()
