import { useCallback, useEffect, useMemo, useState } from "react";

import { api } from "../services/api";
import type { BobResponse } from "../types/bob";
import type { Checkpoint, CheckpointDiff, Milestone } from "../types/checkpoint";
import type { Project } from "../types/project";
import type { Workflow } from "../types/workflow";

const nextStates: Record<Milestone, Milestone[]> = {
  plan: ["code"],
  code: ["debug", "test"],
  debug: ["code", "test"],
  test: ["code", "done"],
  done: []
};

export function useDevFlow() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [activeProjectId, setActiveProjectId] = useState("");
  const [workflow, setWorkflow] = useState<Workflow | null>(null);
  const [checkpoints, setCheckpoints] = useState<Checkpoint[]>([]);
  const [bobResponse, setBobResponse] = useState<BobResponse | null>(null);
  const [checkpointDiff, setCheckpointDiff] = useState<CheckpointDiff | null>(null);
  const [restoredState, setRestoredState] = useState<Record<string, unknown> | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const activeProject = useMemo(
    () => projects.find((project) => project.id === activeProjectId) ?? projects[0],
    [activeProjectId, projects]
  );

  const refreshProjects = useCallback(async () => {
    const nextProjects = await api.listProjects();
    setProjects(nextProjects);
    setActiveProjectId((current) => current || nextProjects[0]?.id || "");
  }, []);

  const refreshCheckpoints = useCallback(async (projectId: string) => {
    if (!projectId) return;
    setCheckpoints(await api.listCheckpoints(projectId));
  }, []);

  useEffect(() => {
    refreshProjects().catch((caught: Error) => setError(caught.message));
  }, [refreshProjects]);

  useEffect(() => {
    if (activeProject?.id) {
      refreshCheckpoints(activeProject.id).catch((caught: Error) => setError(caught.message));
    }
  }, [activeProject?.id, refreshCheckpoints]);

  async function runAction(action: () => Promise<void>) {
    setLoading(true);
    setError("");
    try {
      await action();
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Something went wrong");
    } finally {
      setLoading(false);
    }
  }

  return {
    projects,
    activeProject,
    workflow,
    checkpoints,
    bobResponse,
    checkpointDiff,
    restoredState,
    loading,
    error,
    nextStates: workflow ? nextStates[workflow.current_state] : [],
    setActiveProjectId,
    createProject: (name: string, description: string) =>
      runAction(async () => {
        const project = await api.createProject({
          name,
          description,
          tech_stack: { backend: "FastAPI", frontend: "React", ai: "IBM BOB demo layer" }
        });
        setProjects((current) => [project, ...current]);
        setActiveProjectId(project.id);
        setWorkflow(null);
        setCheckpoints([]);
      }),
    initializeWorkflow: () =>
      runAction(async () => {
        if (!activeProject) return;
        const created = await api.initializeWorkflow(activeProject.id, {
          project: activeProject.name,
          goal: activeProject.description
        });
        setWorkflow(created);
      }),
    createCheckpoint: (milestone: Milestone, note: string) =>
      runAction(async () => {
        if (!activeProject) return;
        await api.createCheckpoint({
          project_id: activeProject.id,
          milestone,
          state_data: {
            project: activeProject.name,
            workflow_state: workflow?.current_state ?? milestone,
            context: workflow?.context ?? {},
            note
          },
          metadata: { source: "manual-ui", note }
        });
        await refreshCheckpoints(activeProject.id);
      }),
    transitionWorkflow: (targetState: Milestone) =>
      runAction(async () => {
        if (!workflow || !activeProject) return;
        const updated = await api.transitionWorkflow(workflow.id, targetState, `Moved to ${targetState}`);
        setWorkflow(updated);
        await refreshCheckpoints(activeProject.id);
      }),
    restoreCheckpoint: (checkpointId: string) =>
      runAction(async () => {
        const restored = await api.restoreCheckpoint(checkpointId);
        setRestoredState(restored.state_data);
        if (workflow) {
          setWorkflow(await api.rollbackWorkflow(workflow.id, checkpointId));
        }
      }),
    compareLatest: () =>
      runAction(async () => {
        if (checkpoints.length < 2) return;
        const left = checkpoints[checkpoints.length - 2];
        const right = checkpoints[checkpoints.length - 1];
        setCheckpointDiff(await api.diffCheckpoints(left.id, right.id));
      }),
    askBobForPlan: () =>
      runAction(async () => {
        if (!activeProject) return;
        setBobResponse(await api.bobPlan(activeProject.description || activeProject.name, { workflow, checkpoints }));
      }),
    chatWithBob: (message: string) =>
      runAction(async () => {
        setBobResponse(await api.bobChat(message, workflow?.id ?? "", { activeProject, checkpoint_count: checkpoints.length }));
      }),
    askBobForTests: () =>
      runAction(async () => {
        setBobResponse(await api.bobTest(JSON.stringify({ workflow, checkpoints }, null, 2), { activeProject }));
      })
  };
}
