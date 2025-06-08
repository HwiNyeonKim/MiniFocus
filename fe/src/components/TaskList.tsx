import React, { useState } from "react";
import type { Task } from "../types/task";
import TaskItem from "./TaskItem";

interface Props {
  tasks: Task[];
  onToggleComplete: (id: string) => void;
  onAddTask: (title: string, dueDate?: string) => void;
  onDeleteTask: (id: string) => void;
  onEditTask: (id: string, title: string) => void;
  addTaskInputRef?: React.RefObject<HTMLInputElement | null>;
}

export default function TaskList({
  tasks,
  onToggleComplete,
  onAddTask,
  onDeleteTask,
  onEditTask,
  addTaskInputRef,
}: Props) {
  const [newTitle, setNewTitle] = useState("");
  const [newDueDate, setNewDueDate] = useState("");

  const handleAdd = () => {
    if (newTitle.trim()) {
      onAddTask(newTitle.trim(), newDueDate || undefined);
      setNewTitle("");
      setNewDueDate("");
      addTaskInputRef?.current?.focus();
    }
  };

  return (
    <div className="flex-1 p-4">
      <div className="font-bold mb-2">Tasks</div>
      <div className="flex mb-2 gap-2">
        <input
          ref={addTaskInputRef}
          className="border rounded px-2 py-1 flex-1"
          value={newTitle}
          onChange={e => setNewTitle(e.target.value)}
          onKeyDown={e => e.key === "Enter" && handleAdd()}
          placeholder="Add a new task"
        />
        <input
          type="date"
          className="border rounded px-2 py-1"
          value={newDueDate}
          onChange={e => setNewDueDate(e.target.value)}
        />
        <button className="bg-blue-500 text-white px-3 py-1 rounded" onClick={handleAdd}>
          Add
        </button>
      </div>
      <ul>
        {tasks.map((t) => (
          <TaskItem
            key={t.id}
            task={t}
            onToggleComplete={onToggleComplete}
            onDelete={onDeleteTask}
            onEdit={onEditTask}
          />
        ))}
      </ul>
    </div>
  );
}
