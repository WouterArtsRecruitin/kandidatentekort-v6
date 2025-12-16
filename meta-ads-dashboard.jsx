import React, { useState, useMemo } from 'react';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell, ScatterChart, Scatter, ZAxis } from 'recharts';
import { TrendingUp, TrendingDown, AlertTriangle, Target, DollarSign, Users, MousePointer, Eye, Zap, RefreshCw, Award, AlertCircle } from 'lucide-react';

// Mock data - vervang met echte Meta API data via Zapier
const campaignData = [
  { id: 1, name: 'Kandidatentekort - Lookalike 1%', audience: 'Lookalike 1%', status: 'active', spend: 1250, impressions: 45000, clicks: 890, leads: 42, cpl: 29.76, ctr: 1.98, convRate: 4.72, frequency: 2.1, roas: 3.2 },
  { id: 2, name: 'Kandidatentekort - HR Managers', audience: 'HR Managers', status: 'active', spend: 980, impressions: 32000, clicks: 640, leads: 28, cpl: 35.00, ctr: 2.0, convRate: 4.38, frequency: 2.8, roas: 2.8 },
  { id: 3, name: 'Kandidatentekort - Technische Directeuren', audience: 'Tech Directors', status: 'active', spend: 1450, impressions: 28000, clicks: 560, leads: 35, cpl: 41.43, ctr: 2.0, convRate: 6.25, frequency: 3.2, roas: 2.4 },
  { id: 4, name: 'RecruitmentAPK - MKB Owners', audience: 'MKB Owners', status: 'active', spend: 750, impressions: 22000, clicks: 380, leads: 18, cpl: 41.67, ctr: 1.73, convRate: 4.74, frequency: 1.8, roas: 2.1 },
  { id: 5, name: 'RecruitmentAPK - Retargeting', audience: 'Retargeting', status: 'active', spend: 320, impressions: 8500, clicks: 245, leads: 22, cpl: 14.55, ctr: 2.88, convRate: 8.98, frequency: 4.1, roas: 5.8 },
  { id: 6, name: 'Lookalike - Manufacturing', audience: 'Manufacturing LAL', status: 'paused', spend: 650, impressions: 18000, clicks: 270, leads: 8, cpl: 81.25, ctr: 1.5, convRate: 2.96, frequency: 2.4, roas: 1.2 },
  { id: 7, name: 'Interest - Oil & Gas', audience: 'Oil & Gas Interest', status: 'active', spend: 890, impressions: 25000, clicks: 425, leads: 19, cpl: 46.84, ctr: 1.7, convRate: 4.47, frequency: 2.6, roas: 1.9 },
  { id: 8, name: 'Interest - Construction', audience: 'Construction', status: 'active', spend: 720, impressions: 21000, clicks: 378, leads: 16, cpl: 45.00, ctr: 1.8, convRate: 4.23, frequency: 2.3, roas: 2.0 },
];

const creativeData = [
  { id: 1, name: 'Video - "Stop Scrolling"', format: 'Video', impressions: 52000, clicks: 1040, leads: 48, ctr: 2.0, cpl: 28.50, status: 'winner', daysActive: 14 },
  { id: 2, name: 'Carousel - 5 Redenen', format: 'Carousel', impressions: 38000, clicks: 684, leads: 32, ctr: 1.8, cpl: 32.00, status: 'testing', daysActive: 7 },
  { id: 3, name: 'Static - Vacature Analyse', format: 'Image', impressions: 45000, clicks: 765, leads: 28, ctr: 1.7, cpl: 38.50, status: 'active', daysActive: 21 },
  { id: 4, name: 'Video - Testimonial Klant', format: 'Video', impressions: 28000, clicks: 476, leads: 24, ctr: 1.7, cpl: 35.00, status: 'active', daysActive: 10 },
  { id: 5, name: 'Static - ROI Calculator', format: 'Image', impressions: 31000, clicks: 434, leads: 15, ctr: 1.4, cpl: 52.00, status: 'fatigued', daysActive: 28 },
  { id: 6, name: 'Video - "Waarom 78% faalt"', format: 'Video', impressions: 22000, clicks: 506, leads: 29, ctr: 2.3, cpl: 24.00, status: 'winner', daysActive: 5 },
];

