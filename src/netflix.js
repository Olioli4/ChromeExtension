// netflix.js
// Extract Netflix title and image from the current page (to be injected by background.js)
export function extractNetflixTitleAndImage() {
  try {
    // Try to find a script tag with application/ld+json (Netflix uses this for metadata)
    const script = document.querySelector('script[type="application/ld+json"]');
    if (script) {
      let json;
      try {
        json = JSON.parse(script.textContent);
      } catch (e) {
        return { success: false, error: 'Could not parse ld+json', url: window.location.href };
      }
      if (json && json.name && json.image) {
        return {
          success: true,
          name: json.name,
          image: json.image,
          url: window.location.href
        };
      }
    }
    // Fallback: try to find a title and image in the markup
    const titleEl = document.querySelector('h1, .title-logo, .video-title, .previewModal--player-titleTreatment-logo');
    const imgEl = document.querySelector('img');
    return {
      success: true,
      name: titleEl ? (titleEl.textContent || titleEl.alt || 'No title') : 'No title',
      image: imgEl ? imgEl.src : '',
      url: window.location.href
    };
  } catch (e) {
    return { success: false, error: 'Error parsing Netflix page: ' + e.message, url: window.location.href };
  }
}
