/**
 * GOAT Integration with UCM
 * Example of how GOAT connects to the central Caleon service
 */

// services/ucm_client.js
const { CaleonClient } = require('../shared/ucm_client');

class GOATCaleonBridge {
    constructor() {
        this.caleon = new CaleonClient({
            baseUrl: process.env.UCM_URL || 'http://localhost:8000'
        });
        this.sessionId = null;
    }

    async initialize() {
        // Create session for GOAT user
        const session = await this.caleon.createSession();
        this.sessionId = session.session_id;
        console.log('GOAT Caleon session initialized:', this.sessionId);
    }

    async askCaleon(message, user = 'goat_user') {
        try {
            const response = await this.caleon.ask(message, {
                sessionId: this.sessionId,
                user: user
            });
            return response;
        } catch (error) {
            console.error('GOAT Caleon error:', error);
            throw error;
        }
    }

    async streamCaleon(message, onToken, user = 'goat_user') {
        try {
            await this.caleon.stream(message, onToken, {
                sessionId: this.sessionId,
                user: user
            });
        } catch (error) {
            console.error('GOAT Caleon stream error:', error);
            throw error;
        }
    }

    async learnFact(fact) {
        return await this.caleon.learn(fact);
    }

    async setUserPreference(user, key, value) {
        return await this.caleon.setPreference(user, key, value);
    }
}

// Export singleton instance
const goatCaleon = new GOATCaleonBridge();
module.exports = goatCaleon;

// Example usage in GOAT:
/*
// Initialize on app startup
await goatCaleon.initialize();

// Use in components
const response = await goatCaleon.askCaleon("How can I optimize this workflow?");

// Stream responses
await goatCaleon.streamCaleon("Tell me about this data", (token) => {
    console.log('Token:', token);
});
*/