import type { Project } from "../types/project";
import type { Task } from "../types/task";

const API_BASE = "/api/v1";

// 프로젝트
export async function fetchProjects(): Promise<Project[]> {
  const res = await fetch(`${API_BASE}/projects/`);
  if (!res.ok) throw new Error("Failed to fetch projects");
  return res.json();
}

export async function createProject(data: Partial<Project>): Promise<Project> {
  const res = await fetch(`${API_BASE}/projects/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error("Failed to create project");
  return res.json();
}

export async function updateProject(id: string, data: Partial<Project>): Promise<Project> {
  const res = await fetch(`${API_BASE}/projects/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error("Failed to update project");
  return res.json();
}

export async function deleteProject(id: string): Promise<void> {
  const res = await fetch(`${API_BASE}/projects/${id}`, {
    method: "DELETE",
  });
  if (!res.ok) throw new Error("Failed to delete project");
}

// 할 일(Task)
export async function fetchItems(project_id: string): Promise<Task[]> {
  const res = await fetch(`${API_BASE}/projects/${project_id}/items/`);
  if (!res.ok) throw new Error("Failed to fetch items");
  return res.json();
}

export async function createItem(project_id: string, data: Partial<Task>): Promise<Task> {
  const res = await fetch(`${API_BASE}/projects/${project_id}/items/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error("Failed to create task");
  return res.json();
}

export async function updateItem(project_id: string, id: string, data: Partial<Task>): Promise<Task> {
  const res = await fetch(`${API_BASE}/projects/${project_id}/items/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error("Failed to update task");
  return res.json();
}

export async function deleteItem(project_id: string, id: string): Promise<void> {
  const res = await fetch(`${API_BASE}/projects/${project_id}/items/${id}`, {
    method: "DELETE",
  });
  if (!res.ok) throw new Error("Failed to delete task");
}
