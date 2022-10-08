from PIL import Image

import Module_Graph
import Module_Input_Parametrs


def image_constructor():

    """The task of the function is to combine five rendered schemes into one"""

    size_total_img = [0, 0]

    with Image.open("temp\Clust.png") as left_img:
        left_img.load()
        left_img_size = left_img.size
    with Image.open("temp\Scheme_render.png") as centre_img:
        centre_img.load()
        centre_img_size = centre_img.size
    with Image.open("temp\Bau_fuel.png") as right_img:
        right_img.load()
        right_img_size = right_img.size
    with Image.open("temp\Oil_graph.png") as under_img:
        under_img.load()
        under_img_size = under_img.size
    with Image.open("temp\Top_graph.png") as top_img:
        top_img.load()
        top_img_size = top_img.size

    """Determining the Width and Height of Merged Schemas Based on Their Dimensions"""
    if Module_Input_Parametrs.Scheme_process[0][5] in (13, 19, 53, 55, 56, 23, 24):
        size_total_img[0] = max(left_img_size[0], top_img_size[0])
        size_total_img[1] = left_img_size[1] + top_img_size[1]
        var = None
    elif centre_img_size[1] < 0.75 * under_img_size[1]:
        var = True
        size_total_img[0] += left_img_size[0]
        if centre_img_size[0] < under_img_size[0]:
            size_total_img[0] += max(under_img_size[0], top_img_size[0]) + right_img_size[0]
        else:
            size_total_img[0] += max(centre_img_size[0], top_img_size[0], centre_img_size[0] + right_img_size[0])
        size_total_img[1] = under_img_size[1] + top_img_size[1] + centre_img_size[1]
        var_bau = None
    else:
        var = False
        if under_img_size[1] >= right_img_size[1]:
            if under_img_size[1] == right_img_size[1]:
                var_bau = None
            else:
                var_bau = True
            size_total_img[0] += left_img_size[0] + max(centre_img_size[0], top_img_size[0], right_img_size[0],
                                                        right_img_size[0] + centre_img_size[0]) + under_img_size[0]
            size_total_img[1] = max(left_img_size[1], centre_img_size[1], right_img_size[1], under_img_size[1]) + top_img_size[1]
        else:
            var_bau = False
            size_total_img[0] += left_img_size[0] + max(top_img_size[0], centre_img_size[0] + under_img_size[0], centre_img_size[0] + right_img_size[0])
            size_total_img[1] = max(left_img_size[1], centre_img_size[1], right_img_size[1] + under_img_size[1]) + top_img_size[1]

    """Create a blank canvas"""
    total_img = Module_Input_Parametrs.total_img = Image.new('RGB', (size_total_img[0], size_total_img[1]), '#7f7f7f')

    """Layout"""
    if var is None:
        total_img.paste(top_img, (0, 0))
        total_img.paste(left_img, (top_img_size[0] - left_img_size[0], top_img_size[1]))
    else:
        total_img.paste(left_img, (0, top_img_size[1]))
        total_img.paste(top_img, (left_img_size[0], 0))
        total_img.paste(centre_img, (left_img.size[0], top_img_size[1]))
        if var is False:
            if var_bau is True:
                total_img.paste(under_img, (left_img_size[0] + centre_img_size[0], top_img_size[1]))
                total_img.paste(right_img, (left_img_size[0] + centre_img_size[0] + under_img_size[0], top_img_size[1]))
            elif var_bau is False:
                total_img.paste(right_img, (left_img_size[0] + centre_img_size[0], top_img_size[1]))
                total_img.paste(under_img, (left_img_size[0] + centre_img_size[0], top_img_size[1] + right_img_size[1]))
            else:
                pass
        else:
            total_img.paste(under_img, (left_img_size[0], top_img_size[1] + centre_img_size[1]))
            total_img.paste(right_img, (left_img_size[0] + max(centre_img_size[0], under_img_size[0]), top_img_size[1]))

    """Create a blank canvas"""
    total_img.show()


def image_save(img_folder):

    """Saving the schema if needed"""

    if img_folder is None:
        return
    total_img = Module_Input_Parametrs.total_img
    total_img.save(img_folder)
    return
