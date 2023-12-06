import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import EndpointAudit from "./components/EndpointAudit"
import AppStats from "./components/AppStats"
import Health from './components/Health'
import './App.css'

function App() {

  return (
    <>
      <div>
        <a href="https://vitejs.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Latest Stats</h1>
      <Health />
      <AppStats />
      <EndpointAudit endpoint='orders'/>
      <EndpointAudit endpoint='stocks'/>
    </>
  )
}

export default App
