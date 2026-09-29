import { useState } from 'react'
import './App.css'

const builds = [
  {
    id: '#125',
    status: 'FAILED',
    branch: 'feature/login',
    duration: '2m 34s',
    time: '2 minutes ago',
    error: 'ModuleNotFoundError',
    diagnosis: 'Required dependency was not found during the build.',
    fix: 'Install the missing dependency and run the pipeline again.',
  },
  {
    id: '#124',
    status: 'SUCCESS',
    branch: 'main',
    duration: '1m 48s',
    time: '18 minutes ago',
    error: '-',
    diagnosis: 'Build completed successfully.',
    fix: '-',
  },
  {
    id: '#123',
    status: 'SUCCESS',
    branch: 'feature/api',
    duration: '2m 01s',
    time: '1 hour ago',
    error: '-',
    diagnosis: 'Build completed successfully.',
    fix: '-',
  },
]

function App() {
  const [selectedBuild, setSelectedBuild] = useState(builds[0])

  const isFailed = selectedBuild.status === 'FAILED'

  return (
    <div className="app">
      <header className="topbar">
        <div>
          <h1>Build Inspector</h1>
          <p>AI-powered DevOps Pipeline Analyzer</p>
        </div>

        <div className="connection">
          <span className="online-dot"></span>
          Pipeline Connected
        </div>
      </header>

      <main className="dashboard">

        {/* Summary Cards */}
        <section className="summary-grid">

          <div className="card">
            <span className="label">CURRENT BUILD</span>
            <strong>{selectedBuild.id}</strong>
            <span>{selectedBuild.branch}</span>
          </div>

          <div className="card">
            <span className="label">STATUS</span>
            <strong className={isFailed ? 'failed' : 'success'}>
              {selectedBuild.status}
            </strong>
            <span>{selectedBuild.time}</span>
          </div>

          <div className="card">
            <span className="label">DURATION</span>
            <strong>{selectedBuild.duration}</strong>
            <span>Build execution time</span>
          </div>

          <div className="card">
            <span className="label">AI CONFIDENCE</span>
            <strong>91%</strong>
            <span>Diagnosis confidence</span>
          </div>

        </section>

        {/* Main Content */}
        <section className="content-grid">

          {/* Pipeline Panel */}
          <div className="panel">

            <div className="panel-header">
              <div>
                <h2>Pipeline Status</h2>
                <p>Latest build execution details</p>
              </div>

              <span
                className={`status-badge ${
                  isFailed ? 'failed-badge' : 'success-badge'
                }`}
              >
                ● {selectedBuild.status}
              </span>
            </div>

            {/* Pipeline Steps */}
            <div className="pipeline">

              <div className="step completed">
                <span>✓</span>
                <div>
                  <strong>Source Checkout</strong>
                  <small>Completed</small>
                </div>
              </div>

              <div className="line"></div>

              <div className="step completed">
                <span>✓</span>
                <div>
                  <strong>Install Dependencies</strong>
                  <small>Completed</small>
                </div>
              </div>

              <div className="line"></div>

              <div
                className={
                  isFailed
                    ? 'step failed-step'
                    : 'step completed'
                }
              >
                <span>{isFailed ? '!' : '✓'}</span>

                <div>
                  <strong>Build</strong>

                  <small>
                    {isFailed ? 'Failed' : 'Completed'}
                  </small>
                </div>
              </div>

              <div className="line"></div>

              <div
                className={
                  isFailed
                    ? 'step pending'
                    : 'step completed'
                }
              >
                <span>{isFailed ? '○' : '✓'}</span>

                <div>
                  <strong>Deploy</strong>

                  <small>
                    {isFailed ? 'Not started' : 'Completed'}
                  </small>
                </div>
              </div>

            </div>

            {/* Error / Success Message */}
            {isFailed ? (
              <div className="error-box">

                <div className="error-title">
                  <span>⚠</span>
                  Build Error
                </div>

                <code>{selectedBuild.error}</code>

                <p>
                  The build failed because a required dependency
                  could not be found.
                </p>

              </div>
            ) : (
              <div className="success-box">

                <div className="success-title">
                  <span>✓</span>
                  Build Completed Successfully
                </div>

                <p>
                  All build stages completed successfully.
                  No errors were detected.
                </p>

              </div>
            )}

          </div>

          {/* AI Diagnosis Panel */}
          <div className="panel ai-panel">

            <div className="ai-heading">

              <span className="ai-icon">✦</span>

              <div>
                <h2>AI Diagnosis</h2>
                <p>Analysis generated by AI Analyzer</p>
              </div>

            </div>

            <div className="diagnosis">

              <span className="label">ROOT CAUSE</span>

              <h3>
                {selectedBuild.diagnosis}
              </h3>

            </div>

            <div className="fix-box">

              <span className="label">
                SUGGESTED FIX
              </span>

              <p>
                {selectedBuild.fix}
              </p>

            </div>

            <div className="confidence">

              <div>
                <span>Confidence</span>
                <strong>91%</strong>
              </div>

              <div className="progress">
                <div className="progress-fill"></div>
              </div>

            </div>

          </div>

        </section>

        {/* Build History */}
        <section className="panel history-panel">

          <div className="panel-header">

            <div>
              <h2>Build History</h2>
              <p>Select a build to inspect its result</p>
            </div>

          </div>

          <div className="history-list">

            {builds.map((build) => (

              <button
                className={`history-row ${
                  selectedBuild.id === build.id
                    ? 'selected'
                    : ''
                }`}
                key={build.id}
                onClick={() => setSelectedBuild(build)}
              >

                <span className="build-number">
                  {build.id}
                </span>

                <span
                  className={
                    build.status === 'FAILED'
                      ? 'history-status failed'
                      : 'history-status success'
                  }
                >
                  {build.status}
                </span>

                <span>{build.branch}</span>

                <span>{build.duration}</span>

                <span>{build.time}</span>

              </button>

            ))}

          </div>

        </section>

      </main>

      <footer>
        DevOps Memory Agent • Build Inspector
      </footer>

    </div>
  )
}

export default App