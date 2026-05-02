import type { Milestone } from "../../types/checkpoint";
import type { Workflow } from "../../types/workflow";

const states: Milestone[] = ["plan", "code", "debug", "test", "done"];

interface Props {
  workflow: Workflow | null;
  nextStates: Milestone[];
  loading: boolean;
  onInitialize: () => void;
  onTransition: (target: Milestone) => void;
  onCheckpoint: (milestone: Milestone, note: string) => void;
}

export function WorkflowBoard({ workflow, nextStates, loading, onInitialize, onTransition, onCheckpoint }: Props) {
  return (
    <section className="panel workflow-panel">
      <div className="panel-heading">
        <div>
          <p className="eyebrow">Workflow</p>
          <h2>{workflow ? workflow.current_state : "Not started"}</h2>
        </div>
        {!workflow && <button onClick={onInitialize} disabled={loading} type="button">Start</button>}
      </div>

      <div className="state-strip">
        {states.map((state) => (
          <div className={`state-pill ${workflow?.current_state === state ? "current" : ""}`} key={state}>
            <span>{state}</span>
          </div>
        ))}
      </div>

      <div className="actions-row">
        {nextStates.map((state) => (
          <button key={state} disabled={loading} onClick={() => onTransition(state)} type="button">
            Move to {state}
          </button>
        ))}
        <button
          disabled={loading}
          onClick={() => onCheckpoint(workflow?.current_state ?? "plan", "Manual checkpoint from dashboard")}
          type="button"
        >
          Checkpoint
        </button>
      </div>

      <div className="history">
        {(workflow?.state_history ?? []).slice(-4).map((item, index) => (
          <div className="history-row" key={`${item.at}-${index}`}>
            <span>{String(item.from ?? "start")}</span>
            <strong>{String(item.to)}</strong>
            <small>{String(item.note ?? "")}</small>
          </div>
        ))}
      </div>
    </section>
  );
}