const weeklyTrends = [
  { week: 'W44', spend: 4200, leads: 145, cpl: 28.97, ctr: 1.82, convRate: 4.8 },
  { week: 'W45', spend: 4800, leads: 168, cpl: 28.57, ctr: 1.95, convRate: 5.1 },
  { week: 'W46', spend: 5200, leads: 178, cpl: 29.21, ctr: 1.88, convRate: 4.9 },
  { week: 'W47', spend: 5100, leads: 182, cpl: 28.02, ctr: 2.02, convRate: 5.3 },
  { week: 'W48', spend: 5500, leads: 195, cpl: 28.21, ctr: 2.08, convRate: 5.5 },
  { week: 'W49', spend: 6010, leads: 188, cpl: 31.97, ctr: 1.92, convRate: 4.7 },
];

const funnelData = [
  { stage: 'Impressies', value: 199500, color: '#3b82f6' },
  { stage: 'Clicks', value: 3788, color: '#6366f1' },
  { stage: 'Landingpage', value: 3030, color: '#8b5cf6' },
  { stage: 'Form Start', value: 1212, color: '#a855f7' },
  { stage: 'Leads', value: 188, color: '#22c55e' },
];

const COLORS = ['#3b82f6', '#22c55e', '#f59e0b', '#ef4444', '#8b5cf6', '#06b6d4'];

