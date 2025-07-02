import { useAuth } from "../contexts/AuthContext";

interface Props {
  onAddProject: () => void;
  onAddTask: () => void;
}

export default function Toolbar({ onAddProject, onAddTask }: Props) {
  const { user, logout } = useAuth();
  return (
    <div className="w-full h-12 bg-white border-b flex items-center px-4 gap-2">
      <span className="font-bold text-lg flex-1">Mini Focus</span>
      <div className="flex items-center gap-2">
        <span className="text-sm text-gray-600">
          {user?.email}
        </span>
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
        <button
          className="bg-red-500 text-white px-3 py-1 rounded"
          onClick={logout}
        >
          Logout
        </button>
      </div>
    </div>
  );
}