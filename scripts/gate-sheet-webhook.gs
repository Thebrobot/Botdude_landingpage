/**
 * Bot Dude · Niche gate → Google Sheet + email alert
 *
 * Tab name must be: Gate
 * Deploy as Web app → Execute as: Me → Who has access: Anyone
 *
 * First-time email setup (required once):
 * 1. Paste this full script and Save
 * 2. Select function testEmailAlert → Run → Allow permissions
 * 3. Deploy → Manage deployments → Edit (pencil) → Version: New version → Deploy
 *
 * Saving alone does NOT update the live webhook URL. You must create a New version.
 */

var SHEET_NAME = 'Gate';

var ALERT_EMAIL = 'info@thebrobot.com';

var HEADERS = [
  'Timestamp',
  'Business',
  'Niche',
  'Niche Label',
  'Source',
  'Event',
  'UTM Source',
  'UTM Medium',
  'UTM Campaign',
  'UTM Content',
  'Referrer',
  'Landing Page',
  'First Seen At',
  'Submitted At'
];

function doGet(e) {
  return handleGateHit(e && e.parameter ? e.parameter : {});
}

function doPost(e) {
  var params = {};
  if (e && e.parameter) params = e.parameter;
  if (e && e.postData && e.postData.contents) {
    try {
      var parsed = JSON.parse(e.postData.contents);
      for (var key in parsed) {
        if (Object.prototype.hasOwnProperty.call(parsed, key)) {
          params[key] = parsed[key];
        }
      }
    } catch (err) {
      // Keep query/form params if JSON parse fails.
    }
  }
  return handleGateHit(params);
}

/**
 * Run this once from the Apps Script editor to authorize MailApp.
 * Do NOT use Deploy for this. Use the Run button at the top.
 * If Google shows "unverified app", click Advanced → Go to ... → Allow.
 */
function testEmailAlert() {
  MailApp.sendEmail({
    to: ALERT_EMAIL,
    subject: 'New Bot Dude gate: Manual Apps Script test',
    body: 'If you got this, MailApp permission is working.'
  });
}

function handleGateHit(params) {
  var business = String(params.business || params.companyName || '').trim();
  if (!business) {
    return jsonResponse({ ok: false, error: 'business required' });
  }

  var niche = String(params.niche || '');
  var nicheLabel = String(params.niche_label || '');
  var source = String(params.source || 'botdude.ai niche gate');
  var eventName = String(params.event || 'botdude_gate_interaction');
  var utmSource = String(params.utm_source || '');
  var utmMedium = String(params.utm_medium || '');
  var utmCampaign = String(params.utm_campaign || '');
  var utmContent = String(params.utm_content || '');
  var referrer = String(params.referrer || '');
  var landingPage = String(params.landing_page || '');
  var firstSeenAt = String(params.first_seen_at || '');
  var submittedAt = String(params.submitted_at || '');

  var sheet = getOrCreateSheet_();
  ensureHeaders_(sheet);

  sheet.appendRow([
    new Date(),
    business,
    niche,
    nicheLabel,
    source,
    eventName,
    utmSource,
    utmMedium,
    utmCampaign,
    utmContent,
    referrer,
    landingPage,
    firstSeenAt,
    submittedAt
  ]);

  var emailResult = sendGateAlert_({
    business: business,
    niche: niche,
    nicheLabel: nicheLabel,
    source: source,
    utmSource: utmSource,
    utmCampaign: utmCampaign,
    landingPage: landingPage
  });

  return jsonResponse({
    ok: true,
    emailSent: !!emailResult.sent,
    emailError: emailResult.error || ''
  });
}

function sendGateAlert_(data) {
  if (!ALERT_EMAIL || ALERT_EMAIL.indexOf('@') === -1) {
    return { sent: false, error: 'ALERT_EMAIL not set' };
  }

  var nicheText = data.nicheLabel || data.niche || 'unknown niche';
  var subject = 'New Bot Dude gate: ' + data.business;
  var body = [
    'New niche gate submission',
    '',
    'Business: ' + data.business,
    'Niche: ' + nicheText,
    'Source: ' + (data.source || ''),
    'UTM Source: ' + (data.utmSource || ''),
    'UTM Campaign: ' + (data.utmCampaign || ''),
    'Landing page: ' + (data.landingPage || ''),
    '',
    'Open your Gate sheet to review the full row.'
  ].join('\n');

  try {
    MailApp.sendEmail({
      to: ALERT_EMAIL,
      subject: subject,
      body: body
    });
    return { sent: true, error: '' };
  } catch (err) {
    return {
      sent: false,
      error: String(err && err.message ? err.message : err)
    };
  }
}

function getOrCreateSheet_() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName(SHEET_NAME);
  if (!sheet) sheet = ss.insertSheet(SHEET_NAME);
  return sheet;
}

function ensureHeaders_(sheet) {
  if (sheet.getLastRow() > 0) return;
  sheet.appendRow(HEADERS);
  sheet.setFrozenRows(1);
}

function jsonResponse(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}
