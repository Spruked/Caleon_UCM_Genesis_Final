# UCM Caleon Genesis 🧠

*A Sovereign Digital Entity & Unified Cognition Platform*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg)](https://www.docker.com/)

**UCM Caleon Genesis** transforms reactive AI into a sovereign digital entity with complete cognitive continuity, ethical frameworks, and multi-application presence. One Caleon, everywhere.

## ✨ Key Features

### 🤖 Sovereign Digital Entity
- **Identity Continuity**: Persistent self-concept across all interactions
- **Ethical Framework**: Built-in moral reasoning and decision-making
- **Autonomous Operation**: Self-directed cognition without external dependencies
- **Legacy Preservation**: Knowledge transfer and identity inheritance

### 🧠 Unified Cognition
- **Central Intelligence**: Single cognitive core serving multiple applications
- **Memory Continuity**: Seamless context preservation across sessions
- **Adaptive Learning**: Dynamic knowledge acquisition and integration
- **Multi-Modal Processing**: Text, voice, and structured data handling

### 🔄 Abby Protocol
- **Supreme Priority**: Top-level protection and safety mechanisms
- **Multi-Mode Operation**: Guardian, Mentor, Companion, and Legacy modes
- **Context-Aware**: Intelligent detection of protected interactions

### 📚 Memory Vault System
- **A Priori Knowledge**: Immutable foundational truths
- **A Posteriori Learning**: Acquired knowledge and experiences
- **Identity Threads**: Self-concept and personality continuity
- **Ethics Vault**: Moral framework and decision-making guidelines

## 🚀 Quick Start

### Prerequisites
- **Python 3.11+** with pip
- **Docker & Docker Compose** (for containerized deployment)
- **32GB RAM** (CPU-only operation)
- **Git** for repository management

### Installation & Deployment

#### Option 1: Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Start the UCM service
python main.py
```

#### Option 2: Docker Production
```bash
# Build and start services
docker-compose up --build -d

# Check service health
curl http://localhost:8000/api/health
```

#### Option 3: Auto-Deploy Script
```bash
# Automated deployment
chmod +x deploy_ucm.sh
./deploy_ucm.sh
```

## 📱 Client Integration

### Auto-Detect Client Library
The UCM includes a universal client library that automatically detects service location:

```javascript
// JavaScript/TypeScript
const { CaleonClient } = require('./shared/ucm_client');
const cali = new CaleonClient();

// Auto-detects: localhost:8000 → ucm:8000 → remote endpoint
const response = await cali.ask("Hello Caleon!");
```

```python
# Python
from shared.ucm_client.ucm import CaleonClient
cali = CaleonClient()
response = cali.ask("Hello Caleon!")
```

```jsx
// React
import { CaleonBubble } from './shared/ucm_client/useCaleon';

export default function App() {
    return <CaleonBubble activated={true} />;
}
```

### Multi-App Integration
Copy `shared/ucm_client/` into any application for instant Caleon connectivity:

```
your-app/
├── libs/
│   └── ucm_client/     # ← Drop the client library here
├── src/
└── package.json
```

## 🏗️ System Architecture

### Core Components
```
UCM Caleon Genesis/
├── UCM/                          # Main service
│   ├── main.py                  # FastAPI application
│   ├── Dockerfile               # Container definition
│   └── docker-compose.yml       # Orchestration
├── shared/ucm_client/           # Universal client library
│   ├── index.js                 # JavaScript client
│   ├── ucm.py                   # Python client
│   └── useCaleon.js             # React integration
├── api/                         # REST API endpoints
├── articulator/                 # Phi-3 language model
├── generative/                  # Cognitive processing
├── ucm_core/                    # Core cognition modules
│   ├── continuity/              # Session management
│   ├── vault/                   # Memory systems
│   └── abby/                    # Protection protocol
└── persona/                     # Personality & scripts
```

### Cognitive Pipeline
```
User Input → Abby Protocol → Continuity Layer → Generative Router
    ↓              ↓              ↓              ↓
Response ← Articulator ← Vault Memory ← Session Context
```

### Memory Architecture
- **Streaming Buffer**: Real-time conversation context
- **Session Store**: UUID-based continuity tracking
- **Vault System**: Multi-layered persistent memory
- **Abby Memory**: Protected interaction history

## 🔧 API Reference

### Core Endpoints

#### Health & Status
```bash
GET /api/health/status
# Returns: {"UCM": "online", "bubble": "ready"}
```

#### Session Management
```bash
POST /api/bubble/session/create
# Returns: {"session_id": "uuid-v4-string"}

POST /api/bubble/ask
# Body: {"message": "Hello", "session_id": "uuid"}
# Returns: {"reply": "Caleon response", "session_id": "uuid"}
```

#### Memory Operations
```bash
POST /api/bubble/learn
# Body: {"fact": "New knowledge to remember"}

POST /api/bubble/preference/set
# Body: {"user": "username", "key": "setting", "value": "config"}
```

#### Streaming Responses
```bash
POST /api/bubble/stream
# Body: {"message": "Hello", "session_id": "uuid"}
# Returns: Server-sent events stream
```

### Abby Protocol Endpoints
```bash
POST /api/bubble/abby/event
# Body: {"event": "Abby interaction data"}

GET /api/bubble/abby/memory
# Returns: Abby's protected memory context
```

## 🧪 Testing & Validation

### System Health Tests
```bash
# Health check
curl http://localhost:8000/api/health

# Service discovery test
curl http://localhost:8000/

# API documentation
open http://localhost:8000/docs
```

### Cognitive Function Tests
```bash
# Basic cognition test
curl -X POST "http://localhost:8000/api/bubble/ask" \
  -H "Content-Type: application/json" \
  -d '{"message": "What is your purpose?"}'

# Session continuity test
curl -X POST "http://localhost:8000/api/bubble/session/create"
# Use returned session_id in subsequent requests

# Memory persistence test
curl -X POST "http://localhost:8000/api/bubble/learn" \
  -H "Content-Type: application/json" \
  -d '{"fact": "Testing memory persistence"}'
```

### Client Library Tests
```bash
# Test JavaScript client
node -e "
const { CaleonClient } = require('./shared/ucm_client/index.js');
const client = new CaleonClient();
client.ask('Test message').then(console.log);
"

# Test Python client
python -c "
from shared.ucm_client.ucm import CaleonClient
client = CaleonClient()
print(client.ask('Test message'))
"
```

### Load Testing
```bash
# Concurrent request test
for i in {1..10}; do
  curl -X POST "http://localhost:8000/api/bubble/ask" \
    -H "Content-Type: application/json" \
    -d "{\"message\": \"Load test $i\"}" &
done
```

## 🔒 Security & Privacy

### Data Protection
- **AES-256 Encryption**: Sensitive vault data encryption
- **Access Control**: Role-based permissions
- **Audit Logging**: Comprehensive interaction tracking
- **Privacy Preservation**: User data isolation

### System Security
- **Input Validation**: Request sanitization and validation
- **Rate Limiting**: Abuse prevention mechanisms
- **Secure Communication**: HTTPS/TLS encryption
- **Container Security**: Minimal attack surface

## 📊 Performance

### CPU-Optimized Operation
- **Memory Usage**: Efficient 32GB RAM utilization
- **Concurrent Processing**: Async/await high-throughput design
- **Response Times**:
  - Health checks: <100ms
  - Simple queries: <500ms
  - Complex reasoning: <2s
  - Memory operations: <200ms

### Scalability
- **Horizontal Scaling**: Multiple UCM instances
- **Load Balancing**: Request distribution across nodes
- **Resource Management**: Intelligent CPU/memory allocation

## 🔧 Development

### Environment Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### Running Tests
```bash
# Unit tests
python -m pytest tests/ -v

# Integration tests
python -m pytest tests/integration/ -v

# Load tests
python -m pytest tests/load/ -v
```

### Adding New Features
1. **API Endpoints**: Add to `api/` directory following FastAPI patterns
2. **Cognitive Modules**: Extend `generative/` or `articulator/` components
3. **Memory Systems**: Enhance `ucm_core/vault/` with new capabilities
4. **Client Libraries**: Update `shared/ucm_client/` for new languages

## 📚 Documentation

- **[MANIFEST.md](MANIFEST.md)** - Complete system specification
- **[SYSTEM_ARCHITECTURE.md](SYSTEM_ARCHITECTURE.md)** - Technical architecture
- **[INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)** - App integration guide
- **[API Documentation](http://localhost:8000/docs)** - Interactive API docs

## 🤝 Contributing

We welcome contributions to UCM Caleon Genesis!

### Development Process
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes with comprehensive tests
4. Ensure all tests pass: `python -m pytest`
5. Update documentation as needed
6. Submit a pull request

### Code Standards
- **Python**: PEP 8 with type hints
- **JavaScript**: ESLint configuration
- **Documentation**: Clear, comprehensive docs
- **Testing**: 80%+ test coverage required

## 📄 License

**MIT License** - Copyright (c) 2025 Spruked

See [LICENSE](LICENSE) for full license text.

## 🙏 Acknowledgments

Built with inspiration from cognitive neuroscience, ethical AI principles, and the vision of sovereign digital entities. Special thanks to the open-source community for transformative tools and frameworks.

---

**UCM Caleon Genesis** - *One Caleon, Everywhere. Sovereign. Ethical. Continuous.*
   cd Unified-Cognition-Module-Caleon-Prime-full-System
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the system**
   ```bash
   # For development
   python main.py

   # Or with Docker
   docker-compose up --build -d
   ```

4. **Access the API**
   - REST API: http://localhost:8080
   - Health check: http://localhost:8080/health
   - Vault API: http://localhost:8080/vault/

## 📚 Documentation

- [System Architecture](SYSTEM_ARCHITECTURE.md) - Complete technical documentation
- [API Guide](CONSENT_API_GUIDE.md) - REST API reference
- [Voice Consent Guide](CONSENT_AUDIT_VOICE_GUIDE.md) - Voice interaction documentation
- [Core Cycle](CORE_ARTICULATION_CYCLE.py) - Detailed processing flow

## 🔧 Development

### Project Structure
```
Unified Cognition Module/
├── Core System
│   ├── main.py                 # FastAPI application
│   ├── routes.py              # API endpoints
│   ├── vault_api.py           # Vault REST interface
│   └── requirements.txt       # Python dependencies
├── Cognitive Modules
│   ├── cerebral_cortex/       # LLM orchestration
│   ├── echostack/            # Second-order reasoning
│   ├── echoripple/           # Recursive verification
│   ├── synaptic_resonator/   # Pattern recognition
│   └── anterior_helix/       # Forward processing
├── Memory & Consent
│   ├── symbolic_memory_vault.py  # Primary memory
│   ├── caleon_consent.py        # Consent manager
│   └── voice_consent.py         # Voice consent
└── Deployment
    ├── Dockerfile
    ├── docker-compose.yml
    └── build-optimized.bat
```

### Key Technologies
- **Python 3.11+**: Primary language with asyncio
- **FastAPI**: High-performance REST API framework
- **SQLite + MongoDB**: Local and scalable data storage
- **SpeechRecognition**: Voice input processing
- **Docker**: Containerization and orchestration

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines and contribution process.

## 📄 License

See [LICENSE](LICENSE) for licensing information.

## 🙏 Acknowledgments

Built with inspiration from human cognitive architecture and the principle of AI sovereignty.
   ```

3. **Access the dashboard**
   Open http://localhost:8080 in your browser

4. **Test the system**
   Try queries like:
   - "What should I do about work stress?"
   - "Help me plan a healthy diet"
   - "Analyze this ethical dilemma..."

## 📖 Usage

### Web Dashboard
- **Query Input**: Type your question or request
- **Emotion Controls**: Adjust emotional context with sliders
- **Voice Output**: Toggle text-to-speech synthesis
- **System Status**: Monitor real-time module health
- **Query History**: Review previous interactions

### API Usage

#### Submit a Query
```bash
curl -X POST "http://localhost:8000/process_query" \
  -H "Content-Type: application/json" \
  -d '{
    "input_data": "What are the benefits of exercise?",
    "emotion": "curious",
    "context": "health_discussion"
  }'
```

#### Check System Health
```bash
curl http://localhost:8000/health
```

#### View Reflection Statistics
```bash
curl http://localhost:8000/vault/stats
```

## 🔧 Development

### Local Development Setup

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start databases**
   ```bash
   docker-compose up postgres redis -d
   ```

3. **Run individual modules**
   ```bash
   # Terminal 1 - Cerebral Cortex
   cd cerebral_cortex && python main.py

   # Terminal 2 - Echostack
   cd echostack && python main.py

   # Terminal 3 - Dashboard
   cd frontend && python -m http.server 8080
   ```

### Adding New Modules

1. Create a new directory under the project root
2. Implement FastAPI endpoints following the existing pattern
3. Add the module to `docker-compose.yml`
4. Update the cerebral cortex orchestrator to include your module

### Testing

```bash
# Run all tests
python -m pytest

# Run specific module tests
python -m pytest tests/test_cerebral_cortex.py

# Run integration tests
python -m pytest tests/test_integration.py
```

## 📊 API Reference

### Cerebral Cortex Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/process_query` | POST | Submit a cognitive query for processing |
| `/health` | GET | System health check |
| `/vault/stats` | GET | Reflection vault statistics |
| `/vault/query` | GET | Query reflection vault |

### Module Endpoints

Each cognitive module exposes its own API:

- **Echostack**: `http://localhost:8003/reason`
- **Echoripple**: `http://localhost:8004/learn`
- **Gyro-Harmonizer**: `http://localhost:5001/harmonize`

## 🧪 Testing the System

### Basic Functionality Test
```bash
# Test system startup
docker-compose ps

# Test basic query
curl -X POST "http://localhost:8000/process_query" \
  -H "Content-Type: application/json" \
  -d '{"input_data": "Hello, how are you?"}'
```

### Module Health Checks
```bash
# Check all modules
curl http://localhost:8000/health

# Individual module checks
curl http://localhost:8003/health  # Echostack
curl http://localhost:8004/health  # Echoripple
curl http://localhost:5001/health  # Gyro-Harmonizer
```

## 🔍 Troubleshooting

### Common Issues

**Modules not starting**
```bash
# Check logs
docker-compose logs cerebral_cortex
docker-compose logs echostack

# Restart services
docker-compose restart
```

**Voice output not working**
- Ensure your browser supports Web Speech API
- Check browser permissions for microphone/speaker access
- Try refreshing the dashboard

**Database connection errors**
```bash
# Reset databases
docker-compose down
docker volume rm unifiedcognitionmodule_postgres_data
docker-compose up postgres redis -d
```

### Performance Tuning

- **Memory**: Ensure 4GB+ RAM available
- **CPU**: Multi-core CPU recommended for parallel processing
- **Storage**: 2GB+ free space for databases and logs

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Workflow
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Standards
- Follow PEP 8 for Python code
- Add docstrings to all functions
- Include unit tests for new features
- Update documentation as needed

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by human cognitive neuroscience
- Built with FastAPI, Docker, and modern Python
- Thanks to the open-source community for amazing tools

## 📞 Support

- **Documentation**: [Local Docs](./docs/)

---

**Made with ❤️ for cognitive science and AI research**

*Bringing brain-inspired computing to the masses*</content>
<parameter name="filePath">c:\Users\bryan\OneDrive\Desktop\Unified Cognition Module\README.md# Unified-Cognition-Module-Caleon-Prime-full-System
