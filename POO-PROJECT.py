import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
import matplotlib.pyplot as plt

class SimpleMLP(nn.Module): 
    def __init__(self):
        super(SimpleMLP, self).__init__()
        self.fc1 = nn.Linear(28*28, 128)
        self.relu1 = nn.ReLU()
        self.fc2 = nn.Linear(128, 64)
        self.relu2 = nn.ReLU()
        self.fc3 = nn.Linear(64, 10)
        self.dropout = nn.Dropout(0.25)
    def forward(self, x):
        x = x.view(-1, 28*28)
        x = self.fc1(x)
        x = self.relu1(x)
        x = self.dropout(x)
        x = self.fc2(x)
        x = self.relu2(x)
        x = self.dropout(x)
        x = self.fc3(x)
        return x
transform = transforms.Compose([transforms.ToTensor(),transforms.Normalize((0.5,), (0.5,))])

train_dataset = datasets.MNIST(
    root='./data_mnist',  # Dossier différent pour éviter les conflits
    train=True,
    download=True,
    transform=transform)

test_dataset = datasets.MNIST(
    root='./data_mnist',
    train=False,
    download=True,
    transform=transform)

train_loader = DataLoader(
    dataset=train_dataset,
    batch_size=64,
    shuffle=True,
    num_workers=0)  

test_loader = DataLoader(
    dataset=test_dataset,
    batch_size=64,
    shuffle=False,
    num_workers=0)
model = SimpleMLP()
print(model)

criterion = nn.CrossEntropyLoss()  # Pour classification multi-classes
optimizer = optim.Adam(model.parameters(), lr=0.001)

num_epochs = 3
train_loss_history = []
train_acc_history = []

for epoch in range(num_epochs):
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0
    
    for batch_idx, (images, labels) in enumerate(train_loader):
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        
        loss.backward()
        optimizer.step()
        
        running_loss += loss.item()
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()
        
        if (batch_idx + 1) % 100 == 0:
            print(f'  Batch [{batch_idx+1}/{len(train_loader)}], Loss: {loss.item():.4f}')
    
    epoch_loss = running_loss / len(train_loader)
    epoch_acc = 100 * correct / total
    
    train_loss_history.append(epoch_loss)
    train_acc_history.append(epoch_acc)
    
data_iter = iter(test_loader)
images, labels = next(data_iter)

with torch.no_grad():
    outputs = model(images[:16])
    _, predictions = torch.max(outputs, 1)

fig, axes = plt.subplots(4, 4, figsize=(10, 10))
for i, ax in enumerate(axes.flat):
    ax.imshow(images[i].squeeze(), cmap='gray')
    ax.set_title(f'Vrai: {labels[i]}, Prédit: {predictions[i].item()}', color='green' if labels[i] == predictions[i] else 'red',fontsize=10)
    ax.axis('off')

plt.suptitle('Exemples de prédictions sur MNIST', fontsize=16)
plt.tight_layout()
plt.savefig('exemples_predictions.png', dpi=100)
plt.show()
print("Exemples de prédictions sauvegardés")
torch.save(model.state_dict(), 'modele_mnist.pth')
