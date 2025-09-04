import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import pandas as pd
import torch
import numpy as np
import torch.nn as nn
import database
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from transformers import AutoTokenizer, AutoModel, Trainer, TrainingArguments
from demande import Demande, load_data, reorder_data


class Model:
    def __init__(self):
        df = pd.DataFrame(load_data())
        if len(df)==0:
            self.df_train = []
            self.df_test = []
            self.df_pred = []
            print("database is empty")
            return None
        df["date_demande"] = pd.to_datetime(df["date_demande"], format='%Y-%m-%d %H:%M:%S')

        acceptance_rate_user = {"code": [], "acceptance_rate_user": []}
        acceptance_rate_direction = {"code": [], "acceptance_rate_direction": []}
        time_gaps = {"code": [], "time_gaps": []}
        number_of_past_demandes = {"code": [], "number_of_past_demandes": []}

        for i in range(len(df)):
            code = df.loc[i, "code"]
            ppr = df.loc[i, "ppr"]
            date_demande = df.loc[i, "date_demande"]
            direction = df.loc[i, "direction"]
            number_of_past_demandes["code"].append(code)
            time_gaps["code"].append(code)
            acceptance_rate_direction["code"].append(code)
            acceptance_rate_user["code"].append(code)

            past_data = reorder_data(Demande.get_past_demandes(ppr, date_demande))
            if len(past_data) == 0:
                gaps = [999999 for _ in range(10)]
                time_gaps["time_gaps"].append(gaps)
                acceptance_rate_direction["acceptance_rate_direction"].append(1)
                acceptance_rate_user["acceptance_rate_user"].append(1)
                number_of_past_demandes["number_of_past_demandes"].append(0)
                continue

            past_df = pd.DataFrame(past_data)
            past_df["date_demande"] = pd.to_datetime(past_df["date_demande"])

            nbr = len(past_df)
            number_of_past_demandes["number_of_past_demandes"].append(nbr)

            gaps = []
            for j in range(10):
                if j < nbr:
                    delta = (date_demande - past_df.loc[j, "date_demande"]).total_seconds() / 86400.0
                    gaps.append(delta)
                else:
                    gaps.append(999999)
            time_gaps["time_gaps"].append(gaps)

            accepted_user = len(past_df[(past_df["ppr"] == ppr) & (past_df["etat"] == 3)])
            total_user = len(past_df[(past_df["ppr"] == ppr) & (past_df["etat"] >= 3)])
            acceptance_rate_user["acceptance_rate_user"].append(
                accepted_user / total_user if total_user > 0 else 1
            )

            accepted_dir = len(past_df[(past_df["direction"] == direction) & (past_df["etat"] == 3)])
            total_dir = len(past_df[(past_df["direction"] == direction) & (past_df["etat"] >= 3)])
            acceptance_rate_direction["acceptance_rate_direction"].append(
                accepted_dir / total_dir if total_dir > 0 else 1
            )
        df_acc_user = pd.DataFrame(acceptance_rate_user)
        df_acc_dir = pd.DataFrame(acceptance_rate_direction)
        df_time_gaps = pd.DataFrame(time_gaps)
        df_num_past = pd.DataFrame(number_of_past_demandes)

        df = df.merge(df_acc_user, on="code", how="left")
        df = df.merge(df_acc_dir, on="code", how="left")
        df = df.merge(df_time_gaps, on="code", how="left")
        df = df.merge(df_num_past, on="code", how="left")
        df["hour_of_submission"] = df["date_demande"].dt.hour
        a = []
        for i in range(10):
            for j in range(len(df)):
                a.append(df["time_gaps"].get(i+1))
            df["time_gap"+str(i+1)] = a
            a = []
        df["target"] = df["etat"].apply(lambda x: 0 if x == 3 else 1)

        cat_features = ["bureau", "direction"]
        num_features = ["number_of_past_demandes", "acceptance_rate_user", "acceptance_rate_direction", "hour_of_submission"]
        num_features.extend(["time_gap"+str(i+1) for i in range(10)])
        df[num_features] = df[num_features].apply(pd.to_numeric, errors="coerce").fillna(-1)

        ohe = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
        scaler = StandardScaler()

        index_train_test = [i for i in range(len(df.where(df["etat"]>=3)))]
        np.random.shuffle(index_train_test)
        index_train = [index_train_test[i] for i in range(round(0.75*len(index_train_test)))]
        index_test = [index_train_test[i] for i in range(round(0.75*len(index_train_test)), len(index_train_test))]
        self.df_train = df.iloc[index_train]
        self.df_test = df.iloc[index_test]
        self.df_pred = df.copy()

        cat_encoded = ohe.fit_transform(self.df_train[cat_features])
        num_scaled = scaler.fit_transform(self.df_train[num_features])
        cat_encoded_test = ohe.transform(self.df_test[cat_features])
        num_scaled_test = scaler.transform(self.df_test[num_features])
        cat_encoded_pred = ohe.transform(self.df_pred[cat_features])
        num_scaled_pred = scaler.transform(self.df_pred[num_features])

        self.tabular_features = np.hstack([cat_encoded, num_scaled])
        self.tabular_features_test = np.hstack([cat_encoded_test, num_scaled_test])
        self.tabular_features_pred = np.hstack([cat_encoded_pred, num_scaled_pred])

        tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
        self.df_train["text"] = self.df_train["objet"].astype(str) + ":\n " + self.df_train["description"].astype(str)
        self.train_encodings = tokenizer(
            self.df_train["text"].tolist(),
            truncation=True,
            padding=True,
            max_length=128,
            return_tensors="pt"
        )
        self.df_test["text"] = self.df_test["objet"].astype(str) + ":\n " + self.df_test["description"].astype(str)
        self.test_encodings = tokenizer(
            self.df_test["text"].tolist(),
            truncation=True,
            padding=True,
            max_length=128,
            return_tensors="pt"
        )
        self.df_pred["text"] = self.df_pred["objet"].astype(str) + ":\n " + self.df_pred["description"].astype(str)
        self.pred_encodings = tokenizer(
            self.df_pred["text"].tolist(),
            truncation=True,
            padding=True,
            max_length=128,
            return_tensors="pt"
        )

