import pygtk
import gtk
import sys
import random
 
class Window(gtk.Window):
 
    def __init__(self):
        super(Window, self).__init__()
 
        self.connect('destroy', self.destroy_event)
 
        self.vbox = gtk.VBox()
 
        for i in range(10):
            entry = gtk.Entry()
            attrname = 'entry{}'.format(i)
            setattr(self, attrname, entry)
            self.vbox.pack_start(entry)
 
        self.button = gtk.Button('Generate')
        self.button.connect('clicked', self.button_clicked)
        self.vbox.pack_start(self.button)
 
        self.output = gtk.Label()
        self.vbox.pack_start(self.output)
 
        self.add(self.vbox)
 
        self.show_all()
 
    def button_clicked(self, widget):
        choice = random.choice(range(1, 21))
        self.output.set_text(str(choice))
 
    def destroy_event(self, widget):
        gtk.main_quit()
 
 
def main():
    window = Window()
    gtk.main()
 
if __name__ == '__main__':
    sys.exit(main())
