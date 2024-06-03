import './App.css';
import { useState } from 'react';
import { Button } from '@mui/material';


function MpForm({urlValue, loading}) {
    const [url, setUrl] = useState('');
    async function search  (event) {
        event.preventDefault()
        await urlValue(url);
    }
    let buttonDisabled = loading || url === '';
  return (
    <div className="MpForm">
      <form onSubmit={search}>
        <label >
          <input 
            name="urlValue" 
            placeholder="mountain project user url" 
            onChange={(e)=>setUrl(e.target.value)}/> 
        </label>
        <Button type="submit" disabled={buttonDisabled}>Generate plot</Button>
      </form>
    </div>
  );
}

export default MpForm;
