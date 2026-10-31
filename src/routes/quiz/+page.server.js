import { fail } from '@sveltejs/kit';
import questions from '../../lib/server/quiz-questions.json';

// @ts-ignore
export async function load({ fetch }) {
    try {
        const response = await fetch('http://127.0.0.1:8000/quiz/questions');
        if (response.ok) {
            const data = await response.json();
            if (Array.isArray(data) && data.length === questions.length &&
                data.every((question, index) => question.id === questions[index].id &&
                    question.title && question.question && question.image && question.nope && question.like)) {
                return { questions: data, offline: false };
            }
        }
    } catch {
        // Allow the UI to be reviewed before the group's FastAPI is available.
    }
    return { questions, offline: true };
}

export const actions = {
    // 1. ฟังก์ชันสำหรับการกดยืนยันตอนทำ Quiz เสร็จ
    // @ts-ignore
    submit: async ({ request }) => {
        const data = await request.formData();
        const ans = {
            ans_1: data.get('question_1'),
            ans_2: data.get('question_2'),
            ans_3: data.get('question_3'),
            ans_4: data.get('question_4'),
            ans_5: data.get('question_5')
        };

        if (!ans.ans_1 || !ans.ans_2 || !ans.ans_3 || !ans.ans_4 || !ans.ans_5) {
             return fail(400, { error: 'กรุณาตอบคำถามให้ครบทั้ง 5 ข้อ' });
        }

        try {
            const response = await fetch('http://127.0.0.1:8000/personas/quiz', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ user_id: 1, ...ans })
            });
            const result = await response.json();
            if (!response.ok) return fail(400, { error: result.detail || 'คุณได้รับคอลเลกชันไปแล้ว!' });

            return { success: true, faction: result.matched_faction, artifact: result.starting_artifact, imageUrl: result.image_url };
        } catch (err) {
            return fail(500, { error: 'ไม่สามารถเชื่อมต่อเซิร์ฟเวอร์ Backend ได้' });
        }
    },

    // 2. ฟังก์ชันปุ่มสุ่มโชค (DRAW YOUR FATE) - ใช้ user_id: 1 เพื่อไม่ให้สุ่มซ้ำได้
    draw: async () => {
        const choices = ['like', 'nope'];
        const randomAns = () => choices[Math.floor(Math.random() * choices.length)];
        
        try {
            const response = await fetch('http://127.0.0.1:8000/personas/quiz', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    user_id: 1, // 👈 ล็อก user_id เป็น 1 เพื่อให้ดักจับการรับการ์ดไปแล้วได้จริง
                    ans_1: randomAns(), 
                    ans_2: randomAns(), 
                    ans_3: randomAns(), 
                    ans_4: randomAns(), 
                    ans_5: randomAns() 
                })
            });
            const result = await response.json();
            
            if (!response.ok) return fail(400, { error: result.detail || 'You have already claimed this collection!' });

            return { success: true, faction: result.matched_faction, artifact: result.starting_artifact, imageUrl: result.image_url };
        } catch (err) {
            return fail(500, { error: 'ไม่สามารถเชื่อมต่อเซิร์ฟเวอร์ Backend ได้' });
        }
    }
};