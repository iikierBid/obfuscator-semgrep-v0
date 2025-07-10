// ================================
// ARQUIVO DE VULNERABILIDADES INTENCIONAIS
// Para testes e validação do Semgrep
// ================================

const crypto = require('crypto');
const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');

// ================================
// 1. INJECTION ATTACKS
// ================================

// SQL Injection - Múltiplas variações
function sqlInjection1(userId) {
    const query = "SELECT * FROM users WHERE id = " + userId; // Vulnerável
    return query;
}

function sqlInjection2(email) {
    const sql = `SELECT * FROM accounts WHERE email = '${email}'`; // Vulnerável
    return sql;
}

function sqlInjection3(name) {
    const query = "INSERT INTO users (name) VALUES ('" + name + "')"; // Vulnerável
    return query;
}

// NoSQL Injection
function nosqlInjection(userInput) {
    const query = { $where: userInput }; // Vulnerável - MongoDB
    return query;
}

// Command Injection
function commandInjection1(filename) {
    const command = "cat " + filename; // Vulnerável
    exec(command, (error, stdout) => {
        console.log(stdout);
    });
}

function commandInjection2(userInput) {
    exec(`ping -c 4 ${userInput}`, (error, stdout) => { // Vulnerável
        console.log(stdout);
    });
}

// LDAP Injection
function ldapInjection(username) {
    const filter = `(uid=${username})`; // Vulnerável
    return filter;
}

// XPath Injection
function xpathInjection(user) {
    const xpath = `//user[name='${user}']`; // Vulnerável
    return xpath;
}

// ================================
// 2. CROSS-SITE SCRIPTING (XSS)
// ================================

// Reflected XSS
function reflectedXSS(userInput) {
    document.getElementById('output').innerHTML = userInput; // Vulnerável
}

// DOM-based XSS
function domXSS() {
    const hash = location.hash.substring(1);
    document.write(hash); // Vulnerável
}

// XSS via outerHTML
function outerHTMLXSS(content) {
    document.getElementById('container').outerHTML = content; // Vulnerável
}

// XSS via insertAdjacentHTML
function insertAdjacentXSS(html) {
    document.body.insertAdjacentHTML('beforeend', html); // Vulnerável
}

// ================================
// 3. CRYPTOGRAPHY ISSUES
// ================================

// Weak Hash Algorithms
function weakHashing1(password) {
    return crypto.createHash('md5').update(password).digest('hex'); // Vulnerável
}

function weakHashing2(data) {
    return crypto.createHash('sha1').update(data).digest('hex'); // Vulnerável
}

// Hardcoded Encryption Keys
const ENCRYPTION_KEY = "hardcoded-secret-key-123"; // Vulnerável

// Weak Random Number Generation
function weakRandom() {
    return Math.random(); // Vulnerável para criptografia
}

// Insecure Crypto Algorithm
function insecureCrypto(plaintext) {
    const cipher = crypto.createCipher('des', 'password'); // Vulnerável - DES
    return cipher.update(plaintext, 'utf8', 'hex') + cipher.final('hex');
}

// ================================
// 4. PATH TRAVERSAL & FILE SECURITY
// ================================

// Path Traversal
function pathTraversal1(filename) {
    const filePath = path.join(__dirname, filename); // Vulnerável
    return fs.readFileSync(filePath);
}

function pathTraversal2(userPath) {
    const content = fs.readFileSync('./uploads/' + userPath); // Vulnerável
    return content;
}

// File Upload without validation
function unsafeFileUpload(filename, content) {
    fs.writeFileSync(filename, content); // Vulnerável
}

// ================================
// 5. AUTHENTICATION & AUTHORIZATION
// ================================

// Hardcoded Passwords
const DATABASE_PASSWORD = "admin123"; // Vulnerável
const API_SECRET = "secret-api-key-456"; // Vulnerável

// JWT Vulnerabilities
function insecureJWT() {
    const jwt = require('jsonwebtoken');
    const token = jwt.sign({user: 'admin'}, 'weak-secret'); // Vulnerável
    return token;
}

