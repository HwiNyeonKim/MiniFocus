import React from "react";

interface Props {
  onAddProject: () => void;
  onAddTask: () => void;
}

export default function Toolbar({ onAddProject, onAddTask }: Props) {
  return (
    <div className="w-full h-12 bg-white border-b flex items-center px-4 gap-2">
      <span className="font-bold text-lg flex-1">Mini Focus</span>
      <button
        className="bg-green-500 text-white px-3 py-1 rounded"
        onClick={onAddProject}
      >
        + Project
      </button>
      <button
        className="bg-blue-500 text-white px-3 py-1 rounded"
        onClick={onAddTask}
      >
        + Task
      </button>
    </div>
  );
}