import './App.css';
import Carousel from './components/Carousel';

function App() {
  let currentlyReadingEndpoint = 'https://www.goodreads.com/review/list/<USER-ID>.xml?key=<KEY>&v=2&shelf=currently-reading'
    .replace('<USER-ID>', process.env.REACT_APP_GR_USER_ID)
    .replace('<KEY>', process.env.REACT_APP_GR_KEY);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Eric is currently reading:</h1>
        <Carousel grEndpoint={currentlyReadingEndpoint}/>
        <p>Goodreads API Key: {process.env.REACT_APP_GR_KEY}</p>
        <a href={currentlyReadingEndpoint}>Currently Reading</a>
      </header>
    </div>
  );
}

export default App;
