import tempfile, os, logging
from subprocess import Popen, PIPE
from . import constants

logger = logging.getLogger(__name__)

class Pandoc(object):

    CALL = ["pandoc", "-t","html5","--section-divs", "-s"]

    def __init__(self,template_args):
        self.orig_template = constants.PATHS['TEMPLATE_FILE']
        self.template = self.getTemplate(template_args)

        self.pandoc = Pandoc.CALL + ["--template", self.template.name] + \
            ["-V","base-url=%s" % constants.PATHS['TEMPLATE_PATH'] ] # baes-url pandoc variable


    def __del__(self):
        "clean up template directory"
        os.unlink(self.template.name)

    def call(self,content,output): 
        "call pandoc with content as stdin and output as stdout"
        # Execute pandoc to generate output
        pid = Popen(self.pandoc, stdin=PIPE,stdout=PIPE)
        out = pid.communicate(content.encode('utf-8'))

        output.write(out[0])
        output.flush()

    def selfContained(self):
        'encode external resources in base64'
        self.pandoc+= ["--self-contained"]


    def getTemplate(self,targs): 
        "create temporary pandoc template file from targs"
        template = tempfile.NamedTemporaryFile(mode='wb',delete=False,suffix=".html")
        with open(self.orig_template, 'r') as orig:
            template.write((orig.read().decode('utf-8') % targs).encode('utf-8'))
            template.flush()

        logger.info("pandoc template written to %s" % template.name)

        return template