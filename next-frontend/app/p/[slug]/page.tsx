'use client';

export default function PlotPage({
  params: { slug },
}: {
  params: { slug: string };
}) {
  const baseUrl = process.env.NEXT_PUBLIC_DEFAULT_IFRAME_URL || 'http://localhost:3000';
  const iframeUrl = `${baseUrl}/p/${slug}`;

  return (
    <div className="min-h-screen">
      <iframe 
        src={iframeUrl}
        className="w-full h-screen border-0"
        allow="fullscreen"
      />
    </div>
  );
}
