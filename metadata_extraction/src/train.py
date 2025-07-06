from transformers import Trainer, TrainingArguments, AutoTokenizer, AutoModelForQuestionAnswering
from datasets import Dataset
import json
import os

# Prepares training data in SQuAD format
def prepare_squad_format(data, questions):
    squad = []
    for context, labels in data:
        for field, answer in labels.items():
            if not answer or not answer.strip():
                continue
            question = questions[field]
            start = context.find(answer)
            if start == -1:
                continue  # skip if answer not found in context
            squad.append({
                "context": context,
                "question": question,
                "answers": {"text": [answer], "answer_start": [start]},
                "id": str(len(squad))
            })
    return squad

# Trains the QA model using HuggingFace Trainer
def train_model(data, model_name="distilbert-base-uncased", output_dir="./model"):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForQuestionAnswering.from_pretrained(model_name)

    squad_data = prepare_squad_format(data, {
        "Agreement Value": "What is the agreement value?",
        "Agreement Start Date": "What is the agreement start date?",
        "Agreement End Date": "What is the agreement end date?",
        "Renewal Notice": "What is the renewal notice period?",
        "Party One": "Who is the first party?",
        "Party Two": "Who is the second party?"
    })

    dataset = Dataset.from_list(squad_data)

    def preprocess(example):
        return tokenizer(
            example["question"],
            example["context"],
            truncation=True,
            padding="max_length",
            max_length=512
        )

    tokenized_dataset = dataset.map(preprocess, batched=True)

    training_args = TrainingArguments(
        output_dir=output_dir,
        evaluation_strategy="no",
        learning_rate=2e-5,
        per_device_train_batch_size=4,
        num_train_epochs=2,
        weight_decay=0.01,
        logging_dir=f"{output_dir}/logs"
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset
    )

    trainer.train()
    model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)
