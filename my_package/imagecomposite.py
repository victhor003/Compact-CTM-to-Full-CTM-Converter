from PIL import Image
import os
import numpy as np


res_options = [
            "x16",
            "x32",
            "x64",
            "x128",
            "x256",
            "x512",
        ]
res_cropping = {
    "x16" : 8,
    "x32" : 16,
    "x64" : 32,
    "x128" : 64,
    "x256" : 128,
    "x512" : 256,
}

class ImageLoader:
    def __init__(self):
        self.loaded_imgs = []
        self.opened_images = []
        self.current_inputs = []
        self.missing_entries = []
        self.inputloaded_images = []
        self.all_files_found = False

    def load_imgs(self, folder, missing_entries):
        print("Clearing Cache")

        self.all_files_found = False
        self.missing_entries = missing_entries
        self.current_inputs.clear()

        print("Starting scan")

        for path in os.listdir(folder):

            full_path = folder+"/"+path
            if os.path.isfile(full_path) and path.endswith(".png"):

                fn, fext = os.path.splitext(path)

                if fn in self.missing_entries:

                    self.missing_entries.remove(fn)
                    self.current_inputs.append(fn)
                    self.loaded_imgs.append(full_path)
                    print("✔ Found: " + str(full_path))
                    print(self.current_inputs)
                    img = Image.open(full_path)
                    self.opened_images.append(img)
                    resized_image = img.resize((128, 128), Image.NEAREST)
                    self.inputloaded_images.append(resized_image)

                else:

                    pass

            else:

                print("✘ Excluded: " + str(full_path))

        print("End of scan")

        if not self.missing_entries:
            self.all_files_found = True
            print("Compositing Preview")

    def get_loaded_images(self, index=None):
        if index is not None:
            return self.loaded_imgs[index]
        else:
            return self.loaded_imgs

    def get_loaded_files(self, index=None):
        if index is not None:
            return self.opened_images[index]
        else:
            return self.opened_images

    def clear_loaded_files(self):
        print('Cleared images')
        self.loaded_imgs.clear()
        self.opened_images.clear()
        self.inputloaded_images.clear()

    def generate_full_ctm(self, sel_res):
        components_a = []
        components_b = []
        components_c = []
        components_d = []
        components_e = []

        count_dic = {
            0 : components_a,
            1 : components_b,
            2 : components_c,
            3 : components_d,
            4 : components_e,
        }

        e = 0
        for image in self.opened_images:
            print(f'Image:{image}')
            # image.show()

            # 1º Quarter
            img = image.crop((0,0,sel_res,sel_res))
            count_dic[e].append(img)
            # img.show()

            # 2º Quarter
            img = image.crop((sel_res, 0, sel_res*2, sel_res))
            count_dic[e].append(img)
            # img.show()

            # 3º Quarter
            img = image.crop((0, sel_res, sel_res, sel_res*2))
            count_dic[e].append(img)
            # img.show()

            # 4º Quarter
            img = image.crop((sel_res, sel_res, sel_res*2, sel_res*2))
            count_dic[e].append(img)
            # img.show()

            e += 1

        print(f'A:{components_a}')
        print(f'B:{components_b}')
        print(f'C:{components_c}')
        print(f'D:{components_d}')
        print(f'E:{components_e}')

        return mount_ctms(components_a, components_b, components_c, components_d, components_e, 0)

    def generate_overlay(self, sel_res):
        if len(self.opened_images) < 5:
            empty = Image.new('RGBA', (sel_res*2, sel_res*2), (0, 0, 0, 0))
            self.opened_images.insert(0, empty)
        components_a = []
        components_b = []
        components_c = []
        components_d = []
        components_e = []

        count_dic = {
            0 : components_a,
            1 : components_b,
            2 : components_c,
            3 : components_d,
            4 : components_e,
        }

        e = 0
        for image in self.opened_images:
            count_dic[e].clear()
            print(f'Image:{image}')
            # image.show()

            # 1º Quarter
            img = image.crop((0,0,sel_res,sel_res))
            count_dic[e].append(img)
            # img.show()

            # 2º Quarter
            img = image.crop((sel_res, 0, sel_res*2, sel_res))
            count_dic[e].append(img)
            # img.show()

            # 3º Quarter
            img = image.crop((0, sel_res, sel_res, sel_res*2))
            count_dic[e].append(img)
            # img.show()

            # 4º Quarter
            img = image.crop((sel_res, sel_res, sel_res*2, sel_res*2))
            count_dic[e].append(img)
            # img.show()

            e += 1

        print(f'A:{components_a}')
        print(f'B:{components_b}')
        print(f'C:{components_c}')
        print(f'D:{components_d}')
        print(f'E:{components_e}')

        return mount_ctms(components_a, components_b, components_c, components_d, components_e, 1)

