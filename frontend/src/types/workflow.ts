import type { Milestone } from "./checkpoint";

export interface Workflow {
  id: string;
  project_id: string;
  current_state: Milestone;
  context: Record<string, unknown>;
  state_history: Array<Record<string, unknown>>;
  last_checkpoint_id?: string | null;
  created_at: string;
  updated_at: string;
}
