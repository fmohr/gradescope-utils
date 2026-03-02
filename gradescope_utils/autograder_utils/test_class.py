import unittest
import base64
from io import BytesIO

class TestTemplate(unittest.TestCase):

    
    def plot_figure(self, fig):

        tmpfile = BytesIO()
        fig.savefig(tmpfile, format='png')
        encoded = base64.b64encode(tmpfile.getvalue()).decode("iso-8859-1")
        print(f'<img src="data:image/png;base64,{encoded}" />')
