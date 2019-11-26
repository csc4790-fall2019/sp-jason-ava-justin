import React from 'react';
import logo from './logo.svg';
import './App.css';

import { ThemeProvider } from 'emotion-theming'
import theme from '@rebass/preset'
//import theme from './Styles/styles.js'

import Display from './Components/Display.js';

function App() {
  return (
    <ThemeProvider theme={theme}>
      <div className="App">
          <Display/>
      </div>
    </ThemeProvider>
  );
}

export default App;
