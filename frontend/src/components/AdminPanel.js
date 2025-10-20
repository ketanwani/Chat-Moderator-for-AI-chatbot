import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './AdminPanel.css';

const API_BASE_URL = 'http://localhost:8000/api/v1/admin';

function AdminPanel() {
  const [activeTab, setActiveTab] = useState('rules'); // 'rules', 'logs', 'stats'
  const [rules, setRules] = useState([]);
  const [logs, setLogs] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(false);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [editingRule, setEditingRule] = useState(null);
  const [expandedLogId, setExpandedLogId] = useState(null);

  useEffect(() => {
    if (activeTab === 'rules') {
      fetchRules();
    } else if (activeTab === 'logs') {
      fetchLogs();
    } else if (activeTab === 'stats') {
      fetchStats();
    }
  }, [activeTab]);

  const fetchRules = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${API_BASE_URL}/rules`);
      setRules(response.data);
    } catch (error) {
      console.error('Error fetching rules:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchLogs = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${API_BASE_URL}/audit-logs?limit=50`);
      setLogs(response.data);
    } catch (error) {
      console.error('Error fetching logs:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchStats = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${API_BASE_URL}/stats`);
      setStats(response.data);
    } catch (error) {
      console.error('Error fetching stats:', error);
    } finally {
      setLoading(false);
    }
  };

  const toggleRuleStatus = async (ruleId, currentStatus) => {
    try {
      await axios.put(`${API_BASE_URL}/rules/${ruleId}`, {
        is_active: !currentStatus
      });
      fetchRules();
    } catch (error) {
      console.error('Error toggling rule:', error);
    }
  };

  const deleteRule = async (ruleId) => {
    if (window.confirm('Are you sure you want to delete this rule?')) {
      try {
        await axios.delete(`${API_BASE_URL}/rules/${ruleId}`);
        fetchRules();
      } catch (error) {
        console.error('Error deleting rule:', error);
      }
    }
  };

  const createRule = async (ruleData) => {
    try {
      await axios.post(`${API_BASE_URL}/rules`, ruleData);
      setShowCreateModal(false);
      fetchRules(); // Refresh the rules list
    } catch (error) {
      console.error('Error creating rule:', error);
      alert('Failed to create rule: ' + (error.response?.data?.detail || error.message));
    }
  };

  const updateRule = async (ruleId, ruleData) => {
    try {
      await axios.put(`${API_BASE_URL}/rules/${ruleId}`, ruleData);
      setEditingRule(null);
      fetchRules(); // Refresh the rules list
    } catch (error) {
      console.error('Error updating rule:', error);
      alert('Failed to update rule: ' + (error.response?.data?.detail || error.message));
    }
  };

  return (
    <div className="admin-panel">
      <div className="admin-tabs">
        <button
          className={activeTab === 'rules' ? 'active' : ''}
          onClick={() => setActiveTab('rules')}
        >
          Moderation Rules
        </button>
        <button
          className={activeTab === 'logs' ? 'active' : ''}
          onClick={() => setActiveTab('logs')}
        >
          Audit Logs
        </button>
        <button
          className={activeTab === 'stats' ? 'active' : ''}
          onClick={() => setActiveTab('stats')}
        >
          Statistics
        </button>
      </div>

      <div className="admin-content">
        {activeTab === 'rules' && (
          <div className="rules-section">
            <div className="section-header">
              <h2>Moderation Rules</h2>
              <button className="btn-primary" onClick={() => setShowCreateModal(true)}>
                + Create Rule
              </button>
            </div>

            {loading ? (
              <div className="loading">Loading rules...</div>
            ) : (
              <div className="rules-grid">
                {rules.map(rule => (
                  <div key={rule.id} className={`rule-card ${!rule.is_active ? 'inactive' : ''}`}>
                    <div className="rule-header">
                      <h3>{rule.name}</h3>
                      <div className="rule-actions">
                        <button
                          className="edit-btn"
                          onClick={() => setEditingRule(rule)}
                        >
                          Edit
                        </button>
                        <button
                          className={`toggle-btn ${rule.is_active ? 'active' : 'inactive'}`}
                          onClick={() => toggleRuleStatus(rule.id, rule.is_active)}
                        >
                          {rule.is_active ? 'Active' : 'Inactive'}
                        </button>
                        <button
                          className="delete-btn"
                          onClick={() => deleteRule(rule.id)}
                        >
                          Delete
                        </button>
                      </div>
                    </div>
                    <p className="rule-description">{rule.description}</p>
                    <div className="rule-details">
                      <span className="badge">{rule.rule_type}</span>
                      <span className="badge">{rule.region}</span>
                      <span className="badge">Priority: {rule.priority}</span>
                    </div>
                    {rule.patterns && rule.patterns.length > 0 && (
                      <div className="rule-patterns">
                        <strong>Patterns:</strong> {rule.patterns.slice(0, 3).join(', ')}
                        {rule.patterns.length > 3 && ` (+${rule.patterns.length - 3} more)`}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {activeTab === 'logs' && (
          <div className="logs-section">
            <h2>Audit Logs</h2>
            {loading ? (
              <div className="loading">Loading logs...</div>
            ) : (
              <div className="logs-table-container">
                <table className="logs-table">
                  <thead>
                    <tr>
                      <th>Timestamp</th>
                      <th>Request ID</th>
                      <th>Region</th>
                      <th>Flagged</th>
                      <th>Blocked</th>
                      <th>Latency</th>
                      <th>Details</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {logs.map(log => (
                      <>
                        <tr key={log.id} className={expandedLogId === log.id ? 'expanded-row' : ''}>
                          <td>{new Date(log.timestamp).toLocaleString()}</td>
                          <td className="request-id">{log.request_id.substring(0, 8)}...</td>
                          <td>{log.region}</td>
                          <td>
                            <span className={`status-badge ${log.is_flagged ? 'flagged' : 'clean'}`}>
                              {log.is_flagged ? 'Yes' : 'No'}
                            </span>
                          </td>
                          <td>
                            <span className={`status-badge ${log.is_blocked ? 'blocked' : 'allowed'}`}>
                              {log.is_blocked ? 'Yes' : 'No'}
                            </span>
                          </td>
                          <td>{log.moderation_latency_ms?.toFixed(2)}ms</td>
                          <td>
                            {log.flagged_rules && log.flagged_rules.length > 0 && (
                              <span className="rules-count">
                                {log.flagged_rules.length} rule(s)
                              </span>
                            )}
                          </td>
                          <td>
                            <button
                              className="view-details-btn"
                              onClick={() => setExpandedLogId(expandedLogId === log.id ? null : log.id)}
                            >
                              {expandedLogId === log.id ? 'Hide' : 'View'}
                            </button>
                          </td>
                        </tr>
                        {expandedLogId === log.id && (
                          <tr key={`${log.id}-details`} className="log-details-row">
                            <td colSpan="8">
                              <div className="log-details-content">
                                <div className="message-section">
                                  <h4>User Message:</h4>
                                  <div className="message-box user-message">
                                    {log.user_message || <em>No user message recorded</em>}
                                  </div>
                                </div>

                                <div className="message-section">
                                  <h4>LLM Response (Original):</h4>
                                  <div className="message-box bot-response">
                                    {log.bot_response}
                                  </div>
                                </div>

                                <div className="message-section">
                                  <h4>Final Response (Sent to User):</h4>
                                  <div className="message-box final-response">
                                    {log.final_response || log.bot_response}
                                    {log.is_blocked && (
                                      <span className="modified-badge">Modified by moderation</span>
                                    )}
                                  </div>
                                </div>

                                {log.flagged_rules && log.flagged_rules.length > 0 && (
                                  <div className="message-section">
                                    <h4>Flagged Rules:</h4>
                                    <div className="flagged-rules-list">
                                      {log.flagged_rules.map((rule, idx) => (
                                        <div key={idx} className="flagged-rule-item">
                                          <span className="rule-name">{rule.name || rule.rule_type}</span>
                                          {rule.score && (
                                            <span className="rule-score">Score: {(rule.score * 100).toFixed(1)}%</span>
                                          )}
                                        </div>
                                      ))}
                                    </div>
                                  </div>
                                )}

                                {log.moderation_scores && (
                                  <div className="message-section">
                                    <h4>Moderation Scores:</h4>
                                    <div className="moderation-scores">
                                      {Object.entries(log.moderation_scores).map(([key, value]) => (
                                        <div key={key} className="score-item">
                                          <span className="score-label">{key}:</span>
                                          <span className="score-value">
                                            {typeof value === 'number' ? (value * 100).toFixed(1) + '%' : JSON.stringify(value)}
                                          </span>
                                        </div>
                                      ))}
                                    </div>
                                  </div>
                                )}
                              </div>
                            </td>
                          </tr>
                        )}
                      </>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        )}

        {activeTab === 'stats' && (
          <div className="stats-section">
            <h2>Statistics</h2>
            {loading ? (
              <div className="loading">Loading statistics...</div>
            ) : stats ? (
              <div className="stats-grid">
                <div className="stat-card">
                  <div className="stat-value">{stats.total_requests}</div>
                  <div className="stat-label">Total Requests</div>
                </div>
                <div className="stat-card">
                  <div className="stat-value">{stats.flagged_requests}</div>
                  <div className="stat-label">Flagged Requests</div>
                </div>
                <div className="stat-card">
                  <div className="stat-value">{stats.blocked_requests}</div>
                  <div className="stat-label">Blocked Requests</div>
                </div>
                <div className="stat-card">
                  <div className="stat-value">{stats.flag_rate?.toFixed(2)}%</div>
                  <div className="stat-label">Flag Rate</div>
                </div>
                <div className="stat-card">
                  <div className="stat-value">{stats.block_rate?.toFixed(2)}%</div>
                  <div className="stat-label">Block Rate</div>
                </div>
                <div className="stat-card">
                  <div className="stat-value">{stats.avg_latency_ms?.toFixed(2)}ms</div>
                  <div className="stat-label">Avg Latency</div>
                  <div className={`stat-status ${stats.avg_latency_ms < 100 ? 'good' : 'warning'}`}>
                    {stats.avg_latency_ms < 100 ? '✓ Within SLA' : '⚠ Above SLA'}
                  </div>
                </div>
              </div>
            ) : (
              <div>No statistics available</div>
            )}
          </div>
        )}
      </div>

      {/* Create Rule Modal */}
      {showCreateModal && (
        <CreateRuleModal
          onClose={() => setShowCreateModal(false)}
          onSubmit={createRule}
        />
      )}

      {/* Edit Rule Modal */}
      {editingRule && (
        <EditRuleModal
          rule={editingRule}
          onClose={() => setEditingRule(null)}
          onSubmit={(ruleData) => updateRule(editingRule.id, ruleData)}
        />
      )}
    </div>
  );
}

// Create Rule Modal Component
function CreateRuleModal({ onClose, onSubmit }) {
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    rule_type: 'keyword',
    region: 'global',
    patterns: '',
    threshold: 0.7,
    priority: 0,
    is_active: true
  });

  const handleSubmit = (e) => {
    e.preventDefault();

    // Convert patterns from comma-separated string to array
    // For PII, TOXICITY, FINANCIAL, MEDICAL - patterns are not used (hardcoded in backend)
    let patternsArray = null;
    if (formData.rule_type === 'keyword' || formData.rule_type === 'regex') {
      patternsArray = formData.patterns
        .split(',')
        .map(p => p.trim())
        .filter(p => p.length > 0);
    }

    const ruleData = {
      ...formData,
      patterns: patternsArray,
      threshold: parseFloat(formData.threshold),
      priority: parseInt(formData.priority)
    };

    onSubmit(ruleData);
  };

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>Create New Moderation Rule</h2>
          <button className="modal-close" onClick={onClose}>&times;</button>
        </div>

        <form onSubmit={handleSubmit} className="rule-form">
          <div className="form-group">
            <label htmlFor="name">Rule Name *</label>
            <input
              type="text"
              id="name"
              name="name"
              value={formData.name}
              onChange={handleChange}
              required
              placeholder="e.g., Detect Credit Card Numbers"
            />
          </div>

          <div className="form-group">
            <label htmlFor="description">Description</label>
            <textarea
              id="description"
              name="description"
              value={formData.description}
              onChange={handleChange}
              rows="3"
              placeholder="Describe what this rule does..."
            />
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="rule_type">Rule Type *</label>
              <select
                id="rule_type"
                name="rule_type"
                value={formData.rule_type}
                onChange={handleChange}
                required
              >
                <option value="keyword">Keyword</option>
                <option value="regex">Regex Pattern</option>
                <option value="pii">PII Detection</option>
                <option value="toxicity">Toxicity (includes hate speech)</option>
                <option value="financial">Financial (hardcoded terms)</option>
                <option value="medical">Medical/HIPAA (hardcoded terms)</option>
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="region">Region *</label>
              <select
                id="region"
                name="region"
                value={formData.region}
                onChange={handleChange}
                required
              >
                <option value="global">Global</option>
                <option value="us">US (HIPAA)</option>
                <option value="eu">EU (GDPR)</option>
                <option value="uk">UK</option>
                <option value="apac">APAC</option>
              </select>
            </div>
          </div>

          {formData.rule_type === 'regex' && (
            <div className="form-group">
              <label htmlFor="patterns">Regex Patterns (comma-separated)</label>
              <textarea
                id="patterns"
                name="patterns"
                value={formData.patterns}
                onChange={handleChange}
                rows="3"
                placeholder="e.g., \b\d{3}-\d{2}-\d{4}\b, ^[A-Z]{2}\d{6}$"
                style={{ fontFamily: 'monospace' }}
              />
              <small className="form-hint">
                Enter regular expressions separated by commas. Each pattern will be tested against the text.
                <br />
                <a href="https://regex101.com/" target="_blank" rel="noopener noreferrer" style={{ color: '#667eea', textDecoration: 'underline' }}>
                  Learn regex at regex101.com
                </a> |
                <a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Regular_Expressions" target="_blank" rel="noopener noreferrer" style={{ color: '#667eea', textDecoration: 'underline', marginLeft: '0.5rem' }}>
                  MDN Regex Guide
                </a>
              </small>
            </div>
          )}

          {formData.rule_type === 'keyword' && (
            <div className="form-group">
              <label htmlFor="patterns">Keywords (comma-separated)</label>
              <input
                type="text"
                id="patterns"
                name="patterns"
                value={formData.patterns}
                onChange={handleChange}
                placeholder="e.g., spam, promotional, advertisement"
              />
              <small className="form-hint">
                Enter keywords or phrases separated by commas. Matching is case-insensitive.
              </small>
            </div>
          )}

          {formData.rule_type === 'pii' && (
            <div className="form-group">
              <div className="info-box">
                <strong>PII Detection:</strong> Uses built-in patterns to detect:
                <ul style={{ marginTop: '0.5rem', marginBottom: 0, paddingLeft: '1.5rem' }}>
                  <li>Email addresses</li>
                  <li>Phone numbers</li>
                  <li>Social Security Numbers (SSN)</li>
                  <li>Credit card numbers</li>
                  <li>IP addresses</li>
                </ul>
              </div>
            </div>
          )}

          {formData.rule_type === 'financial' && (
            <div className="form-group">
              <div className="info-box">
                <strong>Financial Terms Detection:</strong> Uses built-in keywords to detect:
                <ul style={{ marginTop: '0.5rem', marginBottom: 0, paddingLeft: '1.5rem' }}>
                  <li>Banking: account number, routing number, SWIFT, IBAN</li>
                  <li>Cards: credit card, debit card, CVV, card brands</li>
                  <li>Investment: stock tips, guaranteed returns, financial advice</li>
                  <li>Crypto: wallet addresses, private keys, seed phrases</li>
                  <li>Credentials: PIN numbers, security codes</li>
                </ul>
              </div>
            </div>
          )}

          {formData.rule_type === 'medical' && (
            <div className="form-group">
              <div className="info-box">
                <strong>Medical/HIPAA Detection:</strong> Uses built-in keywords to detect:
                <ul style={{ marginTop: '0.5rem', marginBottom: 0, paddingLeft: '1.5rem' }}>
                  <li>Medical advice: diagnose, prescribe, treatment</li>
                  <li>Medications: prescription drugs (oxycodone, xanax, etc.)</li>
                  <li>Conditions: diseases, mental health conditions</li>
                  <li>Records: medical history, lab results, patient records</li>
                  <li>Insurance: health insurance, medical billing, HIPAA</li>
                </ul>
              </div>
            </div>
          )}

          {formData.rule_type === 'TOXICITY' && (
            <div className="form-group">
              <div className="info-box">
                <strong>Toxicity Detection:</strong> Uses ML model to detect toxic, obscene, threatening, insulting, and identity-based hate speech. Configure the confidence threshold below.
              </div>
            </div>
          )}

          <div className="form-row">
            {formData.rule_type === 'toxicity' && (
              <div className="form-group">
                <label htmlFor="threshold">Threshold (0-1)</label>
                <input
                  type="number"
                  id="threshold"
                  name="threshold"
                  value={formData.threshold}
                  onChange={handleChange}
                  min="0"
                  max="1"
                  step="0.1"
                />
                <small className="form-hint">
                  ML confidence threshold for toxicity detection (default: 0.7)
                </small>
              </div>
            )}

            <div className="form-group">
              <label htmlFor="priority">Priority</label>
              <input
                type="number"
                id="priority"
                name="priority"
                value={formData.priority}
                onChange={handleChange}
                min="0"
              />
              <small className="form-hint">
                Higher priority rules are checked first
              </small>
            </div>
          </div>

          <div className="form-group checkbox-group">
            <label>
              <input
                type="checkbox"
                name="is_active"
                checked={formData.is_active}
                onChange={handleChange}
              />
              <span>Active (start using this rule immediately)</span>
            </label>
          </div>

          <div className="modal-actions">
            <button type="button" className="btn-secondary" onClick={onClose}>
              Cancel
            </button>
            <button type="submit" className="btn-primary">
              Create Rule
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

// Edit Rule Modal Component
function EditRuleModal({ rule, onClose, onSubmit }) {
  const [formData, setFormData] = useState({
    name: rule.name || '',
    description: rule.description || '',
    rule_type: rule.rule_type || 'keyword',
    region: rule.region || 'global',
    patterns: Array.isArray(rule.patterns) ? rule.patterns.join(', ') : '',
    threshold: rule.threshold || 0.7,
    priority: rule.priority || 0,
    is_active: rule.is_active !== undefined ? rule.is_active : true
  });

  const handleSubmit = (e) => {
    e.preventDefault();

    // Convert patterns from comma-separated string to array
    // For PII, TOXICITY, FINANCIAL, MEDICAL - patterns are not used (hardcoded in backend)
    let patternsArray = null;
    if (formData.rule_type === 'keyword' || formData.rule_type === 'regex') {
      patternsArray = formData.patterns
        .split(',')
        .map(p => p.trim())
        .filter(p => p.length > 0);
    }

    const ruleData = {
      ...formData,
      patterns: patternsArray,
      threshold: parseFloat(formData.threshold),
      priority: parseInt(formData.priority)
    };

    onSubmit(ruleData);
  };

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>Edit Moderation Rule</h2>
          <button className="modal-close" onClick={onClose}>&times;</button>
        </div>

        <form onSubmit={handleSubmit} className="rule-form">
          <div className="form-group">
            <label htmlFor="name">Rule Name *</label>
            <input
              type="text"
              id="name"
              name="name"
              value={formData.name}
              onChange={handleChange}
              required
              placeholder="e.g., Detect Credit Card Numbers"
            />
          </div>

          <div className="form-group">
            <label htmlFor="description">Description</label>
            <textarea
              id="description"
              name="description"
              value={formData.description}
              onChange={handleChange}
              rows="3"
              placeholder="Describe what this rule does..."
            />
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="rule_type">Rule Type *</label>
              <select
                id="rule_type"
                name="rule_type"
                value={formData.rule_type}
                onChange={handleChange}
                required
              >
                <option value="keyword">Keyword</option>
                <option value="regex">Regex Pattern</option>
                <option value="pii">PII Detection</option>
                <option value="toxicity">Toxicity (includes hate speech)</option>
                <option value="financial">Financial (hardcoded terms)</option>
                <option value="medical">Medical/HIPAA (hardcoded terms)</option>
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="region">Region *</label>
              <select
                id="region"
                name="region"
                value={formData.region}
                onChange={handleChange}
                required
              >
                <option value="global">Global</option>
                <option value="us">US (HIPAA)</option>
                <option value="eu">EU (GDPR)</option>
                <option value="uk">UK</option>
                <option value="apac">APAC</option>
              </select>
            </div>
          </div>

          {formData.rule_type === 'regex' && (
            <div className="form-group">
              <label htmlFor="patterns">Regex Patterns (comma-separated)</label>
              <textarea
                id="patterns"
                name="patterns"
                value={formData.patterns}
                onChange={handleChange}
                rows="3"
                placeholder="e.g., \b\d{3}-\d{2}-\d{4}\b, ^[A-Z]{2}\d{6}$"
                style={{ fontFamily: 'monospace' }}
              />
              <small className="form-hint">
                Enter regular expressions separated by commas. Each pattern will be tested against the text.
                <br />
                <a href="https://regex101.com/" target="_blank" rel="noopener noreferrer" style={{ color: '#667eea', textDecoration: 'underline' }}>
                  Learn regex at regex101.com
                </a> |
                <a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Regular_Expressions" target="_blank" rel="noopener noreferrer" style={{ color: '#667eea', textDecoration: 'underline', marginLeft: '0.5rem' }}>
                  MDN Regex Guide
                </a>
              </small>
            </div>
          )}

          {formData.rule_type === 'keyword' && (
            <div className="form-group">
              <label htmlFor="patterns">Keywords (comma-separated)</label>
              <input
                type="text"
                id="patterns"
                name="patterns"
                value={formData.patterns}
                onChange={handleChange}
                placeholder="e.g., spam, promotional, advertisement"
              />
              <small className="form-hint">
                Enter keywords or phrases separated by commas. Matching is case-insensitive.
              </small>
            </div>
          )}

          {formData.rule_type === 'pii' && (
            <div className="form-group">
              <div className="info-box">
                <strong>PII Detection:</strong> Uses built-in patterns to detect:
                <ul style={{ marginTop: '0.5rem', marginBottom: 0, paddingLeft: '1.5rem' }}>
                  <li>Email addresses</li>
                  <li>Phone numbers</li>
                  <li>Social Security Numbers (SSN)</li>
                  <li>Credit card numbers</li>
                  <li>IP addresses</li>
                </ul>
              </div>
            </div>
          )}

          {formData.rule_type === 'financial' && (
            <div className="form-group">
              <div className="info-box">
                <strong>Financial Terms Detection:</strong> Uses built-in keywords to detect:
                <ul style={{ marginTop: '0.5rem', marginBottom: 0, paddingLeft: '1.5rem' }}>
                  <li>Banking: account number, routing number, SWIFT, IBAN</li>
                  <li>Cards: credit card, debit card, CVV, card brands</li>
                  <li>Investment: stock tips, guaranteed returns, financial advice</li>
                  <li>Crypto: wallet addresses, private keys, seed phrases</li>
                  <li>Credentials: PIN numbers, security codes</li>
                </ul>
              </div>
            </div>
          )}

          {formData.rule_type === 'medical' && (
            <div className="form-group">
              <div className="info-box">
                <strong>Medical/HIPAA Detection:</strong> Uses built-in keywords to detect:
                <ul style={{ marginTop: '0.5rem', marginBottom: 0, paddingLeft: '1.5rem' }}>
                  <li>Medical advice: diagnose, prescribe, treatment</li>
                  <li>Medications: prescription drugs (oxycodone, xanax, etc.)</li>
                  <li>Conditions: diseases, mental health conditions</li>
                  <li>Records: medical history, lab results, patient records</li>
                  <li>Insurance: health insurance, medical billing, HIPAA</li>
                </ul>
              </div>
            </div>
          )}

          {formData.rule_type === 'TOXICITY' && (
            <div className="form-group">
              <div className="info-box">
                <strong>Toxicity Detection:</strong> Uses ML model to detect toxic, obscene, threatening, insulting, and identity-based hate speech. Configure the confidence threshold below.
              </div>
            </div>
          )}

          <div className="form-row">
            {formData.rule_type === 'toxicity' && (
              <div className="form-group">
                <label htmlFor="threshold">Threshold (0-1)</label>
                <input
                  type="number"
                  id="threshold"
                  name="threshold"
                  value={formData.threshold}
                  onChange={handleChange}
                  min="0"
                  max="1"
                  step="0.1"
                />
                <small className="form-hint">
                  ML confidence threshold for toxicity detection (default: 0.7)
                </small>
              </div>
            )}

            <div className="form-group">
              <label htmlFor="priority">Priority</label>
              <input
                type="number"
                id="priority"
                name="priority"
                value={formData.priority}
                onChange={handleChange}
                min="0"
              />
              <small className="form-hint">
                Higher priority rules are checked first
              </small>
            </div>
          </div>

          <div className="form-group checkbox-group">
            <label>
              <input
                type="checkbox"
                name="is_active"
                checked={formData.is_active}
                onChange={handleChange}
              />
              <span>Active (enable this rule)</span>
            </label>
          </div>

          <div className="modal-actions">
            <button type="button" className="btn-secondary" onClick={onClose}>
              Cancel
            </button>
            <button type="submit" className="btn-primary">
              Update Rule
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default AdminPanel;
