import unittest
import base64
from io import BytesIO

class TestTemplate(unittest.TestCase):

    
    def plot_figure(self, fig):

        tmpfile = BytesIO()
        #fig.savefig(tmpfile, format='png')
        fig.savefig(
            tmpfile,
            format="webp",
            dpi=100,
            bbox_inches="tight",
            pad_inches=0.02,
            pil_kwargs={
                "quality": 70,
                "method": 6    # best compression, slower
            })
        encoded = base64.b64encode(tmpfile.getvalue()).decode("iso-8859-1")
        print(f'<img src="data:image/webp;base64,{encoded}" />')
