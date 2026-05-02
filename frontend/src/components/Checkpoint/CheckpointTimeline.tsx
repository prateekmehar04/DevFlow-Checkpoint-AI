import type { Checkpoint, CheckpointDiff } from "../../types/checkpoint";

interface Props {
  checkpoints: Checkpoint[];
  diff: CheckpointDiff | null;
  restoredState: Record<string, unknown> | null;
  loading: boolean;
  onRestore: (checkpointId: string) => void;
  onCompare: () => void;
}

export function CheckpointTimeline({ checkpoints, diff, restoredState, loading, onRestore, onCompare }: Props) {
  return (
    <section className="panel timeline-panel">
      <div className="panel-heading">
        <div>
          <p className="eyebrow">Checkpoints</p>
          <h2>Timeline</h2>
        </div>
        <button disabled={loading || checkpoints.length < 2} onClick={onCompare} type="button">Compare latest</button>
      </div>

      <div className="timeline">
        {checkpoints.map((checkpoint) => (
          <article className="checkpoint-card" key={checkpoint.id}>
            <div>
              <span className="version">v{checkpoint.version}</span>
              <strong>{checkpoint.milestone}</strong>
              <small>{new Date(checkpoint.created_at).toLocaleString()}</small>
            </div>
            <button disabled={loading} onClick={() => onRestore(checkpoint.id)} type="button">Restore</button>
          </article>
        ))}
        {checkpoints.length === 0 && <p className="empty">No checkpoints yet.</p>}
      </div>

      {diff && (
        <pre className="code-block">{JSON.stringify(diff.diff, null, 2)}</pre>
      )}
      {restoredState && (
        <pre className="code-block">{JSON.stringify(restoredState, null, 2)}</pre>
      )}
    </section>
  );
}