export default function MetaDashboard() {
  const [activeTab, setActiveTab] = useState('overview');
  const [dateRange, setDateRange] = useState('30d');
  
  const totals = useMemo(() => {
    const active = campaignData.filter(c => c.status === 'active');
    return {
      spend: active.reduce((sum, c) => sum + c.spend, 0),
      leads: active.reduce((sum, c) => sum + c.leads, 0),
      impressions: active.reduce((sum, c) => sum + c.impressions, 0),
      clicks: active.reduce((sum, c) => sum + c.clicks, 0),
      avgCpl: active.reduce((sum, c) => sum + c.spend, 0) / active.reduce((sum, c) => sum + c.leads, 0),
      avgCtr: (active.reduce((sum, c) => sum + c.clicks, 0) / active.reduce((sum, c) => sum + c.impressions, 0) * 100),
      avgConvRate: (active.reduce((sum, c) => sum + c.leads, 0) / active.reduce((sum, c) => sum + c.clicks, 0) * 100),
    };
  }, []);

  const alerts = useMemo(() => {
    const issues = [];
    campaignData.forEach(c => {
      if (c.frequency > 3) issues.push({ type: 'fatigue', campaign: c.name, value: c.frequency, severity: 'high' });
      if (c.cpl > 50) issues.push({ type: 'cpl', campaign: c.name, value: c.cpl, severity: 'medium' });
      if (c.ctr < 1.5) issues.push({ type: 'ctr', campaign: c.name, value: c.ctr, severity: 'low' });
    });
    creativeData.forEach(cr => {
      if (cr.status === 'fatigued') issues.push({ type: 'creative_fatigue', campaign: cr.name, value: cr.daysActive, severity: 'high' });
    });
    return issues;
  }, []);

  const recommendations = useMemo(() => {
    const recs = [];
    
    // Winner scaling
    const winners = creativeData.filter(c => c.status === 'winner');
    if (winners.length > 0) {
      recs.push({ type: 'scale', priority: 'high', text: `Scale ${winners.length} winning creatives naar nieuwe audiences`, action: 'Verhoog budget 20%' });
    }
    
    // Fatigue issues
    const fatigued = campaignData.filter(c => c.frequency > 3);
    if (fatigued.length > 0) {
      recs.push({ type: 'refresh', priority: 'high', text: `${fatigued.length} campagnes hebben creative fatigue (freq >3)`, action: 'Nieuwe creatives nodig' });
    }
    
    // High CPL
    const highCpl = campaignData.filter(c => c.cpl > 50 && c.status === 'active');
    if (highCpl.length > 0) {
      recs.push({ type: 'optimize', priority: 'medium', text: `${highCpl.length} campagnes met CPL >€50`, action: 'Pauseer of optimize targeting' });
    }
    
    // Top performer
    const topPerformer = campaignData.filter(c => c.status === 'active').sort((a, b) => a.cpl - b.cpl)[0];
    if (topPerformer) {
      recs.push({ type: 'lookalike', priority: 'medium', text: `Beste performer: ${topPerformer.audience} (€${topPerformer.cpl.toFixed(2)} CPL)`, action: 'Maak Lookalike van converters' });
    }
    
    // Retargeting opportunity
    const retargeting = campaignData.find(c => c.audience === 'Retargeting');
    if (retargeting && retargeting.roas > 4) {
      recs.push({ type: 'budget', priority: 'high', text: `Retargeting ROAS ${retargeting.roas}x - onderbenut`, action: 'Verhoog retargeting budget 50%' });
    }
    
    return recs;
  }, []);

  const MetricCard = ({ title, value, change, icon: Icon, format = 'number', good = 'up' }) => {
    const isPositive = good === 'up' ? change > 0 : change < 0;
    return (
      <div className="bg-white rounded-xl p-5 shadow-sm border border-gray-100">
        <div className="flex justify-between items-start mb-3">
          <span className="text-gray-500 text-sm font-medium">{title}</span>
          <Icon className="w-5 h-5 text-gray-400" />
        </div>
        <div className="flex items-end gap-2">
          <span className="text-2xl font-bold text-gray-900">
            {format === 'currency' && '€'}{typeof value === 'number' ? value.toLocaleString('nl-NL', { maximumFractionDigits: 2 }) : value}{format === 'percent' && '%'}
          </span>
          {change !== undefined && (
            <span className={`flex items-center text-sm font-medium ${isPositive ? 'text-green-600' : 'text-red-500'}`}>
              {isPositive ? <TrendingUp className="w-4 h-4 mr-1" /> : <TrendingDown className="w-4 h-4 mr-1" />}
              {Math.abs(change)}%
            </span>
          )}
        </div>
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      {/* Header */}
      <div className="mb-6">
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Meta Ads Dashboard</h1>
            <p className="text-gray-500 mt-1">Recruitin B.V. | kandidatentekort.nl & RecruitmentAPK</p>
          </div>
          <div className="flex gap-3">
            <select 
              value={dateRange} 
              onChange={(e) => setDateRange(e.target.value)}
              className="px-4 py-2 bg-white border border-gray-200 rounded-lg text-sm font-medium"
            >
              <option value="7d">Laatste 7 dagen</option>
              <option value="30d">Laatste 30 dagen</option>
              <option value="90d">Laatste 90 dagen</option>
            </select>
            <button className="px-4 py-2 bg-blue-600 text-white rounded-lg text-sm font-medium flex items-center gap-2 hover:bg-blue-700">
              <RefreshCw className="w-4 h-4" /> Sync Meta
            </button>
          </div>
        </div>

        {/* Tabs */}
        <div className="flex gap-1 mt-4 bg-gray-100 p-1 rounded-lg w-fit">
          {['overview', 'campaigns', 'creatives', 'audiences', 'insights'].map(tab => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`px-4 py-2 rounded-md text-sm font-medium transition-all ${
                activeTab === tab ? 'bg-white text-gray-900 shadow-sm' : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              {tab.charAt(0).toUpperCase() + tab.slice(1)}
            </button>
          ))}
        </div>
      </div>

      {/* Alerts Banner */}
      {alerts.filter(a => a.severity === 'high').length > 0 && (
        <div className="mb-6 bg-amber-50 border border-amber-200 rounded-xl p-4">
          <div className="flex items-center gap-3">
            <AlertTriangle className="w-5 h-5 text-amber-600" />
            <div>
              <span className="font-medium text-amber-800">{alerts.filter(a => a.severity === 'high').length} kritieke alerts</span>
              <span className="text-amber-700 ml-2">Creative fatigue en hoge CPL detected</span>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'overview' && (
        <>
          {/* KPI Cards */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
            <MetricCard title="Total Spend" value={totals.spend} change={8.2} icon={DollarSign} format="currency" good="down" />
            <MetricCard title="Leads" value={totals.leads} change={12.5} icon={Users} />
            <MetricCard title="Gem. CPL" value={totals.avgCpl} change={-5.3} icon={Target} format="currency" good="down" />
            <MetricCard title="Conv. Rate" value={totals.avgConvRate} change={4.1} icon={Zap} format="percent" />
          </div>

          {/* Charts Row */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
            {/* Trend Chart */}
            <div className="bg-white rounded-xl p-5 shadow-sm border border-gray-100">
              <h3 className="font-semibold text-gray-900 mb-4">Performance Trend</h3>
              <ResponsiveContainer width="100%" height={280}>
                <LineChart data={weeklyTrends}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                  <XAxis dataKey="week" tick={{ fontSize: 12 }} />
                  <YAxis yAxisId="left" tick={{ fontSize: 12 }} />
                  <YAxis yAxisId="right" orientation="right" tick={{ fontSize: 12 }} />
                  <Tooltip />
                  <Legend />
                  <Line yAxisId="left" type="monotone" dataKey="leads" stroke="#22c55e" strokeWidth={2} name="Leads" />
                  <Line yAxisId="right" type="monotone" dataKey="cpl" stroke="#3b82f6" strokeWidth={2} name="CPL (€)" />
                </LineChart>
              </ResponsiveContainer>
            </div>

            {/* Funnel */}
            <div className="bg-white rounded-xl p-5 shadow-sm border border-gray-100">
              <h3 className="font-semibold text-gray-900 mb-4">Conversion Funnel</h3>
              <div className="space-y-3">
                {funnelData.map((stage, i) => {
                  const width = (stage.value / funnelData[0].value) * 100;
                  const dropoff = i > 0 ? ((funnelData[i-1].value - stage.value) / funnelData[i-1].value * 100).toFixed(1) : 0;
                  return (
                    <div key={stage.stage} className="relative">
                      <div className="flex justify-between text-sm mb-1">
                        <span className="font-medium text-gray-700">{stage.stage}</span>
                        <div className="flex items-center gap-3">
                          <span className="text-gray-900 font-semibold">{stage.value.toLocaleString()}</span>
                          {i > 0 && <span className="text-red-500 text-xs">-{dropoff}%</span>}
                        </div>
                      </div>
                      <div className="h-8 bg-gray-100 rounded-lg overflow-hidden">
                        <div 
                          className="h-full rounded-lg transition-all duration-500"
                          style={{ width: `${width}%`, backgroundColor: stage.color }}
                        />
                      </div>
                    </div>
                  );
                })}
              </div>
              <div className="mt-4 pt-4 border-t border-gray-100">
                <div className="flex justify-between text-sm">
                  <span className="text-gray-500">Overall Conversion Rate</span>
                  <span className="font-bold text-green-600">{(funnelData[4].value / funnelData[1].value * 100).toFixed(2)}%</span>
                </div>
              </div>
            </div>
          </div>

          {/* Recommendations */}
          <div className="bg-white rounded-xl p-5 shadow-sm border border-gray-100 mb-6">
            <h3 className="font-semibold text-gray-900 mb-4 flex items-center gap-2">
              <Zap className="w-5 h-5 text-amber-500" />
              AI Aanbevelingen
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {recommendations.map((rec, i) => (
                <div key={i} className={`p-4 rounded-lg border-l-4 ${
                  rec.priority === 'high' ? 'bg-red-50 border-red-500' : 
                  rec.priority === 'medium' ? 'bg-amber-50 border-amber-500' : 'bg-blue-50 border-blue-500'
                }`}>
                  <div className="flex justify-between items-start mb-2">
                    <span className="text-sm font-medium text-gray-900">{rec.text}</span>
                    <span className={`text-xs px-2 py-1 rounded-full font-medium ${
                      rec.priority === 'high' ? 'bg-red-100 text-red-700' : 
                      rec.priority === 'medium' ? 'bg-amber-100 text-amber-700' : 'bg-blue-100 text-blue-700'
                    }`}>{rec.priority}</span>
                  </div>
                  <span className="text-sm text-gray-600">→ {rec.action}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Campaign Performance Table */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
            <div className="p-5 border-b border-gray-100">
              <h3 className="font-semibold text-gray-900">Campaign Performance</h3>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Campagne</th>
                    <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase">Spend</th>
                    <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase">Leads</th>
                    <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase">CPL</th>
                    <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase">CTR</th>
                    <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase">Conv %</th>
                    <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase">Freq</th>
                    <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase">ROAS</th>
                    <th className="px-4 py-3 text-center text-xs font-medium text-gray-500 uppercase">Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-100">
                  {campaignData.sort((a, b) => a.cpl - b.cpl).map(campaign => (
                    <tr key={campaign.id} className="hover:bg-gray-50">
                      <td className="px-4 py-3">
                        <div className="font-medium text-gray-900 text-sm">{campaign.name}</div>
                        <div className="text-xs text-gray-500">{campaign.audience}</div>
                      </td>
                      <td className="px-4 py-3 text-right text-sm font-medium">€{campaign.spend.toLocaleString()}</td>
                      <td className="px-4 py-3 text-right text-sm font-semibold text-green-600">{campaign.leads}</td>
                      <td className={`px-4 py-3 text-right text-sm font-medium ${campaign.cpl > 50 ? 'text-red-600' : campaign.cpl < 30 ? 'text-green-600' : 'text-gray-900'}`}>
                        €{campaign.cpl.toFixed(2)}
                      </td>
                      <td className={`px-4 py-3 text-right text-sm ${campaign.ctr < 1.5 ? 'text-red-500' : 'text-gray-900'}`}>
                        {campaign.ctr.toFixed(2)}%
                      </td>
                      <td className="px-4 py-3 text-right text-sm">{campaign.convRate.toFixed(2)}%</td>
                      <td className={`px-4 py-3 text-right text-sm ${campaign.frequency > 3 ? 'text-red-600 font-medium' : 'text-gray-900'}`}>
                        {campaign.frequency.toFixed(1)}
                        {campaign.frequency > 3 && <AlertCircle className="w-3 h-3 inline ml-1" />}
                      </td>
                      <td className={`px-4 py-3 text-right text-sm font-medium ${campaign.roas >= 3 ? 'text-green-600' : campaign.roas < 2 ? 'text-red-500' : 'text-gray-900'}`}>
                        {campaign.roas.toFixed(1)}x
                      </td>
                      <td className="px-4 py-3 text-center">
                        <span className={`inline-flex px-2 py-1 text-xs font-medium rounded-full ${
                          campaign.status === 'active' ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-600'
                        }`}>
                          {campaign.status}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </>
      )}

      {activeTab === 'creatives' && (
        <div className="space-y-6">
          {/* Creative Performance */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <MetricCard title="Winners" value={creativeData.filter(c => c.status === 'winner').length} icon={Award} />
            <MetricCard title="In Test" value={creativeData.filter(c => c.status === 'testing').length} icon={Eye} />
            <MetricCard title="Fatigued" value={creativeData.filter(c => c.status === 'fatigued').length} icon={AlertTriangle} />
          </div>

          {/* Creative Table */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
            <div className="p-5 border-b border-gray-100">
              <h3 className="font-semibold text-gray-900">Creative Performance</h3>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Creative</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Format</th>
                    <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase">Impressies</th>
                    <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase">CTR</th>
                    <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase">Leads</th>
                    <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase">CPL</th>
                    <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase">Dagen</th>
                    <th className="px-4 py-3 text-center text-xs font-medium text-gray-500 uppercase">Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-100">
                  {creativeData.sort((a, b) => a.cpl - b.cpl).map(creative => (
                    <tr key={creative.id} className="hover:bg-gray-50">
                      <td className="px-4 py-3 font-medium text-gray-900 text-sm">{creative.name}</td>
                      <td className="px-4 py-3">
                        <span className={`px-2 py-1 text-xs rounded-full ${
                          creative.format === 'Video' ? 'bg-purple-100 text-purple-700' :
                          creative.format === 'Carousel' ? 'bg-blue-100 text-blue-700' : 'bg-gray-100 text-gray-700'
                        }`}>{creative.format}</span>
                      </td>
                      <td className="px-4 py-3 text-right text-sm">{creative.impressions.toLocaleString()}</td>
                      <td className={`px-4 py-3 text-right text-sm font-medium ${creative.ctr >= 2 ? 'text-green-600' : 'text-gray-900'}`}>
                        {creative.ctr.toFixed(1)}%
                      </td>
                      <td className="px-4 py-3 text-right text-sm font-semibold text-green-600">{creative.leads}</td>
                      <td className={`px-4 py-3 text-right text-sm font-medium ${creative.cpl < 30 ? 'text-green-600' : 'text-gray-900'}`}>
                        €{creative.cpl.toFixed(2)}
                      </td>
                      <td className={`px-4 py-3 text-right text-sm ${creative.daysActive > 21 ? 'text-amber-600' : 'text-gray-900'}`}>
                        {creative.daysActive}d
                      </td>
                      <td className="px-4 py-3 text-center">
                        <span className={`inline-flex px-2 py-1 text-xs font-medium rounded-full ${
                          creative.status === 'winner' ? 'bg-green-100 text-green-700' :
                          creative.status === 'testing' ? 'bg-blue-100 text-blue-700' :
                          creative.status === 'fatigued' ? 'bg-red-100 text-red-700' : 'bg-gray-100 text-gray-600'
                        }`}>
                          {creative.status}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* A/B Test Matrix */}
          <div className="bg-white rounded-xl p-5 shadow-sm border border-gray-100">
            <h3 className="font-semibold text-gray-900 mb-4">A/B Test Priority (volgende tests)</h3>
            <div className="grid grid-cols-1 md:grid-cols-5 gap-3">
              {['Offer/Value Prop', 'CTA Text', 'Headline', 'Visual/Video', 'Body Copy'].map((test, i) => (
                <div key={test} className={`p-4 rounded-lg text-center ${
                  i === 0 ? 'bg-green-100 border-2 border-green-500' : 'bg-gray-50'
                }`}>
                  <span className="text-2xl font-bold text-gray-400">#{i + 1}</span>
                  <p className="text-sm font-medium text-gray-900 mt-1">{test}</p>
                  {i === 0 && <span className="text-xs text-green-700 font-medium">PRIORITEIT</span>}
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {activeTab === 'audiences' && (
        <div className="space-y-6">
          {/* Audience Scatter Plot */}
          <div className="bg-white rounded-xl p-5 shadow-sm border border-gray-100">
            <h3 className="font-semibold text-gray-900 mb-4">Audience Performance Matrix (CPL vs Volume)</h3>
            <ResponsiveContainer width="100%" height={400}>
              <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                <XAxis type="number" dataKey="leads" name="Leads" unit="" tick={{ fontSize: 12 }} label={{ value: 'Leads', position: 'bottom' }} />
                <YAxis type="number" dataKey="cpl" name="CPL" unit="€" tick={{ fontSize: 12 }} label={{ value: 'CPL (€)', angle: -90, position: 'left' }} />
                <ZAxis type="number" dataKey="spend" range={[100, 500]} name="Spend" />
                <Tooltip cursor={{ strokeDasharray: '3 3' }} formatter={(value, name) => [name === 'CPL' ? `€${value}` : value, name]} />
                <Scatter name="Audiences" data={campaignData} fill="#3b82f6">
                  {campaignData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.cpl < 30 ? '#22c55e' : entry.cpl > 50 ? '#ef4444' : '#f59e0b'} />
                  ))}
                </Scatter>
              </ScatterChart>
            </ResponsiveContainer>
            <div className="flex justify-center gap-6 mt-4">
              <div className="flex items-center gap-2"><div className="w-3 h-3 rounded-full bg-green-500" /><span className="text-sm text-gray-600">CPL &lt;€30</span></div>
              <div className="flex items-center gap-2"><div className="w-3 h-3 rounded-full bg-amber-500" /><span className="text-sm text-gray-600">CPL €30-50</span></div>
              <div className="flex items-center gap-2"><div className="w-3 h-3 rounded-full bg-red-500" /><span className="text-sm text-gray-600">CPL &gt;€50</span></div>
            </div>
          </div>

          {/* Audience Breakdown */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-white rounded-xl p-5 shadow-sm border border-gray-100">
              <h3 className="font-semibold text-gray-900 mb-4">Spend per Audience</h3>
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={campaignData}
                    cx="50%"
                    cy="50%"
                    innerRadius={60}
                    outerRadius={100}
                    fill="#8884d8"
                    paddingAngle={2}
                    dataKey="spend"
                    nameKey="audience"
                    label={({ audience, percent }) => `${audience}: ${(percent * 100).toFixed(0)}%`}
                  >
                    {campaignData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip formatter={(value) => [`€${value}`, 'Spend']} />
                </PieChart>
              </ResponsiveContainer>
            </div>

            <div className="bg-white rounded-xl p-5 shadow-sm border border-gray-100">
              <h3 className="font-semibold text-gray-900 mb-4">ROAS per Audience</h3>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={campaignData.sort((a, b) => b.roas - a.roas)} layout="vertical">
                  <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                  <XAxis type="number" tick={{ fontSize: 12 }} />
                  <YAxis dataKey="audience" type="category" width={100} tick={{ fontSize: 11 }} />
                  <Tooltip formatter={(value) => [`${value}x`, 'ROAS']} />
                  <Bar dataKey="roas" name="ROAS">
                    {campaignData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.roas >= 3 ? '#22c55e' : entry.roas >= 2 ? '#f59e0b' : '#ef4444'} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'insights' && (
        <div className="space-y-6">
          {/* Weekly Summary */}
          <div className="bg-gradient-to-r from-blue-600 to-indigo-600 rounded-xl p-6 text-white">
            <h3 className="text-lg font-semibold mb-4">Week 49 Samenvatting</h3>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
              <div>
                <p className="text-blue-200 text-sm">Spend</p>
                <p className="text-2xl font-bold">€6.010</p>
                <p className="text-green-300 text-sm">+9.3% vs W48</p>
              </div>
              <div>
                <p className="text-blue-200 text-sm">Leads</p>
                <p className="text-2xl font-bold">188</p>
                <p className="text-red-300 text-sm">-3.6% vs W48</p>
              </div>
              <div>
                <p className="text-blue-200 text-sm">CPL</p>
                <p className="text-2xl font-bold">€31.97</p>
                <p className="text-red-300 text-sm">+13.3% vs W48</p>
              </div>
              <div>
                <p className="text-blue-200 text-sm">Conv Rate</p>
                <p className="text-2xl font-bold">4.7%</p>
                <p className="text-red-300 text-sm">-14.5% vs W48</p>
              </div>
            </div>
          </div>

          {/* Action Items */}
          <div className="bg-white rounded-xl p-5 shadow-sm border border-gray-100">
            <h3 className="font-semibold text-gray-900 mb-4 flex items-center gap-2">
              <Target className="w-5 h-5 text-blue-600" />
              Actie Items Deze Week
            </h3>
            <div className="space-y-3">
              {[
                { action: 'Refresh creatives voor "Technische Directeuren" campagne', status: 'urgent', due: 'Vandaag' },
                { action: 'Scale "Stop Scrolling" video naar HR Managers audience', status: 'high', due: 'Morgen' },
                { action: 'Maak Lookalike 2% van Retargeting converters', status: 'medium', due: 'Deze week' },
                { action: 'Pauseer Manufacturing LAL campagne (ROAS 1.2x)', status: 'high', due: 'Vandaag' },
                { action: 'Test nieuwe "Waarom 78% faalt" hook in Carousel format', status: 'medium', due: 'Deze week' },
                { action: 'Verhoog retargeting budget van €320 naar €480', status: 'high', due: 'Morgen' },
              ].map((item, i) => (
                <div key={i} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div className="flex items-center gap-3">
                    <input type="checkbox" className="w-4 h-4 rounded border-gray-300" />
                    <span className="text-sm text-gray-900">{item.action}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className={`text-xs px-2 py-1 rounded-full font-medium ${
                      item.status === 'urgent' ? 'bg-red-100 text-red-700' :
                      item.status === 'high' ? 'bg-amber-100 text-amber-700' : 'bg-blue-100 text-blue-700'
                    }`}>{item.due}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Benchmarks */}
          <div className="bg-white rounded-xl p-5 shadow-sm border border-gray-100">
            <h3 className="font-semibold text-gray-900 mb-4">Benchmarks vs Industry</h3>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="text-left text-xs font-medium text-gray-500 uppercase">
                    <th className="pb-3">Metric</th>
                    <th className="pb-3">Jouw Performance</th>
                    <th className="pb-3">Industry Avg</th>
                    <th className="pb-3">Top 10%</th>
                    <th className="pb-3">Status</th>
                  </tr>
                </thead>
                <tbody className="text-sm">
                  <tr className="border-t border-gray-100">
                    <td className="py-3 font-medium">CPL</td>
                    <td className="py-3">€{totals.avgCpl.toFixed(2)}</td>
                    <td className="py-3 text-gray-500">€35-50</td>
                    <td className="py-3 text-gray-500">&lt;€25</td>
                    <td className="py-3"><span className="px-2 py-1 bg-green-100 text-green-700 rounded-full text-xs font-medium">Beter dan avg</span></td>
                  </tr>
                  <tr className="border-t border-gray-100">
                    <td className="py-3 font-medium">CTR</td>
                    <td className="py-3">{totals.avgCtr.toFixed(2)}%</td>
                    <td className="py-3 text-gray-500">1.0-1.5%</td>
                    <td className="py-3 text-gray-500">&gt;2.5%</td>
                    <td className="py-3"><span className="px-2 py-1 bg-green-100 text-green-700 rounded-full text-xs font-medium">Beter dan avg</span></td>
                  </tr>
                  <tr className="border-t border-gray-100">
                    <td className="py-3 font-medium">Conv Rate</td>
                    <td className="py-3">{totals.avgConvRate.toFixed(2)}%</td>
                    <td className="py-3 text-gray-500">3-5%</td>
                    <td className="py-3 text-gray-500">&gt;8%</td>
                    <td className="py-3"><span className="px-2 py-1 bg-amber-100 text-amber-700 rounded-full text-xs font-medium">Gemiddeld</span></td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'campaigns' && (
        <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
          <div className="p-5 border-b border-gray-100 flex justify-between items-center">
            <h3 className="font-semibold text-gray-900">Alle Campagnes</h3>
            <div className="flex gap-2">
              <button className="px-3 py-1.5 text-sm bg-green-100 text-green-700 rounded-lg font-medium">Active ({campaignData.filter(c => c.status === 'active').length})</button>
              <button className="px-3 py-1.5 text-sm bg-gray-100 text-gray-600 rounded-lg font-medium">Paused ({campaignData.filter(c => c.status === 'paused').length})</button>
            </div>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Campagne</th>
                  <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase">Budget</th>
                  <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase">Spent</th>
                  <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase">Impressies</th>
                  <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase">Clicks</th>
                  <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase">Leads</th>
                  <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase">CPL</th>
                  <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase">ROAS</th>
                  <th className="px-4 py-3 text-center text-xs font-medium text-gray-500 uppercase">Acties</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {campaignData.map(campaign => (
                  <tr key={campaign.id} className={`hover:bg-gray-50 ${campaign.status === 'paused' ? 'opacity-60' : ''}`}>
                    <td className="px-4 py-4">
                      <div className="font-medium text-gray-900">{campaign.name}</div>
                      <div className="text-xs text-gray-500 mt-1">{campaign.audience}</div>
                    </td>
                    <td className="px-4 py-3 text-right text-sm">€{(campaign.spend * 1.2).toFixed(0)}</td>
                    <td className="px-4 py-3 text-right text-sm font-medium">€{campaign.spend.toLocaleString()}</td>
                    <td className="px-4 py-3 text-right text-sm text-gray-600">{campaign.impressions.toLocaleString()}</td>
                    <td className="px-4 py-3 text-right text-sm text-gray-600">{campaign.clicks.toLocaleString()}</td>
                    <td className="px-4 py-3 text-right text-sm font-semibold text-green-600">{campaign.leads}</td>
                    <td className={`px-4 py-3 text-right text-sm font-medium ${campaign.cpl > 50 ? 'text-red-600' : campaign.cpl < 30 ? 'text-green-600' : ''}`}>
                      €{campaign.cpl.toFixed(2)}
                    </td>
                    <td className={`px-4 py-3 text-right text-sm font-medium ${campaign.roas >= 3 ? 'text-green-600' : campaign.roas < 2 ? 'text-red-500' : ''}`}>
                      {campaign.roas.toFixed(1)}x
                    </td>
                    <td className="px-4 py-3 text-center">
                      <div className="flex justify-center gap-1">
                        <button className="p-1.5 hover:bg-gray-100 rounded" title="Edit">✏️</button>
                        <button className="p-1.5 hover:bg-gray-100 rounded" title="Duplicate">📋</button>
                        <button className="p-1.5 hover:bg-gray-100 rounded" title={campaign.status === 'active' ? 'Pause' : 'Activate'}>
                          {campaign.status === 'active' ? '⏸️' : '▶️'}
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
