from base64 import b64encode
import db


async def decode_images(img_category, decode=True):
    context = []  # image_file, image_name, image_alt
    if decode:
        data_list = await db.get_images(img_category, with_bin=True)
        for item in data_list:
            _ = {
                'image_file': b64encode(bytes(item[0])).decode(),
                'image_name': item[1],
                'image_alt': item[2]
            }
            context.append(_)
    else:
        data_list = await db.get_images(img_category, with_bin=False)
        for item in data_list:
            _ = {
                'image_name': item[0],
                'image_alt': item[1]
            }
            context.append(_)
    return context


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['png', 'jpg', 'jpeg']
