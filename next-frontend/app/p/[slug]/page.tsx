'use client';
import {use, useState, useRef, useEffect} from 'react';

const sampleMessages = [
  { id: 1, role: 'user', content: 'Can you analyze the agricultural data?' },
  { id: 2, role: 'assistant', content: 'I\'d be happy to help analyze the agricultural data. What specific aspects would you like to explore?' },
  { id: 3, role: 'user', content: 'Show me trends in corn stocks over time.' },
  { id: 4, role: 'assistant', content: 'I\'ve loaded the visualization showing corn stock trends. You can see there are significant seasonal variations, with peaks typically occurring after harvest seasons.' },
];

export default function PlotPage({
  params
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = use(params);
  const baseUrl = process.env.NEXT_PUBLIC_DEFAULT_IFRAME_URL || 'http://localhost:3000';
  const iframeUrl = `${baseUrl}/p/${slug}`;
  const [input, setInput] = useState('');
  const [isCollapsed, setIsCollapsed] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);


  const handleKeyPress = async (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      const newMessage = { id: sampleMessages.length + 1, role: 'user', content: input };
      sampleMessages.push(newMessage);
      setInput('');

      try {
        const response = await fetch('/api/messages', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ message: input, slug: slug }),
        });

        if (!response.ok) {
          throw new Error('Failed to send message');
        }
        
        // Scroll to bottom after API call completes and DOM updates
        setTimeout(() => {
          messagesEndRef.current?.scrollIntoView();
        }, 20);
      } catch (error) {
        console.error('Error sending message:', error);
        // TODO: Add proper error handling UI
      }
    }
  };

  return (
    <div className="min-h-screen font-[family-name:var(--font-geist-sans)] light">
      <main className="h-screen">
        <div className={`chat-sidebar left-0 top-0 bottom-0 border-r border-gray-200 flex flex-col relative ${isCollapsed ? 'collapsed' : ''}`}>
          {/* Messages container */}
          <div className="messages-container overflow-hidden">
            <div className="messages-content p-4 w-[360px]">
              <div className="flex flex-col gap-4">
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
              <div ref={messagesEndRef} />
            </div>
          </div>
          <div className="p-4 border-t border-gray-200">
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyPress}
              placeholder="Explore the data..."
              className="w-full p-2 border rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-blue-500"
              rows={3}
            />
          </div>
        </div>
        <div className={`fixed right-0 top-0 bottom-0 ${isCollapsed ? 'left-[48px]' : 'left-[384px]'} bg-white transition-[left] duration-300 ease-in-out pointer-events-none border-l border-gray-200 z-20`}>
          <button 
            className="toggle-button"
            onClick={() => setIsCollapsed(!isCollapsed)}
            aria-label={isCollapsed ? 'Expand chat' : 'Collapse chat'}
          >
            {isCollapsed ? '›' : '‹'}
          </button>
          <iframe
            src={iframeUrl}
            className="w-full h-full border-0 pointer-events-auto"
            allow="fullscreen"
          />
        </div>
      </main>
    </div>
  );
}
