import './App.css'
import { Outlet } from 'react-router-dom';


function App() {
    return (
        <div className = "app-layout">
            <header className="header">
                <div className="logo-section">
                    <h1>AI Model Workspace</h1>
                    <p>Manage document models and interact with them through a conversational interface.</p>
                </div>
            </header>
            <main className = "main-content">
                <Outlet />
            </main>
        </div>
    )
}

export default App