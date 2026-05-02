import type { BobResponse } from "../types/bob";
import type { Checkpoint, CheckpointDiff, Milestone } from "../types/checkpoint";
import type { Project, ProjectCreate } from "../types/project";
import type { Workflow } from "../types/workflow";

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000/api/v1";

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...options.headers
    },
    ...options
  });
  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: response.statusText }));
    throw new Error(typeof error.detail === "string" ? error.detail : "Request failed");
  }
  if (response.status === 204) {
    return undefined as T;
  }
  return response.json() as Promise<T>;
}

export const api = {
  listProjects: () => request<Project[]>("/projects"),
  createProject: (payload: ProjectCreate) =>
    request<Project>("/projects", { method: "POST", body: JSON.stringify(payload) }),
  createCheckpoint: (payload: {
    project_id: string;
    milestone: Milestone;
    state_data: Record<string, unknown>;
    metadata?: Record<string, unknown>;
  }) => request<Checkpoint>("/checkpoints", { method: "POST", body: JSON.stringify(payload) }),
  listCheckpoints: (projectId: string) => request<Checkpoint[]>(`/projects/${projectId}/checkpoints`),
  restoreCheckpoint: (checkpointId: string) =>
    request<{ state_data: Record<string, unknown> }>(`/checkpoints/${checkpointId}/restore`, { method: "POST" }),
  diffCheckpoints: (leftId: string, rightId: string) =>
    request<CheckpointDiff>(`/checkpoints/diff?left_id=${leftId}&right_id=${rightId}`),
  initializeWorkflow: (projectId: string, context: Record<string, unknown>) =>
    request<Workflow>("/workflows", {
      method: "POST",
      body: JSON.stringify({ project_id: projectId, context })
    }),
  transitionWorkflow: (workflowId: string, targetState: Milestone, note: string) =>
    request<Workflow>(`/workflows/${workflowId}/transition`, {
      method: "POST",
      body: JSON.stringify({ target_state: targetState, note, auto_checkpoint: true })
    }),
  rollbackWorkflow: (workflowId: string, checkpointId: string) =>
    request<Workflow>(`/workflows/${workflowId}/rollback`, {
      method: "POST",
      body: JSON.stringify({ target_checkpoint_id: checkpointId })
    }),
  bobPlan: (project_description: string, context: Record<string, unknown>) =>
    request<BobResponse>("/bob/plan", { method: "POST", body: JSON.stringify({ project_description, context }) }),
  bobChat: (message: string, workflow_id: string, context: Record<string, unknown>) =>
    request<BobResponse>("/bob/chat", { method: "POST", body: JSON.stringify({ message, workflow_id, context }) }),
  bobTest: (code: string, context: Record<string, unknown>) =>
    request<BobResponse>("/bob/test", {
      method: "POST",
      body: JSON.stringify({ code, test_type: "unit", context })
    })
};
