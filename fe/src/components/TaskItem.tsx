import React, { useState } from "react";
import type { Task } from "../types/task";

interface Props {
  task: Task;
  onToggleComplete: (id: string) => void;
  onDelete: (id: string) => void;
  onEdit: (id: string, title: string) => void;
}

export default function TaskItem({ task, onToggleComplete, onDelete, onEdit }: Props) {
  const [editing, setEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(task.title);

  const handleEdit = () => {
    if (editTitle.trim() && editTitle !== task.title) {
      onEdit(task.id, editTitle.trim());
    }
    setEditing(false);
  };

  return (
    <li className="p-2 border-b flex items-center gap-2 group">
      <input
        type="checkbox"
        checked={task.completed}
        onChange={() => onToggleComplete(task.id)}
        className="mr-2"
      />
      {editing ? (
        <input
          className="border rounded px-1 py-0.5"
          value={editTitle}
          onChange={e => setEditTitle(e.target.value)}
          onBlur={handleEdit}
          onKeyDown={e => e.key === "Enter" && handleEdit()}
          autoFocus
        />
      ) : (
        <span
          className={task.completed ? "line-through text-gray-400" : ""}
          onDoubleClick={() => setEditing(true)}
        >
          {task.title}
        </span>
      )}
      {task.flagged && (
        <span title="Flagged" className="ml-2 text-orange-500">⚑</span>
      )}
      {task.tags && task.tags.map(tag => (
        <span key={tag} className="ml-1 px-2 py-0.5 bg-gray-200 rounded text-xs">{tag}</span>
      ))}
      {task.dueDate && (
        <span className="ml-2 text-xs text-gray-500">
          {new Date(task.dueDate).toLocaleDateString()}
        </span>
      )}
      <button
        className="ml-auto text-red-400 opacity-0 group-hover:opacity-100"
        onClick={() => onDelete(task.id)}
        title="Delete"
      >
        ×
      </button>
    </li>
  );
}
