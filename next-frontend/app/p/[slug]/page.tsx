'use client';
import {use, useState, useRef, KeyboardEvent} from 'react';

type Message = {
  id: number;
  role: 'user' | 'assistant' | 'system';
  content: string;
};

const sampleMessages: Message[] = [
  { id: 1, role: 'user', content: "Let's dive into this dataset" },
  { id: 2, role: 'assistant', content: 'Sounds good, I can help with visualizations, sql queries, and more.' },
  // { id: 3, role: 'system', content: 'Loading visualization Sounds good, I can help with...' }
];


export default function PlotPage({
  params
}: {
  params: Promise<{ slug: string}>;
}) {
  const { slug } = use(params);
  const baseUrl = process.env.NEXT_PUBLIC_DEFAULT_IFRAME_URL || 'http://localhost:3000';
  const iframeUrl = `${baseUrl}/d/${slug}`;
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState<Message[]>(sampleMessages);
  const [isLoading, setIsLoading] = useState(false);
  const [isCollapsed, setIsCollapsed] = useState(false);

  const messagesEndRef = useRef<HTMLDivElement>(null);


  const handleKeyPress = async (e: KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      const newMessage: Message = { id: messages.length + 1, role: 'user', content: input };
      setMessages((prev: Message[]) => [...prev, newMessage]);
      setInput('');
      setIsLoading(true);

      try {
        // Scroll to bottom immediately after user message
        setTimeout(() => {
          messagesEndRef.current?.scrollIntoView();
        }, 24);

        const response = await fetch('/api/messages', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ message: input, slug: slug }),
        });

        const reader = response.body?.getReader();
        const decoder = new TextDecoder();

        if (!reader) {
          throw new Error('No reader available');
        }

        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          const chunk = decoder.decode(value);
          const events = chunk.split('\n\n').filter(Boolean);

          for (const event of events) {
            if (event.startsWith('data: ')) {
              console.log('~~~~~~~~~~~~~~~\n\nReceived event:', event);
              const data = JSON.parse(event.slice(6));
              
              switch (data.type) {
                case 'start':
                  setMessages(prev => [...prev, { 
                    id: prev.length + 1, 
                    role: 'system', 
                    content: data.message 
                  }]);
                  break;
                case 'commit':
                  setMessages(prev => [...prev, {
                    id: prev.length + 1,
                    role: 'system',
                    content: `Committed changes: ${data.message}`
                  }]);
                  break;
                case 'summary':
                  setMessages(prev => [...prev, {
                    id: prev.length + 1,
                    role: 'assistant',
                    content: data.message
                  }]);
                  break;
                case 'complete':
                  // Refresh the iframe or update chart as needed
                  break;
              }
              
              setTimeout(() => {
                messagesEndRef.current?.scrollIntoView();
              }, 24);
            }
          }
        }

        setIsLoading(false);
      } catch (error) {
        setIsLoading(false);
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
              {messages.map((message) => (
                <div
                  key={message.id}
                  className={`max-w-[85%] ${
                    message.role === 'system' 
                      ? 'text-gray-500 text-sm px-2 text-center mx-auto my-2'
                      : `p-3 rounded-lg shadow-sm border ${
                          message.role === 'user'
                            ? 'bg-blue-100 ml-auto border-blue-200'
                            : 'bg-gray-100 border-gray-200'
                        }`
                  }`}
                >
                  {message.content}
                </div>
              ))}
              </div>
              {isLoading && (
                <div className="inline-flex gap-1 pt-3 pb-2 px-3 bg-gray-200 rounded-lg mt-4 shadow-sm border border-gray-300">
                  <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce [animation-delay:-0.3s]"></div>
                  <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce [animation-delay:-0.15s]"></div>
                  <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce"></div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>
          </div>
          <div className="p-4 border-t border-gray-200">
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyPress}
              placeholder="Explore the data..."
              className="w-full p-2 border rounded-lg resize-none focus:outline-none"
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
