import React from 'react';
import { Statistics } from '../types';

interface StatisticsPanelProps {
  statistics: Statistics | null;
  loading: boolean;
}

const StatisticsPanel: React.FC<StatisticsPanelProps> = ({ statistics, loading }) => {
  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (!statistics) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500">Aucune statistique disponible</p>
      </div>
    );
  }

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical': return 'bg-red-500';
      case 'high': return 'bg-orange-500';
      case 'medium': return 'bg-yellow-500';
      case 'low': return 'bg-green-500';
      default: return 'bg-gray-500';
    }
  };

  const formatTimestamp = (timestamp: number) => {
    return new Date(timestamp * 1000).toLocaleString('fr-FR');
  };

  return (
    <div className="space-y-6">
      {/* En-tête des statistiques */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">
          📊 Vue d'ensemble du système
        </h2>
        
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="bg-blue-50 p-4 rounded-lg">
            <div className="text-2xl font-bold text-blue-600">
              {statistics.total_alerts}
            </div>
            <div className="text-sm text-blue-600">Total des alertes</div>
          </div>
          
          <div className="bg-green-50 p-4 rounded-lg">
            <div className="text-2xl font-bold text-green-600">
              {statistics.recent_activity.length}
            </div>
            <div className="text-sm text-green-600">Activité récente (24h)</div>
          </div>
          
          <div className="bg-yellow-50 p-4 rounded-lg">
            <div className="text-2xl font-bold text-yellow-600">
              {Object.keys(statistics.alerts_by_type).length}
            </div>
            <div className="text-sm text-yellow-600">Types d'événements</div>
          </div>
          
          <div className="bg-purple-50 p-4 rounded-lg">
            <div className="text-2xl font-bold text-purple-600">
              {statistics.top_users.length}
            </div>
            <div className="text-sm text-purple-600">Utilisateurs actifs</div>
          </div>
        </div>
      </div>

      {/* Alertes par sévérité */}
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          🚨 Répartition par niveau de risque
        </h3>
        
        <div className="space-y-3">
          {Object.entries(statistics.alerts_by_severity).map(([severity, count]) => (
            <div key={severity} className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <div className={`w-4 h-4 rounded-full ${getSeverityColor(severity)}`}></div>
                <span className="capitalize font-medium">{severity}</span>
              </div>
              <div className="flex items-center space-x-2">
                <div className="w-32 bg-gray-200 rounded-full h-2">
                  <div
                    className={`h-2 rounded-full ${getSeverityColor(severity)}`}
                    style={{
                      width: `${(count / statistics.total_alerts) * 100}%`
                    }}
                  ></div>
                </div>
                <span className="text-sm font-medium text-gray-600 w-8 text-right">
                  {count}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Types d'événements */}
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          📋 Types d'événements détectés
        </h3>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {Object.entries(statistics.alerts_by_type).map(([eventType, count]) => (
            <div key={eventType} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <span className="font-medium text-gray-700">{eventType}</span>
              <span className="text-sm font-bold text-gray-900">{count}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Top utilisateurs */}
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          👥 Utilisateurs les plus actifs
        </h3>
        
        <div className="space-y-2">
          {statistics.top_users.slice(0, 10).map((user, index) => (
            <div key={user.user} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <div className="flex items-center space-x-3">
                <span className="text-sm font-medium text-gray-500">#{index + 1}</span>
                <span className="font-medium text-gray-700">{user.user}</span>
              </div>
              <span className="text-sm font-bold text-gray-900">{user.count} alertes</span>
            </div>
          ))}
        </div>
      </div>

      {/* Top IPs */}
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          🌐 Adresses IP les plus actives
        </h3>
        
        <div className="space-y-2">
          {statistics.top_ips.slice(0, 10).map((ip, index) => (
            <div key={ip.ip} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <div className="flex items-center space-x-3">
                <span className="text-sm font-medium text-gray-500">#{index + 1}</span>
                <span className="font-mono text-sm font-medium text-gray-700">{ip.ip}</span>
              </div>
              <span className="text-sm font-bold text-gray-900">{ip.count} événements</span>
            </div>
          ))}
        </div>
      </div>

      {/* Activité récente */}
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          ⏰ Activité récente (24 dernières heures)
        </h3>
        
        <div className="space-y-2 max-h-64 overflow-y-auto">
          {statistics.recent_activity.slice(0, 20).map((activity) => (
            <div key={activity.alert_id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <div className="flex items-center space-x-3">
                <div className={`w-3 h-3 rounded-full ${getSeverityColor(activity.severity)}`}></div>
                <div>
                  <div className="font-medium text-gray-700">{activity.title}</div>
                  <div className="text-sm text-gray-500">{activity.user} • {activity.source_ip}</div>
                </div>
              </div>
              <div className="text-sm text-gray-500">
                {formatTimestamp(activity.timestamp)}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default StatisticsPanel; 