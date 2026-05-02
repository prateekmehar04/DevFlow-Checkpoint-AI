import { FormEvent, useState } from "react";

import type { Project } from "../../types/project";

interface Props {
  projects: Project[];
  activeProject?: Project;
  loading: boolean;
  onSelect: (projectId: string) => void;
  onCreate: (name: string, description: string) => void;
}

export function ProjectPanel({ projects, activeProject, loading, onSelect, onCreate }: Props) {
  const [name, setName] = useState("IBM Bob Dev Day Demo");
  const [description, setDescription] = useState("Checkpoint workflow assistant for plan, code, debug, and test recovery.");

  function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (name.trim()) {
      onCreate(name.trim(), description.trim());
    }
  }

  return (
    <section className="panel project-panel">
      <div className="panel-heading">
        <div>
          <p className="eyebrow">Projects</p>
          <h2>Checkpoint workspace</h2>
        </div>
        <span className="count">{projects.length}</span>
      </div>

      <form className="project-form" onSubmit={submit}>
        <input value={name} onChange={(event) => setName(event.target.value)} placeholder="Project name" />
        <textarea value={description} onChange={(event) => setDescription(event.target.value)} placeholder="Project goal" />
        <button disabled={loading} type="submit">Create</button>
      </form>

      <div className="project-list">
        {projects.map((project) => (
          <button
            className={`project-row ${activeProject?.id === project.id ? "active" : ""}`}
            key={project.id}
            onClick={() => onSelect(project.id)}
            type="button"
          >
            <strong>{project.name}</strong>
            <span>{project.status}</span>
          </button>
        ))}
      </div>
    </section>
  );
}
