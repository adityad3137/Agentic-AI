import './Home.css'
import { useNavigate } from 'react-router-dom';

export function Home() {
    
    const navigate = useNavigate()

    const clickExisting = () => {
        navigate('/Chatbot')
    };

    const clickNew = () => {
        navigate('/NewModels')
    };

    return (
        <section className = "home-page">   
        <div className="container-home">

            <button onClick = {clickExisting}>
                <div className="icon">🤖</div>
                <div className="card-title">Chatbot</div>
                <div className="card-description">Chat with an existing model</div>
            </button>

            <button onClick = {clickNew}>
                <div className="icon">🧠</div>
                <div className="card-title">Build Model</div>
                <div className="card-description">Create a completely new model or append a pre-existing one.</div>
            </button>

        </div>
        </section>
    )
}