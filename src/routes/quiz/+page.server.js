import { fail } from '@sveltejs/kit';
import questions from '../../lib/server/quiz-questions.json';

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
    submit: async ({ request }) => {
        const data = await request.formData();
        const answers = questions.map((question) => ({
            question_id: question.id,
            choice: data.get(`question_${question.id}`)
        }));
        if (answers.some((answer) => answer.choice !== 'like' && answer.choice !== 'nope')) {
            return fail(400, { error: 'กรุณาตอบคำถามให้ครบทั้ง 5 ข้อ' });
        }
        // This payload is ready for the teammate's Faction service.
        // Do not call the old four-question endpoint or grant a collection card here.
        return { success: true, answers };
    }
};
