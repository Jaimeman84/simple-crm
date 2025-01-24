# 🚀 Simple CRM System

A powerful yet lightweight CRM (Customer Relationship Management) system built with Python, Streamlit, and SQLite. Perfect for small to medium businesses looking to manage their sales pipeline and prospect relationships effectively.

## 📁 Directory Structure
```
simple-crm/
├── app.py                 # 🎯 Main Streamlit application entry point
├── requirements.txt       # 📦 Project dependencies
├── setup.py              # ⚙️ Package installation configuration
├── crm.db               # 🗄️ SQLite database (auto-created)
└── src/
    ├── database/
    │   └── db_manager.py # 💾 Database operations & SQL queries
    └── models/
        └── prospect.py   # 👤 Prospect data model & validation
```

## ✨ Features

### 🎯 Core Features
- 👥 Complete prospect lifecycle management
- 📊 Real-time analytics dashboard
- 🔍 Advanced search and filtering capabilities
- 📱 Responsive and modern UI with Streamlit
- 🗄️ Persistent SQLite storage
- 🔒 Email duplicate prevention

### 📊 Dashboard Features
- 📈 Total prospects metrics
- 🎯 Active leads tracking
- 💰 Closed deals monitoring
- 📉 Visual pipeline breakdown
- 🔄 Real-time updates

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/simple-crm.git
cd simple-crm
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## 🎮 Usage

1. Launch the application:
```bash
streamlit run app.py
```

2. Open your browser: `http://localhost:8501`

3. Navigate using the sidebar menu:
   - 📊 **Dashboard**: Real-time metrics and pipeline visualization
   - ➕ **Add Prospect**: Create new prospect entries with validation
   - 👥 **View Prospects**: Manage existing prospects with advanced filtering

## 🔧 Technical Requirements

- 🐍 Python 3.8+
- 📊 streamlit==1.32.0
- 🐼 pandas==2.2.0
- 🗃️ sqlalchemy==2.0.27
- 🧪 pytest==8.0.0
- 🔐 python-dotenv==1.0.0
- 🛠️ setuptools

## 👨‍💻 Development

### 🧪 Testing
```bash
pytest
```

### 🗄️ Database Schema
SQLite database with prospects table:
- 👤 `full_name` (TEXT): Prospect's full name
- 📱 `phone_number` (TEXT): Contact number
- 📧 `email` (TEXT): Unique email address
- 📊 `status` (TEXT): Current pipeline stage
- 📝 `notes` (TEXT): Additional information
- ⏰ `created_at` (TIMESTAMP): Record creation time
- 🔄 `updated_at` (TIMESTAMP): Last update time

### 🔄 Pipeline Workflow
1. ❄️ Cold Lead
2. 📞 Contacted
3. ✅ Qualified
4. 📄 Proposal Sent
5. 💼 Negotiation
6. 🎯 Closed - Won
7. ❌ Closed - Lost
8. ⏰ Follow-up Needed

## 🔒 Security Features
- 🛡️ Input validation
- 🔐 Email duplication prevention
- ✅ Data integrity checks
- 🔄 Transaction support

## 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.