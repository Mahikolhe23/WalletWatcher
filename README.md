# WalletWatcher
WalletWatcher is a personal finance data extractor and summarizer that automatically fetches transaction-related emails, parses financial details, and sends a daily summary of your expenses. This is a prototype for building a full SaaS solution capable of handling data from emails, SMS, WhatsApp, and other sources.

---

## 🔍 Features

- ✅ Fetch transaction data from Gmail inbox
- ✅ Parse credit/debit amounts from alert emails
- ✅ Store in a structured DataFrame
- ✅ Email daily expense summaries to user
- 📈 Future: Integrate with SQL Server and create dashboards
- 💬 Future: Fetch from SMS, WhatsApp, PDFs

---

## 📂 Project Structure

```
walletwatcher/
├── src/                # All scripts for fetch, parse, push, summarize
├── data/               # Raw and processed data
├── config/             # Store credentials securely (not committed)
├── main.py             # Main orchestration script
├── requirements.txt
├── README.md
└── .gitignore
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/walletwatcher.git
cd walletwatcher
```

### 2. Create a Virtual Environment (Optional but Recommended)

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Email Access

For testing:
- Use app-specific password or allow less secure apps for Gmail (temporary).
- Store your credentials in `config/credentials.json` or use `.env`.

### 5. Run the App

```bash
python main.py
```

---

## 🛡️ Security Note

Never hardcode or push email passwords to Git. Use environment variables, `.env`, or a secure vault manager like `keyring`.

---

## 🛠️ Roadmap

- [x] Email transaction parser
- [ ] Load to SQL Server raw → bronze → silver → gold layers
- [ ] Dashboard in Power BI or Streamlit
- [ ] Add SMS and WhatsApp data support
- [ ] SaaS version with user accounts

---

## 🙌 Contribution

This is a personal learning project. You’re welcome to fork and extend it for your own finance tracking or portfolio use.

---

## 📜 License

MIT License – feel free to modify and reuse with attribution.
