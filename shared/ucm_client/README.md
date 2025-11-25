# Shared UCM Client Libraries

This directory contains client libraries that allow any application to connect to the central Unified Cognition Module (UCM) running Caleon Prime.

## 🚀 Quick Start

### JavaScript/Node.js
```javascript
const { CaleonClient } = require('./shared/ucm_client');

const caleon = new CaleonClient();
const response = await caleon.ask("Hello Caleon!");
console.log(response.reply);
```

### Python
```python
from shared.ucm_client.ucm import CaleonClient

caleon = CaleonClient()
response = await caleon.ask("Hello Caleon!")
print(response['reply'])
```

### React
```jsx
import { useCaleon, CaleonBubble } from './shared/ucm_client/useCaleon.js';

function MyComponent() {
    const { ask, loading } = useCaleon();

    const handleAsk = async () => {
        const response = await ask("Hello Caleon!");
        console.log(response.reply);
    };

    return (
        <div>
            <CaleonBubble activated={true} />
            <button onClick={handleAsk} disabled={loading}>
                Ask Caleon
            </button>
        </div>
    );
}
```

## 📚 API Reference

### Core Methods

#### `ask(message, options?)`
Ask Caleon a question and get her response.

**Parameters:**
- `message` (string): The question or message
- `options.sessionId` (string, optional): Session ID for continuity
- `options.user` (string, optional): User identifier for personalization

**Returns:** Promise resolving to response object with `reply` field

#### `stream(message, onToken, options?)`
Stream Caleon's response token by token.

**Parameters:**
- `message` (string): The question or message
- `onToken` (function): Callback function called for each token
- `options.sessionId` (string, optional): Session ID for continuity
- `options.user` (string, optional): User identifier

#### `createSession()`
Create a new conversation session for continuity.

**Returns:** Promise resolving to `{session_id: "uuid"}`

#### `learn(fact)`
Teach Caleon a new fact for her long-term memory.

**Parameters:**
- `fact` (string): The fact to learn

#### `setPreference(user, key, value)`
Set a user preference.

**Parameters:**
- `user` (string): User identifier
- `key` (string): Preference key
- `value` (string): Preference value

### Abby-Specific Methods

#### `addAbbyEvent(event)`
Add an event to Abby's timeline memory.

#### `setAbbyPreference(key, value)`
Set a preference for Abby.

#### `getAbbyMemory()`
Get Abby's complete memory profile.

## 🔧 Configuration

### Environment Variables

- `UCM_URL`: Base URL of the UCM service (default: `http://localhost:8000`)

### Client Options

```javascript
const caleon = new CaleonClient({
    baseUrl: 'http://my-ucm-server:8000',
    headers: {
        'Authorization': 'Bearer token'
    }
});
```

## 🏗️ Integration Examples

See the `examples/` directory for complete integration examples:

- `goat_integration.js` - GOAT application integration
- `dals_integration.py` - DALS application integration
- `react_integration.jsx` - React frontend integration

## 🐳 Deployment

The UCM service can run in multiple ways:

### Local Development
```bash
cd UCM
python main.py
```

### Docker
```bash
cd UCM
docker build -t ucm .
docker run -p 8000:8000 ucm
```

### Docker Compose
```bash
cd UCM
docker-compose up
```

## 🔄 Architecture

```
┌─────────────────┐    ┌─────────────────┐
│   GOAT App      │    │   DALS App      │
│                 │    │                 │
│  caleon.ask()   │◄──►│  caleon.ask()   │
│  caleon.stream()│    │  caleon.stream()│
└─────────────────┘    └─────────────────┘
         │                       │
         └───────────────────────┘
                 │
        ┌─────────────────┐
        │   UCM Service   │
        │                 │
        │  Caleon Prime   │
        │                 │
        │ • Vault Memory  │
        │ • Abby Protocol │
        │ • Phi-3 Artic.  │
        │ • Continuity    │
        └─────────────────┘
```

## 📋 Checklist for App Integration

- [ ] Copy `shared/ucm_client/` to your project
- [ ] Install dependencies (aiohttp for Python, none for JS)
- [ ] Initialize client with appropriate base URL
- [ ] Create session on app startup
- [ ] Use `ask()` or `stream()` methods in your UI
- [ ] Handle errors gracefully
- [ ] Test with UCM service running

## 🆘 Troubleshooting

**Connection refused?**
- Ensure UCM service is running on the configured URL
- Check firewall settings
- Verify Docker networking if using containers

**Abby Protocol not activating?**
- Pass `user` parameter with "abby" or "my daughter"
- Check that message contains Abby-related keywords

**Streaming not working?**
- Ensure your environment supports Server-Sent Events
- Check browser console for CORS errors

## 🤝 Contributing

When adding new features to the UCM:

1. Update the client libraries to expose new endpoints
2. Add examples in the `examples/` directory
3. Update this README with new API methods
4. Test across all supported languages/frameworks