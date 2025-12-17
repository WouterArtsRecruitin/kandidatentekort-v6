/**
 * Kandidatentekort Campaign Dashboard - Google Apps Script
 * Enhanced automation for Supermetrics data processing
 */

// Configuration
const CONFIG = {
  SUPERMETRICS_API_KEY: 'api_9BLJx4w6XC5b8ZmfHKLTT6PtMlg4zkay2A9Uf_zIG4NJX7FHWNthRsiz0zw6BAOcb7lP6s7iLwAIEHrhXDLzRiu_DHnOzriba65e',
  SHEET_ID: '1gbo-7RJSCakhqaoicxwMops9yK0BHUsQWbWl5adxB3Q',
  DAILY_BUDGET: 240,
  TARGET_CPA: 15,
  MIN_CTR: 0.01,
  SLACK_WEBHOOK: 'YOUR_SLACK_WEBHOOK_URL'
};

/**
 * Main function - runs after Supermetrics data refresh
 */
function onDataRefresh() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  
  // Update calculations
  calculateKPIs(ss);
  updateDashboard(ss);
  checkAlerts(ss);
  
  // Log update
  console.log('Dashboard updated at: ' + new Date());
}

/**
 * Calculate recruitment-specific KPIs
 */
function calculateKPIs(spreadsheet) {
  const dataSheet = spreadsheet.getSheetByName('Raw Data');
  const kpiSheet = spreadsheet.getSheetByName('KPIs') || spreadsheet.insertSheet('KPIs');
  
  // Clear existing KPIs
  kpiSheet.clear();
  
  // Set headers
  const headers = [
    ['KPI', 'Value', 'Target', 'Status'],
    ['Cost per Application', '', '€15', ''],
    ['Application Rate', '', '5%', ''],
    ['Total Applications', '', '', ''],
    ['Improvement vs Baseline', '', '40%', ''],
    ['Daily Spend', '', '€240', ''],
    ['Overall ROAS', '', '3.0', '']
  ];
  
  kpiSheet.getRange(1, 1, headers.length, headers[0].length).setValues(headers);
  
  // Calculate metrics from raw data
  const data = dataSheet.getDataRange().getValues();
  calculateApplicationMetrics(data, kpiSheet);
}

/**
 * Calculate application-specific metrics
 */
function calculateApplicationMetrics(data, kpiSheet) {
  let totalSpend = 0;
  let totalClicks = 0;
  let totalApplications = 0;
  let totalRevenue = 0;
  
  // Skip header row
  for (let i = 1; i < data.length; i++) {
    const row = data[i];
    totalSpend += parseFloat(row[3]) || 0; // Spend column
    totalClicks += parseInt(row[2]) || 0; // Clicks column
    totalApplications += parseInt(row[5]) || 0; // Conversions/Applications
    totalRevenue += parseFloat(row[6]) || 0; // Revenue column
  }
  
  // Calculate KPIs
  const costPerApplication = totalApplications > 0 ? totalSpend / totalApplications : 0;
  const applicationRate = totalClicks > 0 ? (totalApplications / totalClicks) * 100 : 0;
  const roas = totalSpend > 0 ? totalRevenue / totalSpend : 0;
  
  // Update KPI sheet
  kpiSheet.getRange('B2').setValue('€' + costPerApplication.toFixed(2));
  kpiSheet.getRange('B3').setValue(applicationRate.toFixed(2) + '%');
  kpiSheet.getRange('B4').setValue(totalApplications);
  kpiSheet.getRange('B6').setValue('€' + totalSpend.toFixed(2));
  kpiSheet.getRange('B7').setValue(roas.toFixed(2));
  
  // Set status colors
  setStatusColors(kpiSheet, costPerApplication, applicationRate, totalSpend, roas);
}

/**
 * Set color coding for KPI status
 */
function setStatusColors(sheet, cpa, appRate, spend, roas) {
  // Cost per Application status
  const cpaCell = sheet.getRange('D2');
  if (cpa <= 15) {
    cpaCell.setValue('✅').setBackground('#d4edda');
  } else {
    cpaCell.setValue('⚠️').setBackground('#f8d7da');
  }
  
  // Application Rate status
  const appRateCell = sheet.getRange('D3');
  if (appRate >= 5) {
    appRateCell.setValue('✅').setBackground('#d4edda');
  } else {
    appRateCell.setValue('⚠️').setBackground('#f8d7da');
  }
  
  // Daily Spend status
  const spendCell = sheet.getRange('D6');
  if (spend <= CONFIG.DAILY_BUDGET) {
    spendCell.setValue('✅').setBackground('#d4edda');
  } else {
    spendCell.setValue('⚠️').setBackground('#f8d7da');
  }
  
  // ROAS status
  const roasCell = sheet.getRange('D7');
  if (roas >= 3.0) {
    roasCell.setValue('✅').setBackground('#d4edda');
  } else {
    roasCell.setValue('⚠️').setBackground('#f8d7da');
  }
}

/**
 * Update main dashboard with visualizations
 */
function updateDashboard(spreadsheet) {
  const dashboardSheet = spreadsheet.getSheetByName('Dashboard') || spreadsheet.insertSheet('Dashboard');
  
  // Create summary cards
  createSummaryCards(dashboardSheet);
  
  // Update charts
  updateCharts(dashboardSheet);
}

/**
 * Create summary cards for key metrics
 */
