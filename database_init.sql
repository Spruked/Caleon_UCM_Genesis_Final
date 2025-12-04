-- Database initialization for Unified Cognition Module
-- Create tables for learning and cognitive data storage

CREATE TABLE IF NOT EXISTS learning_history (
    id SERIAL PRIMARY KEY,
    input_pattern TEXT NOT NULL,
    module_responses JSONB,
    final_decision TEXT,
    outcome_score FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index for faster queries
CREATE INDEX IF NOT EXISTS idx_learning_input ON learning_history(input_pattern);
CREATE INDEX IF NOT EXISTS idx_learning_created ON learning_history(created_at);

-- Table for storing cognitive patterns
CREATE TABLE IF NOT EXISTS cognitive_patterns (
    id SERIAL PRIMARY KEY,
    pattern_key VARCHAR(255) UNIQUE NOT NULL,
    pattern_data JSONB,
    confidence_score FLOAT DEFAULT 0.0,
    usage_count INTEGER DEFAULT 0,
    last_used TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index for pattern lookup
CREATE INDEX IF NOT EXISTS idx_patterns_key ON cognitive_patterns(pattern_key);

-- Unanswered Query Vault tables
CREATE TABLE IF NOT EXISTS unanswered_query (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id VARCHAR(36) NOT NULL,
    session_id VARCHAR(36) NOT NULL,
    query_text TEXT NOT NULL,
    query_vec TEXT,  -- JSON string for optional embedding
    skg_clusters_returned INTEGER DEFAULT 0,
    max_cluster_conf REAL DEFAULT 0.0,
    worker_name VARCHAR(20),  -- Regent/Nora/Mark
    vault_reason VARCHAR(50),  -- "no_cluster"|"low_conf"|"escalated"
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_unanswered_user ON unanswered_query(user_id);
CREATE INDEX IF NOT EXISTS idx_unanswered_reason ON unanswered_query(vault_reason);
CREATE INDEX IF NOT EXISTS idx_unanswered_created ON unanswered_query(created_at);

-- Caleon cluster tables
CREATE TABLE IF NOT EXISTS cluster_node (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    label VARCHAR(255) UNIQUE NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_cluster_node_label ON cluster_node(label);

CREATE TABLE IF NOT EXISTS cluster_edge (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    node_a_id INTEGER NOT NULL,
    node_b_id INTEGER NOT NULL,
    confidence REAL DEFAULT 0.0,
    density REAL DEFAULT 0.0,
    users TEXT,  -- JSON string for set of user IDs
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (node_a_id) REFERENCES cluster_node(id),
    FOREIGN KEY (node_b_id) REFERENCES cluster_node(id)
);

CREATE INDEX IF NOT EXISTS idx_cluster_edge_nodes ON cluster_edge(node_a_id, node_b_id);

CREATE TABLE IF NOT EXISTS predicate (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) UNIQUE NOT NULL,
    signature TEXT,  -- JSON string for list of node labels
    confidence REAL DEFAULT 0.0,
    definition TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_predicate_name ON predicate(name);

-- Vault audit log
CREATE TABLE IF NOT EXISTS vault_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    kind VARCHAR(50),  -- cluster_ingest | predicate_invent
    payload TEXT,  -- JSON string
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_vault_log_kind ON vault_log(kind);
CREATE INDEX IF NOT EXISTS idx_vault_log_created ON vault_log(created_at);