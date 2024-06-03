import './App.css';
import { useState } from 'react';


function MpForm({urlValue}) {
    const [url, setUrl] = useState('');
    async function search  (event) {
        event.preventDefault()
        await urlValue(url);
    }
  return (
    <div className="MpForm">
      <form onSubmit={search}>
        <label >
          <input 
            name="urlValue" 
            placeholder="mountain project user url" 
            onChange={(e)=>setUrl(e.target.value)}/> 
        </label>
        <button type="submit" >Generate plot</button>
      </form>
    </div>
  );
}

export default MpForm;
