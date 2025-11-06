import React from 'react';
import { LiveAnnouncer } from 'react-aria-live';
import TripPlanner from './components/TripPlanner';

const App: React.FC = () => {
  return (
    <LiveAnnouncer>
      <div className="app" role="application">
        <header className="app__header">
          <h1>RailNav Pro Planner</h1>
          <p>Plan, review, and sync accessible journeys for Allan and Jane.</p>
        </header>
        <main>
          <TripPlanner />
        </main>
      </div>
    </LiveAnnouncer>
  );
};

export default App;