class HybridModel(nn.Module):
    def __init__(self, transformer_name, tabular_input_dim, num_labels):
        super().__init__()
        self.transformer = AutoModel.from_pretrained(transformer_name)
        transformer_hidden_size = self.transformer.config.hidden_size
        
        self.tabular_fc = nn.Linear(tabular_input_dim, 128)
        self.classifier = nn.Linear(transformer_hidden_size + 128, num_labels)

    def forward(self, input_ids, attention_mask, tabular_data, labels=None):
        text_outputs = self.transformer(input_ids=input_ids, attention_mask=attention_mask)
        text_cls = text_outputs.last_hidden_state[:, 0, :]
        
        tabular_emb = torch.relu(self.tabular_fc(tabular_data))
        combined = torch.cat([text_cls, tabular_emb], dim=1)
        
        logits = self.classifier(combined)
        
        loss = None
        if labels is not None:
            loss = nn.CrossEntropyLoss()(logits, labels)
        
        return {"loss": loss, "logits": logits}
    

class CustomDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, tabular_features, labels):
        self.encodings = encodings
        self.tabular_features = torch.tensor(tabular_features, dtype=torch.float)
        self.labels = torch.tensor(labels, dtype=torch.long)

    def __getitem__(self, idx):
        item = {key: val[idx] for key, val in self.encodings.items()}
        item["tabular_data"] = self.tabular_features[idx]
        item["labels"] = self.labels[idx]
        return item

    def __len__(self):
        return len(self.labels)


class Model_Prediction:
    def __init__(self):        
        model = Model()
        self.df_pred = model.df_pred
        if len(self.df_pred)==0:
            return None

        train_dataset = CustomDataset(model.train_encodings, model.tabular_features, model.df_train["target"].values)
        test_dataset = CustomDataset(model.test_encodings, model.tabular_features_test, model.df_test["target"].values)
        pred_dataset = CustomDataset(model.pred_encodings, model.tabular_features_pred, [0]*len(model.df_pred))


        training_args = TrainingArguments(
            output_dir="./results",
            evaluation_strategy="epoch",
            per_device_train_batch_size=8,
            num_train_epochs=3,
            logging_dir="./logs",
            logging_steps=50,
        )

        model = HybridModel("bert-base-uncased", tabular_input_dim=model.tabular_features.shape[1], num_labels=2)

        self.trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=test_dataset,
        )

    def train(self):
        if len(self.df_pred)==0:
            return None
        self.trainer.train()

    def predict(self):
        if len(self.df_pred)==0:
            return None
        model = Model()
        self.df_pred = model.df_pred

        train_dataset = CustomDataset(model.train_encodings, model.tabular_features, model.df_train["target"].values)
        test_dataset = CustomDataset(model.test_encodings, model.tabular_features_test, model.df_test["target"].values)
        pred_dataset = CustomDataset(model.pred_encodings, model.tabular_features_pred, [0]*len(model.df_pred))


        training_args = TrainingArguments(
            output_dir="./results",
            evaluation_strategy="epoch",
            per_device_train_batch_size=8,
            num_train_epochs=3,
            logging_dir="./logs",
            logging_steps=50,
        )

        model = HybridModel("bert-base-uncased", tabular_input_dim=model.tabular_features.shape[1], num_labels=2)

        self.trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=test_dataset,
        )
        
        preds = self.trainer.predict(pred_dataset)
        logits = preds.predictions
        probs = torch.softmax(torch.tensor(logits), dim=1)[:, 1]
        pred_labels = torch.argmax(torch.tensor(logits), dim=1)
        self.df_pred["pred_proba"] = probs.numpy()
        self.df_pred["pred_label"] = pred_labels.numpy()

        
