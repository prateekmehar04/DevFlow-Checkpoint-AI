import { FormEvent, useState } from "react";

import type { BobResponse } from "../../types/bob";

interface Props {
  response: BobResponse | null;
  loading: boolean;
  onPlan: () => void;
  onTest: () => void;
  onChat: (message: string) => void;
}

export function BobPanel({ response, loading, onPlan, onTest, onChat }: Props) {
  const [message, setMessage] = useState("What should I checkpoint before the next demo step?");

  function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    onChat(message);
  }

  return (
    <section className="panel bob-panel">
      <div className="panel-heading">
        <div>
          <p className="eyebrow">IBM BOB</p>
          <h2>Context copilot</h2>
        </div>
      </div>

      <div className="actions-row">
        <button disabled={loading} onClick={onPlan} type="button">Plan</button>
        <button disabled={loading} onClick={onTest} type="button">Tests</button>
      </div>

      <form className="chat-form" onSubmit={submit}>
        <textarea value={message} onChange={(event) => setMessage(event.target.value)} />
        <button disabled={loading} type="submit">Send</button>
      </form>

      {response && (
        <div className="bob-response">
          <strong>{response.agent} / {response.mode}</strong>
          <p>{response.message ?? response.summary ?? response.diagnosis}</p>
          <ul>
            {(response.next_steps ?? response.recommended_cases ?? response.suggestions ?? response.risks ?? []).map((item) => (
              <li key={item}>{item}</li>
            ))}
            {response.milestones?.map((item) => (
              <li key={item.name}>{item.name}: {item.goal}</li>
            ))}
          </ul>
        </div>
      )}
    </section>
  );
}
