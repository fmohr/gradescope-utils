import unittest
import base64
from io import BytesIO
import pathlib

from gradescope_utils.autograder_utils.json_test_runner import DisabledTestException

created_figures = []

class TestTemplate(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.state = {
            "flags": set()
        }
    
    def check_state_existence(self):
        if not hasattr(self, "state"):
            raise ValueError(
                "The test has no 'state' attribute. This attribute is automatically instantiated upon test creation."
                f" The most likely explanation for this is that your class {type(self)} overwrite the setUpClass method without invoking this method in the parent class.")

    def skip_on_missing_flag(self, flag, msg):
        self.check_state_existence()
        if flag not in self.state["flags"]:
            raise DisabledTestException(msg)
    
    def set_flag(self, flag):
        self.check_state_existence()
        self.state["flags"].add(flag)

    @property
    def flags(self):
        self.check_state_existence()
        return frozenset(self.state["flags"])
    
    def plot_figure(self, fig, dpi=100, quality=70):
        self.check_state_existence()

        imgdir = pathlib.Path("img/")
        imgdir.mkdir(parents=True, exist_ok=True)

        # create index for this figure
        fig_num = len(created_figures)
        
        # produce figure output
        tmpfile = BytesIO()
        for target in [tmpfile, f"{imgdir}/{fig_num}.webp"]:
            fig.savefig(
                target,
                format="webp",
                dpi=dpi,
                bbox_inches="tight",
                pad_inches=0.02,
                pil_kwargs={
                    "quality": quality,
                    "method": 6    # best compression, slower
                })
        
        encoded = base64.b64encode(tmpfile.getvalue()).decode("iso-8859-1")
        print(f'<img src="data:image/webp;base64,{encoded}" />')

        # memorize this
        if "images" not in self.state:
            self.state["images"] = []
        self.state["images"].append(encoded)
        created_figures.append(fig)