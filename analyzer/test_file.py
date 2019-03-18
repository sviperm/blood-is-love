import matplotlib.pyplot as plt
import io
import urllib
import base64


def image_to_string(image):
    plt.imshow(image)
    fig = plt.gcf()

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())

    uri = 'data:image/png;base64,' + urllib.parse.quote(string)
    html = f'<img src = "{uri}"/>'
    return html
