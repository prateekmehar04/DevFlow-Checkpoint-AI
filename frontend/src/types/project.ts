export interface Project {
  id: string;
  name: string;
  description: string;
  tech_stack: Record<string, unknown>;
  status: string;
  created_at: string;
  updated_at: string;
}

export interface ProjectCreate {
  name: string;
  description?: string;
  tech_stack?: Record<string, unknown>;
  status?: string;
}
