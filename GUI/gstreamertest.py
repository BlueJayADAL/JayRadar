import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gst', '1.0')
from gi.repository import Gtk, Gst
from PIL import Image
from PIL.Image import Image as PILImage
from PIL.ImageTk import PhotoImage
import cv2
import numpy as np

class CameraWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Camera Display")

        # Create a video drawing area
        self.drawing_area = Gtk.DrawingArea()
        self.add(self.drawing_area)

        # Initialize GStreamer
        Gst.init(None)

        # Create a GStreamer pipeline
        self.pipeline = Gst.Pipeline()

        # Create elements for the pipeline
        self.videosrc = Gst.ElementFactory.make('v4l2src', None)
        self.videoconvert = Gst.ElementFactory.make('videoconvert', None)
        self.appsink = Gst.ElementFactory.make('appsink', None)

        # Configure the appsink
        self.appsink.set_property('emit-signals', True)
        self.appsink.set_property('caps', Gst.Caps.from_string('video/x-raw, format=BGR'))

        # Connect the appsink's "new-sample" signal
        self.appsink.connect('new-sample', self.on_new_sample)

        # Add elements to the pipeline
        self.pipeline.add(self.videosrc)
        self.pipeline.add(self.videoconvert)
        self.pipeline.add(self.appsink)

        # Link the elements
        self.videosrc.link(self.videoconvert)
        self.videoconvert.link(self.appsink)

        # Start the pipeline
        self.pipeline.set_state(Gst.State.PLAYING)

        # Register a callback for the window's "delete-event" signal
        self.connect('delete-event', self.on_delete_event)

    def on_new_sample(self, sink):
        # Retrieve the sample from the appsink
        sample = sink.emit('pull-sample')

        # Extract the image data from the sample
        buffer = sample.get_buffer()
        result, mapinfo = buffer.map(Gst.MapFlags.READ)
        width = buffer.get_size()[0]
        height = buffer.get_size()[1]

        # Create a numpy array from the buffer data
        array = np.ndarray(shape=(height, width, 3), dtype=np.uint8, buffer=mapinfo.data)

        # Create a PIL Image from the numpy array
        image = Image.fromarray(array)

        # Convert the PIL Image to a Tkinter PhotoImage
        photo = PhotoImage(image)

        # Update the drawing area with the new image
        self.drawing_area.set_size_request(width, height)
        self.drawing_area.set_from_image(photo)

        # Unmap the buffer
        buffer.unmap(mapinfo)

        return Gst.FlowReturn.OK

    def on_delete_event(self, *args):
        # Stop the pipeline when the window is closed
        self.pipeline.set_state(Gst.State.NULL)
        Gtk.main_quit(*args)


if __name__ == "__main__":
    # Initialize GTK
    Gtk.init(None)

    # Create a new camera window
    win = CameraWindow()
    win.show_all()

    # Start the GTK main loop
    Gtk.main()