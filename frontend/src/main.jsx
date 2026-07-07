import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App.jsx'
import { Home } from './Home.jsx'
import { NewModels } from './NewModels.jsx'
import { Chatbot } from './Chatbot.jsx'
import {BrowserRouter, Routes, Route} from 'react-router-dom'

createRoot(document.getElementById('root')).render(
    <StrictMode>
      <BrowserRouter>
      <Routes>
        <Route path="/" element={<App />}>
          <Route index element={<Home />} />
          <Route path="NewModels" element={<NewModels />} />
          <Route path="Chatbot" element={<Chatbot />} />
        </Route>
      </Routes>
      </BrowserRouter>
    </StrictMode>
)
