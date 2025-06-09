import type { Project } from "./src/types/project";

export function buildProjectTree(
  projects: Project[],
  parentId: string | null = null
): (Project & { children?: Project[] })[] {
  return projects
    .filter(p => {
      // parent_id와 parentId를 모두 string 또는 null로 변환해서 비교
      const pParentId = p.parent_id !== undefined && p.parent_id !== null ? String(p.parent_id) : null;
      const parentIdStr = parentId !== undefined && parentId !== null ? String(parentId) : null;
      return pParentId === parentIdStr;
    })
    .map(p => ({
      ...p,
      children: buildProjectTree(projects, String(p.id)),
    }));
}