def mount_ctms(a_list, b_list, c_list, d_list, e_list, mode):
    a1 = a_list[0]
    a2 = a_list[1]
    a3 = a_list[2]
    a4 = a_list[3]
    b1 = b_list[0]
    b2 = b_list[1]
    b3 = b_list[2]
    b4 = b_list[3]
    c1 = c_list[0]
    c2 = c_list[1]
    c3 = c_list[2]
    c4 = c_list[3]
    d1 = d_list[0]
    d2 = d_list[1]
    d3 = d_list[2]
    d4 = d_list[3]
    e1 = e_list[0]
    e2 = e_list[1]
    e3 = e_list[2]
    e4 = e_list[3]
    selected_dict = None

    if mode == 0:
        fullctm_dict = {
            0: (a1, a2, a3, a4),
            1: (a1, d2, a3, d4),
            2: (d1, d2, d3, d4),
            3: (d1, a2, d3, a4),
            4: (a1, d2, c3, e4),
            5: (d1, a2, e3, c4),
            6: (c1, e2, c3, e4),
            7: (d1, d2, e3, e4),
            8: (e1, b2, e3, e4),
            9: (e1, e2, e3, b4),
            10: (b1, e2, b3, e4),
            11: (b1, b2, e3, e4),
            12: (a1, a2, c3, c4),
            13: (a1, d2, c3, b4),
            14: (d1, d2, b3, b4),
            15: (d1, a2, b3, c4),
            16: (c1, e2, a3, d4),
            17: (e1, c2, d3, a4),
            18: (e1, e2, d3, d4),
            19: (e1, c2, e3, c4),
            20: (b1, e2, e3, e4),
            21: (e1, e2, b3, e4),
            22: (e1, e2, b3, b4),
            23: (e1, b2, e3, b4),
            24: (c1, c2, c3, c4),
            25: (c1, b2, c3, b4),
            26: (b1, b2, b3, b4),
            27: (b1, c2, b3, c4),
            28: (c1, e2, c3, b4),
            29: (d1, d2, b3, e4),
            30: (c1, b2, c3, e4),
            31: (d1, d2, e3, b4),
            32: (b1, b2, b3, e4),
            33: (b1, b2, e3, b4),
            34: (e1, b2, b3, e4),
            35: (b1, e2, e3, b4),
            36: (c1, c2, a3, a4),
            37: (c1, b2, a3, d4),
            38: (b1, b2, d3, d4),
            39: (b1, c2, d3, a4),
            40: (e1, b2, d3, d4),
            41: (b1, c2, e3, c4),
            42: (b1, e2, d3, d4),
            43: (e1, c2, b3, c4),
            44: (b1, e2, b3, b4),
            45: (e1, b2, b3, b4),
            46: (e1, e2, e3, e4)
        }
        selected_dict = fullctm_dict

    if mode == 1:
        overlay_dict = {
            0: (a1, a2, a3, e4),
            1: (a1, a2, d3, d4),
            2: (a1, a2, e3, a4),
            3: (a1, c2, d3, b4),
            4: (c1, a2, b3, d4),
            5: (c1, c2, b3, b4),
            6: (b1, d2, b3, d4),
            7: (a1, c2, a3, c4),
            8: (b1, b2, b3, b4),
            9: (c1, a2, c3, a4),
            10: (d1, b2, a3, c4),
            11: (b1, d2, c3, a4),
            12: (d1, b2, d3, b4),
            13: (b1, b2, c3, c4),
            14: (a1, e2, a3, a4),
            15: (d1, d2, a3, a4),
            16: (e1, a2, a3, a4),
        }
        selected_dict = overlay_dict
    if selected_dict:
        output_image_list = [to_grid(selected_dict[i], 2) for i in selected_dict]
    else:
        print("❌ Error: No dictionary Assigned!")
    '''
    Old method, #Optimizations
    
    output_image_list = []

    for i in range(47):
        full_image = to_grid(fullctm_dict[i],2)
        output_image_list.append(full_image)
    '''
    return output_image_list

def to_grid(images, max_horiz=np.iinfo(int).max):
    n_images = len(images)
    n_horiz = min(n_images, max_horiz)
    h_sizes, v_sizes = [0] * n_horiz, [0] * ((n_images // n_horiz) + (1 if n_images % n_horiz > 0 else 0))
    for i, im in enumerate(images):
        h, v = i % n_horiz, i // n_horiz
        h_sizes[h] = max(h_sizes[h], im.size[0])
        v_sizes[v] = max(v_sizes[v], im.size[1])
    h_sizes, v_sizes = np.cumsum([0] + h_sizes), np.cumsum([0] + v_sizes)
    im_grid = Image.new('RGBA', (h_sizes[-1], v_sizes[-1]), color='#F0F0F0')
    for i, im in enumerate(images):
        im_grid.paste(im, (h_sizes[i % n_horiz], v_sizes[i // n_horiz]))
    return im_grid
