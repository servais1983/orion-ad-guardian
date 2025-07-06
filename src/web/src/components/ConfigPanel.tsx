import React from 'react';

interface ConfigPanelProps {
  config: any;
  loading: boolean;
}

const ConfigPanel: React.FC<ConfigPanelProps> = ({ config, loading }) => {
  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (!config) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500">Configuration non disponible</p>
      </div>
    );
  }

  const getStatusColor = (value: boolean) => {
    return value ? 'text-green-600' : 'text-red-600';
  };

  const getStatusIcon = (value: boolean) => {
    return value ? '✅' : '❌';
  };

  return (
    <div className="space-y-6">
      {/* Configuration générale */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">
          ⚙️ Configuration du système
        </h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h3 className="text-lg font-medium text-gray-900 mb-3">Informations générales</h3>
            <div className="space-y-3">
              <div className="flex justify-between items-center">
                <span className="text-gray-600">Version:</span>
                <span className="font-medium">{config.version}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-600">Mode production:</span>
                <span className={`font-medium ${getStatusColor(config.production_mode)}`}>
                  {getStatusIcon(config.production_mode)} {config.production_mode ? 'Activé' : 'Désactivé'}
                </span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-600">Max alertes:</span>
                <span className="font-medium">{config.max_alerts?.toLocaleString()}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-600">Rétention (jours):</span>
                <span className="font-medium">{config.alert_retention_days}</span>
              </div>
            </div>
          </div>
          
          <div>
            <h3 className="text-lg font-medium text-gray-900 mb-3">Origines autorisées</h3>
            <div className="space-y-2">
              {config.allowed_origins?.map((origin: string, index: number) => (
                <div key={index} className="flex items-center space-x-2">
                  <span className="text-green-500">🌐</span>
                  <span className="font-mono text-sm bg-gray-100 px-2 py-1 rounded">
                    {origin}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Statut des services */}
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          🔧 Statut des services
        </h3>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="p-4 bg-green-50 rounded-lg">
            <div className="flex items-center space-x-2">
              <span className="text-2xl">🟢</span>
              <div>
                <div className="font-medium text-green-800">API Backend</div>
                <div className="text-sm text-green-600">Opérationnel</div>
              </div>
            </div>
          </div>
          
          <div className="p-4 bg-green-50 rounded-lg">
            <div className="flex items-center space-x-2">
              <span className="text-2xl">🟢</span>
              <div>
                <div className="font-medium text-green-800">Interface Web</div>
                <div className="text-sm text-green-600">Opérationnel</div>
              </div>
            </div>
          </div>
          
          <div className="p-4 bg-green-50 rounded-lg">
            <div className="flex items-center space-x-2">
              <span className="text-2xl">🟢</span>
              <div>
                <div className="font-medium text-green-800">Agent AD</div>
                <div className="text-sm text-green-600">Opérationnel</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Recommandations de sécurité */}
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          🔒 Recommandations de sécurité
        </h3>
        
        <div className="space-y-4">
          {!config.production_mode && (
            <div className="p-4 bg-yellow-50 border-l-4 border-yellow-400">
              <div className="flex">
                <div className="flex-shrink-0">
                  <span className="text-yellow-400 text-xl">⚠️</span>
                </div>
                <div className="ml-3">
                  <h4 className="text-sm font-medium text-yellow-800">
                    Mode développement détecté
                  </h4>
                  <p className="text-sm text-yellow-700 mt-1">
                    Pour la production, activez PRODUCTION_MODE=true et changez l'API_KEY par défaut.
                  </p>
                </div>
              </div>
            </div>
          )}
          
          <div className="p-4 bg-blue-50 border-l-4 border-blue-400">
            <div className="flex">
              <div className="flex-shrink-0">
                <span className="text-blue-400 text-xl">💡</span>
              </div>
              <div className="ml-3">
                <h4 className="text-sm font-medium text-blue-800">
                  Configuration recommandée
                </h4>
                <ul className="text-sm text-blue-700 mt-1 space-y-1">
                  <li>• Utilisez HTTPS en production</li>
                  <li>• Configurez une base de données PostgreSQL</li>
                  <li>• Activez les notifications par email/Slack</li>
                  <li>• Configurez la rotation des logs</li>
                </ul>
              </div>
            </div>
          </div>
          
          <div className="p-4 bg-green-50 border-l-4 border-green-400">
            <div className="flex">
              <div className="flex-shrink-0">
                <span className="text-green-400 text-xl">✅</span>
              </div>
              <div className="ml-3">
                <h4 className="text-sm font-medium text-green-800">
                  Bonnes pratiques appliquées
                </h4>
                <ul className="text-sm text-green-700 mt-1 space-y-1">
                  <li>• Authentification par token API</li>
                  <li>• CORS configuré</li>
                  <li>• Logging structuré</li>
                  <li>• Gestion des erreurs</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Informations techniques */}
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          🔧 Informations techniques
        </h3>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h4 className="font-medium text-gray-900 mb-2">Backend</h4>
            <div className="space-y-1 text-sm text-gray-600">
              <div>Framework: FastAPI</div>
              <div>Langage: Python 3.8+</div>
              <div>Port: 8006</div>
              <div>Workers: {config.production_mode ? '4' : '1'}</div>
            </div>
          </div>
          
          <div>
            <h4 className="font-medium text-gray-900 mb-2">Frontend</h4>
            <div className="space-y-1 text-sm text-gray-600">
              <div>Framework: React 18</div>
              <div>Langage: TypeScript</div>
              <div>Styling: Tailwind CSS</div>
              <div>Port: 3180</div>
            </div>
          </div>
        </div>
      </div>

      {/* Actions de configuration */}
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          🛠️ Actions de configuration
        </h3>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <button className="p-4 border-2 border-gray-200 rounded-lg hover:border-blue-300 hover:bg-blue-50 transition-colors">
            <div className="text-center">
              <div className="text-2xl mb-2">📝</div>
              <div className="font-medium text-gray-900">Modifier la config</div>
              <div className="text-sm text-gray-500">Éditer le fichier .env</div>
            </div>
          </button>
          
          <button className="p-4 border-2 border-gray-200 rounded-lg hover:border-green-300 hover:bg-green-50 transition-colors">
            <div className="text-center">
              <div className="text-2xl mb-2">🔄</div>
              <div className="font-medium text-gray-900">Redémarrer</div>
              <div className="text-sm text-gray-500">Relancer les services</div>
            </div>
          </button>
          
          <button className="p-4 border-2 border-gray-200 rounded-lg hover:border-purple-300 hover:bg-purple-50 transition-colors">
            <div className="text-center">
              <div className="text-2xl mb-2">📊</div>
              <div className="font-medium text-gray-900">Monitoring</div>
              <div className="text-sm text-gray-500">Voir les métriques</div>
            </div>
          </button>
        </div>
      </div>
    </div>
  );
};

export default ConfigPanel; 