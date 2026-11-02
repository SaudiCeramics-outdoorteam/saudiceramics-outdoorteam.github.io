/**
 * سجل عملاء "شطّب بيتك مع الخزف السعودي"
 * يستقبل البيانات من الموقع ويضيف سطر لكل حدث في ورقة "العملاء".
 * الإعداد: Extensions > Apps Script، الصق هذا الكود، ثم Deploy > New deployment > Web app
 * (Execute as: Me — Who has access: Anyone) وانسخ رابط الـ Web app.
 */
const SHEET_NAME = 'العملاء';
const HEADERS = ['الوقت', 'الحدث', 'اسم العميل', 'الجوال', 'عدد المنتجات', 'المنتجات', 'الجهاز', 'رقم الزيارة'];

function sheet_() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sh = ss.getSheetByName(SHEET_NAME);
  if (!sh) {
    sh = ss.insertSheet(SHEET_NAME);
    sh.appendRow(HEADERS);
    sh.getRange(1, 1, 1, HEADERS.length).setFontWeight('bold').setBackground('#1f4e8c').setFontColor('#ffffff');
    sh.setFrozenRows(1);
    sh.setRightToLeft(true);
  }
  return sh;
}

function clean_(v, max) {
  // keep it plain text: no formulas from the web, bounded length
  let s = String(v == null ? '' : v).slice(0, max || 500);
  if (/^[=+\-@]/.test(s)) s = "'" + s;
  return s;
}

function doPost(e) {
  try {
    const d = JSON.parse(e.postData.contents || '{}');
    const lock = LockService.getScriptLock();
    lock.waitLock(10000);
    sheet_().appendRow([
      new Date(),
      clean_(d.event, 40),
      clean_(d.name, 80),
      clean_(d.phone, 20),
      Number(d.count) || 0,
      clean_(d.items, 4000),
      clean_(d.device, 20),
      clean_(d.session, 40)
    ]);
    lock.releaseLock();
  } catch (err) {
    // ignore malformed posts
  }
  return ContentService.createTextOutput('ok');
}

function doGet() {
  return ContentService.createTextOutput('سجل العملاء يعمل ✓');
}
