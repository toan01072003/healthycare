import pandas as pd
import torch
from torch import nn
from torch.utils.data import Dataset, DataLoader
from transformers import DistilBertTokenizer, DistilBertModel
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from tqdm import tqdm

# ==== Load và xử lý dữ liệu ====
df = pd.read_csv("C:/Users/Toan/Documents/LapTrinh/python/smartphc/chatbot/logic/bert_dataset.csv")
texts = df["text"].tolist()
labels = df["label"].tolist()

label_encoder = LabelEncoder()
encoded_labels = label_encoder.fit_transform(labels)
num_classes = len(label_encoder.classes_)

# Train/test split
train_texts, test_texts, train_labels, test_labels = train_test_split(
    texts, encoded_labels, test_size=0.2, random_state=42
)

# ==== Tokenizer ====
tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")

class SymptomDataset(Dataset):
    def __init__(self, texts, labels):
        self.encodings = tokenizer(texts, truncation=True, padding=True, return_tensors='pt')
        self.labels = torch.tensor(labels)

    def __getitem__(self, idx):
        item = {key: val[idx] for key, val in self.encodings.items()}
        item["labels"] = self.labels[idx]
        return item

    def __len__(self):
        return len(self.labels)

train_dataset = SymptomDataset(train_texts, train_labels)
test_dataset = SymptomDataset(test_texts, test_labels)

train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=16)

# ==== Model: DistilBERT + MLP ====
class BertMLP(nn.Module):
    def __init__(self, hidden_size=768, num_classes=10):
        super().__init__()
        self.bert = DistilBertModel.from_pretrained("distilbert-base-uncased")
        self.classifier = nn.Sequential(
            nn.Linear(hidden_size, 256),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(256, num_classes)
        )

    def forward(self, input_ids, attention_mask):
        outputs = self.bert(input_ids=input_ids, attention_mask=attention_mask)
        cls_embed = outputs.last_hidden_state[:, 0, :]  # [CLS]
        return self.classifier(cls_embed)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = BertMLP(num_classes=num_classes).to(device)

# ==== Training setup ====
optimizer = torch.optim.AdamW(model.parameters(), lr=2e-5)
criterion = nn.CrossEntropyLoss()

# ==== Train loop ====
epochs = 3
model.train()
for epoch in range(epochs):
    loop = tqdm(train_loader, desc=f"Epoch {epoch+1}")
    total_loss = 0
    for batch in loop:
        input_ids = batch["input_ids"].to(device)
        attention_mask = batch["attention_mask"].to(device)
        labels = batch["labels"].to(device)

        optimizer.zero_grad()
        outputs = model(input_ids, attention_mask)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        loop.set_postfix(loss=loss.item())
        total_loss += loss.item()

# ==== Evaluation ====
model.eval()
correct = 0
total = 0
with torch.no_grad():
    for batch in test_loader:
        input_ids = batch["input_ids"].to(device)
        attention_mask = batch["attention_mask"].to(device)
        labels = batch["labels"].to(device)

        outputs = model(input_ids, attention_mask)
        preds = torch.argmax(outputs, dim=1)

        correct += (preds == labels).sum().item()
        total += labels.size(0)

print(f"✅ Accuracy: {correct / total:.2%}")

# ==== Lưu mô hình và encoder ====
torch.save(model.state_dict(), "bert_mlp_model.pt")
import joblib
joblib.dump(label_encoder, "label_encoder.pkl")

print("✅ Saved model and label encoder.")
