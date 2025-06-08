import { useState } from "react";
import type { Project } from "../types/project";

interface TreeProject extends Project {
    children?: TreeProject[];
}

interface Props {
    projects: TreeProject[];
    onSelect: (projectId: string) => void;
    selectedId: string;
    onAdd: (parentId: string | null) => void;
    onDelete: (id: string) => void;
    onEdit: (id: string, name: string) => void;
}

function ProjectNode({
    project,
    onSelect,
    selectedId,
    onAdd,
    onDelete,
    onEdit,
    level = 0,
}: {
    project: TreeProject;
    onSelect: (id: string) => void;
    selectedId: string;
    onAdd: (parentId: string) => void;
    onDelete: (id: string) => void;
    onEdit: (id: string, name: string) => void;
    level?: number;
}) {
    const isSelected = selectedId === project.id;
    const [editing, setEditing] = useState(false);
    const [editName, setEditName] = useState(project.name);

    const handleEdit = () => {
        if (editName.trim() && editName !== project.name) {
            onEdit(project.id, editName.trim());
        }
        setEditing(false);
    };

    return (
        <li>
            <div
                className={`flex items-center cursor-pointer p-1 rounded ${isSelected ? "bg-blue-200" : ""}`}
                style={{ marginLeft: level * 16 }}
                onClick={() => onSelect(project.id)}
            >
                {editing ? (
                    <input
                        className="border rounded px-1 py-0.5"
                        value={editName}
                        onChange={e => setEditName(e.target.value)}
                        onBlur={handleEdit}
                        onKeyDown={e => e.key === "Enter" && handleEdit()}
                        autoFocus
                        onClick={e => e.stopPropagation()}
                    />
                ) : (
                    <span
                        onDoubleClick={e => {
                            e.stopPropagation();
                            setEditing(true);
                        }}
                    >
                        {project.name}
                    </span>
                )}
                <button
                    className="ml-3 px-2 py-1 text-sm text-green-700 bg-green-100 rounded hover:bg-green-200"
                    onClick={e => {
                        e.stopPropagation();
                        onAdd(project.id);
                    }}
                    title="Add subproject"
                >
                    +
                </button>
                <button
                    className="ml-2 px-2 py-1 text-sm text-red-700 bg-red-100 rounded hover:bg-red-200"
                    onClick={e => {
                        e.stopPropagation();
                        if (window.confirm("정말로 이 프로젝트를 삭제하시겠습니까?")) {
                            onDelete(project.id);
                        }
                    }}
                    title="Delete"
                >
                    ×
                </button>
            </div>
            {project.children && project.children.length > 0 && (
                <ul>
                    {project.children.map(child => (
                        <ProjectNode
                            key={child.id}
                            project={child}
                            onSelect={onSelect}
                            selectedId={selectedId}
                            onAdd={onAdd}
                            onDelete={onDelete}
                            onEdit={onEdit}
                            level={level + 1}
                        />
                    ))}
                </ul>
            )}
        </li>
    );
}

export default function ProjectTree({ projects, onSelect, selectedId, onAdd, onDelete, onEdit }: Props) {
    return (
        <div className="w-64 bg-gray-100 h-full p-2">
            <div className="font-bold mb-2">Projects</div>
            <ul>
                {projects.map((p) => (
                    <ProjectNode
                        key={p.id}
                        project={p}
                        onSelect={onSelect}
                        selectedId={selectedId}
                        onAdd={onAdd}
                        onDelete={onDelete}
                        onEdit={onEdit}
                    />
                ))}
            </ul>
        </div>
    );
}