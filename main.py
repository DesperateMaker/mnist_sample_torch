import torch
from torch.autograd import Variable
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms

import matplotlib.pyplot as plt

def load_data(batch_size):
    train_loader = torch.utils.data.DataLoader(
        datasets.MNIST('../data', train=True, download=True,
                       transform=transforms.Compose([
                           transforms.ToTensor(),
                           transforms.Normalize((0.1307,), (0.3081,))
                       ])),
        batch_size=batch_size, shuffle=True)
    test_loader = torch.utils.data.DataLoader(
        datasets.MNIST('../data', train=False, transform=transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize((0.1307,), (0.3081,))
        ])),
        batch_size=batch_size, shuffle=True)
    return train_loader, test_loader
#
# def create_nn(batch_size=200, learning_rate=0.01, epochs=10,
#               log_interval=10):

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(28 * 28, 200)
        self.fc2 = nn.Linear(200, 200)
        self.fc3 = nn.Linear(200, 10)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return F.log_softmax(x)

    def train(self):

        # create a stochastic gradient descent optimizer
        optimizer = optim.SGD(net.parameters(), lr=0.001, momentum=0.9)
        # create a loss function
        criterion = nn.NLLLoss()

        # run the main training loop
        for epoch in range(10):
            for batch_idx, (data, target) in enumerate(train_loader):
                data, target = Variable(data), Variable(target)

                # resize data from (batch_size, 1, 28, 28) to (batch_size, 28*28)
                data = data.view(-1, 28*28)
                optimizer.zero_grad()
                net_out = net(data)
                loss = criterion(net_out, target)
                loss.backward()
                optimizer.step()

                if batch_idx % 10 == 0:
                    print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
                        epoch, batch_idx * len(data), len(train_loader.dataset),
                               100. * batch_idx / len(train_loader), loss.item()))
        PATH = './mnist.pth'
        torch.save(net.state_dict(), PATH)

    def test(self):
        PATH = './mnist.pth'
        net.load_state_dict(torch.load(PATH))

        # run a test loop
        test_loss = 0
        correct = 0
        # create a loss function
        criterion = nn.NLLLoss()

        for data, target in test_loader:
            data, target = Variable(data, volatile=True), Variable(target)
            data = data.view(-1, 28 * 28)
            net_out = net(data)
            # sum up batch loss
            test_loss += criterion(net_out, target).item()
            pred = net_out.data.max(1)[1]  # get the index of the max log-probability
            correct += pred.eq(target.data).sum()

        test_loss /= len(test_loader.dataset)
        print('\nTest set: Average loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)\n'.format(
            test_loss, correct, len(test_loader.dataset),
            100. * correct / len(test_loader.dataset)))

    def demo(self):
        PATH = './mnist.pth'
        net.load_state_dict(torch.load(PATH))

        for data, target in test_loader:
            data, target = Variable(data, volatile=True), Variable(target)
            data = data.view(-1, 28 * 28)
            net_out = net(data)

            plt.imshow(data)



if __name__ == "__main__":
    run_opt = 2
    train_loader, test_loader = load_data(200)
    net = Net()
    print(net)

    if run_opt == 1:
        net.train()
    elif run_opt == 2:
        net.demo()
        # net.test()