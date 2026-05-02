export type Milestone = "plan" | "code" | "debug" | "test" | "done";

export interface Checkpoint {
  id: string;
  project_id: string;
  milestone: Milestone;
  state_data: Record<string, unknown>;
  metadata: Record<string, unknown>;
  version: number;
  created_at: string;
}

export interface CheckpointDiff {
  from_checkpoint_id: string;
  to_checkpoint_id: string;
  diff: {
    added: Array<Record<string, unknown>>;
    removed: Array<Record<string, unknown>>;
    changed: Array<Record<string, unknown>>;
  };
}
