import './Chatbot.css'
import { useState, useEffect } from 'react'
import ReactMarkdown from 'react-markdown';

export function Chatbot(){
    const [myQuery, setMyQuery] = useState("");
    const [messages, setMessage] = useState([{sender: "bot", content: "Hello! How can I help you today?" }])
    const [modelSelected, isModelSelected] = useState(false);
    const [ModelList, setModelList] = useState([]);
    const [myModel, setMyModel] = useState("");
    const [confirmModelButtonOn, setConfirmModelButtonOn] = useState(false);

    const History = [{sender: "bot", content: "Hello! How can I help you today?" }]

    useEffect(() => {
            const fetchModelList = async() => {
            try {
                const response = await fetch("http://127.0.0.1:5000/api/models");
                const data = await response.json();

                setModelList(data.models);
            }

            catch(e){
                console.error(e);
            }
        };
        
        fetchModelList();
    },[]);

    const handleModelSelection = (e) =>{
        const modelSelectedCurrently = e.target.value;
        setMyModel(modelSelectedCurrently);

        setConfirmModelButtonOn( !(modelSelectedCurrently == ""));
    }

    const InvokeConversation = async() => {
        console.log("invoking conversation");
        try{
            PrintQuery();
            await SendQuery();
            await GetReply();
        }
        catch(e){
            console.error(e);
        }
    }

    const PrintQuery = () => {
        if(!myQuery.trim())
            return;
        
        setMessage((History) => [...History, {sender : "user", content : myQuery.trim()}]);

        setMyQuery("");
    }

    const SendQuery = async() => {

        console.log("sending query");

        const queryInformation = {
            model : myModel,
            query : myQuery
        }

        try {
            const response = await fetch("http://127.0.0.1:5000/api/query", {
                method : 'POST',
                headers : {
                    'Content-type' : 'application/json',
                },
                body : JSON.stringify(queryInformation)
            });

            if(response.ok) {
                console.log("Query Sent");
            }
            else
                console.log("Query NOT Sent");
        }

        catch(error){
            console.error(error)
        }
    }

    const GetReply = async() => {
        try{
            const response = await fetch("http://127.0.0.1:5000/api/reply");
            const rawText = await response.text();
            const data = JSON.parse(rawText);
            const answer = data.answer;
            
            console.log(answer);

            if(response.ok){
                console.log("Reply received");
                setMessage((History) => [...History, {sender : "bot", content : answer}]);
            }
            else{
                console.error("No reply received");
            }
        }

        catch(e){
            console.error(e);
        }
    }

    return (
        <div>
            { !modelSelected && (
            <div className="model-overlay">
                <div className = "selecting-model">
                    <div className = "simple-card">
                        <div className="card-header">
                            <h3>Choose the model you want to chat with</h3>
                        </div>

                        <div className = "card-select">
                            <select value = {myModel} onChange = {handleModelSelection}>
                                <option value = "">Select a model</option>
                                {ModelList.map((model, index) => <option key = {index} value = {model}>{model}</option>)}
                            </select>
                        </div>
                
                        <div className = "confirmButtonSpace">
                            {!confirmModelButtonOn && (
                                <button className = "confirmButton" disabled>Confirm Model</button>
                            )}

                            { confirmModelButtonOn && (
                                <button className = "confirmButton" onClick = {() => {isModelSelected(true)}}>Confirm Model</button>
                            )}
                        </div>
                    </div>
                </div>
            </div>
            )}

            { modelSelected && (
            <div className="chat-page">
                <div className="chat-header">
                    <span className="chat-model-label">MODEL</span>
                    <span className="chat-model-name">{myModel}</span>
                </div>
                <div className="chat-messages">
                    {messages.map((msg, index) => 
                        <div key = {index} className = {`message ${msg.sender}`}>
                            <ReactMarkdown>{msg.content}</ReactMarkdown>
                        </div>
                    )}
                </div>

                <div className="chat-input-container">
                    <input type="text" placeholder="Type your message..." 
                    value = {myQuery} 
                    onChange = {(e) => { setMyQuery(e.target.value)}} 
                    onKeyDown = {(e)=> {if(e.key === "Enter") {InvokeConversation();}}} />
                    <button onClick = {InvokeConversation}>Send</button>
                </div>
            </div>
        )}
        </div>
    );
}