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
                    </tr>
                  </thead>
                  <tbody>
                    {logs.map(log => (
                      <tr key={log.id}>
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
                      </tr>
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
    </div>
  );
}

export default AdminPanel;
