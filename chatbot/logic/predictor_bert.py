import torch
from torch import nn
from transformers import DistilBertModel, DistilBertTokenizer
import joblib
import os

# Load model + encoder
MODEL_PATH = os.path.join(os.path.dirname(__file__), "bert_mlp_model.pt")
ENCODER_PATH = os.path.join(os.path.dirname(__file__), "label_encoder.pkl")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Define model architecture
class BertMLP(nn.Module):
    def __init__(self, hidden_size=768, num_classes=10):
        super().__init__()
        self.bert = DistilBertModel.from_pretrained("distilbert-base-uncased")
        for p in self.bert.parameters():
            p.requires_grad = False
        self.classifier = nn.Sequential(
            nn.Linear(hidden_size, 256),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(256, num_classes)
        )

    def forward(self, input_ids, attention_mask):
        outputs = self.bert(input_ids=input_ids, attention_mask=attention_mask)
        cls_embed = outputs.last_hidden_state[:, 0, :]
        return self.classifier(cls_embed)

# Load tokenizer, encoder, model
tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")
label_encoder = joblib.load(ENCODER_PATH)

model = BertMLP(num_classes=len(label_encoder.classes_))
model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
model.to(device)
model.eval()

# Dự đoán
def predict_disease_from_text(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.softmax(outputs, dim=1).cpu().numpy()[0]

    print("🔍 INPUT:", text)
    print("🔢 PROBS:", dict(zip(label_encoder.classes_, probs)))  # DEBUG

    topk = sorted(
        zip(label_encoder.classes_, probs),
        key=lambda x: x[1],
        reverse=True
    )[:5]

    return [{"disease": d, "confidence": round(p * 100, 2)} for d, p in topk if p > 0.01]
