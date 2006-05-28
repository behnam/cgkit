# Shadow module for module "ImageDraw"

try:

    # Try to import the original module...
    from ImageDraw import *
    
except ImportError:

    # Create dummy symbols...


    def Draw(*args, **keyargs):
        raise ImportError("No module named ImageDraw. Please install PIL (http://www.pythonware.com/products/pil/index.htm).")

    def ImageDraw(*args, **keyargs):
        raise ImportError("No module named ImageDraw. Please install PIL (http://www.pythonware.com/products/pil/index.htm).")

    def Outline(*args, **keyargs):
        raise ImportError("No module named ImageDraw. Please install PIL (http://www.pythonware.com/products/pil/index.htm).")

