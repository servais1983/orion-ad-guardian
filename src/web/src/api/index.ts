import { Alert, Statistics } from '../types';

export const fetchAlerts = async (
  apiKey: string,
  filters: {
    severity?: string;
    status?: string;
    limit?: number;
  } = {}
): Promise<{ alerts: Alert[]; total: number }> => {
  const params = new URLSearchParams();
  if (filters.severity) params.append('severity', filters.severity);
  if (filters.status) params.append('status', filters.status);
  if (filters.limit) params.append('limit', filters.limit.toString());

  const response = await fetch(`/api/v1/alerts?${params}`, {
    headers: {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    throw new Error(`Erreur HTTP: ${response.status}`);
  }

  return response.json();
};

export const fetchStatistics = async (apiKey: string): Promise<Statistics> => {
  const response = await fetch('/api/v1/statistics', {
    headers: {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    throw new Error(`Erreur HTTP: ${response.status}`);
  }

  return response.json();
};

export const fetchConfig = async (apiKey: string): Promise<any> => {
  const response = await fetch('/api/v1/config', {
    headers: {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    throw new Error(`Erreur HTTP: ${response.status}`);
  }

  return response.json();
};

export const exportAlerts = async (
  apiKey: string,
  format: 'json' | 'csv' = 'json',
  severity?: string
): Promise<{ content: string; content_type: string; filename: string }> => {
  const params = new URLSearchParams();
  params.append('format', format);
  if (severity) params.append('severity', severity);

  const response = await fetch(`/api/v1/export/alerts?${params}`, {
    headers: {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    throw new Error(`Erreur HTTP: ${response.status}`);
  }

  return response.json();
}; 