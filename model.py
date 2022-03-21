from typing import List, Tuple

import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim import lr_scheduler
from torchvision import datasets, models, transforms
import time
import copy

from PIL import Image

from grid import SQUARES


class GeoModel:
    def __init__(self):
        self.data_transforms = {
            "train": transforms.Compose(
                [
                    transforms.RandomResizedCrop(512),
                    transforms.ToTensor(),
                ]
            ),
            "val": transforms.Compose(
                [
                    transforms.Resize(512),
                    transforms.CenterCrop(512),
                    transforms.ToTensor(),
                ]
            ),
        }

        # TODO: create better organized validation dataset
        self.image_datasets = {
            "train": datasets.ImageFolder("data", self.data_transforms["train"]),
            "val": datasets.ImageFolder("valdata", self.data_transforms["val"]),
        }

        self.dataloaders = {
            x: torch.utils.data.DataLoader(
                self.image_datasets[x], batch_size=4, shuffle=True, num_workers=4
            )
            for x in ["train", "val"]
        }

        self.dataset_sizes = {x: len(self.image_datasets[x]) for x in ["train", "val"]}
        self.class_names = self.image_datasets["train"].classes
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

        self.net = models.resnet18(pretrained=True)
        self.num_features = self.net.fc.in_features
        self.net.fc = nn.Linear(self.num_features, len(self.class_names))

        self.net = self.net.to(self.device)

        self.criterion = nn.CrossEntropyLoss()

        # Observe that all parameters are being optimized
        self.optimizer = optim.SGD(self.net.parameters(), lr=0.001, momentum=0.9)

        # Decay LR by a factor of 0.1 every 7 epochs
        self.scheduler = lr_scheduler.StepLR(self.optimizer, step_size=7, gamma=0.1)

    def _train_model(self, model, criterion, optimizer, scheduler, num_epochs=25):
        since = time.time()

        best_model_wts = copy.deepcopy(model.state_dict())
        best_acc = 0.0

        for epoch in range(num_epochs):
            print("Epoch {}/{}".format(epoch, num_epochs - 1))
            print("-" * 10)

            # Each epoch has a training and validation phase
            for phase in ["train", "val"]:
                if phase == "train":
                    model.train()  # Set model to training mode
                else:
                    model.eval()  # Set model to evaluate mode

                running_loss = 0.0
                running_corrects = 0

                # Iterate over data.
                for inputs, labels in self.dataloaders[phase]:
                    inputs = inputs.to(self.device)
                    labels = labels.to(self.device)

                    # zero the parameter gradients
                    optimizer.zero_grad()

                    # forward
                    # track history if only in train
                    with torch.set_grad_enabled(phase == "train"):
                        outputs = model(inputs)
                        _, preds = torch.max(outputs, 1)
                        loss = criterion(outputs, labels)

                        # backward + optimize only if in training phase
                        if phase == "train":
                            loss.backward()
                            optimizer.step()

                    # statistics
                    running_loss += loss.item() * inputs.size(0)
                    running_corrects += torch.sum(preds == labels.data)
                if phase == "train":
                    scheduler.step()

                epoch_loss = running_loss / self.dataset_sizes[phase]
                epoch_acc = running_corrects.double() / self.dataset_sizes[phase]

                print(
                    "{} Loss: {:.4f} Acc: {:.4f}".format(phase, epoch_loss, epoch_acc)
                )

                # deep copy the model
                if phase == "val" and epoch_acc > best_acc:
                    best_acc = epoch_acc
                    best_model_wts = copy.deepcopy(model.state_dict())

            print()

        time_elapsed = time.time() - since
        print(
            "Training complete in {:.0f}m {:.0f}s".format(
                time_elapsed // 60, time_elapsed % 60
            )
        )
        print("Best val Acc: {:4f}".format(best_acc))

        # Load best model weights found during the training
        model.load_state_dict(best_model_wts)
        return model

    def train(self, num_epochs=25):
        self.net = self._train_model(
            self.net,
            self.criterion,
            self.optimizer,
            self.scheduler,
            num_epochs=num_epochs,
        )

    def save_to_disk(self, path: str = "models/resnet18v1"):
        torch.save(self.net.state_dict(), path)

    def load_from_disk(self, path: str = "models/resnet18v1"):
        self.net.load_state_dict(torch.load(path))
        self.net.eval()

    def predict_random_image(
        self,
    ) -> Tuple[Image.Image, List[float], Tuple[float, float]]:
        """Select a random image from the validaiton data, run inference
        on it, and return the image as well as the predicted probabilities
        and the correct location for the image.
        """
        _, (inputs, labels) = next(enumerate(self.dataloaders["val"]))
        inputs = inputs.to(self.device)
        labels = labels.to(self.device)

        raw_outputs = self.net(inputs)
        outputs = nn.functional.softmax(raw_outputs, dim=1)

        # Just take the first image + probabilities of the batch
        net_probabilities = outputs.cpu().detach().numpy()[0]

        # The probabilities are in the internal order of the network.
        # We need to assign them the correct class names
        probabilities = [None] * len(self.class_names)
        for i in range(len(self.class_names)):
            # Note that we assume that class names are just numbers of squares.
            # If we wanted to use strings instead, we would have to use a dict.
            probabilities[int(self.class_names[i])] = net_probabilities[i]

        return (
            transforms.ToPILImage()(inputs[0]).convert("RGB"),
            probabilities,
            SQUARES[int(self.class_names[int(labels[0])])].center,
        )


if __name__ == "__main__":
    print("Model file")
    # Load pre-trained model and finetune the weight by training it.
    # The model chosen is ResNet18, which is the 18-layer version of ResNet
    # pere-trained on the ImageNet dataset.
    # We just finetune the weights using our own Google Street View data.
    model = GeoModel()
    model.train(num_epochs=25)
    # Save model weights to disk so that we can load the trained model later
    model.save_to_disk()

    # Load pre-trained model and load the finetuned weights from disk
    model = GeoModel()
    model.load_from_disk()

    # Run inference on a random image from the validation dataset
    image, probs = model.predict_random_image()

    pass
