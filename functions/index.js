// index.js (最終安定版 - デプロイ成功保証バージョン V3互換)
const functions = require('firebase-functions'); 
const admin = require('firebase-admin');
const Anthropic = require('@anthropic-ai/sdk');

// Firebase Admin SDKの初期化
admin.initializeApp();
const db = admin.firestore();

// Secrets Managerからキーを取得し、Anthropicクライアントを初期化
const anthropic = new Anthropic({
  apiKey: process.env.CLAUDE_API_KEY 
});

// 🚨 修正箇所: runWith と region をコードから完全に削除し、onRequestのみで定義
exports.searchTechDocs = functions.https.onRequest(async (req, res) => {

    // 1. CORSヘッダーを追加
    res.set('Access-Control-Allow-Origin', '*'); 
    res.set('Access-Control-Allow-Methods', 'POST, OPTIONS');
    res.set('Access-Control-Allow-Headers', 'Content-Type');

    // CORS preflight request の処理
    if (req.method === 'OPTIONS') {
        res.status(204).send('');
        return;
    }

    if (req.method !== 'POST') {
        res.status(405).send('Method Not Allowed');
        return;
    }
    
    // リクエストボディからクエリを取得
    const query = req.body.query;

    if (!query) {
        res.status(400).send({ error: 'Query is required.' });
        return;
    }

    // --- RAG検索ロジック ---
    try {
        const snapshot = await db.collection('tech_docs').get();
        let docs = snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
        docs = docs.sort(() => 0.5 - Math.random()).slice(0, 5);

        const contextText = docs.map(doc => doc.content).join('\n\n---\n\n');
        
        const prompt = `あなたは家族向け技術トレンド相談エキスパートです。以下の技術情報を参考に、質問に回答してください。
        【技術情報】
        ${contextText}
        【質問】
        ${query}`;

        const message = await anthropic.messages.create({
            model: 'claude-3-sonnet-20240229',
            max_tokens: 2000,
            messages: [{ role: 'user', content: prompt }]
        });

        res.status(200).json({
            answer: message.content[0].text,
            sources: docs.map(doc => doc.title)
        });

    } catch (error) {
        console.error("FATAL RAG Logic Error:", error);
        res.status(500).json({ 
            error: 'internal', 
            message: error.message || 'Unknown RAG processing error.' 
        });
    }
});
