import React, { useState, useEffect } from 'react';
import './AlertsDashboard.css';

// Types de données
interface Alert {
  id: string;
  event_id: string;
  timestamp: string;
  risk_level: string;
  justification: string;
  source: string;
  user: string;
  action_taken: string;
  risk_score?: number;
  raw_data?: any;
  device_context?: any;
  user_context?: any;
}

interface AlertModalProps {
  alert: Alert | null;
  isOpen: boolean;
  onClose: () => void;
}

// Composant Modal pour les détails d'alerte
const AlertModal: React.FC<AlertModalProps> = ({ alert, isOpen, onClose }) => {
  if (!isOpen || !alert) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>Détails de l'Alerte</h2>
          <button className="close-button" onClick={onClose}>×</button>
        </div>
        <div className="modal-body">
          <div className="detail-row">
            <strong>ID:</strong> {alert.id}
          </div>
          <div className="detail-row">
            <strong>Événement ID:</strong> {alert.event_id}
          </div>
          <div className="detail-row">
            <strong>Timestamp:</strong> {new Date(alert.timestamp).toLocaleString('fr-FR')}
          </div>
          <div className="detail-row">
            <strong>Source:</strong> {alert.source}
          </div>
          <div className="detail-row">
            <strong>Utilisateur:</strong> {alert.user}
          </div>
          <div className="detail-row">
            <strong>Niveau de Risque:</strong> 
            <span className="risk-badge" style={{ 
              backgroundColor: getRiskLevelColor(alert.risk_level),
              marginLeft: '10px'
            }}>
              {alert.risk_level}
            </span>
          </div>
          <div className="detail-row">
            <strong>Justification:</strong> {alert.justification}
          </div>
          <div className="detail-row">
            <strong>Action Prise:</strong> {alert.action_taken}
          </div>
          {alert.raw_data && (
            <div className="detail-section">
              <h3>Données Brutes</h3>
              <pre>{JSON.stringify(alert.raw_data, null, 2)}</pre>
            </div>
          )}
          {alert.device_context && (
            <div className="detail-section">
              <h3>Contexte Appareil</h3>
              <pre>{JSON.stringify(alert.device_context, null, 2)}</pre>
            </div>
          )}
        </div>
        <div className="modal-footer">
          <button className="btn btn-secondary" onClick={onClose}>Fermer</button>
        </div>
      </div>
    </div>
  );
};

// Composant Toast pour les notifications
const Toast: React.FC<{ message: string; type: 'success' | 'error' | 'info'; onClose: () => void }> = ({ 
  message, 
  type, 
  onClose 
}) => {
  useEffect(() => {
    const timer = setTimeout(onClose, 3000);
    return () => clearTimeout(timer);
  }, [onClose]);

  return (
    <div className={`toast toast-${type}`}>
      <span>{message}</span>
      <button onClick={onClose}>×</button>
    </div>
  );
};

// Fonctions utilitaires
const getRiskLevelColor = (riskLevel: string) => {
  switch (riskLevel) {
    case 'CRITICAL': return '#dc3545';
    case 'HIGH': return '#fd7e14';
    case 'MEDIUM': return '#ffc107';
    case 'LOW': return '#28a745';
    default: return '#6c757d';
  }
};

const getSourceIcon = (source: string) => {
  switch (source) {
    case 'Hydra': return '🕷️';
    case 'Cassandra': return '🔮';
    default: return '⚠️';
  }
};

