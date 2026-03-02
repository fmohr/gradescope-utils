import unittest
import base64
from io import BytesIO
import pathlib

created_figures = []

class TestTemplate(unittest.TestCase):

    
    def plot_figure(self, fig):

        imgdir = pathlib.Path("img/")
        imgdir.mkdir(parents=True, exist_ok=True)

        #
        fig_num = len(created_figures)
        fig.savefig(f"{imgdir}/{fig_num}.png", format='png')
        created_figures.append(fig)

        # produce figure output
        tmpfile = BytesIO()
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
