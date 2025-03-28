import React, { useRef, useState, useEffect } from 'react';
import './Dashboard.css';
import fakeRecordings from '../../assets/fakeRecordings';

function Dashboard() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState('');
  const [recordings, setRecordings] = useState(fakeRecordings);
  const [showRenameBox, setShowRenameBox] = useState(false);
  const [renameInput, setRenameInput] = useState('');
  const [pendingRecordingData, setPendingRecordingData] = useState(null);
  const [expandedId, setExpandedId] = useState(null);
  const [showFullTranscript, setShowFullTranscript] = useState(false);

  const fileInputRef = useRef(null);
  const renameInputRef = useRef(null);

  const handleUploadClick = () => {
    fileInputRef.current.click();
  };

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      setSelectedFile(file);
      handleUpload(file);
    }
  };

  const handleUpload = async (file) => {
    setUploadStatus('');
    setIsUploading(true);

    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await fetch('http://localhost:8000/meetings/upload_meeting_recording', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Upload failed');
      }

      const data = await response.json();

      setPendingRecordingData({
        transcription: data.transcription,
        summary: data.summary,
        duration: data.duration,
      });

      setRenameInput('');
      setShowRenameBox(true);
    } catch (error) {
      setUploadStatus(`Upload failed: ${error.message}`);
    } finally {
      setIsUploading(false);
    }
  };

  const confirmRename = () => {
    const nameToUse = renameInput.trim() || selectedFile.name;
    const now = new Date();
    const formattedDate = now.toLocaleDateString('en-US', {
      weekday: 'short',
      day: 'numeric',
      month: 'long',
      year: 'numeric',
    });

    const newRecording = {
      id: Date.now(),
      title: nameToUse,
      dateUploaded: formattedDate,
      duration: pendingRecordingData?.duration || 'Unknown',
      transcript: pendingRecordingData?.transcript || '',
      summary: pendingRecordingData?.summary || '',
    };

    setRecordings(prev => [newRecording, ...prev]);
    setShowRenameBox(false);
    setRenameInput('');
    setSelectedFile(null);
    setPendingRecordingData(null);
    setUploadStatus('Upload successful!');
  };

  useEffect(() => {
    if (showRenameBox && renameInputRef.current) {
      renameInputRef.current.focus();
    }
  }, [showRenameBox]);

  const toggleExpand = (id) => {
    if (expandedId === id) {
      setExpandedId(null);
      setShowFullTranscript(false);
    } else {
      setExpandedId(id);
      setShowFullTranscript(false);
    }
  };

  return (
    <div className="dashboard-container" id="dashboard">
      <div className="upload-column">
        <input
          type="file"
          ref={fileInputRef}
          onChange={handleFileChange}
          accept="audio/*,video/*"
          style={{ display: 'none' }}
        />

        <button
          className="upload-button"
          onClick={handleUploadClick}
          disabled={isUploading}
        >
          {isUploading ? 'uploading...' : 'upload meeting recordings'}
        </button>

        {uploadStatus && (
          <div className={uploadStatus.includes('failed') ? 'upload-error' : 'upload-success'}>
            {uploadStatus}
          </div>
        )}
      </div>

      {/* Rename Modal */}
      {showRenameBox && (
        <div className="rename-modal">
          <div className="rename-box">
            <p>Rename your recording:</p>
            <input
              type="text"
              value={renameInput}
              ref={renameInputRef}
              onChange={(e) => setRenameInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && confirmRename()}
              placeholder={selectedFile?.name}
            />
            <button className="confirm-button" onClick={confirmRename}>Confirm</button>
          </div>
        </div>
      )}

      <div className="recordings-table">
        <div className="table-header">
          <span></span>
          <span>title</span>
          <span>date</span>
          <span>duration</span>
          <span>summarized key points</span>
        </div>

        {recordings.map((rec, index) => (
          <div key={rec.id} className="recording-row">
            <div className="recording-index">{index + 1}.</div>
            <div className="recording-title">{rec.title}</div>
            <div className="recording-date">{rec.dateUploaded}</div>
            <div className="recording-duration">
              {Math.floor(rec.duration / 60)}:{(rec.duration % 60).toString().padStart(2, '0')}
            </div>
            <div className="summarized-key">{rec.summary || rec.transcript}</div>
            <button onClick={() => toggleExpand(rec.id)} className="view-transcript-btn">
              view full transcript
            </button>

            {expandedId === rec.id && (
              <div className="transcript-wrapper">
                <div className="outer-shadow" />

                <div className="transcript-card">
                  <div className="side-label left">full transcript</div>

                  <div className={`transcript-content ${showFullTranscript ? 'expanded' : ''}`}>
                    <p>{rec.transcript}</p>
                  </div>

                  <div
                    className="watch-more"
                    onClick={() => setShowFullTranscript(prev => !prev)}
                  >
                    {showFullTranscript ? 'Show less' : 'Watch more...'}
                  </div>

                  <div className="side-label right">full transcript</div>
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

export default Dashboard;
