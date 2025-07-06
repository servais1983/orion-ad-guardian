import React, { useState, useEffect } from 'react';
import { Alert, AlertAction, Statistics } from '../types';
import AlertList from './AlertList';
import StatisticsPanel from './StatisticsPanel';
import ExportPanel from './ExportPanel';
import ConfigPanel from './ConfigPanel';
import { fetchAlerts, fetchStatistics, fetchConfig } from '../api';

interface DashboardProps {
  apiKey: string;
}

const Dashboard: React.FC<DashboardProps> = ({ apiKey }) => {
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [statistics, setStatistics] = useState<Statistics | null>(null);
  const [config, setConfig] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<'alerts' | 'stats' | 'export' | 'config'>('alerts');
  const [filters, setFilters] = useState({
    severity: '',
    status: '',
    limit: 50
  });

  // Fonction de rafraîchissement des données
  const refreshData = async () => {
    try {
      setLoading(true);
      setError(null);

      // Charger les alertes
      const alertsData = await fetchAlerts(apiKey, filters);
      setAlerts(alertsData.alerts);

      // Charger les statistiques
      const statsData = await fetchStatistics(apiKey);
      setStatistics(statsData);

      // Charger la configuration
      const configData = await fetchConfig(apiKey);
      setConfig(configData);

    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erreur lors du chargement des données');
    } finally {
      setLoading(false);
    }
  };

  // Chargement initial et rafraîchissement périodique
  useEffect(() => {
    refreshData();
    
    const interval = setInterval(refreshData, 5000);
    return () => clearInterval(interval);
  }, [filters]);

  // Gestion des actions sur les alertes
  const handleAlertAction = async (alertId: string, action: 'mark-read' | 'remediate') => {
    try {
      if (action === 'mark-read') {
        await fetch(`/api/v1/alerts/${alertId}/mark-read`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${apiKey}`,
            'Content-Type': 'application/json'
          }
        });
      } else if (action === 'remediate') {
        await fetch(`/api/v1/alerts/${alertId}/remediate`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${apiKey}`,
            'Content-Type': 'application/json'
          }
        });
      }
      
      // Rafraîchir les données
      refreshData();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erreur lors de l\'action');
    }
  };

  // Gestion des filtres
  const handleFilterChange = (newFilters: typeof filters) => {
    setFilters(newFilters);
  };

  if (loading && alerts.length === 0) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Chargement des données...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="text-red-600 text-6xl mb-4">⚠️</div>
          <h2 className="text-xl font-semibold text-gray-800 mb-2">Erreur de connexion</h2>
          <p className="text-gray-600 mb-4">{error}</p>
          <button
            onClick={refreshData}
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
          >
            Réessayer
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold text-gray-900">
                🛡️ Orion AD Guardian
              </h1>
              <span className="ml-2 px-2 py-1 text-xs bg-green-100 text-green-800 rounded-full">
                v2.0.0
              </span>
            </div>
            
            <div className="flex items-center space-x-4">
              <div className="text-sm text-gray-500">
                {config?.production_mode ? (
                  <span className="text-red-600">🔴 Production</span>
                ) : (
                  <span className="text-yellow-600">🟡 Développement</span>
                )}
              </div>
              
              <button
                onClick={refreshData}
                className="bg-blue-600 text-white px-3 py-1 rounded text-sm hover:bg-blue-700"
              >
                🔄 Actualiser
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Navigation */}
      <nav className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex space-x-8">
            <button
              onClick={() => setActiveTab('alerts')}
              className={`py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'alerts'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              🚨 Alertes ({alerts.length})
            </button>
            
            <button
              onClick={() => setActiveTab('stats')}
              className={`py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'stats'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              📊 Statistiques
            </button>
            
            <button
              onClick={() => setActiveTab('export')}
              className={`py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'export'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              📤 Export
            </button>
            
            <button
              onClick={() => setActiveTab('config')}
              className={`py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'config'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              ⚙️ Configuration
            </button>
          </div>
        </div>
      </nav>

      {/* Contenu principal */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeTab === 'alerts' && (
          <AlertList
            alerts={alerts}
            onAlertAction={handleAlertAction}
            filters={filters}
            onFilterChange={handleFilterChange}
            loading={loading}
          />
        )}
        
        {activeTab === 'stats' && (
          <StatisticsPanel
            statistics={statistics}
            loading={loading}
          />
        )}
        
        {activeTab === 'export' && (
          <ExportPanel
            alerts={alerts}
            apiKey={apiKey}
          />
        )}
        
        {activeTab === 'config' && (
          <ConfigPanel
            config={config}
            loading={loading}
          />
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t mt-auto">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="text-center text-sm text-gray-500">
            Orion AD Guardian v2.0.0 - Système de surveillance Active Directory
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Dashboard; 