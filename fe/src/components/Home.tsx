import { useEffect, useState, useRef } from "react";
import ProjectTree from "./ProjectTree";
import TaskList from "./TaskList";
import Toolbar from "./Toolbar";
import type { Project } from "../types/project";
import type { Task } from "../types/task";
import {
  fetchProjects,
  createProject,
  updateProject,
  deleteProject,
  fetchItems,
  createItem,
  updateItem,
  deleteItem,
} from "../services/api";
import { buildProjectTree } from "../../tree";

export default function Home() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [selectedProject, setSelectedProject] = useState<string>("");
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const addTaskInputRef = useRef<HTMLInputElement>(null);

  // 프로젝트/할 일 불러오기
  useEffect(() => {
    setLoading(true);
    fetchProjects()
      .then((data) => {
        setProjects(data);
        if (data.length > 0) setSelectedProject(data[0].id);
      })
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    if (!selectedProject) return;
    setLoading(true);
    fetchItems(selectedProject)
      .then(setTasks)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, [selectedProject]);

  // 5분마다 동기화
  useEffect(() => {
    const interval = setInterval(() => {
      if (!selectedProject) return;
      fetchProjects().then(setProjects);
      fetchItems(selectedProject).then(setTasks);
    }, 5 * 60 * 1000);
    return () => clearInterval(interval);
  }, [selectedProject]);

  // 프로젝트 추가/수정/삭제
  const handleAddProject = async (parentId: string | null) => {
    const name = window.prompt("새 프로젝트 이름을 입력하세요", "New Project");
    if (!name) return;
    try {
      const newProject = await createProject({
        name,
        parent_id: parentId || undefined
      });
      setProjects((prev) => [...prev, newProject]);
      setSelectedProject(newProject.id);
    } catch (e: any) {
      setError(e.message);
    }
  };

  const handleDeleteProject = async (id: string) => {
    try {
      await deleteProject(id);
      setProjects((prev) => prev.filter((p) => p.id !== id));
      if (selectedProject === id) setSelectedProject("");
    } catch (e: any) {
      setError(e.message);
    }
  };

  const handleEditProject = async (id: string, name: string) => {
    try {
      const updated = await updateProject(id, { name });
      setProjects((prev) =>
        prev.map((p) => (p.id === id ? { ...p, name: updated.name } : p))
      );
    } catch (e: any) {
      setError(e.message);
    }
  };

  // 할 일 추가/수정/삭제
  const handleAddTask = async (title: string, dueDate?: string) => {
    if (!selectedProject) return;
    try {
      const newTask = await createItem(selectedProject, { title, due_date: dueDate });
      setTasks((prev) => [...prev, newTask]);
      setTimeout(() => addTaskInputRef.current?.focus(), 0);
    } catch (e: any) {
      setError(e.message);
    }
  };

  const handleDeleteTask = async (id: string) => {
    if (!selectedProject) return;
    try {
      await deleteItem(selectedProject, id);
      setTasks((prev) => prev.filter((t) => t.id !== id));
    } catch (e: any) {
      setError(e.message);
    }
  };

  const handleEditTask = async (id: string, title: string) => {
    if (!selectedProject) return;
    try {
      const updated = await updateItem(selectedProject, id, { title });
      setTasks((prev) =>
        prev.map((t) => (t.id === id ? { ...t, title: updated.title } : t))
      );
    } catch (e: any) {
      setError(e.message);
    }
  };

  const handleToggleComplete = async (id: string) => {
    if (!selectedProject) return;
    const task = tasks.find((t) => t.id === id);
    if (!task) return;
    try {
      const updated = await updateItem(selectedProject, id, { completed: !task.completed });
      setTasks((prev) =>
        prev.map((t) => (t.id === id ? { ...t, completed: updated.completed } : t))
      );
    } catch (e: any) {
      setError(e.message);
    }
  };

  // 툴바에서 +Task 클릭 시 입력창 포커스
  const handleToolbarAddTask = () => {
    addTaskInputRef.current?.focus();
  };

  const treeProjects = buildProjectTree(projects);

  return (
    <div className="h-screen flex flex-col">
      <Toolbar
        onAddProject={() => handleAddProject(null)}
        onAddTask={handleToolbarAddTask}
      />
      <div className="flex flex-1">
        <ProjectTree
          projects={treeProjects}
          onSelect={setSelectedProject}
          selectedId={selectedProject}
          onAdd={handleAddProject}
          onDelete={handleDeleteProject}
          onEdit={handleEditProject}
        />
        <TaskList
          tasks={tasks}
          onToggleComplete={handleToggleComplete}
          onAddTask={handleAddTask}
          onDeleteTask={handleDeleteTask}
          onEditTask={handleEditTask}
          addTaskInputRef={addTaskInputRef}
        />
      </div>
      {loading && <div className="fixed bottom-4 right-4 bg-gray-200 px-4 py-2 rounded shadow">Loading...</div>}
      {error && <div className="fixed bottom-4 left-4 bg-red-200 px-4 py-2 rounded shadow">{error}</div>}
    </div>
  );
}
