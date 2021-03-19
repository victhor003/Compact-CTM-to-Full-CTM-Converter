import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
from my_package import imagecomposite as ic
import os

class CTMTab(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.main = tk.Frame(parent)
        self.img_l = ic.ImageLoader()
        self.ready_e1 = False
        self.ready_e2 = False

        # Frames
        self.input_frame = tk.LabelFrame(self,text="Compact CTM Input",labelanchor="n")
        self.output_frame = tk.LabelFrame(self,text="Full CTM Output",labelanchor="n")
        self.side_frame = tk.Frame(self,width=90,height=500)
        self.input_img_frame = tk.LabelFrame(self.input_frame,text="Input Images",width=320, height=64,relief="sunken")
        self.output_preview_frame = tk.LabelFrame(self.output_frame
                                                  , text="Output Preview"
                                                  , width=520, height=500
                                                  , relief="sunken"
                                                  )

        # Input Frame Components
        self.readfrom_lable = tk.Label(self.input_frame, text="Read from:")
        self.input_entry = tk.Entry(self.input_frame, width=120, state="readonly")
        self.input_search_button = tk.Button(self.input_frame,
                                             text="Search",
                                             command=lambda: self.searchfolder(0)
                                             )

        # Input Frame Drawing
        self.readfrom_lable.grid(row=0, column=0, sticky="W")
        self.input_entry.grid(row=1, column=0, pady=5, padx=5)
        self.input_search_button.grid(row=1, column=1, pady=5, ipadx=5)

        # Imput Images Frame
        self.ph_imgage_1 = ImageTk.PhotoImage(Image.new('RGBA', (640, 128), color='#F0F0F0'))
        self.input_panel = tk.Label(self.input_img_frame, image=self.ph_imgage_1)
        self.input_panel.pack()

        # Output Frame Components
        self.output_lable = tk.Label(self.output_frame, text="Output to:")
        self.output_entry = tk.Entry(self.output_frame, width=120, state="readonly")
        self.output_search_button = tk.Button(self.output_frame,
                                              text="Search",
                                              command=lambda: self.searchfolder(1)
                                              )

        # Output Frame Drawing
        self.output_lable.grid(row=0, column=0, sticky="W")
        self.output_entry.grid(row=1, column=0, pady=5, padx=5)
        self.output_search_button.grid(row=1, column=1, pady=5, ipadx=5)

        # Output Preview Components
        self.ph_imgage_2 = ImageTk.PhotoImage(Image.new('RGBA', (768, 256), color='#F0F0F0'))
        self.output_preview_lable = tk.Label(self.output_preview_frame, image=self.ph_imgage_2)
        self.output_preview_lable.pack()

        # Side Frame Components
        self.texture_res_lable = tk.Label(self.side_frame, text="Texture\nResolution")
        self.res_combo = tk.ttk.Combobox(self.side_frame, value=ic.res_options, state="readonly")
        self.res_combo.current(0)
        self.preview_button = tk.Button(self.side_frame,
                                        text="Preview Output",
                                        state="disabled",
                                        command=self.preview_output
                                        )
        self.comfirm_conversion_button = tk.Button(self.side_frame
                                                   , text="Confirm",
                                                   state="disabled",
                                                   command=self.output_results
                                                   )

        # Side Frame Drawing
        self.texture_res_lable.grid(row=0, column=0, sticky="N", columnspan=2)
        self.res_combo.grid(row=1, column=0, columnspan=2, pady=5)
        self.preview_button.grid(row=2, column=0, pady=220)
        self.comfirm_conversion_button.grid(row=2, column=1, pady=220)

        # Draw Frames
        self.input_frame.grid(row=0, column=0, pady=30, padx=5)
        self.output_frame.grid(row=1, column=0, pady=10, padx=5)
        self.side_frame.grid(row=0, column=1, rowspan=2, pady=35, padx=5, sticky='N')
        self.input_img_frame.grid(row=2, column=0, columnspan=2, pady=5, padx=5)
        self.output_preview_frame.grid(row=2, column=0, columnspan=2, pady=5, padx=5)

    def searchfolder(self, mode):
        self.mode = {0:'Input', 1:'Output'}
        self.main.selectedfolder = tk.filedialog.askdirectory(title='Select ' + self.mode[mode] + ' Folder', initialdir="/")
        input_equals_output = False
        if os.path.exists(self.main.selectedfolder):
            if mode == 0:
                self.img_l.clear_loaded_files()
                self.input_entry.config(state='normal')
                self.input_entry.delete(0, tk.END)
                self.input_entry.insert(0, self.main.selectedfolder)
                self.input_entry.config(state='readonly')
                self.img_l.load_imgs(self.main.selectedfolder, ["0", "1", "2", "3", "4"])

                # Searching for all the necessary files
                if self.img_l.all_files_found:
                    self.loaded_preview = ic.to_grid(self.img_l.inputloaded_images)
                    self.tk_loaded_preview = ImageTk.PhotoImage(self.loaded_preview)
                    self.input_panel.configure(image=self.tk_loaded_preview)
                    self.input_panel.image = self.tk_loaded_preview
                    self.ready_e1 = True

                # Missing files, Canceling sequence and reporting error.
                else:
                    print("Files " + str(self.img_l.missing_entries) + " are missing")
                    stylized_error=[]
                    for missing in self.img_l.missing_entries:
                        stylized_error.append(str(missing))
                        stylized_error.append(".png\n")
                        print(stylized_error)
                    self.input_panel.config(image=self.ph_imgage_1)
                    error_text = "".join(stylized_error)
                    tk.messagebox.showerror("Missing Files","Files:\n" + str(error_text) + "not found.\n\nPlease make sure that the files you want\nto convert follow naming standards.")
                    self.ready_e1 = False

            if mode == 1:
                if os.access(self.main.selectedfolder, os.W_OK):
                    self.output_entry.config(state='normal')
                    self.output_entry.delete(0, tk.END)
                    self.output_entry.insert(0, self.main.selectedfolder)
                    self.output_entry.config(state='readonly')
                    self.ready_e2 = True
                else:
                    tk.messagebox.showerror("ERROR","Please select a writable folder.")
                    self.ready_e2 = False

            if self.output_entry.get() == self.input_entry.get():
                tk.messagebox.showwarning("WARNING","Input and Output directories are the same,\nthis WILL cause an overwrite.")
                input_equals_output = True

        self.check_if_ready()

    def check_if_ready(self):
        if self.ready_e1 and self.ready_e2:
            self.preview_button.config(state='normal')
            print('Ready to work')
        else:
            self.preview_button.config(state='disabled')
            print('Not ready to work')

    # Function of the preview button(Generate and show the output)
    def preview_output(self):
        self.preview_button.config(state='disabled')
        cropsize = ic.res_cropping[self.res_combo.get()]
        self.output = self.img_l.generate_full_ctm(cropsize)
        self.output_preview = self.output
        print(self.output_preview)
        self.composed_output_preview = ic.to_grid(self.output_preview,12)
        self.composed_output_preview = self.composed_output_preview.resize((768,256), Image.NEAREST)
        self.tk_composed_output = ImageTk.PhotoImage(self.composed_output_preview)
        self.output_preview_lable.configure(image=self.tk_composed_output)
        self.output_preview_lable.image = self.tk_composed_output
        self.preview_button.config(state='normal')
        if self.ready_e1 and self.ready_e2:
            self.comfirm_conversion_button.config(state='normal')


    # Function of the output button(Export the generated images to the selected folder)
    def output_results(self):
        o_path = self.output_entry.get()
        for i, image in enumerate(self.output):
            fp = o_path + f'/{i}.png'
            try:
                image.save(fp)
            except Exception:
                print('Something went Wrong!')