// Session Management Issues
function insecureSession(req, res) {
    req.session.regenerate = false; // Vulnerável
    req.session.cookie.secure = false; // Vulnerável
    req.session.cookie.httpOnly = false; // Vulnerável
}

// ================================
// 6. INFORMATION DISCLOSURE
// ================================

// Sensitive Data in Logs
function sensitiveLogging(creditCard, ssn) {
    console.log(`Credit Card: ${creditCard}, SSN: ${ssn}`); // Vulnerável
}

// Debug Information
function debugInfo(error) {
    console.error(error.stack); // Vulnerável em produção
    return error.message;
}

// Password in URL
function passwordInURL(password) {
    const url = `https://api.example.com/login?password=${password}`; // Vulnerável
    return url;
}

// ================================
// 7. INSECURE DESERIALIZATION
// ================================

// Unsafe JSON Parsing
function unsafeJSONParse(userInput) {
    return JSON.parse(userInput); // Vulnerável se não validado
}

// Unsafe eval with user input
function unsafeEval(expression) {
    return eval(expression); // Vulnerável
}

// ================================
// 8. SECURITY MISCONFIGURATIONS
// ================================

// CORS Misconfiguration
function insecureCORS(req, res) {
    res.header('Access-Control-Allow-Origin', '*'); // Vulnerável
    res.header('Access-Control-Allow-Credentials', 'true'); // Vulnerável
}

// Insecure Headers
function insecureHeaders(res) {
    res.removeHeader('X-Frame-Options'); // Vulnerável
    res.removeHeader('X-Content-Type-Options'); // Vulnerável
}

// ================================
// 9. REGEX VULNERABILITIES
// ================================

// ReDoS (Regular Expression Denial of Service)
function regexDoS(input) {
    const regex = /^(a+)+$/; // Vulnerável
    return regex.test(input);
}

// ================================
// 10. BUFFER OVERFLOW (Node.js context)
// ================================

// Unsafe Buffer Operations
function unsafeBuffer(size) {
    const buffer = Buffer.allocUnsafe(size); // Vulnerável
    return buffer;
}

// ================================
// 11. RACE CONDITIONS
// ================================

// TOCTOU (Time-of-Check to Time-of-Use)
function toctouVulnerability(filename) {
    if (fs.existsSync(filename)) { // Check
        // Time gap aqui
        const content = fs.readFileSync(filename); // Use - Vulnerável
        return content;
    }
}

// ================================
// 12. PROTOTYPE POLLUTION
// ================================

// Prototype Pollution
function prototypePollution(obj, key, value) {
    obj[key] = value; // Vulnerável se key for "__proto__"
}

// ================================
// 13. EXTERNAL CONTROL OF FILENAME
// ================================

// File path manipulation
function unsafeFileAccess(userFile) {
    const filePath = `/var/www/uploads/${userFile}`; // Vulnerável
    return fs.readFileSync(filePath);
}

// ================================
// 14. INSECURE RANDOM
// ================================

// Insecure random for crypto
function insecureRandomToken() {
    return Math.random().toString(36); // Vulnerável para tokens
}

// ================================
// 15. DANGEROUS FUNCTIONS
// ================================

// Dangerous function calls
function dangerousFunctions(code) {
    new Function(code)(); // Vulnerável
    setTimeout(code, 1000); // Vulnerável se code for string
}

module.exports = {
    sqlInjection1,
    sqlInjection2,
    sqlInjection3,
    nosqlInjection,
    commandInjection1,
    commandInjection2,
    ldapInjection,
    xpathInjection,
    reflectedXSS,
    domXSS,
    outerHTMLXSS,
    insertAdjacentXSS,
    weakHashing1,
    weakHashing2,
    weakRandom,
    insecureCrypto,
    pathTraversal1,
    pathTraversal2,
    unsafeFileUpload,
    insecureJWT,
    insecureSession,
    sensitiveLogging,
    debugInfo,
    passwordInURL,
    unsafeJSONParse,
    unsafeEval,
    insecureCORS,
    insecureHeaders,
    regexDoS,
    unsafeBuffer,
    toctouVulnerability,
    prototypePollution,
    unsafeFileAccess,
    insecureRandomToken,
    dangerousFunctions
}; 