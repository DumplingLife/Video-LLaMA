import torch
from video_llama.models.ImageBind import data
from video_llama.models.ImageBind.models import imagebind_model
from video_llama.models.ImageBind.models.imagebind_model import ModalityType

text_list=["A dog.", "A car", "A bird"]
assets_folder = "video_llama/models/ImageBind/.assets/"
image_paths=["dog_image.jpg", "car_image.jpg", "bird_image.jpg"]
image_paths = [assets_folder + x for x in image_paths]
audio_paths=["dog_audio.wav", "car_audio.wav", "bird_audio.wav"]
audio_paths = [assets_folder + x for x in audio_paths]

device = "cuda:0" if torch.cuda.is_available() else "cpu"

# Instantiate model
model, emb_size = imagebind_model.imagebind_huge()
model.load_state_dict(torch.load("../Video-LLaMA-2-7B-Finetuned/imagebind_huge.pth"))
model.eval()
model.to(device)

# Load data
inputs = {
    ModalityType.TEXT: data.load_and_transform_text(text_list, device),
    ModalityType.VISION: data.load_and_transform_vision_data(image_paths, device),
    ModalityType.AUDIO: data.load_and_transform_audio_data(audio_paths, device),
}

with torch.no_grad():
    embeddings = model(inputs)

print(
    "Vision x Text: ",
    torch.softmax(embeddings[ModalityType.VISION] @ embeddings[ModalityType.TEXT].T, dim=-1),
)
print(
    "Audio x Text: ",
    torch.softmax(embeddings[ModalityType.AUDIO] @ embeddings[ModalityType.TEXT].T, dim=-1),
)
print(
    "Vision x Audio: ",
    torch.softmax(embeddings[ModalityType.VISION] @ embeddings[ModalityType.AUDIO].T, dim=-1),
)

print(embeddings[ModalityType.VISION])
print(embeddings[ModalityType.AUDIO])
print(embeddings[ModalityType.TEXT])

# Expected output:
#
# Vision x Text:
# tensor([[9.9761e-01, 2.3694e-03, 1.8612e-05],
#         [3.3836e-05, 9.9994e-01, 2.4118e-05],
#         [4.7997e-05, 1.3496e-02, 9.8646e-01]])
#
# Audio x Text:
# tensor([[1., 0., 0.],
#         [0., 1., 0.],
#         [0., 0., 1.]])
#
# Vision x Audio:
# tensor([[0.8070, 0.1088, 0.0842],
#         [0.1036, 0.7884, 0.1079],
#         [0.0018, 0.0022, 0.9960]])
