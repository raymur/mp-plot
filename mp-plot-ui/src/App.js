import { useState } from 'react';
import './App.css';
import MpForm from './MpForm';
import MpPlot from './MpPlot';

function App() {
  const [plot, setPlot] = useState('');
  const  handleUrl = async (url) => {
    await fetch('http://127.0.0.1:5000').then((result)=> result.json()).then(data => setPlot(data['message']));
  }
  return (
    <div className="App">
      <h1>Mountain Project Tick Plot</h1>
      <MpForm urlValue={handleUrl}/>
      <div>{plot}</div>
      <MpPlot />
    </div>
  );
}

export default App;
