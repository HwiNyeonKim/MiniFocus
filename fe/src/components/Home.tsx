import React, { useState, useRef } from "react";
import ProjectTree from "./ProjectTree";
import TaskList from "./TaskList";
import Toolbar from "./Toolbar";
import type { Project } from "../types/project";
import type { Task } from "../types/task";

// 더미 데이터
const initialProjects: Project[] = [
  {
    id: "1",
    name: "Work",
    children: [
      { id: "2", name: "Subproject" },
      {
        id: "4",
        name: "Deep Project",
        children: [{ id: "5", name: "Very Deep" }],
      },
    ],
  },
  { id: "3", name: "Personal" },
];
const initialTasks: Task[] = [
  { id: "t1", projectId: "1", title: "Sample Task 1", completed: false, flagged: true, tags: ["Office"], dueDate: "2024-06-10" },
  { id: "t2", projectId: "2", title: "Subproject Task", completed: false, tags: ["Sub"], dueDate: "2024-06-12" },
  { id: "t3", projectId: "3", title: "Personal Task", completed: true, tags: ["Home"] },
];

export default function Home() {
  const [projects, setProjects] = useState<Project[]>(initialProjects);
  const [selectedProject, setSelectedProject] = useState("1");
  const [tasks, setTasks] = useState<Task[]>(initialTasks);
  const addTaskInputRef = useRef<HTMLInputElement>(null);

  const handleToggleComplete = (id: string) => {
    setTasks(tasks =>
      tasks.map(t =>
        t.id === id ? { ...t, completed: !t.completed } : t
      )
    );
  };

  const handleAddTask = (title: string, dueDate?: string) => {
    setTasks(tasks => [
      ...tasks,
      {
        id: Math.random().toString(36).slice(2),
        projectId: selectedProject,
        title,
        completed: false,
        dueDate,
      },
    ]);
    setTimeout(() => addTaskInputRef.current?.focus(), 0);
  };

  const handleDeleteTask = (id: string) => {
    setTasks(tasks => tasks.filter(t => t.id !== id));
  };

  const handleEditTask = (id: string, title: string) => {
    setTasks(tasks =>
      tasks.map(t =>
        t.id === id ? { ...t, title } : t
      )
    );
  };

  // 프로젝트 추가
  const handleAddProject = (parentId: string | null) => {
    const newId = Math.random().toString(36).slice(2);
    const newProject: Project = { id: newId, name: "New Project" };

    function addToTree(nodes: Project[]): Project[] {
      return nodes.map(node => {
        if (node.id === parentId) {
          return {
            ...node,
            children: node.children ? [...node.children, newProject] : [newProject],
          };
        }
        if (node.children) {
          return { ...node, children: addToTree(node.children) };
        }
        return node;
      });
    }

    if (parentId) {
      setProjects(prev => addToTree(prev));
    } else {
      setProjects(prev => [...prev, newProject]);
    }
    setSelectedProject(newId);
  };

  // 프로젝트 삭제
  const handleDeleteProject = (id: string) => {
    function removeFromTree(nodes: Project[]): Project[] {
      return nodes
        .filter(node => node.id !== id)
        .map(node =>
          node.children
            ? { ...node, children: removeFromTree(node.children) }
            : node
        );
    }
    setProjects(prev => removeFromTree(prev));
    if (selectedProject === id) setSelectedProject("");
  };

  // 프로젝트 이름 수정
  const handleEditProject = (id: string, name: string) => {
    function editInTree(nodes: Project[]): Project[] {
      return nodes.map(node => {
        if (node.id === id) return { ...node, name };
        if (node.children) return { ...node, children: editInTree(node.children) };
        return node;
      });
    }
    setProjects(prev => editInTree(prev));
  };

  // 툴바에서 +Task 클릭 시 입력창 포커스
  const handleToolbarAddTask = () => {
    addTaskInputRef.current?.focus();
  };

  return (
    <div className="h-screen flex flex-col">
      <Toolbar
        onAddProject={() => handleAddProject(null)}
        onAddTask={handleToolbarAddTask}
      />
      <div className="flex flex-1">
        <ProjectTree
          projects={projects}
          onSelect={setSelectedProject}
          selectedId={selectedProject}
          onAdd={handleAddProject}
          onDelete={handleDeleteProject}
          onEdit={handleEditProject}
        />
        <TaskList
          tasks={tasks.filter(t => t.projectId === selectedProject)}
          onToggleComplete={handleToggleComplete}
          onAddTask={handleAddTask}
          onDeleteTask={handleDeleteTask}
          onEditTask={handleEditTask}
          addTaskInputRef={addTaskInputRef}
        />
      </div>
    </div>
  );
}
