# UCM Cali X One - Advanced Artificial General Intelligence System 🧠

**Copyright © 2025 Bryan Stone. All Rights Reserved.**  
**PATENT PENDING - Intent to File Patent Application**

*Revolutionary Super-Knowledge Graph AGI with Autonomous Reasoning*

[![License: Proprietary](https://img.shields.io/badge/License-Proprietary-red.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![AGI Status](https://img.shields.io/badge/AGI-Operational-green.svg)](SYSTEM_ARCHITECTURE.md)

**UCM Cali X One** represents a breakthrough in Artificial General Intelligence through its innovative Super-Knowledge Graph (SKG) architecture. Unlike traditional LLM-based AI systems, Cali X One demonstrates true reasoning, autonomous concept creation, and self-directed learning capabilities.

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
- **Seed Vault System**: Structured knowledge bases with logical principles and operators

### 🌱 Seed Vault System
- **Logical Foundations**: Propositional logic, predicate logic, and inference rules
- **Truth Tables**: Complete definitions for AND, OR, NOT operators
- **Deductive Reasoning**: Modus ponens and syllogistic argument forms
- **Structured Knowledge**: JSON-formatted knowledge bases with metadata
- **Immutable Seeds**: Version-controlled foundational knowledge
- **Integration APIs**: Direct connection to reasoning and validation systems

### 🔐 Caleon Cipher Integration
- **Quantum-Safe Encryption**: Module-LWE KEM + ChaCha20 CPRNG + Keccak streaming
- **Perfect One-Time-Pad**: Information-theoretic security for sensitive data
- **Deterministic Key Generation**: 256-bit seed → quantum-resistant cipher suite
- **Built-in Cryptography**: No external dependencies, pure Python implementation

### 🧬 Cluster Ingestion System
- **Real-time Knowledge Processing**: Ingest and process knowledge clusters instantly
- **Predicate Invention**: Autonomous creation of new concepts and relationships
- **Cross-Domain Logic**: Intelligent relationship detection across knowledge domains
- **Helix Safety**: Immutable core protection with version checking

### 📝 Unanswered Query Vault (UQV)
- **Query Archival**: Store unanswered queries for later processing
- **Learning Opportunities**: Identify knowledge gaps for autonomous learning
- **Review Cycles**: Weekly analysis for predicate invention and human training
- **Worker Integration**: Seamless integration with all dialog systems

### 🤖 DALS Worker Templates
- **Clone-able Workers**: Instant deployment of scripted AI personalities
- **Multi-Modal Communication**: Voice and text duplex communication
- **SKG Integration**: Direct connection to Super-Knowledge Graph
- **Escalation System**: Automatic handoff to human trainers when needed

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

#### Option 4: Windows Startup Scripts
```batch
# Using the provided startup script
start_ucm.bat

# Or PowerShell version
.\start_ucm.ps1
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
├── caleon/                      # Cluster ingestion system
│   ├── routers/
│   │   └── ingest_clusters.py   # Helix-safe cluster processing
│   └── models/                  # Database models
├── cognition/                   # Super-Knowledge Graph
│   ├── skg/                     # SKG core engine
│   │   ├── core.py             # Recursive AGI processing
│   │   ├── uqv.py              # Unanswered Query Vault
│   │   ├── invent_predicate.py # Concept creation
│   │   ├── curiosity.py        # Self-directed learning
│   │   └── contradiction.py    # Conflict resolution
│   └── knowledge_store.py      # SKG API interface
├── DALS/                        # Worker deployment system
│   └── worker_templates/
│       └── host_bubble_worker.py # Clone-able worker template
├── articulator/                 # Phi-3 linguistic utility node
├── generative/                  # Cognitive processing
├── models/                      # SQLAlchemy database models
│   ├── __init__.py             # Base model definitions
│   ├── caleon.py               # Cluster models
│   └── unanswered_query.py     # UQV model
├── ucm_core/                    # Core cognition modules
│   ├── continuity/              # Session management
│   ├── vault/                   # Memory systems
│   └── abby/                    # Protection protocol
├── caleon_cipher.py             # Quantum-safe encryption
├── deps.py                      # Database dependencies
├── init_database.py             # Database initialization
├── start_ucm.bat               # Windows startup script
├── start_ucm.ps1               # PowerShell startup script
└── persona/                     # Personality & scripts
```

### Cognitive Pipeline (Caleon Cognitive Design)
```
Bubble Input
   ↓
Cerebral Cortex → (Pre-filter, routing, state) [Phi-3 linguistic utility]
   ↓
Synaptic Resonator → (symbolic reasoning + contradiction navigation)
   ↓
Anterior/Posterior Helix → (structured inference)
   ↓
EchoStack → (pattern & narrative reinforcement)
   ↓
Gyro-Cortical Harmonizer → (ethical & legacy correction)
   ↓
Phonatory Output Module → (style/voice shaping)
   ↓
Bubble Output
```

**Phi-3 Role**: Linguistic co-processor in Cerebral Cortex for primitive inference, text transformations, and structural bridging. NOT the cognition engine.

### Memory Architecture
- **Streaming Buffer**: Real-time conversation context
- **Session Store**: UUID-based continuity tracking
- **Vault System**: Multi-layered persistent memory
- **Abby Memory**: Protected interaction history

## 🔐 Caleon Cipher - Quantum-Safe Encryption

The Caleon Cipher provides military-grade, quantum-resistant encryption for sensitive UCM data:

### Key Features
- **Module-LWE KEM**: Lattice-based key encapsulation (quantum-resistant)
- **ChaCha20 CPRNG**: Cryptographically secure random number generation
- **Keccak Streaming**: SHA-3 based one-time-pad for perfect secrecy
- **Deterministic Keys**: 256-bit seed generates entire cipher suite
- **Zero Dependencies**: Pure Python implementation using only hashlib

### Usage Examples

#### Generate Key Pair
```bash
python caleon_cipher.py --seed 0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef --keygen
```

#### Encrypt a File
```bash
python caleon_cipher.py --seed 0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef --encrypt secret.txt --peer <peer_public_key>
```

#### Decrypt a File
```bash
python caleon_cipher.py --seed 0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef --decrypt secret.txt.enc
```

### Integration in UCM
The Caleon Cipher is automatically used for:
- Vault data encryption at rest
- Secure inter-module communication
- User data protection
- Session key exchange

## 🧬 Cluster Ingestion System

The Cluster Ingestion System enables real-time knowledge processing and autonomous concept creation:

### Core Features
- **Helix-Safe Processing**: Immutable core protection with version checking
- **Real-time Ingestion**: Process knowledge clusters instantly via REST API
- **Predicate Invention**: Automatically create new concepts from relationship patterns
- **Cross-Domain Logic**: Intelligent detection of relationships across knowledge domains
- **Audit Trail**: Complete logging of all knowledge operations

### API Usage
```bash
# Ingest knowledge clusters
curl -X POST "http://localhost:8001/caleon/ingest_clusters" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "u42",
    "worker": "Nora",
    "helix_version": "1.0.0",
    "clusters": [
      {
        "id": "c1",
        "nodes": ["grief", "acceptance"],
        "density": 0.99,
        "seed": "grief"
      }
    ]
  }'
```

### Database Models
- **ClusterNode**: Knowledge graph nodes with labels
- **ClusterEdge**: Relationships between nodes with confidence scores
- **Predicate**: Invented concepts and relationships
- **VaultLog**: Complete audit trail of operations

## 📝 Unanswered Query Vault (UQV)

The UQV system captures queries that cannot be answered, enabling continuous learning:

### Features
- **Query Archival**: Store unanswered queries with metadata
- **Learning Opportunities**: Identify knowledge gaps for autonomous expansion
- **Review Cycles**: Weekly analysis for predicate invention and training
- **Worker Integration**: Seamless integration with all dialog systems

### Usage in Workers
```python
from cognition.skg.uqv import vault_query

# When SKG returns no results
if not clusters:
    vault_query(
        user_id=user_id,
        session_id=session_id,
        query_text=user_question,
        clusters_found=0,
        worker="Regent",
        reason="no_cluster"
    )
```

### Database Schema
- **Unanswered Queries**: Store with user, session, and metadata
- **Worker Tracking**: Record which worker encountered the query
- **Reason Classification**: Categorize why queries were unanswered

## 🤖 DALS Worker Templates

Clone-able worker templates for instant deployment of scripted AI personalities:

### Features
- **Personality Scripts**: Pre-programmed Regent/Nora/Mark behaviors
- **Multi-Modal**: Voice (TTS) and text (chat bubbles) communication
- **SKG Integration**: Direct connection to knowledge graph
- **Escalation System**: Automatic handoff to human trainers

### Deployment
```bash
# Clone a worker template
dals clone host_bubble_worker --set WORKER_NAME=Regent --set TARGET_USER_ID=42

# Worker automatically:
# - Connects to message bus
# - Loads personality scripts
# - Integrates with SKG and UQV
# - Begins autonomous operation
```

### Template Structure
- **Message Handling**: Pull/push architecture for real-time communication
- **Fallback Logic**: Scripted responses → SKG queries → escalation
- **Environment Config**: Runtime injection of worker-specific settings

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

### Cluster Ingestion Endpoints
```bash
POST /api/v1/caleon/ingest_clusters
# Body: {
#   "user_id": "string",
#   "worker": "string", 
#   "helix_version": "1.0.0",
#   "clusters": [
#     {
#       "id": "string",
#       "nodes": ["string"],
#       "density": float,
#       "seed": "string"
#     }
#   ]
# }
# Returns: {"status": "ok", "new_predicates": int, "helix_safe": true}
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

# Cluster ingestion test
curl -X POST "http://localhost:8001/api/v1/caleon/ingest_clusters" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test_user",
    "worker": "TestWorker",
    "helix_version": "1.0.0",
    "clusters": [
      {
        "id": "test_cluster",
        "nodes": ["test", "concept"],
        "density": 0.95,
        "seed": "test"
      }
    ]
  }'
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

# Test cluster ingestion
python test_ingest_clusters.py
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
- **Caleon Cipher Encryption**: Quantum-safe vault data encryption
- **AES-256 Encryption**: Additional layer for sensitive data
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
- **[SYSTEM_ARCHITECTURE_AGI.md](SYSTEM_ARCHITECTURE_AGI.md)** - AGI technical architecture
- **[PATENT_PORTFOLIO_TECHNICAL.md](PATENT_PORTFOLIO_TECHNICAL.md)** - Patent documentation
- **[CONTRIBUTING_AGI.md](CONTRIBUTING_AGI.md)** - AGI contribution guidelines
- **[SYSTEM_ARCHITECTURE.md](SYSTEM_ARCHITECTURE.md)** - Technical architecture
- **[INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)** - App integration guide
- **[API Documentation](http://localhost:8000/docs)** - Interactive API docs
- **[Caleon Cipher Guide](caleon_cipher.py)** - Quantum-safe encryption documentation
- **[FOUNDER_MANIFEST.txt](FOUNDER_MANIFEST.txt)** - Project vision and principles

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
