import { BobPanel } from "./components/BOB/BobPanel";
import { CheckpointTimeline } from "./components/Checkpoint/CheckpointTimeline";
import { ProjectPanel } from "./components/Dashboard/ProjectPanel";
import { WorkflowBoard } from "./components/Workflow/WorkflowBoard";
import { useDevFlow } from "./hooks/useDevFlow";
import "./styles.css";

export default function App() {
  const devflow = useDevFlow();

  return (
    <main className="app-shell">
      <header className="topbar">
        <div>
          <p className="eyebrow">Bob Dev Day Hackathon</p>
          <h1>DevFlow Checkpoint AI</h1>
        </div>
        <div className="status-dot">{devflow.loading ? "Working" : "Ready"}</div>
      </header>

      {devflow.error && <div className="error-banner">{devflow.error}</div>}

      <div className="dashboard-grid">
        <ProjectPanel
          projects={devflow.projects}
          activeProject={devflow.activeProject}
          loading={devflow.loading}
          onCreate={devflow.createProject}
          onSelect={devflow.setActiveProjectId}
        />

        <WorkflowBoard
          workflow={devflow.workflow}
          nextStates={devflow.nextStates}
          loading={devflow.loading}
          onInitialize={devflow.initializeWorkflow}
          onTransition={devflow.transitionWorkflow}
          onCheckpoint={devflow.createCheckpoint}
        />

        <CheckpointTimeline
          checkpoints={devflow.checkpoints}
          diff={devflow.checkpointDiff}
          restoredState={devflow.restoredState}
          loading={devflow.loading}
          onRestore={devflow.restoreCheckpoint}
          onCompare={devflow.compareLatest}
        />

        <BobPanel
          response={devflow.bobResponse}
          loading={devflow.loading}
          onPlan={devflow.askBobForPlan}
          onTest={devflow.askBobForTests}
          onChat={devflow.chatWithBob}
        />
      </div>
    </main>
  );
}