function createSummaryCards(sheet) {
  // Clear existing content
  sheet.getRange('A1:H10').clear();
  
  // Title
  sheet.getRange('A1').setValue('Kandidatentekort Campaign Dashboard')
    .setFontSize(20)
    .setFontWeight('bold');
  
  sheet.getRange('A2').setValue('Last updated: ' + new Date().toLocaleString('nl-NL'));
  
  // Create metric cards
  const cards = [
    { title: 'Total Applications', range: 'A4:B6', formula: '=KPIs!B4' },
    { title: 'Cost per Application', range: 'D4:E6', formula: '=KPIs!B2' },
    { title: 'Today\'s Spend', range: 'G4:H6', formula: '=KPIs!B6' },
    { title: 'Application Rate', range: 'A8:B10', formula: '=KPIs!B3' },
    { title: 'ROAS', range: 'D8:E10', formula: '=KPIs!B7' },
    { title: 'Active Campaigns', range: 'G8:H10', formula: '=COUNTIF(\'Raw Data\'!B:B,">0")' }
  ];
  
  cards.forEach(card => {
    const range = sheet.getRange(card.range);
    range.merge();
    range.setBorder(true, true, true, true, false, false);
    range.setVerticalAlignment('middle');
    range.setHorizontalAlignment('center');
    
    // Set title
    const titleCell = range.offset(-1, 0, 1, range.getNumColumns());
    titleCell.setValue(card.title);
    titleCell.setFontWeight('bold');
    titleCell.setBackground('#f0f0f0');
    
    // Set value
    range.setFormula(card.formula);
    range.setFontSize(18);
  });
}

/**
 * Check alerts and send notifications
 */
function checkAlerts(spreadsheet) {
  const kpiSheet = spreadsheet.getSheetByName('KPIs');
  const alerts = [];
  
  // Check Cost per Application
  const cpa = parseFloat(kpiSheet.getRange('B2').getValue().replace('€', ''));
  if (cpa > CONFIG.TARGET_CPA) {
    alerts.push(`🚨 Cost per Application (€${cpa.toFixed(2)}) exceeds target of €${CONFIG.TARGET_CPA}`);
  }
  
  // Check Daily Spend
  const spend = parseFloat(kpiSheet.getRange('B6').getValue().replace('€', ''));
  if (spend > CONFIG.DAILY_BUDGET) {
    alerts.push(`💰 Daily spend (€${spend.toFixed(2)}) exceeds budget of €${CONFIG.DAILY_BUDGET}`);
  }
  
  // Check Application Rate
  const appRate = parseFloat(kpiSheet.getRange('B3').getValue().replace('%', ''));
  if (appRate < 5) {
    alerts.push(`📉 Application rate (${appRate.toFixed(2)}%) is below target of 5%`);
  }
  
  // Send alerts if any
  if (alerts.length > 0) {
    sendAlertEmail(alerts);
    if (CONFIG.SLACK_WEBHOOK) {
      sendSlackAlert(alerts);
    }
  }
}

/**
 * Send email alerts
 */
function sendAlertEmail(alerts) {
  const recipient = Session.getActiveUser().getEmail();
  const subject = '⚠️ Kandidatentekort Campaign Alerts';
  const body = `
    <h2>Campaign Performance Alerts</h2>
    <p>The following metrics need attention:</p>
    <ul>
      ${alerts.map(alert => `<li>${alert}</li>`).join('')}
    </ul>
    <p>View dashboard: <a href="https://docs.google.com/spreadsheets/d/${CONFIG.SHEET_ID}">Open Dashboard</a></p>
  `;
  
  MailApp.sendEmail({
    to: recipient,
    subject: subject,
    htmlBody: body
  });
}

/**
 * Send Slack notification
 */
function sendSlackAlert(alerts) {
  const payload = {
    text: '⚠️ *Kandidatentekort Campaign Alerts*',
    attachments: [{
      color: 'warning',
      fields: alerts.map(alert => ({
        title: 'Alert',
        value: alert,
        short: false
      }))
    }]
  };
  
  UrlFetchApp.fetch(CONFIG.SLACK_WEBHOOK, {
    method: 'post',
    contentType: 'application/json',
    payload: JSON.stringify(payload)
  });
}

/**
 * Create custom menu
 */
function onOpen() {
  const ui = SpreadsheetApp.getUi();
  ui.createMenu('Kandidatentekort')
    .addItem('Update Dashboard', 'onDataRefresh')
    .addItem('Check Alerts', 'checkAlerts')
    .addItem('Export Report', 'exportReport')
    .addSeparator()
    .addItem('Setup Triggers', 'setupTriggers')
    .addToUi();
}

/**
 * Setup automatic triggers
 */
function setupTriggers() {
  // Remove existing triggers
  ScriptApp.getProjectTriggers().forEach(trigger => {
    ScriptApp.deleteTrigger(trigger);
  });
  
  // Create daily trigger at 7 AM
  ScriptApp.newTrigger('onDataRefresh')
    .timeBased()
    .everyDays(1)
    .atHour(7)
    .create();
    
  SpreadsheetApp.getActiveSpreadsheet().toast('✅ Automatic refresh scheduled for 7 AM daily');
}

/**
 * Export report as PDF
 */
function exportReport() {
  const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  const dashboardSheet = spreadsheet.getSheetByName('Dashboard');
  
  // Create PDF
  const url = `https://docs.google.com/spreadsheets/d/${CONFIG.SHEET_ID}/export?` +
    `format=pdf&` +
    `gid=${dashboardSheet.getSheetId()}&` +
    `portrait=false&` +
    `fitw=true`;
    
  const token = ScriptApp.getOAuthToken();
  const response = UrlFetchApp.fetch(url, {
    headers: {
      'Authorization': 'Bearer ' + token
    }
  });
  
  // Save PDF
  const blob = response.getBlob().setName(`Kandidatentekort_Report_${new Date().toISOString().split('T')[0]}.pdf`);
  DriveApp.createFile(blob);
  
  SpreadsheetApp.getActiveSpreadsheet().toast('✅ Report exported to Google Drive');
}