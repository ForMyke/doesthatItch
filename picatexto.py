import json
import torch
from datasets import Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    Trainer,
    TrainingArguments
)
from sklearn.metrics import accuracy_score, f1_score

MODEL_NAME = "dccuchile/bert-base-spanish-wwm-cased"

# Cargar dataset desde el JSON generado por el scraper
with open("dataset_pica.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"Ejemplos cargados: {len(data['text'])}")
print(f"  - Pica (1): {sum(data['label'])}")
print(f"  - No pica (0): {len(data['label']) - sum(data['label'])}")

# Crear dataset
dataset = Dataset.from_dict(data)
dataset = dataset.train_test_split(test_size=0.2, seed=42)

# Tokenizer
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

def tokenize(batch):
    return tokenizer(
        batch["text"],
        truncation=True,
        padding="max_length",
        max_length=128  # Aumentado para textos de Wikipedia
    )

dataset = dataset.map(tokenize, batched=True)
dataset = dataset.remove_columns(["text"])
dataset.set_format("torch")

# Modelo
model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_NAME,
    num_labels=2
)

# Métricas
def compute_metrics(pred):
    labels = pred.label_ids
    preds = pred.predictions.argmax(axis=1)
    return {
        "accuracy": accuracy_score(labels, preds),
        "f1": f1_score(labels, preds)
    }

# Argumentos
training_args = TrainingArguments(
    output_dir="./modelo_pica",
    evaluation_strategy="epoch",
    save_strategy="epoch",
    num_train_epochs=4,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    learning_rate=2e-5,
    weight_decay=0.01,
    load_best_model_at_end=True,
    metric_for_best_model="f1",
    logging_dir="./logs"
)

# Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset["train"],
    eval_dataset=dataset["test"],
    tokenizer=tokenizer,
    compute_metrics=compute_metrics
)

# Entrenar
trainer.train()

# Guardar modelo final
trainer.save_model("./modelo_pica_final")
tokenizer.save_pretrained("./modelo_pica_final")
print("\n✓ Modelo guardado en ./modelo_pica_final")