
'use client';
import { useState } from 'react';

const sampleMessages = [
  { id: 1, role: 'user', content: 'Can you analyze the agricultural data?' },
  { id: 2, role: 'assistant', content: 'I\'d be happy to help analyze the agricultural data. What specific aspects would you like to explore?' },
  { id: 3, role: 'user', content: 'Show me trends in corn stocks over time.' },
  { id: 4, role: 'assistant', content: 'I\'ve loaded the visualization showing corn stock trends. You can see there are significant seasonal variations, with peaks typically occurring after harvest seasons.' },
];

export default function Home() {
  const iframeUrl = process.env.NEXT_PUBLIC_DEFAULT_IFRAME_URL || 'http://localhost:3000/p/agricultural-commodity-beginning-stocks-over-time';
  const [input, setInput] = useState('');
  
  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      // Handle send message here
      setInput('');
    }
  };

  return (
    <div className="min-h-screen font-[family-name:var(--font-geist-sans)] light">
      <main className="grid grid-cols-3 h-screen">
        {/* Left pane - Chat */}
        <div className="col-span-1 border-r border-gray-200 flex flex-col h-full">
          {/* Messages container */}
          <div className="flex-1 overflow-y-auto flex flex-col-reverse p-4 gap-4">
            {sampleMessages.map((message) => (
              <div
                key={message.id}
                className={`max-w-[85%] p-3 rounded-lg ${
                  message.role === 'user'
                    ? 'bg-blue-100 ml-auto'
                    : 'bg-gray-100'
                }`}
              >
                {message.content}
              </div>
            ))}
          </div>
          
          {/* Input box */}
          <div className="p-4 border-t border-gray-200">
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyPress}
              placeholder="Type a message... (Enter to send)"
              className="w-full p-2 border rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-blue-500"
              rows={3}
            />
          </div>
        </div>
        
        {/* Right pane with iframe */}
        <div className="col-span-2">
          <iframe 
            src={iframeUrl}
            className="w-full h-full border-0"
            allow="fullscreen"
          />
        </div>
      </main>
    </div>
  );
}
