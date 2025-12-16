import React, { useState, useCallback, useEffect } from 'react';

const UTMBuilder = () => {
  const [baseUrl, setBaseUrl] = useState('https://recruitin.nl');
  const [utmParams, setUtmParams] = useState({
    source: '',
    medium: '',
    campaign: '',
    content: '',
    term: ''
  });
  const [history, setHistory] = useState([]);
  const [copied, setCopied] = useState(false);
  const [activeTab, setActiveTab] = useState('builder');
  const [validationErrors, setValidationErrors] = useState({});

  // Load history from localStorage on mount
  useEffect(() => {
    const saved = localStorage.getItem('recruitin_utm_history');
    if (saved) {
      try {
        setHistory(JSON.parse(saved));
      } catch (e) {
        console.error('Failed to load history:', e);
      }
    }
  }, []);

  // Save history to localStorage when it changes
  useEffect(() => {
    localStorage.setItem('recruitin_utm_history', JSON.stringify(history));
  }, [history]);

  // UTM Validation - sanitize invalid characters
  const sanitizeUtmValue = (value, field) => {
    // Remove characters that break UTM tracking
    let sanitized = value
      .toLowerCase()
      .replace(/\s+/g, field === 'term' ? '+' : '_') // spaces to _ or + for term
      .replace(/[^a-z0-9_+\-]/g, '') // only allow alphanumeric, underscore, plus, hyphen
      .replace(/_{2,}/g, '_') // no double underscores
      .replace(/^_|_$/g, ''); // no leading/trailing underscores
    
    return sanitized;
  };

  // Validate UTM parameters
  const validateUtm = (field, value) => {
    const errors = { ...validationErrors };
    
    if (value && value !== sanitizeUtmValue(value, field)) {
      errors[field] = 'Bevat ongeldige tekens (auto-gecorrigeerd)';
    } else {
      delete errors[field];
    }
    
    setValidationErrors(errors);
  };

  // Preset options for Recruitin
  const presets = {
    source: [
      { value: 'linkedin', label: 'LinkedIn' },
      { value: 'facebook', label: 'Facebook' },
      { value: 'instagram', label: 'Instagram' },
      { value: 'google', label: 'Google' },
      { value: 'email', label: 'Email' },
      { value: 'direct', label: 'Direct' },
      { value: 'referral', label: 'Referral' }
    ],
    medium: [
      { value: 'social', label: 'Social (organic)' },
      { value: 'paid', label: 'Paid Ads' },
      { value: 'cpc', label: 'CPC' },
      { value: 'email', label: 'Email' },
      { value: 'banner', label: 'Banner' },
      { value: 'video', label: 'Video' },
      { value: 'carousel', label: 'Carousel' }
    ],
    campaign: [
      { value: 'arbeidsmarktkrapte_q4', label: 'Arbeidsmarktkrapte Q4' },
      { value: 'nocurenopay_2024', label: 'No Cure No Pay 2024' },
      { value: 'nocurenopay_2025', label: 'No Cure No Pay 2025' },
      { value: 'technisch_talent', label: 'Technisch Talent' },
      { value: 'regio_gelderland', label: 'Regio Gelderland' },
      { value: 'regio_overijssel', label: 'Regio Overijssel' },
      { value: 'regio_brabant', label: 'Regio Noord-Brabant' },
      { value: 'nieuwjaar_2025', label: 'Nieuwjaar 2025' },
      { value: 'kandidatentekort_q1', label: 'Kandidatentekort Q1' }
    ],
    content: [
      { value: 'testimonial', label: 'Testimonial' },
      { value: 'statistics', label: 'Statistics' },
      { value: 'tips', label: 'Tips/Listicle' },
      { value: 'case_study', label: 'Case Study' },
      { value: 'video_ad', label: 'Video Ad' },
      { value: 'image_ad', label: 'Image Ad' },
      { value: 'carousel_ad', label: 'Carousel Ad' }
    ]
  };

  // Landing pages
  const landingPages = [
    { value: 'https://recruitin.nl', label: 'Homepage' },
    { value: 'https://recruitin.nl/contact', label: 'Contact' },
    { value: 'https://recruitin.nl/diensten', label: 'Diensten' },
    { value: 'https://recruitin.nl/over-ons', label: 'Over Ons' },
    { value: 'https://kandidatentekort.nl', label: 'Kandidatentekort.nl' },
    { value: 'https://recruitmentapk.nl', label: 'RecruitmentAPK.nl' }
  ];

  // Generate UTM URL
  const generateUrl = useCallback(() => {
    const params = new URLSearchParams();
    
    if (utmParams.source) params.append('utm_source', utmParams.source);
    if (utmParams.medium) params.append('utm_medium', utmParams.medium);
    if (utmParams.campaign) params.append('utm_campaign', utmParams.campaign);
    if (utmParams.content) params.append('utm_content', utmParams.content);
    if (utmParams.term) params.append('utm_term', utmParams.term);
    
    const queryString = params.toString();
    return queryString ? `${baseUrl}?${queryString}` : baseUrl;
  }, [baseUrl, utmParams]);

  const generatedUrl = generateUrl();

  // Update UTM param with validation
  const updateUtmParam = (field, value) => {
    const sanitized = sanitizeUtmValue(value, field);
    validateUtm(field, value);
    setUtmParams(prev => ({ ...prev, [field]: sanitized }));
  };

  // Copy to clipboard
  const copyToClipboard = async () => {
    try {
      await navigator.clipboard.writeText(generatedUrl);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      const textArea = document.createElement('textarea');
      textArea.value = generatedUrl;
      document.body.appendChild(textArea);
      textArea.select();
      document.execCommand('copy');
      document.body.removeChild(textArea);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  // Save to history
  const saveToHistory = () => {
    if (utmParams.source && utmParams.medium && utmParams.campaign) {
      const newEntry = {
        id: Date.now(),
        url: generatedUrl,
        params: { ...utmParams },
        baseUrl,
        timestamp: new Date().toLocaleString('nl-NL')
      };
      setHistory(prev => [newEntry, ...prev.slice(0, 19)]);
    }
  };

  // Load from history
  const loadFromHistory = (entry) => {
    setBaseUrl(entry.baseUrl);
    setUtmParams(entry.params);
    setActiveTab('builder');
  };

  // Delete from history
  const deleteFromHistory = (id) => {
    setHistory(prev => prev.filter(entry => entry.id !== id));
  };

  // Clear form
  const clearForm = () => {
    setUtmParams({
      source: '',
      medium: '',
      campaign: '',
      content: '',
      term: ''
    });
    setValidationErrors({});
  };

  // Export history as CSV
  const exportHistory = () => {
    const headers = ['Timestamp', 'URL', 'Source', 'Medium', 'Campaign', 'Content', 'Term'];
    const rows = history.map(entry => [
      entry.timestamp,
      entry.url,
      entry.params.source,
      entry.params.medium,
      entry.params.campaign,
      entry.params.content,
      entry.params.term
    ]);
    
    const csv = [headers, ...rows].map(row => row.map(cell => `"${cell || ''}"`).join(',')).join('\n');
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `recruitin_utm_history_${new Date().toISOString().split('T')[0]}.csv`;
    a.click();
  };

  // Quick templates
  const quickTemplates = [
    {
      name: 'LinkedIn Organic Post',
      params: { source: 'linkedin', medium: 'social', campaign: '', content: '', term: '' }
    },
    {
      name: 'Meta Paid Ad',
      params: { source: 'facebook', medium: 'paid', campaign: '', content: 'image_ad', term: '' }
    },
    {
      name: 'Google Ads',
      params: { source: 'google', medium: 'cpc', campaign: '', content: '', term: '' }
    },
    {
      name: 'Email Newsletter',
      params: { source: 'email', medium: 'email', campaign: 'newsletter', content: '', term: '' }
    },
    {
      name: 'Instagram Story',
      params: { source: 'instagram', medium: 'social', campaign: '', content: 'story', term: '' }
    }
  ];

  const applyTemplate = (template) => {
    setUtmParams(prev => ({ ...prev, ...template.params }));
    setValidationErrors({});
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 p-4 md:p-8">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center gap-3 mb-4">
            <div className="w-12 h-12 bg-gradient-to-br from-emerald-400 to-cyan-500 rounded-xl flex items-center justify-center">
              <span className="text-2xl">🔗</span>
            </div>
            <div className="text-left">
              <h1 className="text-2xl md:text-3xl font-bold text-white">UTM Builder</h1>
              <p className="text-slate-400 text-sm">Recruitin Marketing Tool</p>
            </div>
          </div>
        </div>

        {/* Tabs */}
        <div className="flex gap-2 mb-6">
          <button
            onClick={() => setActiveTab('builder')}
            className={`px-4 py-2 rounded-lg font-medium transition-all ${
              activeTab === 'builder'
                ? 'bg-emerald-500 text-white'
                : 'bg-slate-700 text-slate-300 hover:bg-slate-600'
            }`}
          >
            🛠️ Builder
          </button>
          <button
            onClick={() => setActiveTab('history')}
            className={`px-4 py-2 rounded-lg font-medium transition-all ${
              activeTab === 'history'
                ? 'bg-emerald-500 text-white'
                : 'bg-slate-700 text-slate-300 hover:bg-slate-600'
            }`}
          >
            📋 History ({history.length})
          </button>
        </div>

        {activeTab === 'builder' ? (
          <>
            {/* Quick Templates */}
            <div className="bg-slate-800/50 rounded-xl p-4 mb-6 border border-slate-700">
              <h3 className="text-sm font-medium text-slate-400 mb-3">⚡ Quick Templates</h3>
              <div className="flex flex-wrap gap-2">
                {quickTemplates.map(template => (
                  <button
                    key={template.name}
                    onClick={() => applyTemplate(template)}
                    className="px-3 py-1.5 bg-slate-700 hover:bg-slate-600 text-slate-300 text-sm rounded-lg transition-colors"
                  >
                    {template.name}
                  </button>
                ))}
              </div>
            </div>

            {/* Main Builder */}
            <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700 mb-6">
              {/* Base URL */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-slate-300 mb-2">🌐 Landing Page URL</label>
                <div className="flex gap-2 flex-col md:flex-row">
                  <select
                    value={baseUrl}
                    onChange={(e) => setBaseUrl(e.target.value)}
                    className="flex-1 bg-slate-700 border border-slate-600 rounded-lg px-4 py-3 text-white focus:ring-2 focus:ring-emerald-500"
                  >
                    {landingPages.map(page => (
                      <option key={page.value} value={page.value}>{page.label}</option>
                    ))}
                  </select>
                  <input
                    type="text"
                    value={baseUrl}
                    onChange={(e) => setBaseUrl(e.target.value)}
                    placeholder="Of type custom URL..."
                    className="flex-1 bg-slate-700 border border-slate-600 rounded-lg px-4 py-3 text-white placeholder-slate-500 focus:ring-2 focus:ring-emerald-500"
                  />
                </div>
              </div>

              {/* UTM Parameters Grid */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                {/* Source */}
                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-2">
                    utm_source <span className="text-emerald-400">*</span>
                    <span className="text-slate-500 font-normal ml-2">Traffic bron</span>
                  </label>
                  <select
                    value={utmParams.source}
                    onChange={(e) => setUtmParams(prev => ({ ...prev, source: e.target.value }))}
                    className="w-full bg-slate-700 border border-slate-600 rounded-lg px-4 py-3 text-white focus:ring-2 focus:ring-emerald-500"
                  >
                    <option value="">Selecteer source...</option>
                    {presets.source.map(opt => (
                      <option key={opt.value} value={opt.value}>{opt.label}</option>
                    ))}
                  </select>
                </div>

                {/* Medium */}
                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-2">
                    utm_medium <span className="text-emerald-400">*</span>
                    <span className="text-slate-500 font-normal ml-2">Type marketing</span>
                  </label>
                  <select
                    value={utmParams.medium}
                    onChange={(e) => setUtmParams(prev => ({ ...prev, medium: e.target.value }))}
                    className="w-full bg-slate-700 border border-slate-600 rounded-lg px-4 py-3 text-white focus:ring-2 focus:ring-emerald-500"
                  >
                    <option value="">Selecteer medium...</option>
                    {presets.medium.map(opt => (
                      <option key={opt.value} value={opt.value}>{opt.label}</option>
                    ))}
                  </select>
                </div>

                {/* Campaign */}
                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-2">
                    utm_campaign <span className="text-emerald-400">*</span>
                    <span className="text-slate-500 font-normal ml-2">Campagne naam</span>
                  </label>
                  <select
                    value={utmParams.campaign}
                    onChange={(e) => setUtmParams(prev => ({ ...prev, campaign: e.target.value }))}
                    className="w-full bg-slate-700 border border-slate-600 rounded-lg px-4 py-3 text-white focus:ring-2 focus:ring-emerald-500"
                  >
                    <option value="">Selecteer of type...</option>
                    {presets.campaign.map(opt => (
                      <option key={opt.value} value={opt.value}>{opt.label}</option>
                    ))}
                  </select>
                  <input
                    type="text"
                    value={utmParams.campaign}
                    onChange={(e) => updateUtmParam('campaign', e.target.value)}
                    placeholder="Of type custom campaign..."
                    className={`w-full mt-2 bg-slate-700 border rounded-lg px-4 py-2 text-white text-sm placeholder-slate-500 focus:ring-2 focus:ring-emerald-500 ${
                      validationErrors.campaign ? 'border-amber-500' : 'border-slate-600'
                    }`}
                  />
                  {validationErrors.campaign && (
                    <p className="text-amber-400 text-xs mt-1">⚠️ {validationErrors.campaign}</p>
                  )}
                </div>

                {/* Content */}
                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-2">
                    utm_content
                    <span className="text-slate-500 font-normal ml-2">A/B test variant</span>
                  </label>
                  <select
                    value={utmParams.content}
                    onChange={(e) => setUtmParams(prev => ({ ...prev, content: e.target.value }))}
                    className="w-full bg-slate-700 border border-slate-600 rounded-lg px-4 py-3 text-white focus:ring-2 focus:ring-emerald-500"
                  >
                    <option value="">Optioneel...</option>
                    {presets.content.map(opt => (
                      <option key={opt.value} value={opt.value}>{opt.label}</option>
                    ))}
                  </select>
                  <input
                    type="text"
                    value={utmParams.content}
                    onChange={(e) => updateUtmParam('content', e.target.value)}
                    placeholder="Of type custom content..."
                    className={`w-full mt-2 bg-slate-700 border rounded-lg px-4 py-2 text-white text-sm placeholder-slate-500 focus:ring-2 focus:ring-emerald-500 ${
                      validationErrors.content ? 'border-amber-500' : 'border-slate-600'
                    }`}
                  />
                  {validationErrors.content && (
                    <p className="text-amber-400 text-xs mt-1">⚠️ {validationErrors.content}</p>
                  )}
                </div>

                {/* Term */}
                <div className="md:col-span-2">
                  <label className="block text-sm font-medium text-slate-300 mb-2">
                    utm_term
                    <span className="text-slate-500 font-normal ml-2">Keywords (vooral voor Google Ads)</span>
                  </label>
                  <input
                    type="text"
                    value={utmParams.term}
                    onChange={(e) => updateUtmParam('term', e.target.value)}
                    placeholder="technisch+personeel, recruitment+gelderland, etc."
                    className={`w-full bg-slate-700 border rounded-lg px-4 py-3 text-white placeholder-slate-500 focus:ring-2 focus:ring-emerald-500 ${
                      validationErrors.term ? 'border-amber-500' : 'border-slate-600'
                    }`}
                  />
                  {validationErrors.term && (
                    <p className="text-amber-400 text-xs mt-1">⚠️ {validationErrors.term}</p>
                  )}
                </div>
              </div>

              {/* Clear Button */}
              <div className="flex justify-end">
                <button
                  onClick={clearForm}
                  className="px-4 py-2 text-slate-400 hover:text-white transition-colors"
                >
                  🗑️ Clear Form
                </button>
              </div>
            </div>

            {/* Generated URL */}
            <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700">
              <div className="flex items-center justify-between mb-3">
                <h3 className="text-sm font-medium text-slate-300">📋 Generated URL</h3>
                <span className={`text-xs px-2 py-1 rounded ${
                  utmParams.source && utmParams.medium && utmParams.campaign
                    ? 'bg-emerald-500/20 text-emerald-400'
                    : 'bg-amber-500/20 text-amber-400'
                }`}>
                  {utmParams.source && utmParams.medium && utmParams.campaign
                    ? '✓ Complete'
                    : '⚠ Vul source, medium & campaign in'}
                </span>
              </div>
              
              <div className="bg-slate-900 rounded-lg p-4 mb-4 overflow-x-auto">
                <code className="text-emerald-400 text-sm break-all">
                  {generatedUrl}
                </code>
              </div>

              <div className="flex gap-3">
                <button
                  onClick={copyToClipboard}
                  className={`flex-1 py-3 px-4 rounded-lg font-medium transition-all ${
                    copied
                      ? 'bg-emerald-500 text-white'
                      : 'bg-gradient-to-r from-emerald-500 to-cyan-500 text-white hover:from-emerald-600 hover:to-cyan-600'
                  }`}
                >
                  {copied ? '✓ Gekopieerd!' : '📋 Copy URL'}
                </button>
                <button
                  onClick={saveToHistory}
                  disabled={!utmParams.source || !utmParams.medium || !utmParams.campaign}
                  className="px-4 py-3 bg-slate-700 hover:bg-slate-600 disabled:bg-slate-800 disabled:text-slate-600 text-white rounded-lg font-medium transition-colors"
                >
                  💾 Save
                </button>
              </div>
            </div>

            {/* UTM Parameters Cheat Sheet */}
            <div className="mt-6 bg-slate-800/30 rounded-xl p-4 border border-slate-700/50">
              <h3 className="text-sm font-medium text-slate-400 mb-3">📚 UTM Parameters Cheat Sheet</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                <div>
                  <p className="text-slate-300"><span className="text-emerald-400">utm_source</span> — Waar komt traffic vandaan?</p>
                  <p className="text-slate-500 text-xs">linkedin, facebook, google, email</p>
                </div>
                <div>
                  <p className="text-slate-300"><span className="text-emerald-400">utm_medium</span> — Type marketing kanaal</p>
                  <p className="text-slate-500 text-xs">social, paid, cpc, email, banner</p>
                </div>
                <div>
                  <p className="text-slate-300"><span className="text-emerald-400">utm_campaign</span> — Naam van je campagne</p>
                  <p className="text-slate-500 text-xs">arbeidsmarktkrapte_q4, nocurenopay_2024</p>
                </div>
                <div>
                  <p className="text-slate-300"><span className="text-cyan-400">utm_content</span> — A/B test identifier</p>
                  <p className="text-slate-500 text-xs">video_ad, image_ad, testimonial_v2</p>
                </div>
              </div>
            </div>
          </>
        ) : (
          /* History Tab */
          <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-medium text-white">📋 Saved URLs</h3>
              {history.length > 0 && (
                <button
                  onClick={exportHistory}
                  className="px-3 py-1.5 bg-slate-700 hover:bg-slate-600 text-slate-300 text-sm rounded-lg transition-colors"
                >
                  📥 Export CSV
                </button>
              )}
            </div>

            {history.length === 0 ? (
              <div className="text-center py-12">
                <div className="text-4xl mb-3">📭</div>
                <p className="text-slate-400">Nog geen opgeslagen URLs</p>
                <p className="text-slate-500 text-sm">Maak een URL en klik op "Save"</p>
              </div>
            ) : (
              <div className="space-y-3">
                {history.map(entry => (
                  <div
                    key={entry.id}
                    className="bg-slate-700/50 rounded-lg p-4 border border-slate-600"
                  >
                    <div className="flex items-start justify-between mb-2">
                      <div className="flex gap-2 flex-wrap">
                        <span className="px-2 py-0.5 bg-emerald-500/20 text-emerald-400 text-xs rounded">
                          {entry.params.source}
                        </span>
                        <span className="px-2 py-0.5 bg-cyan-500/20 text-cyan-400 text-xs rounded">
                          {entry.params.medium}
                        </span>
                        <span className="px-2 py-0.5 bg-purple-500/20 text-purple-400 text-xs rounded">
                          {entry.params.campaign}
                        </span>
                      </div>
                      <span className="text-slate-500 text-xs">{entry.timestamp}</span>
                    </div>
                    <code className="text-slate-300 text-xs break-all block mb-3">
                      {entry.url}
                    </code>
                    <div className="flex gap-2">
                      <button
                        onClick={() => {
                          navigator.clipboard.writeText(entry.url);
                          setCopied(true);
                          setTimeout(() => setCopied(false), 2000);
                        }}
                        className="px-3 py-1 bg-slate-600 hover:bg-slate-500 text-white text-xs rounded transition-colors"
                      >
                        📋 Copy
                      </button>
                      <button
                        onClick={() => loadFromHistory(entry)}
                        className="px-3 py-1 bg-slate-600 hover:bg-slate-500 text-white text-xs rounded transition-colors"
                      >
                        ↩️ Load
                      </button>
                      <button
                        onClick={() => deleteFromHistory(entry.id)}
                        className="px-3 py-1 bg-red-500/20 hover:bg-red-500/30 text-red-400 text-xs rounded transition-colors"
                      >
                        🗑️
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* Footer */}
        <div className="text-center mt-8 text-slate-500 text-sm">
          <p>Recruitin UTM Builder v2.0 • Track je marketing performance in Google Analytics</p>
        </div>
      </div>
    </div>
  );
};

export default UTMBuilder;
