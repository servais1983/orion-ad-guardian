export interface Alert {
  alert_id: string;
  event_id: string;
  severity: string;
  title: string;
  description: string;
  timestamp: number;
  source_ip: string;
  user: string;
  status: string;
  read: boolean;
  remediated: boolean;
  remediation_actions: string[];
}

export interface AlertAction {
  action: string;
  timestamp: number;
  user: string;
  details: Record<string, any>;
}

export interface Statistics {
  total_alerts: number;
  alerts_by_severity: Record<string, number>;
  alerts_by_type: Record<string, number>;
  recent_activity: Array<{
    alert_id: string;
    severity: string;
    title: string;
    user: string;
    source_ip: string;
    timestamp: number;
  }>;
  top_users: Array<{
    user: string;
    count: number;
  }>;
  top_ips: Array<{
    ip: string;
    count: number;
  }>;
}

export interface ADEvent {
  event_id: string;
  event_type: string;
  timestamp: number;
  source_ip: string;
  user: string;
  details: Record<string, any>;
} 