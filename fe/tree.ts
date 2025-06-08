import type { Project } from "./src/types/project";

export function buildProjectTree(projects: Project[], parentId: string | null = null): (Project & { children?: Project[] })[] {
  return projects
    .filter(p => (p.parent_id ?? null) === parentId)
    .map(p => ({
      ...p,
      children: buildProjectTree(projects, p.id),
    }));
}
