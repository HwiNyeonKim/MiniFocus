export interface Task {
  id: string;
  project_id: string;
  title: string;
  completed: boolean;
  flagged?: boolean;
  tags?: string[];
  due_date?: string;  // YYYY-MM-DD
  parent_id?: string;
}