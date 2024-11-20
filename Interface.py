from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image


class GuInterface:

    def __init__(self, window):
        self.window = window
        self.image_width = None
        self.image_height = None
        self.watermark_width = None
        self.watermark_height = None
        self.selected_image_path = None
        self.selected_watermark_path = None

        self.canvas = None
        self.apply = None
        self.watermark = None
        self.image = None
        self.title = None
        self.position_variable = None
        self.position_options = None

        self.create_canvas()

    def create_canvas(self):
        self.window.title('Image Watermarking Desktop App')
        self.window.config(padx=100, pady=100, bg='#3E535E')

        # canvas
        self.canvas = Canvas(self.window, width=400, height=400, bg='black')
        self.canvas.grid(column=1, row=1)

        self.title = Label(self.window, text='Watermarking App', font=('Arial', 50, 'bold'), bg='#3E535E', fg='#fff')
        self.title.grid(column=1, row=0)

        self.image = Button(self.window, text='Select An Image', font=('Arial', 10, 'normal'),
                            command=self.select_image)
        self.image.grid(column=0, row=4)

        self.watermark = Button(self.window, text='Upload Watermark', font=('Arial', 10, 'normal'),
                                command=self.select_watermark)
        self.watermark.grid(column=1, row=3)

        self.apply = Button(self.window, text='Apply Watermark', font=('Arial', 10, 'normal'),
                            command=self.apply_watermark)
        self.apply.grid(column=2, row=4)

        self.position_variable = StringVar(value="Select Position")
        self.position_options = OptionMenu(
            self.window,
            self.position_variable,
            "Top-Left",
            "Top-Right",
            "Bottom-Left",
            "Bottom-Right"
        )
        self.position_options.config(highlightthickness=0)
        self.position_options.grid(column=1, row=5)

    def select_image(self):
        canvas_size = (400, 400)      # size of the canvas
        file_path = filedialog.askopenfilename()

        self.selected_image_path = file_path

        destination = Image.open(file_path)
        destination.thumbnail(canvas_size, Image.Resampling.LANCZOS)

        self.image_width, self.image_height = destination.size
        image = ImageTk.PhotoImage(destination)
        self.canvas.image = image
        self.canvas.create_image(200, 200, image=self.canvas.image)

    def select_watermark(self):
        watermark_size = (100, 100)
        file_path = filedialog.askopenfilename()

        self.selected_watermark_path = file_path

        destination = Image.open(file_path)
        destination.thumbnail(watermark_size, Image.Resampling.LANCZOS)

        self.watermark_width, self.watermark_height = destination.size
        watermark = ImageTk.PhotoImage(destination)
        self.canvas.watermark = watermark
        self.canvas.create_image(50, 50, image=self.canvas.watermark)

    def apply_watermark(self):
        positions = {
            "Top-Left": (0, 0),
            "Top-Right": (self.image_width - self.watermark_width, 0),
            "Bottom-Left": (0, self.image_height - self.watermark_height),
            "Bottom-Right": (
                self.image_width - self.watermark_width,
                self.image_height - self.watermark_height,
            ),
        }
        selected_pos = self.position_variable.get()
        position = positions[selected_pos]

        main_img = Image.open(self.selected_image_path).convert('RGBA')
        watermark_img = Image.open(self.selected_watermark_path).convert('RGBA')

        watermark_img = watermark_img.resize((self.watermark_width, self.watermark_height), Image.Resampling.LANCZOS)

        alpha = 150
        watermark_img.putalpha(alpha)

        main_img.thumbnail((self.image_width, self.image_height), Image.Resampling.LANCZOS)
        main_img.paste(watermark_img, position, watermark_img)

        path_to_save = filedialog.asksaveasfilename(defaultextension=".png",
                                                    filetypes=[("PNG Files", "*.png"), ("JPEG Files", "*.jpg")])
        if path_to_save:
            main_img.save(path_to_save)
            print(f'File saved to {path_to_save}')

