# MatchedCover

A fully AI agent-based insurance system that automates the entire insurance lifecycle using autonomous intelligent agents.

## 🧠 Core Concept

MatchedCover is a multi-agent AI system that automates all key functions of an insurance company:
- Underwriting
- Customer onboarding  
- Risk assessment
- Policy management
- Claims adjudication
- Fraud detection
- Personalized recommendations
- Regulatory compliance

## 🤖 Agent Architecture

| Agent Name | Role |
|------------|------|
| Intake Agent | Gathers customer details via chat/voice/image/scan |
| Risk Assessor Agent | Analyzes risk using ML models on user data, geolocation, history |
| Pricing Agent | Calculates premium dynamically using market + risk + LLM insights |
| Policy Agent | Generates and manages smart contract-based policies |
| Claim Intake Agent | Accepts and parses claims via voice, chat, mobile photos, or video |
| Claims Evaluator | Assesses validity of claims using anomaly detection + images |
| Fraud Detection Agent | Flags suspicious activity and investigates anomalies |
| Compliance Agent | Ensures all actions meet regulatory rules (e.g., GDPR, HIPAA) |
| Advisor Agent | Answers customer questions using a fine-tuned LLM |
| Audit Agent | Logs every action for transparency, dispute resolution, and audits |

## ⚙️ Tech Stack

- **LLMs**: OpenAI GPT-4, Anthropic Claude, Meta LLaMA
- **Vision Models**: OpenAI Vision, Google Gemini Vision
- **ML/Fraud Detection**: scikit-learn, XGBoost, TensorFlow
- **Multi-agent System**: CrewAI framework
- **Communication**: FastAPI, Redis, Kafka
- **Database**: PostgreSQL, MongoDB, ChromaDB (vector storage)
- **Blockchain**: Smart contracts for policy management
- **Frontend**: React with TypeScript
- **Deployment**: Docker, Kubernetes

## 🚀 Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   npm install
   ```

2. **Set Environment Variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Run the Application**
   ```bash
   # Start backend services
   docker-compose up -d
   
   # Start the main application
   python src/main.py
   
   # Start frontend (in another terminal)
   cd frontend && npm start
   ```

## 📁 Project Structure

```
MatchedCover/
├── src/                    # Core application code
│   ├── agents/            # AI agent implementations
│   ├── models/            # Data models and schemas
│   ├── services/          # Business logic services
│   ├── api/              # REST API endpoints
│   └── utils/            # Utility functions
├── frontend/              # React frontend application
├── tests/                # Test suites
├── docs/                 # Documentation
├── docker/               # Docker configurations
└── deployment/           # Kubernetes and deployment configs
```

## 🔐 Security Features

- Zero-trust architecture with RBAC for agents
- End-to-end encryption for all user data
- Differential privacy implementation
- Immutable audit trails
- Compliance monitoring (GDPR, HIPAA, SOX)

## 📊 Monitoring & Analytics

- Real-time agent performance monitoring
- Fraud detection metrics
- Customer satisfaction tracking
- Regulatory compliance reporting
- Business intelligence dashboards

## 🧪 Testing

Multiple test scripts are available to verify the functionality of the agents:

1. **Basic Test**: `test_agents.py`
   - Verifies basic agent initialization and method access

2. **Advanced Test**: `advanced_test_agents.py`
   - Tests the agents with realistic customer data scenarios
   - Verifies quote calculation and fraud detection capabilities

3. **Comprehensive Test**: `comprehensive_agent_tests.py`
   - In-depth testing of all agent functionality
   - Tests all pricing strategies and market sensitivity
   - Validates fraud detection indicators and risk levels
   - Tests quantum signature generation and verification

To run the tests, simply use Python from the command line:

```bash
# Basic test
python test_agents.py

# Advanced test with realistic scenarios
python advanced_test_agents.py

# Comprehensive test suite
python comprehensive_agent_tests.py
```

For detailed testing results and analysis, see the `testing_report.md` file.

## 🔧 Pricing Strategies

The PricingAgent supports multiple pricing strategies:

- **Competitive**: Aims to be 7.5% below market average
- **Penetration**: Aggressive pricing (15% below market) with reduced margins
- **Premium**: Higher pricing (5% above market) with increased margins
- **Risk-Based**: Emphasizes risk factors over market positioning
- **Market-Following**: Closely follows market average prices

## 🤝 Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
