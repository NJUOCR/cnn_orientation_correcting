import utils.uimg as uimg
from data import SingleCharData
from main import Main
from utils.utext import TextPage


def process(page_img, draw=False):
    """
    1. auto binarization
    2. orientation correcting
    3. text line segmentation
    4. char segmentation
    5. char image fit-resize
    6. infer
    :param draw:
    :param page_img:
    :return:
    """
    page = TextPage(page_img, 0, drawing_copy=page_img.copy() if draw else None)

    # 1.
    page.auto_bin()

    # 2.
    page.fix_orientation()

    # 3. & 4.
    page.split()

    main = Main()

    # 5. & 6.
    data = SingleCharData(64, 64) \
        .load_char_map("/usr/local/src/data/stage2/all/all.json") \
        .load_alias_map("/usr/local/src/data/stage2/all/aliasmap.json") \
        .set_images(page.make_infer_input()) \
        .init_indices()
    results = main.infer(infer_data=data, input_width=64, input_height=64,
                         num_class=4184, ckpt_dir='/usr/local/src/data/stage2/all/ckpts')
    page.set_result(results)
    for line in page.get_lines():
        line.mark_half()
        line.merge_components()
    uimg.save('/usr/local/src/data/results/single_pld_prob_result.jpg', page.drawing_copy)

    with open('/usr/local/src/data/results/single_pld_prob_result.txt', 'w', encoding='utf-8') as f:
        f.write(page.format_result())
    return page


if __name__ == '__main__':
    page_img_path = "doc_imgs/2014东刑初字第0100号_诈骗罪208页.pdf/img-0296.jpg"
    process(uimg.read(page_img_path, read_flag=1), draw=True)
