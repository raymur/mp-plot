import './App.css';
import { useState } from 'react';


function MpForm({urlValue}) {
    const defaultValue = 'https://www.mountainproject.com/user/201537336/rachel-murphy';
    const [url, setUrl] = useState(defaultValue);
    async function search  (event) {
        event.preventDefault()
        await urlValue(url);
    }
  return (
    <div className="MpForm">
      <form onSubmit={search}>
        <label >
          MP user url:
          <input 
            name="urlValue" 
            placeholder="https://www.mountainproject.com/user/10788/c-miller" 
            defaultValue={defaultValue}
            onChange={(e)=>setUrl(e.target.value)}/> 
        </label>
        <button type="submit" >Search</button>
      </form>
    </div>
  );
}

export default MpForm;
