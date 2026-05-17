import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {

  // STATES

  const [url, setUrl] = useState('');
  const [result, setResult] = useState(null);

  const [qrFile, setQrFile] = useState(null);
  const [qrResult, setQrResult] = useState(null);

  const [message, setMessage] = useState('');
  const [messageResult, setMessageResult] = useState(null);

  // URL SCAN FUNCTION

  const scanURL = async () => {

    try {

      const response = await axios.post(
        'http://127.0.0.1:5000/scan',
        { url }
      );

      setResult(response.data);

    } catch (error) {

      console.log(error);
    }
  };

  // QR SCAN FUNCTION

  const scanQR = async () => {

    if (!qrFile) {

      alert('Please upload QR image');

      return;
    }

    const formData = new FormData();

    formData.append('file', qrFile);

    try {

      const response = await axios.post(
        'http://127.0.0.1:5000/scan-qr',
        formData
      );

      setQrResult(response.data);

    } catch (error) {

      console.log(error);
    }
  };

  // SPAM MESSAGE SCAN FUNCTION

  const scanMessage = async () => {

    try {

      const response = await axios.post(
        'http://127.0.0.1:5000/scan-message',
        { message }
      );

      setMessageResult(response.data);

    } catch (error) {

      console.log(error);
    }
  };

  return (

    <div className="app">

      {/* PROJECT TITLE */}

      <h1>
        CyberShield XDR
      </h1>

      <p className="main-tagline">
        AI Threat Intelligence Platform
      </p>

      {/* DASHBOARD STATS */}

      <div className="dashboard-grid">

        <div className="dashboard-card">

          <h3>Total Threat Scans</h3>

          <p>1248</p>

        </div>

        <div className="dashboard-card danger">

          <h3>Phishing Detected</h3>

          <p>312</p>

        </div>

        <div className="dashboard-card warning">

          <h3>Spam Threats</h3>

          <p>489</p>

        </div>

        <div className="dashboard-card success">

          <h3>QR Threats</h3>

          <p>87</p>

        </div>

      </div>

      {/* SUBTITLE */}

      <p className="subtitle">
        AI-Powered Digital Threat Intelligence Platform
      </p>

      {/* URL SCANNER */}

      <div className="scanner-box">

        <h2>URL Scam Detection</h2>

        <input
          type="text"
          placeholder="Enter suspicious URL"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
        />

        <button onClick={scanURL}>
          Scan URL
        </button>

      </div>

      {/* URL RESULT */}

      {result && (

        <div className="result-box">

          <h2
            className={
              result.classification === 'SAFE'
                ? 'safe-text'
                : result.classification === 'SUSPICIOUS'
                ? 'warning-text'
                : 'danger-text'
            }
          >
            Classification: {result.classification}
          </h2>

          <h3>
            Threat Score: {result.score}
          </h3>

          {/* RISK METER */}

          <div className="risk-meter">

            <div
              className="risk-fill"
              style={{
                width: `${result.score}%`
              }}
            ></div>

          </div>

          <div className="reasons">

            <h4>Detection Reasons:</h4>

            <ul>

              {result.reasons.map((reason, index) => (

                <li key={index}>
                  {reason}
                </li>

              ))}

            </ul>

          </div>

        </div>
      )}

      {/* QR SCANNER */}

      <div className="scanner-box">

        <h2>QR Scam Detection</h2>

        <input
          type="file"
          accept="image/*"
          onChange={(e) =>
            setQrFile(e.target.files[0])
          }
        />

        <button onClick={scanQR}>
          Scan QR
        </button>

      </div>

      {/* QR RESULT */}

      {qrResult && (

        <div className="result-box">

          <h2
            className={
              qrResult.classification === 'SAFE'
                ? 'safe-text'
                : qrResult.classification === 'SUSPICIOUS'
                ? 'warning-text'
                : 'danger-text'
            }
          >
            {qrResult.classification}
          </h2>

          <h3>
            Risk Score: {qrResult.score}
          </h3>

          {/* RISK METER */}

          <div className="risk-meter">

            <div
              className="risk-fill"
              style={{
                width: `${qrResult.score}%`
              }}
            ></div>

          </div>

          <p>
            QR Data: {qrResult.qr_data}
          </p>

          <div className="reasons">

            <h4>Detection Reasons:</h4>

            <ul>

              {qrResult.reasons.map((reason, index) => (

                <li key={index}>
                  {reason}
                </li>

              ))}

            </ul>

          </div>

        </div>
      )}

      {/* SPAM DETECTOR */}

      <div className="scanner-box">

        <h2>AI Spam & Fraud Message Detector</h2>

        <textarea
          placeholder="Paste suspicious SMS or scam message"
          value={message}
          onChange={(e) =>
            setMessage(e.target.value)
          }
          rows="5"
        />

        <br />

        <button onClick={scanMessage}>
          Analyze Message
        </button>

      </div>

      {/* SPAM RESULT */}

      {messageResult && (

        <div className="result-box">

          <h2
            className={
              messageResult.classification === 'SAFE'
                ? 'safe-text'
                : messageResult.classification === 'SUSPICIOUS'
                ? 'warning-text'
                : 'danger-text'
            }
          >
            {messageResult.classification}
          </h2>

          <h3>
            Risk Score: {messageResult.score}
          </h3>

          {/* RISK METER */}

          <div className="risk-meter">

            <div
              className="risk-fill"
              style={{
                width: `${messageResult.score}%`
              }}
            ></div>

          </div>

          <div className="reasons">

            <h4>Detection Reasons:</h4>

            <ul>

              {messageResult.reasons.map((reason, index) => (

                <li key={index}>
                  {reason}
                </li>

              ))}

            </ul>

          </div>

        </div>
      )}

      {/* CYBER SAFETY TIPS */}

      <div className="tips">

        <h2>Cyber Safety Tips</h2>

        <ul>

          <li>Never share OTP with anyone</li>

          <li>Check HTTPS before login</li>

          <li>Avoid clicking suspicious links</li>

          <li>Use strong passwords</li>

          <li>Enable 2-factor authentication</li>

        </ul>

      </div>

      {/* FOOTER */}

      <footer className="footer">

        <p>
          Developed by Ajay Kumar
        </p>

        <p>
          B.Tech Cyber Security Project
        </p>

        <p>
          CyberShield XDR © 2026
        </p>

      </footer>

    </div>
  );
}

export default App;