const AlertsDashboard: React.FC = () => {
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [filteredAlerts, setFilteredAlerts] = useState<Alert[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [selectedAlert, setSelectedAlert] = useState<Alert | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [toast, setToast] = useState<{ message: string; type: 'success' | 'error' | 'info' } | null>(null);
  const [riskFilter, setRiskFilter] = useState<string>('ALL');
  const [searchTerm, setSearchTerm] = useState<string>('');

  // Fonction pour afficher une notification
  const showToast = (message: string, type: 'success' | 'error' | 'info') => {
    setToast({ message, type });
  };

  // Fonction pour marquer une alerte comme lue
  const markAsRead = async (alertId: string) => {
    try {
      const response = await fetch(`/api/v1/alerts/${alertId}/mark-read`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      
      if (!response.ok) {
        throw new Error('Erreur lors du marquage');
      }
      
      const result = await response.json();
      showToast(result.message, 'success');
      
      // Rafraîchir les alertes pour mettre à jour l'état
      const alertsResponse = await fetch('/api/v1/alerts');
      if (alertsResponse.ok) {
        const data = await alertsResponse.json();
        setAlerts(data.alerts || []);
      }
    } catch (error) {
      showToast('Erreur lors du marquage', 'error');
    }
  };

  // Fonction pour déclencher une remédiation
  const triggerRemediation = async (alert: Alert) => {
    try {
      showToast(`Remédiation en cours pour ${alert.user}...`, 'info');
      
      const response = await fetch(`/api/v1/alerts/${alert.id}/remediate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      
      if (!response.ok) {
        throw new Error('Erreur lors de la remédiation');
      }
      
      const result = await response.json();
      showToast(result.message, 'success');
      
      // Afficher les actions prises dans une notification plus détaillée
      if (result.actions_taken && result.actions_taken.length > 0) {
        setTimeout(() => {
          showToast(`Actions: ${result.actions_taken.join(', ')}`, 'info');
        }, 1000);
      }
    } catch (error) {
      showToast('Erreur lors de la remédiation', 'error');
    }
  };

  // Fonction pour ouvrir le modal de détails
  const openAlertDetails = (alert: Alert) => {
    setSelectedAlert(alert);
    setIsModalOpen(true);
  };

  // Filtrage des alertes
  useEffect(() => {
    let filtered = alerts;

    // Filtre par niveau de risque
    if (riskFilter !== 'ALL') {
      filtered = filtered.filter(alert => alert.risk_level === riskFilter);
    }

    // Filtre par recherche
    if (searchTerm) {
      filtered = filtered.filter(alert => 
        alert.user.toLowerCase().includes(searchTerm.toLowerCase()) ||
        alert.justification.toLowerCase().includes(searchTerm.toLowerCase()) ||
        alert.source.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    setFilteredAlerts(filtered);
  }, [alerts, riskFilter, searchTerm]);

  // Récupération des alertes
  useEffect(() => {
    const fetchAlerts = async () => {
      try {
        const response = await fetch('/api/v1/alerts');
        if (!response.ok) {
          throw new Error('Failed to fetch alerts');
        }
        const data = await response.json();
        setAlerts(data.alerts || []);
        setError(null);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchAlerts();
    const interval = setInterval(fetchAlerts, 5000);

    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return <div className="loading">Chargement des alertes...</div>;
  }

  return (
    <div className="alerts-dashboard">
      <h1>🛡️ Orion - Tableau de Bord des Alertes en Temps Réel</h1>
      
      {error && (
        <div className="error-message">
          <p style={{ color: 'red' }}>Erreur: {error}</p>
        </div>
      )}

      {/* Statistiques */}
      <div className="stats">
        <div className="stat-card">
          <h3>Total Alertes</h3>
          <p>{alerts.length}</p>
        </div>
        <div className="stat-card">
          <h3>Critiques</h3>
          <p>{alerts.filter(a => a.risk_level === 'CRITICAL').length}</p>
        </div>
        <div className="stat-card">
          <h3>Élevées</h3>
          <p>{alerts.filter(a => a.risk_level === 'HIGH').length}</p>
        </div>
        <div className="stat-card">
          <h3>Affichées</h3>
          <p>{filteredAlerts.length}</p>
        </div>
      </div>

      {/* Filtres et recherche */}
      <div className="filters-section">
        <div className="filter-group">
          <label>Niveau de Risque:</label>
          <select 
            value={riskFilter} 
            onChange={(e) => setRiskFilter(e.target.value)}
            className="filter-select"
          >
            <option value="ALL">Tous</option>
            <option value="CRITICAL">Critique</option>
            <option value="HIGH">Élevé</option>
            <option value="MEDIUM">Moyen</option>
            <option value="LOW">Faible</option>
          </select>
        </div>
        <div className="filter-group">
          <label>Recherche:</label>
          <input
            type="text"
            placeholder="Utilisateur, justification..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="search-input"
          />
        </div>
      </div>

      {/* Tableau des alertes */}
      <div className="alerts-table">
        <table>
          <thead>
            <tr>
              <th>Timestamp</th>
              <th>Source</th>
              <th>Utilisateur</th>
              <th>Niveau de Risque</th>
              <th>Justification</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {filteredAlerts.length === 0 ? (
              <tr>
                <td colSpan={6} style={{ textAlign: 'center', padding: '20px' }}>
                  Aucune alerte trouvée
                </td>
              </tr>
            ) : (
              filteredAlerts.map((alert) => (
                <tr key={alert.id} className={`alert-row ${alert.risk_level.toLowerCase()}`}>
                  <td>{new Date(alert.timestamp).toLocaleString('fr-FR')}</td>
                  <td>
                    <span className="source-icon">{getSourceIcon(alert.source)}</span>
                    {alert.source}
                  </td>
                  <td>{alert.user}</td>
                  <td>
                    <span 
                      className="risk-badge"
                      style={{ backgroundColor: getRiskLevelColor(alert.risk_level) }}
                    >
                      {alert.risk_level}
                    </span>
                  </td>
                  <td>{alert.justification}</td>
                  <td className="actions-cell">
                    <button 
                      className="btn btn-info btn-sm"
                      onClick={() => openAlertDetails(alert)}
                      title="Voir détails"
                    >
                      👁️
                    </button>
                    <button 
                      className="btn btn-success btn-sm"
                      onClick={() => markAsRead(alert.id)}
                      title="Marquer comme lu"
                    >
                      ✓
                    </button>
                    {alert.risk_level === 'HIGH' || alert.risk_level === 'CRITICAL' ? (
                      <button 
                        className="btn btn-warning btn-sm"
                        onClick={() => triggerRemediation(alert)}
                        title="Déclencher remédiation"
                      >
                        🛡️
                      </button>
                    ) : null}
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Modal de détails */}
      <AlertModal 
        alert={selectedAlert}
        isOpen={isModalOpen}
        onClose={() => {
          setIsModalOpen(false);
          setSelectedAlert(null);
        }}
      />

      {/* Toast notifications */}
      {toast && (
        <Toast
          message={toast.message}
          type={toast.type}
          onClose={() => setToast(null)}
        />
      )}
    </div>
  );
};

export default AlertsDashboard; 