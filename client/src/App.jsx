import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import heroImg from './assets/hero.png'
import './App.css'
import RecentRunsTable from './components/RecentRuns'
import GoalProgressBar from './components/GoalCard'



// App
function App() {
  return (
    <div className='app-container'>
      {/* Header */}
      <h1>Running Dashboard</h1>
      <div>
        <h2>Today's Metrics:</h2>
        <p>Running Fitness: 93.0</p>
        <p>Base Fitness: 196</p>
        <p>Recovery %: 67</p>
      </div>
      
      {/* Recent Runs Table */}
      <div>
        <h2>Recent Runs Table</h2>
        <RecentRunsTable />
      </div>

      {/* Training Goals */}
      <h2>Training Goals</h2>
      <div>
        <GoalProgressBar goal={'2:25 Marathon'} progress={45} />
      </div>
    </div>
  );
};

export default App