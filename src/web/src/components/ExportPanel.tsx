import React, { useState } from 'react';
import { Alert } from '../types';
import { exportAlerts } from '../api';

interface ExportPanelProps {
  alerts: Alert[];
  apiKey: string;
}

const ExportPanel: React.FC<ExportPanelProps> = ({ alerts, apiKey }) => {
  const [exportFormat, setExportFormat] = useState<'json' | 'csv'>('json');
  const [severityFilter, setSeverityFilter] = useState<string>('');
  const [exporting, setExporting] = useState(false);
  const [exportResult, setExportResult] = useState<string | null>(null);

  const handleExport = async () => {
    try {
      setExporting(true);
      setExportResult(null);

      const result = await exportAlerts(apiKey, exportFormat, severityFilter || undefined);
      
      if (exportFormat === 'csv') {
        // Télécharger le fichier CSV
        const blob = new Blob([result.content], { type: 'text/csv' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = result.filename;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        
        setExportResult('Fichier CSV téléchargé avec succès !');
      } else {
        // Afficher le JSON
        setExportResult(result.content);
      }
    } catch (error) {
      setExportResult(`Erreur lors de l'export: ${error instanceof Error ? error.message : 'Erreur inconnue'}`);
    } finally {
      setExporting(false);
    }
  };

  const downloadJson = () => {
    if (exportResult) {
      const blob = new Blob([exportResult], { type: 'application/json' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `alerts_export_${Date.now()}.json`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    }
  };

  return (
    <div className="space-y-6">
      {/* Configuration de l'export */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">
          📤 Export des données
        </h2>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Format d'export
            </label>
            <select
              value={exportFormat}
              onChange={(e) => setExportFormat(e.target.value as 'json' | 'csv')}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="json">JSON</option>
              <option value="csv">CSV</option>
            </select>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Filtre par sévérité
            </label>
            <select
              value={severityFilter}
              onChange={(e) => setSeverityFilter(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Toutes les sévérités</option>
              <option value="critical">Critique</option>
              <option value="high">Élevée</option>
              <option value="medium">Moyenne</option>
              <option value="low">Faible</option>
            </select>
          </div>
          
          <div className="flex items-end">
            <button
              onClick={handleExport}
              disabled={exporting}
              className="w-full bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {exporting ? 'Export en cours...' : '📤 Exporter'}
            </button>
          </div>
        </div>
        
        <div className="text-sm text-gray-600">
          <p>📊 Total des alertes disponibles: <strong>{alerts.length}</strong></p>
          {severityFilter && (
            <p>🔍 Filtre actif: <strong>{severityFilter}</strong></p>
          )}
        </div>
      </div>

      {/* Résultat de l'export */}
      {exportResult && (
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            📋 Résultat de l'export
          </h3>
          
          {exportFormat === 'json' && exportResult.startsWith('{') ? (
            <div>
              <div className="flex justify-between items-center mb-4">
                <span className="text-sm text-gray-600">
                  Données JSON exportées ({exportResult.length} caractères)
                </span>
                <button
                  onClick={downloadJson}
                  className="bg-green-600 text-white px-3 py-1 rounded text-sm hover:bg-green-700"
                >
                  💾 Télécharger JSON
                </button>
              </div>
              <pre className="bg-gray-50 p-4 rounded-lg overflow-x-auto text-sm">
                {JSON.stringify(JSON.parse(exportResult), null, 2)}
              </pre>
            </div>
          ) : (
            <div className="text-center py-4">
              <div className="text-green-600 text-2xl mb-2">✅</div>
              <p className="text-gray-700">{exportResult}</p>
            </div>
          )}
        </div>
      )}

      {/* Statistiques d'export */}
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          📈 Statistiques d'export
        </h3>
        
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="text-center p-4 bg-blue-50 rounded-lg">
            <div className="text-2xl font-bold text-blue-600">{alerts.length}</div>
            <div className="text-sm text-blue-600">Total alertes</div>
          </div>
          
          <div className="text-center p-4 bg-green-50 rounded-lg">
            <div className="text-2xl font-bold text-green-600">
              {alerts.filter(a => !a.read).length}
            </div>
            <div className="text-sm text-green-600">Non lues</div>
          </div>
          
          <div className="text-center p-4 bg-yellow-50 rounded-lg">
            <div className="text-2xl font-bold text-yellow-600">
              {alerts.filter(a => a.remediated).length}
            </div>
            <div className="text-sm text-yellow-600">Remédiées</div>
          </div>
          
          <div className="text-center p-4 bg-purple-50 rounded-lg">
            <div className="text-2xl font-bold text-purple-600">
              {new Set(alerts.map(a => a.user)).size}
            </div>
            <div className="text-sm text-purple-600">Utilisateurs uniques</div>
          </div>
        </div>
      </div>

      {/* Aperçu des données */}
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          👀 Aperçu des données à exporter
        </h3>
        
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  ID
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Sévérité
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Titre
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Utilisateur
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  IP Source
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Statut
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {alerts.slice(0, 10).map((alert) => (
                <tr key={alert.alert_id}>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    {alert.alert_id}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                      alert.severity === 'critical' ? 'bg-red-100 text-red-800' :
                      alert.severity === 'high' ? 'bg-orange-100 text-orange-800' :
                      alert.severity === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                      'bg-green-100 text-green-800'
                    }`}>
                      {alert.severity}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-900 truncate max-w-xs">
                    {alert.title}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {alert.user}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {alert.source_ip}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                      alert.status === 'new' ? 'bg-blue-100 text-blue-800' :
                      alert.status === 'read' ? 'bg-gray-100 text-gray-800' :
                      'bg-green-100 text-green-800'
                    }`}>
                      {alert.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        
        {alerts.length > 10 && (
          <div className="mt-4 text-center text-sm text-gray-500">
            Affichage des 10 premières alertes sur {alerts.length} au total
          </div>
        )}
      </div>
    </div>
  );
};

export default ExportPanel; 