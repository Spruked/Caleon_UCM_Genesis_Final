# Docker Deployment Guide

## Current System Architecture (MASTER PLACEMENT LIST)

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   UCM (8000)    │◄──►│ DALS ISS (8003) │◄──►│ Cali X One      │
│   Caleon Prime  │    │   Core          │    │ Voice System    │
│ • Main AI Core  │    │ • Central Brain │    │ • DALS Int.     │
│ • ISS Proxy     │    │ • Time Anchoring│    │ • Voice Tests   │
│ • Cognition     │    │ • Stardates     │    │ • Signatures    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 ▼
                    ┌─────────────────┐
                    │   Databases     │
                    │ • PostgreSQL    │
                    │ • Redis         │
                    │ • MongoDB       │
                    └─────────────────┘
```

## Service Ports (FINAL MASTER LIST)

| System                 | Dev           | Production  | Port      | Status    |
| ---------------------- | ------------- | ----------- | --------- | --------- |
| **DALS ISS Core**      | Docker        | Docker      | **8003**  | ✅ Active |
| **UCM / Caleon Prime** | Local VS Code | TBD later   | **8000**  | ✅ Active |
| **Cali X One (Phi-3)** | Ollama local  | Same        | **11435** | ✅ Active |
| **GOAT**               | Docker        | Docker      | **9001**  | 🔄 Future |
| **TrueMark**           | Docker        | Docker      | **9002**  | 🔄 Future |
| **CertSig**            | Off for now   | Off for now | **9003**  | ⏸️  Disabled |
| **POM (Coqui)**        | Local         | Local       | **8021**  | 🔄 Future |
| **Cochlear**           | Local         | Local       | **8020**  | 🔄 Future |
| **DALS Dashboard**     | Local Python  | Docker      | **8005**  | 🔄 Future |

## Quick Start

### 1. Build and Start Services
```bash
# Build images
docker-compose -f docker-compose.current.yml build

# Start all services
docker-compose -f docker-compose.current.yml up -d

# Check status
docker-compose -f docker-compose.current.yml ps
```

### 2. Verify Deployment
```bash
# Test UCM
curl http://localhost:8080/health

# Test ISS Module
curl http://localhost:8003/health

# Test UCM-ISS integration
curl http://localhost:8080/iss/status

# Test Cali X One
curl -X POST http://localhost:8080/iss/cali/voice/test \
  -H "Content-Type: application/json" \
  -d '{"message":"Docker test"}'
```

## Service Ports

- **UCM (Main API)**: `http://localhost:8000`
  - `/health` - Health check
  - `/docs` - API documentation
  - `/iss/*` - DALS proxy

- **DALS ISS Module**: `http://localhost:8003`
  - `/health` - ISS health check
  - `/cali/voice/test` - Cali voice testing
  - `/cali/signature/status` - Cali signature status
  - `/sign-cali` - Cali signing interface

- **Cali X One (Ollama)**: `http://localhost:11435`
  - Phi-3 mini model for articulation

- **Databases**:
  - PostgreSQL: `localhost:5432`
  - Redis: `localhost:6379`
  - MongoDB: `localhost:27018`

- **Monitoring**:
  - Prometheus: `http://localhost:9090`

## Docker Commands

```bash
# View logs
docker-compose -f docker-compose.current.yml logs ucm
docker-compose -f docker-compose.current.yml logs iss-module

# Stop services
docker-compose -f docker-compose.current.yml down

# Rebuild specific service
docker-compose -f docker-compose.current.yml build ucm

# Scale services
docker-compose -f docker-compose.current.yml up -d --scale ucm=2
```

## Environment Configuration

The system uses `.env` file for configuration. Key variables:

```env
# UCM Configuration
ENVIRONMENT=production
HOST=0.0.0.0
PORT=8080

# ISS Integration
ISS_HOST=iss-module
ISS_PORT=8003

# Databases
POSTGRES_URL=postgresql://cortex_user:cortex_pass@postgres:5432/cortex_db
REDIS_URL=redis://redis:6379
MONGO_URL=mongodb://mongo:27017
```

## Troubleshooting

### Service Won't Start
```bash
# Check logs
docker-compose -f docker-compose.current.yml logs [service-name]

# Restart specific service
docker-compose -f docker-compose.current.yml restart ucm
```

### Port Conflicts
```bash
# Check what's using ports
netstat -ano | findstr :8080
netstat -ano | findstr :8003

# Change ports in docker-compose.current.yml
ports:
  - "8081:8080"  # Change host port
```

### Database Connection Issues
```bash
# Check database health
docker-compose -f docker-compose.current.yml exec postgres pg_isready -U cortex_user -d cortex_db
```

## Production Deployment

For production, use the full `docker-compose.yml` which includes:
- Nginx reverse proxy
- SSL/TLS termination
- Additional monitoring
- Production database configuration

```bash
docker-compose up -d  # Uses docker-compose.yml
```