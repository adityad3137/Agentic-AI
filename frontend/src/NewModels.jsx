import './NewModels.css';
import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'


export function NewModels() {
    
    const [FileSelected, checkSelection] = useState(false);
    const [ModelList, getModelList] = useState([]);
    const [myModel, selectModel] = useState("Make new model");
    const [newModel, createNewModel] = useState(true);
    const [newModelName, setNewModelName] = useState("");
    const [modelAlreadyExists, setModelAlreadyExists] = useState(false);
    const [file, setFile] = useState(null);
    const [loadMakingModel, isMakingModel] = useState(false);
    const [modelCompleted, isModelComplete] = useState(false);
    const [errorFound, setErrorFound] = useState(false);
    const [errorString, setErrorString] = useState("");

    const handleFileChange = (event) => {
        const selectedFile = event.target.files?.[0];

        setFile(selectedFile);

        if (selectedFile) {
            console.log("Selected file:", selectedFile.name);
            checkSelection(true);
        }
    };

    const createModel = async() => {
        if(!isModelNameUnique())
            return;
        const formData = new FormData();
        formData.append('file', file);
        formData.append('model', myModel);
        formData.append('newModelName', newModelName);

        try{
            isMakingModel(true);

            const response = await fetch("http://127.0.0.1:5000/api/file", {
                method : 'POST',
                body : formData,
            });

            const data = await response.json();

            console.error(data.error);

            if(response.ok){
                console.log('Model made');
                isMakingModel(false);
                isModelComplete(true);
            }
            else{
                console.error('Model could not be made');
                throw new Error(data.error || 'An unexpected error occured');
            }
        }
        catch(e) {
            isMakingModel(false);
            setErrorFound(true);
            setErrorString(e.message);
        }
    }

    const isModelNameUnique = () => {
        setModelAlreadyExists(false);

        for(let i = 0; i < ModelList.length; i ++){
            if(ModelList[i] === newModelName){
                setModelAlreadyExists(true);
                return false;
            }
        }

        return true;
    }

    const choosingModel = (e) => {
        const selectedValue = e.target.value;
        selectModel(selectedValue);

        if(selectedValue === "Make new model")
            createNewModel(true);
        else{
            createNewModel(false);
            setNewModelName("");
        }
    }

    useEffect(() => {
            const fetchModelList = async() => {
            try {
                const response = await fetch("http://127.0.0.1:5000/api/models");
                const data = await response.json();

                getModelList(data.models);
            }

            catch(e){
                console.error(e);
            }
        };
        
        fetchModelList();
    },[]);

    const navigate = useNavigate();

    const goChatbot = () => {
        navigate('/Chatbot');
    };

    return (
    <div className="container-newmodels-screen"> 
        <div className="container-newmodels">
            <div className="model-field">
            <h2>Upload a File</h2> 
        
            { !FileSelected && ( 
                <div> 
                    <input id="file-upload" type="file" onChange={handleFileChange} style={{ display: 'none' }}/> 
                    <p className="subtitle">Drag and drop your file below to get started.</p> 
                    <label htmlFor="file-upload" className="upload-box"> 
                        <div className="upload-icon">📁</div> 
                        <div className="upload-text">Drag & Drop File Here</div> 
                        <div className="upload-hint">or click to browse files</div> 
                    </label> 
                </div> 
            )} 
            
            { FileSelected && ( 
                <div> 
                    <p align="left">File selected</p> 
                    <div className = "selectbox"> 
                        <p>{file.name}</p>
                        <button type="button" className="tiny-cross" onClick = {() => {checkSelection(false)}} aria-label="Close">&times;</button> 
                    </div> 
                </div> 
            ) } 

            </div>
            <div className = "model-field"> 
                <h2 className = "form-header">Choose a Model</h2> 
                <div className="select-container"> 
                    <select value = {myModel} onChange = {choosingModel}> 
                        <option value = "Make new model">Make new model</option> 
                        {ModelList.map((model, index) => <option key = {index} value = {model}>{model}</option>)} 
                    </select> 
                </div>         
            </div> 

            {newModel && ( 
                <div className = "model-field"> 
                    <h2 className = "form-header">Name of the new model</h2> 
                    <input type="text" placeholder = "Enter name" value = {newModelName} onChange = {(e) => {setNewModelName(e.target.value); setModelAlreadyExists(false);}}></input> 
                </div> 
            )} 
            
            { (!FileSelected || (newModel && (newModelName === "")) || errorFound) && (
                <button className="create-btn" disabled>Create Model</button> 
            )}

            { FileSelected && ((!newModel) || (newModel && (newModelName !== ""))) && !loadMakingModel && !modelCompleted && !errorFound && ( 
                <button className="create-btn" onClick = {createModel}>Create Model</button> 
            )} 
            
            {modelAlreadyExists && ( 
                <p className = "error-message">A model with this name already exists.</p> 
            )} 

            {errorFound && (
                <div className="model-error-message">
                    <div className="error-icon">!</div>
                    <div className="error-body">
                        <h3>Unable to Create Model</h3>
                        <p>{errorString}</p>
                        <button className="error-btn" onClick={() => setErrorFound(false)}>RETRY</button>
                    </div>
                </div>
            )}

            {loadMakingModel && ( 
                <div className="model-status-message">
                    <div className="status-dot"></div>
                    <div className="status-content">
                        <h3>Building AI Model</h3>
                        <p>Please wait while your documents are processed and indexed.
                            This may take a few moments.
                        </p>
                    </div>
                </div>
            )} 
            
            {modelCompleted && ( 
                <div className="model-success-message">
                    <div className="success-icon">✓</div>
                    <div className="success-body">
                        <h3>Model created successfully</h3>
                        <p>Your AI model is ready. You can now start chatting with it.</p>
                        <button className="home-btn" onClick={goChatbot}>Open Chatbot</button>
                    </div>
                </div>
            )}

        </div> 
    </div> 
    );
}