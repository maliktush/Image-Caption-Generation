import os
import torch
import base64
from io import BytesIO

class ImageCaptionGenerator(object):
	def __init__(self, model):
		self._model = model

	@classmethod
	def from_path(cls, model_dir):
		model_file = os.path.join(model_dir,'caption_generator.pth')
		model = torch.load(model_file)
		return cls(model)

	def predict(self, instances, **kwargs):
		image_string = instances[0] #assume only one instance is present
		image_string = image_string.encode('utf-8')
		img = BytesIO(base64.b64decode(image_string))
		caption, vis_img_bytes = self._model(img)
		vis_img_string = base64.b64encode(vis_img_bytes.getvalue()).decode()

		return caption, vis_img_string