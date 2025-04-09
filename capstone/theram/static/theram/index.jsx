import { createRoot } from 'react-dom/client';
import { useState } from 'react';
import axios from 'axios';


async function LatestPDF(){
  let source = await axios.get("/latest");
    return (<iframe
        id="inlineFrameExample"
        title="Inline Frame Example"
        width="800"
        height="800"
        src={source.data['paper']}>
      </iframe>);
}

// Render your React component instead
document.addEventListener("DOMContentLoaded", async () => {
  const root = createRoot(document.getElementById("latest"));
  root.render(await LatestPDF());
});