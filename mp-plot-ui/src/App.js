import { useState } from 'react';
import './App.css';
import MpForm from './MpForm';
import MpPlot from './MpPlot';

function App() {
  const [plot, setPlot] = useState(null);
  const  handleUrl = async (url) => {
    await fetch('http://127.0.0.1:5000/plot/', 
     {
      method: "post",
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({url})
    }
    ).then((result)=> result.blob()).then(blob => setPlot(URL.createObjectURL(blob)));
  }
  return (
    <div className="App">
      <div className='Search-Header'>
        <h1>Mountain Project Tick Plot</h1>
        <MpForm urlValue={handleUrl}/>
      </div>
      <img src={plot} alt='ticks'/>
    </div>
  );
}

export default App;
