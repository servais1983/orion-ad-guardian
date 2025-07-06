import React from 'react';
import { Alert } from '../types';

interface AlertListProps {
  alerts: Alert[];
  onAlertAction: (alertId: string, action: "mark-read" | "remediate") => Promise<void>;
  filters: {
    severity: string;
    status: string;
    limit: number;
  };
  onFilterChange: (newFilters: { severity: string; status: string; limit: number }) => void;
  loading: boolean;
}

const AlertList: React.FC<AlertListProps> = ({
  alerts,
  onAlertAction,
  filters,
  onFilterChange,
  loading
}) => {
  const getSeverityColor = (severity: string) => {
    switch (severity.toLowerCase()) {
      case 'critical':
        return 'bg-red-100 text-red-800 border-red-200';
      case 'high':
        return 'bg-orange-100 text-orange-800 border-orange-200';
      case 'medium':
        return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'low':
        return 'bg-green-100 text-green-800 border-green-200';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const getSeverityBadgeColor = (severity: string) => {
    switch (severity.toLowerCase()) {
      case 'critical':
        return 'bg-red-500';
      case 'high':
        return 'bg-orange-500';
      case 'medium':
        return 'bg-yellow-500';
      case 'low':
        return 'bg-green-500';
      default:
        return 'bg-gray-500';
    }
  };

  const formatTimestamp = (timestamp: number) => {
    return new Date(timestamp).toLocaleString('fr-FR', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    });
  };

  // Filtrer les alertes selon les filtres appliqués
  const filteredAlerts = alerts.filter(alert => {
    if (filters.severity && alert.severity.toLowerCase() !== filters.severity.toLowerCase()) {
      return false;
    }
    if (filters.status && alert.status.toLowerCase() !== filters.status.toLowerCase()) {
      return false;
    }
    return true;
  }).slice(0, filters.limit);

  if (loading) {
    return (
      <div className="text-center py-8">
        <div className="text-gray-500 text-lg">Chargement des alertes...</div>
      </div>
    );
  }

  if (filteredAlerts.length === 0) {
    return (
      <div className="text-center py-8">
        <div className="text-gray-500 text-lg">
          {filters.severity 
            ? `Aucune alerte de niveau "${filters.severity}" trouvée`
            : 'Aucune alerte trouvée'
          }
        </div>
        <div className="text-gray-400 text-sm mt-2">
          Les nouvelles alertes apparaîtront ici automatiquement
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {filteredAlerts.map((alert) => (
        <div
          key={alert.alert_id}
          className={`border rounded-lg p-4 transition-all duration-200 hover:shadow-md ${
            alert.read ? 'opacity-75' : ''
          } ${getSeverityColor(alert.severity)}`}
        >
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <div className="flex items-center space-x-3 mb-2">
                <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium text-white ${getSeverityBadgeColor(alert.severity)}`}>
                  {alert.severity.toUpperCase()}
                </span>
                {alert.read && (
                  <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                    LUE
                  </span>
                )}
                <span className="text-sm text-gray-500">
                  {formatTimestamp(alert.timestamp)}
                </span>
              </div>
              
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                {alert.title}
              </h3>
              
              <p className="text-gray-700 mb-3">
                {alert.description}
              </p>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                <div>
                  <span className="font-medium text-gray-600">Utilisateur:</span>
                  <span className="ml-2 text-gray-900">{alert.user}</span>
                </div>
                <div>
                  <span className="font-medium text-gray-600">IP Source:</span>
                  <span className="ml-2 text-gray-900">{alert.source_ip}</span>
                </div>
                <div>
                  <span className="font-medium text-gray-600">Statut:</span>
                  <span className="ml-2 text-gray-900">{alert.status}</span>
                </div>
                <div>
                  <span className="font-medium text-gray-600">Remédié:</span>
                  <span className="ml-2 text-gray-900">{alert.remediated ? 'Oui' : 'Non'}</span>
                </div>
              </div>
            </div>
          </div>
          
          <div className="flex items-center justify-between mt-4 pt-4 border-t border-gray-200">
            <div className="flex space-x-2">
              {!alert.read && (
                <button
                  onClick={() => onAlertAction(alert.alert_id, "mark-read")}
                  className="inline-flex items-center px-3 py-1.5 border border-transparent text-xs font-medium rounded-md text-green-700 bg-green-100 hover:bg-green-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 transition-colors"
                >
                  <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  Marquer comme lue
                </button>
              )}
            </div>
            
            <button
              onClick={() => onAlertAction(alert.alert_id, "remediate")}
              className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 transition-colors"
            >
              <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
              </svg>
              Remédier
            </button>
          </div>
        </div>
      ))}
    </div>
  );
};

export default AlertList; 