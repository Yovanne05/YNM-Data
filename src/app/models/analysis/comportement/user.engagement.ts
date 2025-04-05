export interface UserEngagement {
  total_views: number;
  avg_duration_minutes: number;
  users: {
    user_id: number;
    total_views: number;
    avg_duration_minutes: number;
  }[];
}
