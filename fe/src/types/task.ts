export interface Task {
  id: string;
  projectId: string;
  title: string;
  completed: boolean;
  flagged?: boolean;
  tags?: string[];
  dueDate?: string;  // YYYY-MM-DD
  children?: Task[];
}