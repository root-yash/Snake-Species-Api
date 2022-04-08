import torch
import torchvision

def predict(model, image):
    transformer = torchvision.transforms.Compose([
        torchvision.transforms.Resize(size=(418, 418)),
        torchvision.transforms.ToTensor(),
        torchvision.transforms.Normalize((0.4718, 0.4429, 0.3738), (0.2519, 0.2388, 0.2393))
    ])
    modified_image = transformer(image)
    with torch.no_grad():
        result = model(torch.unsqueeze(modified_image, dim=0))
    return str(int(result.argmax()))


