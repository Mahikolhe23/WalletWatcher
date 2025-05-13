import os
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
import joblib

class EmailAutoCategorizer:
    _instance = None

    # Paths
    MODEL_CATEGORY_PATH = "./config/email_category_model.pkl"
    MODEL_MODE_PATH = "./config/email_mode_model.pkl"
    VECTORIZER_PATH = "./config/vectorizer.pkl"
    LABEL_ENCODER_CATEGORY_PATH = "./config/label_encoder_category.pkl"
    LABEL_ENCODER_MODE_PATH = "./config/label_encoder_mode.pkl"
    DATA_PATH = "./data/labeled_emails.csv"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EmailAutoCategorizer, cls).__new__(cls)
            cls._instance._load_or_train()
        return cls._instance

    def _load_or_train(self):
        if all(os.path.exists(p) for p in [
            self.MODEL_CATEGORY_PATH,
            self.MODEL_MODE_PATH,
            self.VECTORIZER_PATH,
            self.LABEL_ENCODER_CATEGORY_PATH,
            self.LABEL_ENCODER_MODE_PATH
        ]):
            self.category_model = joblib.load(self.MODEL_CATEGORY_PATH)
            self.mode_model = joblib.load(self.MODEL_MODE_PATH)
            self.vectorizer = joblib.load(self.VECTORIZER_PATH)
            self.category_encoder = joblib.load(self.LABEL_ENCODER_CATEGORY_PATH)
            self.mode_encoder = joblib.load(self.LABEL_ENCODER_MODE_PATH)
        else:
            self._train()

    def _train(self):
        if not os.path.exists(self.DATA_PATH):
            raise FileNotFoundError(f"{self.DATA_PATH} not found.")

        df = pd.read_csv(self.DATA_PATH)
        df.dropna(subset=["email_text", "category", "mode"], inplace=True)

        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words="english")
        X = self.vectorizer.fit_transform(df["email_text"])

        # Encode category
        self.category_encoder = LabelEncoder()
        y_category = self.category_encoder.fit_transform(df["category"])
        self.category_model = LogisticRegression()
        self.category_model.fit(X, y_category)

        # Encode mode
        self.mode_encoder = LabelEncoder()
        y_mode = self.mode_encoder.fit_transform(df["mode"])
        self.mode_model = LogisticRegression()
        self.mode_model.fit(X, y_mode)

        # Save models and encoders
        joblib.dump(self.category_model, self.MODEL_CATEGORY_PATH)
        joblib.dump(self.mode_model, self.MODEL_MODE_PATH)
        joblib.dump(self.vectorizer, self.VECTORIZER_PATH)
        joblib.dump(self.category_encoder, self.LABEL_ENCODER_CATEGORY_PATH)
        joblib.dump(self.mode_encoder, self.LABEL_ENCODER_MODE_PATH)

    def predict(self, email_text):
        X = self.vectorizer.transform([email_text])
        category_pred = self.category_model.predict(X)
        mode_pred = self.mode_model.predict(X)

        return {
            "category": self.category_encoder.inverse_transform(category_pred)[0],
            "mode": self.mode_encoder.inverse_transform(mode_pred)[0]
        }

    def append_unlabeled(self, email_text, category="unknown", mode="unknown"):
        df = pd.DataFrame([{
            "email_text": email_text,
            "category": category,
            "mode": mode
        }])
        df.to_csv(self.DATA_PATH, mode='a', header=not os.path.exists(self.DATA_PATH), index=False)
