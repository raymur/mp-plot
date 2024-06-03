import { useState } from 'react';
import './App.css';
import MpForm from './MpForm';
import MpPlot from './MpPlot';


import '@fontsource/roboto/300.css';
import '@fontsource/roboto/400.css';
import '@fontsource/roboto/500.css';
import '@fontsource/roboto/700.css';
import CircularProgress from '@mui/material/CircularProgress';
import Stack from '@mui/material/Stack';
import Box from '@mui/material/Box';

function App() {
  const [plot, setPlot] = useState(null);
  const [loading, setLoading] = useState(false);
  const  handleUrl = async (url) => {
    setLoading(true);
    await fetch('http://127.0.0.1:5000/plot/', 
     {
      method: "post",
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({url})
    }
    ).then((result)=> result.blob())
    .then(blob => {
      setPlot(URL.createObjectURL(blob));
      setLoading(false);
    });
  }
  return (
    <div className="App">
      <div className='Search-Header'>
        <h1>Mountain Project Tick Plot</h1>
        <MpForm urlValue={handleUrl} loading={loading}/>
      </div>
      <Box
        height={480}
        width={640}
        margin="auto"
        my={2}
        alignItems="center"
        justifyContent="center"
    >
      {
        loading ? 
        <Stack spacing={2} justifyContent="center" alignItems="center">
          <CircularProgress />
          <div>Generating plot</div>
        </Stack>
        : <img src={plot} alt=''/>
      }
      </Box>
    </div>
  );
}

export default App;
