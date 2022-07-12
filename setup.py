from setuptools import setup
 
REQUIRED_PACKAGES = ['scikit-image==0.17.2', 'Pillow==8.4.0', 'numpy==1.19.5', 'matplotlib==3.3.4']
 
setup(
   name="caption_generator",
   version="2.0",
   scripts=["model_output.py", "caption_generator.py", "models.py"],
   install_requires=REQUIRED_PACKAGES
)